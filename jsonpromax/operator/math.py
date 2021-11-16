from .operator import Operator


class Mean(Operator):
    def __call__(self, obj, **kwargs):
        if isinstance(obj, list):
            return sum(obj) / len(obj)
        elif isinstance(obj, dict):
            return sum(obj.values()) / len(obj)
