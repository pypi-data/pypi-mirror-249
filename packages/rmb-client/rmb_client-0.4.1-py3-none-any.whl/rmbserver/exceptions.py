# Error Design

# 1000 - 资源和配置类错误
# 2000 - QA对话类错误
# 3000 - 大模型类错误


class DataSourceExists(Exception):
    code = 1001
    message = "数据源已存在"


class DataSourceNotFound(Exception):
    code = 1002
    message = "数据源不存在"


class ChatNotFound(Exception):
    code = 1003
    message = "对话不存在"


class ParameterError(Exception):
    code = 1004
    message = "参数错误"


class DataSourceConfigError(Exception):
    code = 1005
    message = "数据源配置错误"


class BIQAError(Exception):
    code = 2001
    message = "BIQAError查询失败"


class QAErrorNoMatchDataSource(BIQAError):
    code = 2002
    message = "查询失败，原因是没有匹配的数据源"


class QAErrorInsufficientData(BIQAError):
    code = 2003
    message = "查询失败，原因是数据源中缺少必要的数据"


class QAErrorIncompleteQuestion(BIQAError):
    code = 2004
    message = "查询失败，原因是问题不完整"


class PromptTooLong(Exception):
    code = 3001
    message = "Prompt太长"

class InvalidStrucQuery(Exception):
    code = 3001
    message = "语句不合法"
