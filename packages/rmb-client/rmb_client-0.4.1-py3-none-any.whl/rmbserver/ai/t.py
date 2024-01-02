import os
import httpx
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents.output_parsers import ReActSingleInputOutputParser

YOUR_OPENAI_PROXY = "http://127.0.0.1:8001"

# 定义处理BI问题的工具函数
def bi_tool(question):
    # 在这里编写处理BI问题的逻辑，生成文本和图片答案
    text_answer = "昨天销量是1000万"
    return text_answer


tools = [
    Tool(
        name="answer bi question",
        description="useful for when you need to answer questions about BI",
        func=bi_tool,
    ),
]

llm = ChatOpenAI(model="gpt-4-1106-preview", verbose=True)
llm.openai_proxy = YOUR_OPENAI_PROXY


memory = ConversationBufferMemory(memory_key="chat_history")

# from langchain import hub
# from langchain.agents import AgentExecutor
# from langchain.tools.render import render_text_description
# from langchain.agents.format_scratchpad import format_log_to_str
#
# prompt = hub.pull("hwchase17/react-chat")
#
# prompt = prompt.partial(
#     tools=render_text_description(tools),
#     tool_names=", ".join([t.name for t in tools]),
# )
#
# llm_with_stop = llm.bind(stop=["\nObservation"])
#
# agent = (
#     {
#         "input": lambda x: x["input"],
#         "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
#         "chat_history": lambda x: x["chat_history"],
#     }
#     | prompt
#     | llm_with_stop
#     | ReActSingleInputOutputParser()
# )
#
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False, memory=memory)


agent_executor = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    output_parser=ReActSingleInputOutputParser(),
)


# agent_executor.invoke({"input": "hi, iam jeff"})["output"]
#
# agent_executor.invoke({"input": "who am i?"})["output"]

# 定义对话流程
def conversation_flow():
    user_input = input("User: ") or "昨天销量如何"
    while user_input.lower() != "exit":
        # 用户输入作为agent的输入
        response = agent_executor.invoke({"input": user_input})["output"]
        print("Agent:", response)
        user_input = input("User: ")


# 运行对话流程

conversation_flow()

