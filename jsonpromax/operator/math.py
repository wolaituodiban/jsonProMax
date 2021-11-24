from .operator import Operator


class Mean(Operator):
    def __init__(self):
        super().__init__(inplace=False)

    def __call__(self, obj, **kwargs):
        if isinstance(obj, list):
            return sum(obj) / len(obj)
        elif isinstance(obj, dict):
            return sum(obj.values()) / len(obj)
