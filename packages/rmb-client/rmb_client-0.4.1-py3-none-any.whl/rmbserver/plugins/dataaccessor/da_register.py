from rmbserver.plugins.dataaccessor.da_base import BaseDataAccessor
from rmbserver.log import log


# 初始化数据源映射字典
DATA_ACCESSOR_MAP = {}


def register_data_accessor(cls):
    """类装饰器，注册数据源类到 DATA_ACCESSOR_MAP 中。"""

    # 先检查是否符合要求
    # 1. 必须继承自 BaseDataAccessor
    # 2. 必须定义 __source_type__ __access_config_keys_must__ 属性
    # 3. 必须重写 retrieve_meta_data() 方法 ( 这个不好检查，先跳过）
    if not issubclass(cls, BaseDataAccessor):
        raise ValueError(f"{cls} must be subclass of {BaseDataAccessor}")

    if not hasattr(cls, "__source_type__"):
        raise ValueError(f"{cls} must define __source_type__")

    if not hasattr(cls, "__access_config_keys_must__"):
        raise ValueError(f"{cls} must define __access_config_keys_must__")

    DATA_ACCESSOR_MAP[cls.__source_type__] = cls
    return cls


def create_data_accessor(ds_type, **kwargs) -> BaseDataAccessor:
    """创建对应的数据源访问器"""
    data_accessor_class = DATA_ACCESSOR_MAP.get(ds_type)
    if not data_accessor_class:
        log.error(f"{ds_type} is not supported, not in {DATA_ACCESSOR_MAP}")
        raise ValueError(f"Unsupported datasource type: {ds_type}")
    return data_accessor_class(ds_type, **kwargs)
