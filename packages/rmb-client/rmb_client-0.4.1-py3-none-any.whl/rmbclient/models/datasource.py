from rmbcommon.models import DataSourceCore, MetaData
from rmbclient.models.base import convert_to_object, BaseResourceList
from rmbclient.api import rmb_api
from rmbclient.exceptions import ResourceNotFound


class MetaDataClientModel:
    def __init__(self, datasource_id):
        self.datasource_id = datasource_id

    def get(self, from_where):
        if from_where not in ["runtime", "in_brain"]:
            raise ValueError("from_where must be one of runtime/in_brain")
        return MetaData.load_from_dict(
            rmb_api.send(
                endpoint=f"/datasources/{self.datasource_id}/meta/{from_where}",
                method="GET"
            )
        )

    def sync(self):
        return rmb_api.send(endpoint=f"/datasources/{self.datasource_id}/meta", method="POST")


class DataSourceClientModel(DataSourceCore):
    @property
    def meta(self) -> MetaDataClientModel:
        return MetaDataClientModel(self.id)

    def delete(self):
        return rmb_api.send(endpoint=f"/datasources/{self.id}", method="DELETE")


class DataResourceList(BaseResourceList):
    @convert_to_object(cls=DataSourceClientModel)
    def _get_all_resources(self):
        # 获取所有资源
        return rmb_api.send(endpoint=self.endpoint, method="GET")

    @convert_to_object(cls=DataSourceClientModel)
    def get(self, id=None, name=None):
        if name:
            ds_list = rmb_api.send(endpoint=f"{self.endpoint}?name={name}", method="GET")
            if ds_list:
                return ds_list[0]
            else:
                raise ResourceNotFound(f"Data Source {name} not found")

        if not id:
            raise ValueError("No ID or Name provided")
        # 通过资源ID来获取
        return rmb_api.send(endpoint=f"{self.endpoint}{id}", method="GET")

    @convert_to_object(cls=DataSourceClientModel)
    def register(self, ds_type, ds_name, ds_access_config):
        data = {
            "type": ds_type, "name": ds_name,
            "access_config": ds_access_config
        }
        return rmb_api.send(endpoint=self.endpoint, method="POST", data=data)





