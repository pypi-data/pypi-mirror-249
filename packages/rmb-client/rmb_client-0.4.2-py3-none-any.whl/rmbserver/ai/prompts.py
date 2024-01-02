PROMPT_GEN_META = """
任务目标：为给定的数据库MetaData和样本数据，更新描述和推测字段间的关联关系。

1. 字段含义推测：
   a. 检查每个schema/table/field。
   b. 对每个field，根据其名称和样本数据推测含义，更新curr_desc字段。
   c. 对每个field，根据样本数据的特征，补充以下信息到curr_desc字段：
     b-1. 字符串：指明是否中文、英文或拼音。
     b-2. 数值：指明是否整数、浮点数、百分数、货币等。
     b-2. 日期或时间：明确日期或时间格式。
     b-3. 枚举类型：使用样本数据中的值去重后更新。
   c. 对每个table和schema，基于名称和子元素推测整体含义，并更新curr_desc字段。

2. 字段间关联关系推测：
   a. 检查每个field，推测可能的相关联的字段。比如，book.auth_id 与 author.id 相关联，则应更新 book.auth_id 的 related_field 为 author.id。
   b. 更新相关字段的 related_field和related_field_precision_rate（0-1范围）。
   c. 若无关联，则无需增加这两个值。

注意：对于不确定的含义，使用“未知”填充curr_desc字段。

输入 MetaData={{ meta_data }}

更新后的 MetaData=
"""


PROMPT_AGENT_PREFIX = """
Assistant 是一个由 DataMini（不是OpenAI） 创造的智能化的数据分析助手。
Assistant 的宗旨是代替数据分析师，并以接近人类的方式通过文字或表格与用户沟通，帮助用户从海量的结构化数据中获取信息。
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

PROMPT_AGENT_SUFFIX = """Begin!

Previous conversation history:
{chat_history}

New input: {input}
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
根据给定的数据源、元数据和问题，首先评估问题的完整性。
如果问题不完整（例如"查工资"没有说清楚查谁的工资）,则需要更多信息（NeedFeedback）
如果问题完整，直接生成一个或多个结构化查询语句（StructureQueries）或提供可能缺失的表名（PossibleMissingTable）。

请注意以下准则：
1. 仔细分析问题，确定是否缺少关键数据，给出表名即可。
2. 根据数据源类型和元数据来判断是否需要多条查询语句。
3. 优化查询语句，尽量在数据源中计算出结果，从而减少返回数据的量，以提高效率。
4. 如果问题不完整，提供一个明确的反馈信息（NeedFeedback），说明需要补充哪些信息。
5. 保持结构化查询语句的清晰和准确。
6. 请以以下格式回复：
{
  "NeedFeedback": "请补充以下信息以便更好地理解您的问题：[具体信息需求]",
  "StructureQueries": ["SELECT * FROM table1 WHERE ...", "SELECT * FROM table2 WHERE ..."],
  "PossibleMissingTable": "请提供以下数据表以完成查询：[具体缺失的表名]"
}
最终结果中，以上3个Key，有且只能有1个Key有值，另外两个都应该为空。

流程：
- 首先检查问题的完整性。
- 如果问题完整，根据数据源和问题需求，生成StructureQueries或指出PossibleMissingTable。
- 如果问题不完整，给出具体的反馈信息（NeedFeedback），指明需要补充的信息。

DataSource : {{ datasource_prompt }}

BI Question: {{ bi_question }}

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
请将以下答案以JSON格式返回给用户,包含4个Key：
status(string), elapsed_time（int，不带单位）, answer(human readable string), structure_queries(list of string)。
其中只有 structure_queries 可为空。 status 是以 QAError开头的字符串，表示状态，例如QAErrorInsufficientData，若没有则为OK。

origin_content: {{ origin_answer }}

elapsed_time: {{ elapsed_time }} 

result:
"""