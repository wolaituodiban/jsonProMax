import string
from functools import lru_cache
from typing import Iterable, List

from .tokenizer import Tokenizer


class JiebaTokenizer(Tokenizer):
    def __init__(self, dictionary=None, camel_to_snake=False, stopwords=None):
        import jieba
        if dictionary is not None:
            tokenizer = jieba.Tokenizer(dictionary)
        else:
            tokenizer = jieba.Tokenizer()
        tokenizer.initialize()
        tokenizer.lock = None
        self.tokenizer = tokenizer
        self.camel_to_snake = camel_to_snake
        self.stopwords = stopwords

    # ! cut返回的是一个生成器，不能加缓存
    def cut(self, s: str, **kwargs) -> Iterable[str]:
        if self.camel_to_snake:
            from ..utils import camel_to_snake
            s = camel_to_snake(s)
        output = self.tokenizer.cut(s, **kwargs)
        if self.stopwords is not None:
            output = (x for x in output if x not in self.stopwords)
        return output

    @lru_cache()
    def lcut(self, s: str, **kwargs) -> List[str]:
        return list(self.cut(s, **kwargs))

    def __repr__(self):
        return '{}(kill_camel={})'.format(self.__class__.__name__, self.camel_to_snake)


_default_tokenizer = None


def default_tokenizer():
    global _default_tokenizer
    if _default_tokenizer is None and JiebaTokenizer is not None:
        stopwords = set(string.ascii_letters).union(string.punctuation).union(string.digits).union([' ', '__', ''])
        stopwords = stopwords.union("，。/；‘【】、·-=～——+）（*&……%¥#@！「」｜“：？》《")
        _default_tokenizer = JiebaTokenizer(camel_to_snake=True, stopwords=stopwords)
    return _default_tokenizer
