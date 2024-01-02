from rmbcommon.models import StrucQuery, QueryResult, MetaData
from rmbserver.plugins.dataaccessor.da_base import BaseDataAccessor
from rmbserver.plugins.dataaccessor.da_register import register_data_accessor
from rmbserver.log import log

@register_data_accessor
class MongoDataAccessor(BaseDataAccessor):
    __source_type__ = "MongoDB"
    __access_config_keys_must__ = ['user', 'password', 'host']

    def retrieve_meta_data(self) -> MetaData:
        # TODO
        return MetaData('mongo meta')

    def query(self, struc_query: StrucQuery, meta_data: MetaData = None) -> QueryResult:
        # TODO
        return QueryResult('mongo query result')


log.info(f"registering data accessor: {MongoDataAccessor.__source_type__}")
