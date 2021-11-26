import json
import sys
import traceback
from typing import Union, List

from ...operator import Operator


class JsonPathNode(Operator):
    def __init__(self, inplace=False, debug=False, error=False, warning=False):
        self.childs_or_processors: List[Union[JsonPathNode, Operator]] = []
        self.debug = debug
        self.warning = warning
        self.error = error
        super().__init__(inplace=inplace)

    def inplace(self, inplace: bool):
        super().inplace(inplace)
        for child_or_op in self.childs_or_processors:
            child_or_op.inplace(inplace)

    def get(self, obj):
        """

        Args:
            obj:

        Returns:
            obj: 拿到的对象
            flag: 对象是否存在
        """
        return obj, True

    def _call(self, obj, new_obj, **kwargs):
        return new_obj

    def _call_inplace(self, obj, new_obj, **kwargs):
        return new_obj

    def __call__(self, obj, **kwargs):
        """
        计算逻辑，深层优先，同层按照注册顺序排序
        :param obj: 输入的对象
        :param kwargs:
        :return:
        """
        new_obj, flag = self.get(obj)
        if len(self.childs_or_processors) == 0:
            return new_obj
        if not flag:
            return obj
        for i, child_or_op in enumerate(self.childs_or_processors):
            try:
                new_obj = child_or_op(new_obj, **kwargs)
            except Exception as e:
                if self.debug:
                    print('{} encounter error'.format(self.__class__.__name__), file=sys.stderr)
                    print('current node:\n', self, file=sys.stderr)
                    print('child node {}:\n'.format(i), child_or_op, file=sys.stderr)
                    print('input:', json.dumps(new_obj, indent=1), file=sys.stderr)
                if self.warning or self.debug:
                    traceback.print_exc()
                elif self.error:
                    raise e
        return self.call(obj, new_obj, **kwargs)

    def is_duplicate(self, other) -> bool:
        raise NotImplementedError

    @classmethod
    def from_json_path(cls, json_path: str):
        """

        :param json_path:
        :return: (对象, 剩余的json_path)
        如果json_path不合法，那么raise AssertionError
        """
        raise NotImplementedError

    def index_of_last_node_processor(self) -> int:
        i = 0
        while i < len(self.childs_or_processors) and not isinstance(self.childs_or_processors[i], JsonPathNode):
            i += 1
        if i == len(self.childs_or_processors):
            i = 0
        return i

    def insert(self, other):
        index_of_last_node_processor = self.index_of_last_node_processor()
        for child_or_processor in self.childs_or_processors[index_of_last_node_processor:]:
            if isinstance(child_or_processor, JsonPathNode) and child_or_processor.is_duplicate(other):
                return child_or_processor
        self.childs_or_processors.append(other)
        return other

    def extra_repr(self):
        return 'root:$'

    def __repr__(self):
        output = self.extra_repr()
        for child_or_processor in self.childs_or_processors:
            strs = str(child_or_processor).split('\n')
            strs[0] = '|____' + strs[0]
            output += ''.join(['\n     ' + line for line in strs])
        return output
