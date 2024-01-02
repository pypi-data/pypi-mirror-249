from rmbserver.servers.base import api, auth, Resource, request
from rmbserver.log import log
from rmbserver.brain.managers import DataSourceManager
from rmbserver.exceptions import ParameterError

# 定义命名空间
ns_datasource = api.namespace('datasources', description='数据源操作')


# @auth.login_required 放在class上面，不生效！！！
@ns_datasource.route('/')
class DataSourceList(Resource):
    @ns_datasource.doc(params={
        'name': '数据源名称'
    })
    @auth.login_required
    def get(self):
        """
        获取全部数据源
        """
        ds_name = request.args.get('name')
        return [ds.to_dict() for ds in DataSourceManager.get_all_datasources(name=ds_name)]

    @ns_datasource.doc(params={
        'name': '数据源名称',
        'type': '数据源类型，支持 MySQL、MongoDB、Hive',
        'access_config': '数据源连接配置，格式根据不同类型而不同'
    })
    @auth.login_required
    def post(self):
        """
        创建数据源
        """
        data = request.json
        ds_name = data['name']
        ds_type = data['type']
        ds_access_config = data['access_config']

        data_source = DataSourceManager.create_datasource(
            ds_name,
            ds_type,
            ds_access_config
        )

        log.info(f"DataSource created with meta data! {data_source}")

        return data_source.to_dict(), 201



@ns_datasource.route('/<string:datasource_id>')
class SingleDataSource(Resource):

    @ns_datasource.doc(params={
        'datasource_id': 'Data Source ID, 22位随机数'
    })
    @auth.login_required
    def get(self, datasource_id):
        """
        获取某个数据源
        """
        mgr = DataSourceManager(datasource_id)
        return mgr.data_source.to_dict(), 200

    @ns_datasource.doc(params={
        'datasource_id': 'Data Source ID, 22位随机数'
    })
    @auth.login_required
    def delete(self, datasource_id):
        """
        删除数据源
        """
        # 必须先删 Meta 再删 Data Source，否则无法关联到这些Meta Data
        mgr = DataSourceManager(datasource_id)
        mgr.data_source.delete()
        return {'message': f'Datasource deleted with meta data: {datasource_id}'}, 200



@ns_datasource.route('/<string:datasource_id>/meta')
class SingleDataSource(Resource):
    @ns_datasource.doc(params={
        'datasource_id': 'Data Source ID, 22位随机数'
    })
    @auth.login_required
    def post(self, datasource_id):
        """
        更新数据源
        """
        mgr = DataSourceManager(datasource_id)
        mgr.data_source.create_or_update_brain_meta()
        return {'message': f'Datasource updated with meta data: {datasource_id}'}, 200



@ns_datasource.route('/<string:datasource_id>/meta/<string:metadata_from>')
class DataSourceMetaData(Resource):

    @ns_datasource.doc(params={
        'datasource_id': '数据源 ID, 22位随机数',
        'metadata_from': '从哪里获取元数据，支持：runtime、in_brain'
    })
    @auth.login_required
    def get(self, datasource_id, metadata_from=None):
        """
        从数据源中获取最新的元数据
        """
        mgr = DataSourceManager(datasource_id)
        if metadata_from == 'runtime':
            return mgr.data_source.runtime_meta.to_dict(), 200
        elif metadata_from == 'in_brain':
            return mgr.data_source.brain_meta.to_dict(), 200
        else:
            raise ParameterError(f"URI must be /meta/runtime or /meta/in_brain")


if __name__ == '__main__':
    app.run(debug=True)
