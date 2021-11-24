from .base import JsonPathNode


class Subscript(JsonPathNode):
    def __init__(self, index, inplace=False):
        super().__init__(inplace=inplace)
        self.index = int(index)

    def get(self, obj):
        if len(obj) > self.index:
            return obj[self.index], True
        else:
            return None, False

    def _call(self, obj, new_obj, **kwargs):
        return [new_obj if i == self.index else v for i, v in enumerate(obj)]

    def _call_inplace(self, obj, new_obj, **kwargs):
        if len(obj) > self.index:
            obj[self.index] = new_obj
        return obj

    def is_duplicate(self, other) -> bool:
        return type(self) == type(other) and self.index == other.index

    @classmethod
    def from_json_path(cls, json_path: str):
        assert len(json_path) > 2 and json_path[1] == '[', json_path
        right_square_bracket_pos = json_path.find(']')
        assert right_square_bracket_pos > 0, json_path
        index = json_path[2:right_square_bracket_pos]
        assert index.isdigit(), json_path
        return cls(index=index), '$'+json_path[right_square_bracket_pos+1:]

    def extra_repr(self):
        return "[{}]".format(self.index)
