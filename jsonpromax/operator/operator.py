from ..version import __version__


class Operator:
    def __init__(self, inplace: bool):
        self.version = __version__
        self.inplace(inplace)

    def _call(self, obj, **kwargs):
        pass

    def _call_inplace(self, obj, **kwargs):
        pass

    def inplace(self, inplace: bool):
        self.call = self._call_inplace if inplace else self._call

    def __call__(self, obj, **kwargs):
        return self.call(obj, **kwargs)

    def extra_repr(self) -> str:
        return ''

    def __repr__(self):
        extra_repr = str(self.extra_repr())
        if '\n' in extra_repr:
            extra_repr = '\n  ' + '\n  '.join(extra_repr.split('\n')) + '\n'
        return '{}({})'.format(self.__class__.__name__, extra_repr)
