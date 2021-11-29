from .base import JsonPathNode


class Wildcard(JsonPathNode):
    def __init__(self, inplace=False):
        super().__init__(inplace=inplace)

    def _call(self, obj, **kwargs):
        if isinstance(obj, dict):
            output = dict()
            for k, v in obj.items():
                for j in range(len(self.childs_or_processors)):
                    v = self._run_op(v, j, **kwargs)
                output[k] = v
            return output
        elif isinstance(obj, list):
            output = []
            for v in obj:
                for j in range(len(self.childs_or_processors)):
                    v = self._run_op(v, j, **kwargs)
                output.append(v)
            return output
        return obj

    def _call_inplace(self, obj, **kwargs):
        if isinstance(obj, dict):
            for k, v in obj.items():
                for j in range(len(self.childs_or_processors)):
                    v = self._run_op(v, j, **kwargs)
                obj[k] = v
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                for j in range(len(self.childs_or_processors)):
                    v = self._run_op(v, j, **kwargs)
                obj[i] = v
        return obj

    def __call__(self, obj, **kwargs):
        """
        计算逻辑，深层优先，同层按照注册顺序排序
        :param obj: 输入的对象
        :param kwargs:
        :return:
        """
        if len(self.childs_or_processors) == 0:
            return obj
        return self.call(obj, **kwargs)

    def is_duplicate(self, other) -> bool:
        return type(self) == type(other)

    @classmethod
    def from_json_path(cls, json_path: str):
        if json_path.startswith('$.*'):
            return cls(), '$'+json_path[3:]
        elif json_path.startswith('$[*]'):
            return cls(), '$'+json_path[4:]
        else:
            raise AssertionError(json_path)

    def extra_repr(self):
        return ".*"
