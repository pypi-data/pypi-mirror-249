from rmbcommon.models import StrucQuery, QueryResult

class MySQLQuery(StrucQuery):

    @property
    def sql(self):
        return self.content


class MySQLQueryResult(QueryResult):
    __source_type__ = "MySQL"


    @property
    def rows(self):
        return self.content.fetchall()

    @property
    def columns(self):
        return self.content.keys()

    def __str__(self):
        output = ""
        output += f"Columns: {','.join([column for column in self.columns])}\n"
        output += f"Rows: {self.rows}\n"
        return output[0:2000]  # 截取前2000个字符
