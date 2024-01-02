
class BaseCoreModel:
    __init_dict_keys__ = []

    def __init__(self, **kwargs):
        for k in self.__init_dict_keys__:
            setattr(self, k, kwargs.get(k))

    @classmethod
    def load_from_dict(cls, data: dict):
        # log.debug(f"Loading from dict: {data}")
        if not data:
            return None
        return cls(**data)

    def to_dict(self):
        data = {}
        for k in self.__init_dict_keys__:
            data[k] = getattr(self, k)
        return data
