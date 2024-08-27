from abc import abstractmethod
from typing import List, Generic, TypeVar
from monad import Option, Mapper

T = TypeVar("T")


class Pipe(Generic[T], Mapper):
    """
    Type Consistency Pipe
    """

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return f"Pipe<{self.__class__.__name__}>"

    def __call__(self, data: Option[T]) -> Option[T]:
        if data.is_none():
            # data has been filtered out.
            return data
        return self.map(data)

    @abstractmethod
    def map(self, data: Option[T]) -> Option[T]:
        raise NotImplemented


class Sequencer(Pipe[T]):
    def __init__(self, pipes: List[Pipe[T]]):
        self.pipes = pipes

    def map(self, data: Option[T]) -> Option[T]:
        for pipe in self.pipes:
            data = pipe.map(data)
            if data.is_none():
                print(f"Data is filtered out by {pipe}.")
                break
        return data


class Pipeline:
    pass
