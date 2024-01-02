from tabulate import tabulate
from rmbclient.log import log


def convert_to_object(cls):
    # 将JSON对象转换为Model对象
    def decorator(func):
        def wrapper(*args, **kwargs):
            json_or_list_data = func(*args, **kwargs)
            # 如果返回的是JSON or List对象
            if isinstance(json_or_list_data, list):
                return [cls.load_from_dict(json_data) for json_data in json_or_list_data]
            elif isinstance(json_or_list_data, dict):
                return cls.load_from_dict(json_or_list_data)
            else:
                log.error(f"Unsupported data type: {type(json_or_list_data)}")
                raise ValueError("Unsupported data type")

        return wrapper

    return decorator


class BaseResourceList:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def __iter__(self):
        # 实现迭代器协议，允许直接迭代资源列表
        self._current = 0
        self._resources = self._get_all_resources() or []
        return self

    def __next__(self):
        if self._current >= len(self._resources):
            raise StopIteration
        resource = self._resources[self._current]
        self._current += 1
        return resource

    def _get_all_resources(self):
        raise NotImplementedError

    def to_dict(self):
        return [resource.to_dict() for resource in self]

    def __repr__(self):
        # 将资源转换为字典列表
        resources_dicts = [resource.to_dict() for resource in self]

        # 使用 tabulate 来生成表格格式的字符串
        return tabulate(resources_dicts, headers="keys", tablefmt="plain")
