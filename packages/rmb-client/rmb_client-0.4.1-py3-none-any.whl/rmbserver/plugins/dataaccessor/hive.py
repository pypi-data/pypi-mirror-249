from rmbcommon.models import StrucQuery, QueryResult, MetaData
from rmbserver.plugins.dataaccessor.da_base import BaseDataAccessor
from rmbserver.plugins.dataaccessor.da_register import register_data_accessor



@register_data_accessor
class HiveDataAccessor(BaseDataAccessor):
    __source_type__ = "Hive"
    __access_config_keys_must__ = ['host']

    def retrieve_meta_data(self) -> MetaData:
        # TODO
        return MetaData('hive meta')

    def query(self, struc_query: StrucQuery, meta_data: MetaData = None) -> QueryResult:
        # TODO
        return QueryResult('hive query result')
