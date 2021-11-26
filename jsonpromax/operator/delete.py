from .operator import Operator


class Delete(Operator):
    def __init__(self, names, inplace=False):
        assert isinstance(names, (list, tuple, set))
        super().__init__(inplace=inplace)
        self.names = set(names)

    def _call_inplace(self, obj, **kwargs):
        for name in self.names:
            if name in obj:
                del obj[name]
        return obj

    def _call(self, obj, **kwargs):
        return {k: v for k, v in obj.items() if k not in self.names}

    def extra_repr(self):
        return "names={}".format(self.names)
