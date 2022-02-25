import string
from typing import Iterable, List
import jieba
from .tokenizer import Tokenizer


class JiebaTokenizer(Tokenizer):
    def __init__(self, dictionary=None, camel_to_snake=False, stopwords=None):
        if dictionary is not None:
            tokenizer = jieba.Tokenizer(dictionary)
        else:
            tokenizer = jieba.Tokenizer()
        tokenizer.initialize()
        tokenizer.lock = None
        self.tokenizer = tokenizer
        self.camel_to_snake = camel_to_snake
        self.stopwords = stopwords

    def cut(self, s: str, **kwargs) -> Iterable[str]:
        if self.camel_to_snake:
            from ..utils import camel_to_snake
            s = camel_to_snake(s)
        output = self.tokenizer.cut(s, **kwargs)
        if self.stopwords is not None:
            output = (x for x in output if x not in self.stopwords)
        return output

    def lcut(self, s: str, **kwargs) -> List[str]:
        return list(self.cut(s, **kwargs))

    def __repr__(self):
        return '{}(kill_camel={})'.format(self.__class__.__name__, self.camel_to_snake)


_default_tokenizer = None


def default_tokenizer():
    global _default_tokenizer
    if _default_tokenizer is None and JiebaTokenizer is not None:
        stopwords = set(string.ascii_letters).union(string.punctuation).union(string.digits).union([' ', '__'])
        stopwords = stopwords.union("，。/；‘【】、·-=～——+）（*&……%¥#@！「」｜“：？》《")
        _default_tokenizer = JiebaTokenizer(camel_to_snake=True, stopwords=stopwords)
    return _default_tokenizer
