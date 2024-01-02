from functools import wraps
from datetime import timedelta
import httpx
from io import BytesIO


from langchain.agents import (
    # AgentType,
    Tool,
    # initialize_agent,
)
from langchain.agents import AgentExecutor, ConversationalAgent
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from rmbserver import config
from rmbserver.log import log
from rmbserver.ai.prompts.agent import (
    PROMPT_AGENT_PREFIX,
    PROMPT_AGENT_SUFFIX,
    PROMPT_AGENT_FORMAT_INSTRUCTIONS,
    PROMPT_CHOOSE_DATASOURCE,
    PROMPT_GEN_STRUC_QUERY,
    PROMPT_GEN_DISTINCT_QUERIES,
    PROMPT_CORRECT_CONSTANT_VALUE,
    # PROMPT_GEN_BI_ANSWER,
    # PROMPT_CHECK_QUESTION_INTEGRITY,
)

from rmbserver.exceptions import (
    BIQAError,
    QAErrorNoMatchDataSource,
    QAErrorInsufficientData,
    QAErrorIncompleteQuestion,
    InvalidStrucQuery,
)
from rmbserver.analysis.chat import Chat
from rmbserver.brain.datasource import DataSource
from rmbcommon.models import StrucQuery, QueryResult
from rmbserver.ai.generations import ai_generate

from rmbserver.store import oss_bucket
from rmbcommon.tools import gen_excel_file_id



# 记录 LLM 日志的三方服务 Portkey
# from langchain.utilities import Portkey
# PORTKEY_API_KEY = "1aqtCtfA6WrZyNhO2PdOk0iQtjg="
# TRACE_ID = "rmbserver"
#
# openai_headers = Portkey.Config(
#     api_key=PORTKEY_API_KEY,
#     trace_id=TRACE_ID,
# )

def handle_biqa_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BIQAError as e:
            error_type = e.__class__.__name__
            return f"查询失败，原因是 {error_type}: {e}"
    return wrapper


