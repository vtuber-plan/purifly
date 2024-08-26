from abc import ABC, abstractmethod
from typing import Any


class Option:
    def __init__(self, value: Any):
        self.value = value

    def __repr__(self):
        return f"Option({self.value})"

    def __str__(self):
        return f"Option({self.value})"

    def __eq__(self, other):
        if isinstance(other, Option):
            return self.value == other.value
        return False

    def some(self, value: Any):
        self.value = value

    def none(self):
        self.value = None

    def is_some(self):
        return self.value is not None

    def is_none(self):
        return self.value is None

    def unwrap(self):
        if self.is_some():
            return self.value
        raise ValueError("Option is None")

    def unwrap_or(self, default: Any):
        if self.is_some():
            return self.value
        return default


class Mapper(ABC):
    """
    P: Option\\
    Identity Element: I(x) = x\\
    \\
    f: P ——> Some\\
    g: P ——> Some\\
    z: P ——> None\\
    \\
    f·g(x) = f(g(x))\\
    f·I(x) = I·f(x) = f(x)\\
    f·z(x) = z·f(x) = z(x)\\

    """

    def __call__(self, data: Option) -> Option:
        return self.map(data)

    @abstractmethod
    def map(self, data: Option) -> Option:
        raise NotImplemented
