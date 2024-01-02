from rmbcommon.models.bi import StrucQuery, QueryResult


class ExcelQuery(StrucQuery):
    pass


# class ExcelQueryResult(QueryResult):
#     __source_type__ = "Excel"
#
#     # self.content is a pandas.DataFrame
#     # log.debug(f"查询结果 str：{content.to_string()}")
#     # log.debug(f"查询结果 dict：{content.to_dict()}")
#     # log.debug(f"查询结果 numpy：{content.to_numpy()}")
#     # log.debug(f"查询结果 values：{content.values}")
#
#     @property
#     def rows(self):
#
#         # 加上 .astype('int64') 可以避免返回的数据用科学记数法表示，
#         # 但会string会报错，所以暂时不用
#         return self.content.to_numpy()
#
#     @property
#     def columns(self):
#         return self.content.columns
#
#     def __str__(self):
#         return str(self.rows[0:100])  # 截取前100行

class ExcelQueryResult(QueryResult):
    pass
