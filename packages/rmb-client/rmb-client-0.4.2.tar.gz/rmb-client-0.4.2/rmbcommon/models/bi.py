from rmbcommon.models.base import BaseCoreModel

class BIQuestion:

    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content

class BIQueryPlan:
    pass


class NaturalQuery:

    def __init__(self, content: str):
        self.content = content

    def __str__(self):
        return self.content


class StrucQuery:

    def __init__(self, content: str, params: dict = None):
        self.content = content
        self.params = params or {}

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.__str__()

    @property
    def params_for_query(self):
        # 用于查询的参数
        return {key: value["value"] for key, value in self.params.items()}


class QueryResult:

    def __init__(self, query: StrucQuery, result):  # result: DataFrame
        self.query = query
        self.result = result

    def __str__(self):
        # 截取 前100行
        query_str = str(self.query)
        result_str = self.result.head(100).to_string(index=False)
        return f"Query: {query_str}\nResult:\n{result_str}"

    def __repr__(self):
        return f"QueryResult: {self.row_count} 行 {self.column_count} 列"

    @property
    def rows(self):
        return self.result.to_numpy()

    @property
    def columns(self):
        return self.result.columns

    @property
    def row_count(self):
        return len(self.result)

    @property
    def column_count(self):
        return len(self.columns)


class BIAnswer(BaseCoreModel):
    __init_dict_keys__ = [
        'status',
        'elapsed_time',
        'answer_text',
        'answer_file',
        'answer_image',
        'structure_queries',
    ]

    def __str__(self):
        return (f"[{self.status}-{self.elapsed_time}s]{'[F]' if self.answer_file else ''} "
                f"{self.answer_text} ExcelFile: {self.answer_file}")

    def __repr__(self):
        return self.__str__()

