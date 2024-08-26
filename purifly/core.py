from abc import ABC, abstractmethod
from typing import Any, List, Optional, Union
from . import Option, Mapper


class Pipe(Mapper):
    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__

    @abstractmethod
    def map(self, data: Option) -> Option:
        raise NotImplemented


class IdentityPipe(Mapper):
    """Identity Element
    I(x) = x \\
    f·I(x) = I·f(x) = f(x)
    """

    def map(self, data: Option) -> Option:
        return data


class Sequencer(Pipe):
    def __init__(self, pipes: List[Pipe]):
        self.pipes = pipes

    def map(self, data: Option) -> Option:
        for pipe in self.pipes:
            data = pipe.map(data)
            if data.is_none():
                print(f"Data is filtered out by {pipe}.")
                break
        return data


class Pipeline:
    pass
