from functools import lru_cache

from .operator import Operator
from ..utils import rm_ascii


class Lower(Operator):
    def __init__(self):
        super().__init__(inplace=False)

    @lru_cache()
    def __call__(self, obj, **kwargs):
        return obj.lower()


class Split(Operator):
    def __init__(self, sep, maxsplit=-1):
        super().__init__(inplace=False)
        self.sep = sep
        self.maxsplit = maxsplit

    @lru_cache()
    def __call__(self, obj: str, **kwargs):
        return obj.split(sep=self.sep, maxsplit=self.maxsplit)

    def extra_repr(self) -> str:
        return "sep='{}', maxsplit={}".format(self.sep, self.maxsplit)


class Cut(Operator):
    def __init__(self):
        super().__init__(inplace=False)

    @lru_cache()
    def __call__(self, obj: str, tokenizer=None, **kwargs):
        output = tokenizer.lcut(obj)
        if len(output) == 0:
            output = None
        elif len(output) == 1:
            output = output[0]
        return output


class Rename(Operator):
    def __init__(self, old, new, inplace=False):
        super().__init__(inplace=inplace)
        self.old = old
        self.new = new

    def _call(self, obj, **kwargs):
        return {self.new if k == self.old else k: v for k, v in obj.items()}

    def _call_inplace(self, obj, **kwargs):
        if self.old in obj:
            obj[self.new] = obj[self.old]
            del obj[self.old]
        return obj

    def extra_repr(self):
        return "old='{}', new='{}'".format(self.old, self.new)


class RemoveASCII(Operator):
    def __init__(self):
        super().__init__(inplace=False)

    @lru_cache()
    def __call__(self, obj, **kwargs):
        return rm_ascii(obj)


class Slice(Operator):
    def __init__(self, _slice: slice):
        super().__init__(inplace=False)
        self._slice = _slice

    def __call__(self, obj, **kwargs):
        return obj[self._slice]

    def extra_repr(self) -> str:
        return 'slice={}'.format(self._slice)
