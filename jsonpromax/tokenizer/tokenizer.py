from abc import ABC, abstractmethod
from typing import List, Iterable


class Tokenizer(ABC):
    @abstractmethod
    def cut(self, s: str, **kwargs) -> Iterable[str]:
        return []

    @abstractmethod
    def lcut(self, s: str, **kwargs) -> List[str]:
        return []
