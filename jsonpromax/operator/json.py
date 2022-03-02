import json as py_json
from functools import lru_cache
from typing import Set

from .operator import Operator
from ..utils import unstructurize_dict


class JsonLoader(Operator):
    def __init__(self):
        super().__init__(inplace=False)

    def __call__(self, obj, **kwargs):
        return py_json.loads(obj)


class Unstructurizer(Operator):
    def __init__(self, preserved: Set[str] = None, start_level=0, end_level=0):
        super().__init__(inplace=False)
        self.preserved = preserved
        self.start_level = start_level
        self.end_level = end_level

    def __call__(self, obj, **kwargs):
        return unstructurize_dict(obj, preserved=self.preserved, start_level=self.start_level, end_level=self.end_level)

    def extra_repr(self):
        return 'preserved={}, start_level={}, end_level={}'.format(self.preserved, self.start_level, self.end_level)


class DictGetter(Operator):
    def __init__(self, keys: Set[str]):
        super(DictGetter, self).__init__(inplace=False)
        self.keys = keys

    def __call__(self, obj, **kwargs):
        return {k: obj[k] for k in self.keys if k in obj}

    def extra_repr(self) -> str:
        return 'keys={}'.format(self.keys)


class ConcatList(Operator):
    def __init__(self, inputs: set, output: str):
        super(ConcatList, self).__init__(inplace=False)
        assert isinstance(inputs, (list, tuple, set))
        self.inputs = set(inputs)
        self.output = output

    def __call__(self, obj, **kwargs):
        output = {}
        for k, v in obj.items():
            if k in self.inputs:
                output[self.output] = output.get(self.output, []) + v
            else:
                output[k] = v
        return output

    def extra_repr(self):
        return "inputs={}, output='{}'".format(self.inputs, self.output)


class Subscribe(Operator):
    def __init__(self, i):
        super().__init__(inplace=False)
        self.i = i

    def __call__(self, obj, **kwargs):
        return obj[self.i]


class Flatten(Operator):
    def __init__(self, key, inplace=False):
        super().__init__(inplace=inplace)
        self.key = key

    def _call(self, obj, **kwargs):
        if self.key not in obj:
            return obj
        obj = dict(obj)
        for k, v in obj[self.key].items():
            obj['{}.{}'.format(self.key, k)] = v
        return obj

    def _call_inplace(self, obj, **kwargs):
        if self.key not in obj:
            return obj
        for k, v in obj[self.key].items():
            obj['{}.{}'.format(self.key, k)] = v
        return obj


class Updator(Operator):
    def __init__(self, d: dict, inplace=False):
        super().__init__(inplace=inplace)
        self.d = d

    def _call(self, obj, **kwargs):
        obj = dict(obj)
        obj.update(self.d)
        return obj

    def _call_inplace(self, obj, **kwargs):
        obj.update(self.d)
        return obj


class CutKey(Operator):
    def __init__(self):
        super().__init__(False)

    @staticmethod
    @lru_cache()
    def cut(s, tokenizer, **kwargs):
        output = tuple(tokenizer.lcut(s))
        if len(output) == 0:
            output = s
        elif len(output) == 1:
            output = output[0]
        return output

    def __call__(self, obj, **kwargs):
        return {self.cut(k, **kwargs): v for k, v in obj.items()}
