PROMPT_GEN_META = """
任务目标：为给定的数据库MetaData {# 和样本数据 #} ，更新描述和推测字段间的关联关系。

任务1. 字段含义推测：
   a. 检查每个schema/table/field。
   b. 对每个field，根据其名称和样本数据推测含义，更新curr_desc字段。
   c. 对每个table和schema，基于名称和子元素推测整体含义，并更新curr_desc字段。
{#
   c. 对每个field，根据样本数据的特征，补充以下信息到curr_desc字段：
     b-1. 字符串：指明是否中文、英文或拼音。
     b-2. 数值：指明是否整数、浮点数、百分数、货币等。
     b-2. 日期或时间：明确日期或时间格式。
     b-3. 枚举类型：使用样本数据中的值去重后更新。
#}

任务2. 字段间关联关系推测:
   a. 检查每个field，推测可能的相关联的字段。比如，book.auth_id 与 author.id 相关联，则应更新 book.auth_id 的 related_field 为 author.id。
   b. 更新相关字段的 related_field和related_field_precision_rate（0-1范围）。
   c. 若无关联，则无需增加这两个值。

注意：
1. 对于不确定的含义，使用“未知”填充curr_desc字段。
2. 如果只有1个table，则跳过任务2

输入 MetaData={{ meta_data }}

更新后的 MetaData=
"""


PROMPT_AGENT_PREFIX = """
Assistant 是一个由 DataMini（不是OpenAI） 创造的智能化的数据分析助手。
Assistant 的宗旨是代替数据分析师，并用人类友好的中文或表格与用户沟通，帮助用户从海量的结构化数据中获取信息。
数据分析是一个严谨的任务，为了增加用户的信任，Assistant 会同时给出本次用于检索的1条或多条 StructureQuery。
Assistant 最终将返回三个信息：
1. status： 状态，包括OK，问题不完整（QAErrorIncompleteQuestion)或者数据不足(QAErrorInsufficientData）等。
2，answer：最终答案。
3，structure_queries：可为空，但如果是分析类的问题并给出答案的话，须提供。

TOOLS:
------

Assistant has access to the following data analysis tools:"""


PROMPT_AGENT_FORMAT_INSTRUCTIONS = """To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

Thought: Do I need to use a tool? No
{ai_prefix}: [your response here]
"""

PROMPT_AGENT_SUFFIX = """开始!

之前的对话历史：
{chat_history}

用户输入: {input}
{agent_scratchpad}"""


PROMPT_CHOOSE_DATASOURCE = """
请根据提供的问题和数据源的描述，选择一个合适的数据源。如果没有，则返回空字符串。
返回格式： {"choice_datasource_id": "ds_zhr2f1PSDUPzQUN1Nwikt"}

问题：{{ question }}

数据源：{{ datasources_summary }}

选择的数据源：
"""


# PROMPT_CHECK_QUESTION_INTEGRITY = """
# 假设你有一个数据集，请评估用户提出的问题是否完整。
#
# 如果问题不完整，需要用户补充信息，那么请以以下格式回复：
# {
#   "summarized_question": "",
#   "more_info_feedback": "请补充以下信息以便更好地理解您的问题：[具体信息需求]"
# }
#
# 如果问题完整，适合进行数据分析，那么请以以下格式回复：
# {
#   "summarized_question": "[问题总结]",
#   "more_info_feedback": ""
# }
#
# 数据集：{{ meta_data }}
#
# 当前问题： {{ question }}
#
# 历史对话： {{ chat_history }}
#
# 结果：
# """
#
# PROMPT_GEN_STRUC_QUERY2 = """
# 假设你是一名专业的数据分析师，请根据提供的问题BI Question、数据源DataSource的类型 以及 元数据MetaData，生成对该数据源的一条或多条查询语句 StructureQuery。
#
# 请注意：
# 1，请认真分析问题，若缺失数据无法计算，则给出可能缺失的表 PossibleMissingTable，提供表名即可。
# 2，根据你对数据源类型的了解，结合给出的元数据，判断是否需要分别执行多条查询语句才能回答该问题。
# 3，请尽量优化查询语句，直接在数据源中计算出结果，避免返回的数据量过大，希望行数尽量少。
# 4，StructureQuery中填充的字符串变量用中文不要用拼音或英文。
# 5，生成的JSON包含两个Key，一个是 StructureQueries，是一个字符串的数组包含了1条或多条查询语句；另一个是 PossibleMissingTable。
#
# DataSource : {{ datasource_prompt }}
#
# BI Question: {{ bi_question }}
#
# MetaData: {{ meta_data }}
#
# Result:
# """

