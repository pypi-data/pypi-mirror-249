# 通用的数据源类，提供了各种数据源均需要的基本属性和方法，比如Original MetaData以及获取MetaData的方法
from rmbcommon.models.base import BaseCoreModel


class DataSourceCore(BaseCoreModel):

    __init_dict_keys__ = ['id', 'name', 'type', 'access_config']

    def __repr__(self):
        if self.id:
            return f"<{self.id}: {self.name} >"
        else:
            return f"<{self.type}: {self.name} (not saved)>"
    #
    # @property
    # def schemas(self):
    #     # 数据源的所有schema
    #     meta = self.accessor.retrieve_meta_data()
    #     return meta.schemas

    @property
    def safe_access_config(self):
        # TODO: 保护敏感信息
        return self.access_config

    # @property
    # def accessor(self):
    #     # 数据源的数据访问器
    #     return create_data_accessor(
    #         self.type,
    #         ds_name=self.name,
    #         ds_access_config=self.access_config
    #     )
    #
