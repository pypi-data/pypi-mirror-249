from rmbcommon.models import MetaData, StrucQuery, QueryResult
from rmbserver.exceptions import DataSourceConfigError


class BaseDataAccessor:
    __access_config_keys_must__ = []
    PROMPT_GEN_STRUC_QUERY = ""

    def __init__(self, ds_type, ds_name=None, ds_access_config=None):
        self.ds_type = ds_type
        self.ds_name = ds_name
        self.ds_access_config = ds_access_config or {}

        # 检查 Access Config 的完整性
        self._check_access_config()

        # 从access_config 中抽取数据源的连接信息（可能字段不同），并保存到实例属性中
        for _key in self.ds_access_config:
            attr_key = f"ds_{_key}"
            if getattr(self, attr_key, None):
                raise DataSourceConfigError(f"Access Config中的配置项与数据源默认的配置项命名冲突: {_key}")
            setattr(self, attr_key, self.ds_access_config[_key])

    def _check_access_config(self):
        # 检查access_config中的配置项是否符合要求
        # 如果不符合要求，抛出异常
        for _key in self.__access_config_keys_must__:
            if _key not in self.ds_access_config:
                raise DataSourceConfigError(f"Access Config中缺少必要的配置项: {_key}")

    def retrieve_meta_data(self) -> MetaData:
        raise NotImplementedError(
            f"retrieve_meta_data() is not implemented for {self.ds_type}"
        )

    def retrieve_sample_data(self, tables_full_name: list[str], meta_data: MetaData) -> dict:
        raise NotImplementedError(
            f"retrieve_sample_data() is not implemented for {self.ds_type}"
        )

    def query(self, struc_query: StrucQuery, meta_data: MetaData) -> QueryResult:
        raise NotImplementedError(
            f"query() is not implemented for {self.ds_type}"
        )

    def __repr__(self):
        return f"<{self.ds_type}: {self.ds_name}>"