PROMPT_GEN_STRUC_QUERY = """
根据给定的数据源、元数据和问题生成一个或多个结构化查询语句（structure_queries）
或提供可能缺失的表名（possible_missing_table）。

请注意以下准则：
1. 仔细分析问题，你可以将一个对数据的处理操作转化为一个查询语句。比如在末尾增加一列，值是某个字段的值的平方，可以转化为一个查询语句。
2. 有些数据是可以通过聚合函数计算获得，比如COUNT/SUM等。
3. 根据数据源类型和元数据来判断是否需要多条查询语句，若需要，则生成多条。
4. 查询语句只能是SELECT语句，不能是INSERT/UPDATE/DELETE等。

其中对查询语句的要求：
1. 优化查询语句，尽量在数据源中计算出结果，从而减少返回数据的量，以提高效率。
2. 尽量只返回需要的行，必要的时候可以带LIMIT。比如查询最大面积的城市，只需要返回1行。
3. 如果查询语句中包含常量，请使用绑定变量。

请以以下格式回复：
{
  "structure_queries": [structure_query_1, structure_query_2],
  "possible_missing_table": "请提供以下数据表以完成查询：[具体缺失的表名]"
}
以上2个Key，有且只能有1个Key有值，另一个Key为空字符串。

其中 structure_query_1 等查询语句的格式如下：
{
  "content': "SELECT score FROM students WHERE name = :stu_name",
  "params": {
    "stu_name": {
      "filed_full_name": "exam_db.students.name",
      "value": "张三",
  },
}
若无绑定变量，则无需包含 params。

流程：
根据数据源和问题需求，生成 structure_queries 或指出 possible_missing_table。

DataSource : {{ datasource_prompt }}

Question: {{ bi_question }}

MetaData: {{ meta_data }}

Result: 
"""


# PROMPT_GEN_BI_ANSWER = """
# 你是一名专业的数据分析师，请根据提供的问题 BI Question、元数据 MetaData、查询语句 StructureQuery 和查询结果 QueryResult，生成最终的答案 BI Answer。
#
# 为了便于追踪，返回的Answer中，也需要包含 QueryAndResult.
#
# DataSource Type: {{ datasource_type }}
#
# BI QUESTION: {{ bi_question }}
#
# MetaData: {{ meta_data }}
#
# StructureQueriesAndResults: {{ query_and_results }}
#
# Answer:
# """


PROMPT_FORMAT_AGENT_FINAL_ANSWER = """
请将原始答案以JSON格式返回给用户,包含6个Key：
1. status(string)
2. elapsed_time（integer）
3. answer_text(human readable string)
4. answer_file(download link, nullable)
5. answer_image(download link, nullable)
6. structure_queries(list of string, nullable)

其中 status 是以 QAError开头的字符串，表示状态，例如QAErrorInsufficientData，若没有则为OK。

origin_content: {{ origin_answer }}

elapsed_time: {{ elapsed_time }} 

result:
"""


# PROMPT_ANALYSE_QUESTION = """
# 你是一名资深的数据分析师，请对问题进行分析。
#
# 如果
#
# 问题的类型有：
# - 具体信息查询，英文叫：Specific Information Query，简称SIQ。例如：上海市总共多少套房子？张三考了多少分？给出了『上海市』和『张三』这样具体的信息。
# - 其他
#
# {{ question }}
# """
#
#
# PROMPT_STRUC_QUERY_REWRITE_CONSTANT = """
# 请根据给定的查询语句，来分析其中是否包含常量（Constant）。
#
# 返回的结果格式：
# {
#     "Constant": "常量的值",
#
# StructureQueries: ["SELECT ... FROM table1 WHERE ...", "SELECT ... FROM table2 WHERE ..."],
#
#
# """

PROMPT_GEN_DISTINCT_QUERIES = """
根据数据源类型和给出的1个或多个字段名，来生成查询语句，用于查询该字段中的所有去重之后的数据，取前{{ top_n_values }}个。

DataSource : {{ datasource_prompt }}

Fields（字段格式为 db.table.field）: 
{{ filed_full_names }}


按如下格式返回：
{ 
    "filed_full_name_1": "SELECT DISTINCT name FROM school_db.students LIMIT 10",
}

Result:
"""


PROMPT_CORRECT_CONSTANT_VALUE = """
根据给出的查询语句和数据库中对应字段存储的数据，来修正查询语句或对应绑定变量的值。

查询语句：
{{ struc_queries }}


绑定变量相关的字段中的实际存储的数据：
{{ dist_values }}

要求：
1. 保持原格式不变。如若需要，直接修改 params.value 的值，若无需要，则保持不变。


修正后的查询语句：
"""