class ChatAgentManager:

    def __init__(self, chat: Chat):
        self.chat = chat
        self.agent = self.create_agent()

    def _choose_a_data_source(self, question: str) -> DataSource:
        ds_summary = ""
        for ds in self.chat.datasources:
            ds_summary += f"{ds.type}数据源[{ds.name}][{ds.id}]包含以下数据表：\n"
            ds_summary += ds.brain_meta.to_table(level='table')

        choice_datasource = ai_generate(
            "CHOOSE_DATASOURCE",
            PROMPT_CHOOSE_DATASOURCE,
            template_format="jinja2",
            question=question,
            datasources_summary=ds_summary
        )["choice_datasource_id"]
        if choice_datasource:
            return DataSource.get(choice_datasource)
        else:
            raise QAErrorNoMatchDataSource(
                f"从你选择的数据源（{','.join([ds.name for ds in self.chat.datasources])}）"
                f"中无法回答问题【{question}】。"
            )

    def _correct_constant_value(self, data_source, meta_data, struc_queries):
        """
        struc_queries = [
                    {
                      "content': "SELECT score FROM students WHERE name = :stu_name",
                      "params": {
                        "stu_name": {
                          "filed_full_name": "exam_db.students.name",
                          "value": "张三",
                      },
                    }
               ]
        """
        filed_full_names = []
        for query in struc_queries["structure_queries"]:
            params = query.get("params", {})
            for param_name, param_info in params.items():
                field_name = param_info.get('field_full_name', None)
                if field_name:
                    filed_full_names.append(field_name)

        if filed_full_names:
            log.info(f"需要使用绑定变量查询，对绑定的变量值的准确性进行检查...")
            # 如果有字段是绑定变量，则生成对这些字段的查询语句
            dist_values_queries = ai_generate(
                "GEN_DISTINCT_QUERIES",
                PROMPT_GEN_DISTINCT_QUERIES,
                datasource_prompt=data_source.accessor.PROMPT_GEN_STRUC_QUERY,
                filed_full_names=filed_full_names,
                top_n_values=100,  # 最大100(不能超过 model/excel.py 中的最大值）
            )

            # 执行这些查询语句，获取结果
            dist_values = {}
            for _field, _query in dist_values_queries.items():
                rst = data_source.accessor.query(StrucQuery(_query), meta_data)
                dist_values[_field] = [r[0] for r in rst.rows]

            # 根据原语句和部分字段的结果，来修正这些语句
            corrected_struc_queries = ai_generate(
                "CORRECT_CONSTANT_VALUE",
                PROMPT_CORRECT_CONSTANT_VALUE,
                struc_queries=struc_queries,
                dist_values=dist_values,
            )
            if corrected_struc_queries == struc_queries:
                log.info(f"查询语句中的变量值正确，无需修正。")
            else:
                log.info(f"对查询语句中的变量值进行了修正：\n"
                         f"原语句：\n"
                         f"{struc_queries}\n"
                         f"新语句:\n"
                         f"{corrected_struc_queries}\n")
            return corrected_struc_queries
        else:
            log.info("没有使用绑定变量，无需检查变量值。")
            return struc_queries

    def _query_to_a_data_source(
            self,
            data_source: DataSource,
            question: str
    ) -> list[QueryResult]:

        meta_data = data_source.brain_meta

        output = ai_generate(
            "GEN_STRUC_QUERY",
            PROMPT_GEN_STRUC_QUERY,
            datasource_prompt=data_source.accessor.PROMPT_GEN_STRUC_QUERY,
            bi_question=question,
            meta_data=meta_data.to_dict_for_agent(),
        )
        if output.get("possible_missing_table", None):
            log.warning(f"从{data_source.name}[{data_source.id}]中查询：{question}，")
            raise QAErrorInsufficientData(
                f"在{data_source.name}[{data_source.id}]中查询{question}，"
                f"缺失这些信息: {output['possible_missing_table']}")
        elif output.get("need_feedback", None):
            log.warning(f"问题不完整：{question}|{output['need_feedback']}")
            raise QAErrorIncompleteQuestion(output['need_feedback'])

        output.pop("possible_missing_table", None)
        output.pop("need_feedback", None)
        # 检查查询语句中的常量的值是否正确
        corrected_output = self._correct_constant_value(
            data_source,
            meta_data,
            output,
        )

        # 从生成的内容中提取 Query 语句
        struc_queries = []
        for query in corrected_output["structure_queries"]:
            content = query["content"]
            params = query.get("params", None)
            struc_queries.append(
                StrucQuery(content, params)
            )

        results = [data_source.accessor.query(query, meta_data) for query in struc_queries]
        log.info(f"\n数据源：{data_source}"
                 f"\n问题：{question}"
                 f"\n查询结果：{results}")
        return results

    def _get_query_result_by_question(self, question: str) -> list[QueryResult]:
        # choose a data source
        if len(self.chat.datasources) == 1:
            data_source = self.chat.datasources[0]
        else:
            data_source = self._choose_a_data_source(question)

        # query to a data source
        # 如果出现生成的语句不合法，则进行重试
        max_retries = 2
        for attempt in range(1, max_retries + 1):
            try:
                return self._query_to_a_data_source(data_source, question)
            except InvalidStrucQuery as e:
                if attempt == max_retries:
                    log.error(f"查出错误，超过最大重试次数{max_retries}，报错退出")
                    raise
                log.warning(f"查询报错，第{attempt}次重试..")

    @handle_biqa_error
    def tool_data_query(self, question: str) -> str:
        results = self._get_query_result_by_question(question)
        results_str = '\n'.join([str(r) for r in results])
        return results_str

    def _save_results_to_excel_on_oss(self, results: list[QueryResult]):
        # 生成临时Excel文件
        file_name = f"{gen_excel_file_id()}.xlsx"
        excel_file = BytesIO()
        for i, data in enumerate(results):
            log.info(f"将查询结果写入Excel文件的Sheet{i + 1}：{data.result}")
            data.result.to_excel(
                excel_file, sheet_name=f'Sheet{i + 1}', index=False)
        excel_file.seek(0)

        # 上传到OSS
        oss_bucket.put_object(file_name, excel_file)

        # 设置URL的过期时间（例如，1小时）
        expire_time = timedelta(hours=1)
        url = oss_bucket.sign_url('GET', file_name, int(expire_time.total_seconds()))
        return url

    @handle_biqa_error
    def tool_execl_generator(self, question: str) -> str:
        query_results = self._get_query_result_by_question(question)
        url = self._save_results_to_excel_on_oss(query_results)
        return f"您可以从下面地址下载处理好的数据：{url}"

    @property
    def tools(self):
        return [
            Tool(
                name="DataQuery Tool",
                description="Useful for when you need to answer questions using a private database. "
                            "If you only need to query results from table data or generate charts,"
                            " then you need to select this tool.",
                func=self.tool_data_query,
            ),
            # Tool(
            #     name="question integrity check",
            #     description="check if the bi question is complete before answering",
            #     func=self.tool_check_question_integrity,
            # ),
            Tool(
                name="ExcelGenerator Tool",
                description="Useful for when you need to generate an Excel file. "
                            "If it involves processing table data, then you need to select this tool "
                            "to save the processed data.",
                func=self.tool_execl_generator,
            ),
        ]

    @property
    def agent_prompt(self):
        prompt = ConversationalAgent.create_prompt(
            self.tools,
            prefix=PROMPT_AGENT_PREFIX,
            suffix=PROMPT_AGENT_SUFFIX,
            format_instructions=PROMPT_AGENT_FORMAT_INSTRUCTIONS,
        )
        return prompt

    def create_agent(self, ):

        kwargs = {
            "model": config.openai_model_name,
            "openai_api_key": config.openai_api_key,
            "verbose": True,
            # "default_headers": openai_headers,
            # Agent 里面不能用JSON输出，ReAct output parser 要跟着改
            # "model_kwargs": {
            #     "response_format": {"type": "json_object"},
            # },
        }
        if config.openai_proxy:
            kwargs["http_client"] = httpx.Client(
                proxies=config.openai_proxy,
            )

        llm = ChatOpenAI(**kwargs)

        # memory
        memory = ConversationBufferMemory(memory_key="chat_history")

        for msg in self.chat.messages(limit=30):
            if msg.role == 'human':
                memory.chat_memory.add_user_message(str(msg.content))
            elif msg.role == 'ai':
                memory.chat_memory.add_ai_message(str(msg.content))
            else:
                log.warning(f"Unknown message role: {msg}")

        # Re-define Agent Prompt
        llm_chain = LLMChain(llm=llm, prompt=self.agent_prompt)

        agent = ConversationalAgent(
            llm_chain=llm_chain,
            tools=self.tools,
        )

        chat_agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            memory=memory,
            verbose=True,
        )

        # # Direct create agent executor
        # chat_agent_executor = initialize_agent(
        #     self.tools,
        #     llm,
        #     agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        #     verbose=True,
        #     memory=memory,
        #     # output_parser=ReActSingleInputOutputParser(),
        #     # output_parser=ConvoOutputParser(),
        # )

        return chat_agent_executor

    def query(self, question: str) -> str:
        response = self.agent.invoke({"input": question})["output"]
        # log.debug(f"\nHuman: {question} \nAI: {response}")
        return response
