import json
import os
from typing import Union, List, Tuple, Iterable

import pandas as pd

from .node import JsonPathNode, ALL_JSON_PATH_NODE_CLASSES
from ..operator import Operator
from ..utils import strptime, mp_run


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
            error=False, warning=False, tokenizer=None):
        super().__init__(inplace=inplace, debug=debug, error=error, warning=warning)

        if processors is not None:
            for args in processors:
                insert_node(self, *args)
        self.tokenizer = tokenizer

        self.inplace(inplace)
        self.debug(debug)
        self.error(error)
        self.warning(warning)

    def __call__(self, *args, **kwargs):
        if self.tokenizer is not None:
            return super().__call__(*args, tokenizer=self.tokenizer, **kwargs)
        else:
            return super().__call__(*args, **kwargs)

    def _save(self, inputs, data_col, time_col=None, time_format=None):
        chunk, path = inputs
        if time_col not in chunk:
            chunk[time_col] = None
        json_str = []
        for row in chunk[[data_col, time_col]].itertuples():
            obj = row[1]
            if not isinstance(obj, (list, dict)):
                obj = json.loads(obj)
            now = strptime(row[2], time_format=time_format)
            json_str.append(json.dumps(self(obj, now=now)))
        chunk[data_col] = json_str
        chunk.to_csv(path)
        chunk['path'] = path
        return chunk.drop(columns=data_col)

    def save(self, chunks: Iterable[pd.DataFrame], dst: str, data_col, time_col=None, time_format=None, processes=None):
        inputs = ((chunk, os.path.join(dst, '{}.zip'.format(i))) for i, chunk in enumerate(chunks))
        kwds = dict(data_col=data_col, time_col=time_col, time_format=time_format)
        path_df = pd.concat(mp_run(self._save, inputs, kwds=kwds, processes=processes))
        path_df.to_csv(os.path.abspath(dst) + '_path.zip')
        return path_df

    def is_duplicate(self, other) -> bool:
        raise NotImplementedError

    @classmethod
    def from_json_path(cls, json_path: str):
        raise NotImplementedError
