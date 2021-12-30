from typing import Union, List, Tuple

from .node import JsonPathNode, ALL_JSON_PATH_NODE_CLASSES
from ..operator import Operator


def insert_node(root_node: JsonPathNode, json_path: str, processor: Operator = None):
    if json_path in ('$', '$.'):
        if processor is not None:
            root_node.childs_or_processors.append(processor)
    else:
        for cls in ALL_JSON_PATH_NODE_CLASSES.values():
            try:
                node, rest_json_path = cls.from_json_path(json_path)
                node = root_node.insert(node)
                insert_node(node, rest_json_path, processor)
                break
            except AssertionError:
                continue
        else:
            raise ValueError(json_path)


class JsonPathTree(JsonPathNode):
    """
    https://jsonpath.com/
    https://goessner.net/articles/JsonPath/
    """
    def __init__(
            self, processors: List[Union[Tuple[str], Tuple[str, Operator]]] = None, inplace=False, debug=False,
            error=False, warning=False):
        super().__init__(inplace=inplace, debug=debug, error=error, warning=warning)

        if processors is not None:
            for args in processors:
                insert_node(self, *args)

        self.inplace(inplace)
        self.debug(debug)
        self.error(error)
        self.warning(warning)

    def is_duplicate(self, other) -> bool:
        raise NotImplementedError

    @classmethod
    def from_json_path(cls, json_path: str):
        raise NotImplementedError
