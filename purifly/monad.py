from abc import ABC, abstractmethod
from typing import Any, Callable, Iterator, List, Optional, TypeVar, Generic
from error import UnwrapException

T = TypeVar("T")
U = TypeVar("U")


class Option(Generic[T], ABC):
    """`Option` monad for python."""

    @staticmethod
    def from_nullable(value: Optional[T]) -> "Option[T]":
        """Construct an `Option` from a nullable value."""
        if value is None:
            return OpNone()
        else:
            return OpSome(value)

    @staticmethod
    def some(value: T) -> "Option[T]":
        """Create a value of `Some(T)`.

        Args:
            value: Some value of type `T`.

        Returns:
            `Option<Some(T)>`
        """
        return OpSome(value)

    @staticmethod
    def none() -> "Option[T]":
        """Create a value of `None`.

        Returns:
            `Option<None>`
        """
        return OpNone()

    @abstractmethod
    def __bool__(self) -> bool:
        """Returns `False` only if contained value is `None`."""
        ...

    @abstractmethod
    def __str__(self) -> str: ...

    @abstractmethod
    def __repr__(self) -> str: ...

    @abstractmethod
    def __eq__(self, other) -> bool: ...

    @abstractmethod
    def __hash__(self) -> int:
        """`hash(Option)` has the same result as its contained value."""
        ...

    @abstractmethod
    def is_some(self) -> bool:
        """Returns `True` if the option is a `Some` value.

        Returns:
            Whether the option is a `Some` value.

        Examples:
            ```python
            x: Option[int] = Option.some(2)
            assert x.is_some()
            x: Option[int] = Option.none()
            assert not x.is_some()
            ```
        """
        ...

    @abstractmethod
    def is_none(self) -> bool:
        """Returns `True` if the option is a `None` value.

        Returns:
            Whether the option is a `None` value.

        Examples:
            ```python
            x: Option[int] = Option.some(2)
            assert not x.is_none()
            x: Option[int] = Option.none()
            assert x.is_none()
            ```
        """
        ...

    @abstractmethod
    def is_some_and(self, func: Callable[[T], bool]) -> bool:
        """Returns true if the option is a `Some` and the value inside it matches a predicate.

        Args:
            func: A callable object which accepts the *not-none* value of the option and returns a boolean.

        Returns:
            Whether the option is a `Some` and the value inside it matches a predicate.

        Examples:
            ```python
            x: Option[int] = Option.some(2)
            assert x.is_some_and(lambda v: v > 1)
            x: Option[int] = Option.some(0)
            assert not x.is_some_and(lambda v: v > 1)
            x: Option[int] = Option.none()
            assert not x.is_some_and(lambda v: v > 1)
            ```
        """
        ...

    @abstractmethod
    def expect(self, msg: str) -> T:
        """Returns the contained `Some` value.

        Returns the contained `Some` value, and raise an exception if the value is a `None` with a custom panic
        message provided by msg.

        **Recommended Message Style**

        We recommend that `expect` messages are used to describe the reason you *expect* the `Option` should be `Some`.

        ```python
        item = slice.get(0).expect("slice should not be empty");
        ```

        **Hint**: If you’re having trouble remembering how to phrase expect error messages,
        remember to focus on the word “should” as in “env variable should be set by blah”
        or “the given binary should be available and executable by the current user”.

        Args:
            msg: The message to display if this option is none.

        Returns:
            The contained `Some` value.

        Raises:
            error.UnwrapException: Raise an exception if the value is a `None` with a custom message provided by msg.

        Examples:
            ```python
            x: Option[str] = Option.some('value')
            assert x.expect('hey, this is an `Option<None>` object') == 'value'
            x: Option[str] = Option.none()
            try:
                x.expect('hey, this is an `Option<None>` object')
            except UnwrapException as e:
                assert str(e) == 'hey, this is an `Option<None>` object'
            ```
        """
        ...

    @abstractmethod
    def to_array(self) -> List[T]:
        """Returns an array of the possible contained value.

        Examples:
            ```python
            assert Option.some(1).to_array() == [1]
            assert Option.none().to_array() == []
            ```
        """
        ...

    @abstractmethod
    def unwrap(self) -> T:
        """Returns the contained `Some` value.

        Returns:
            The wrapped `Some` value.

        Raises:
            error.UnwrapException: Raise an exception if the value is a `None`.

        Examples:
            ```python
            x: Option[str] = Option.some("air")
            assert x.unwrap() == "air"
            x: Option[str] = Option.none()
            try:
                x.unwrap()
            except UnwrapException as e:
                assert str(e) == 'OptionError: call `Option.unwrap` on an `Option<None>` object'
            ```
        """
        ...

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """Returns the contained `Some` value or a provided defaul

        Arguments passed to `unwrap_or` are eagerly evaluated.<br />If you are passing the result of a function call,
        it is recommended to use `unwrap_or_else`,
        which is lazily evaluated.

        Args:
            default: The default value.

        Returns:
            The contained `Some` value or a provided defaul

        Examples:
            ```python
            assert Option.some("car").unwrap_or("bike") == "car"
            assert Option.none().unwrap_or("bike") == "bike"
            ```
        """
        ...

    @abstractmethod
    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        """Returns the contained `Some` value or computes it from a callable objec

        Args:
            func: A callable object to compute.

        Examples:
            ```python
            k = 10
            assert Option.some(4).unwrap_or_else(lambda: 2 * k) == 4
            assert Option.none().unwrap_or_else(lambda: 2 * k) == 20
            ```
        """
        ...

    @abstractmethod
    def inspect(self, func: Callable[[T], None]) -> "Option[T]":
        """Calls the provided closure with the contained value (if `Some`), and return the option itself.

        Args:
            func: A callable object which accepts the wrapped value and returns nothing.

        Examples:
            ```python
            x = []
            Option.some(2).inspect(lambda s: x.append(s))
            assert x == [2]
            Option.none().inspect(lambda s: x.append(s))
            assert x == [2]
            ```
        """
        ...

    @abstractmethod
    def map(self, func: Callable[[T], U]) -> "Option[U]":
        """Maps an `Option<T>` to `Option<U>` by applying a function
        to a contained value (if `Some`) or returns `None` (if `None`).

        Args:
            func: A callable object that accepts the wrapped value and returns the processed value.

        Returns:
            Returns `Option<Some(U)>` if the option is `Some` and returns `None` otherwise.

        Examples:
            ```python
            maybe_some_string = Option.some("Hello, World!")
            # `Option.map` will create a new option object
            maybe_some_len = maybe_some_string.map(lambda s: len(s))
            assert maybe_some_len == Option.some(13)
            assert Option.none().map(lambda s: len(s)) == Option.none()
            ```
        """
        ...

    @abstractmethod
    def map_or(self, default: U, func: Callable[[T], U]) -> U:
        """Returns the provided default result (if none), or applies a function to the contained value (if any).

        Arguments passed to map_or are eagerly evaluated.<br />If you are passing the result of a function call,
        it is recommended to use `map_or_else`, which is lazily evaluated.

        Args:
            default: The default value if the option is `None`.
            func: The function to apply to the contained value.

        Examples:
            ```python
            assert Option.some('foo').map_or(42, lambda s: len(s)) == 3
            assert Option.none().map_or(42, lambda s: len(s)) == 42
            ```
        """
        ...

    @abstractmethod
    def map_or_else(self, default: Callable[[], U], func: Callable[[T], U]) -> U:
        """Computes a default function result (if none),
        or applies a different function to the contained value (if any).

        Args:
            default: The function to produce a default value.
            func: The function to apply to the contained value.

        Examples:
            ```python
            k = 21
            assert Option.some('bar').map_or_else(lambda: 2 * k, lambda s: len(s)) == 3
            assert Option.none().map_or_else(lambda: 2 * k, lambda s: len(s)) == 42
            ```
        """
        ...

    @abstractmethod
    def filter(self, func: Callable[[T], bool]) -> "Option[T]":
        """Filter the option.

        Returns `None` if the option is `None`, otherwise calls predicate with the wrapped value and returns:

        - `Some(t)` if predicate returns `True` (where `t` is the wrapped value), and
        - `None` if predicate returns `False`.

        This function works similar to `builtin.filter()`.
        You can imagine the `Option<T>` being an iterator over one or zero elements.
        `filter()` lets you decide which elements to keep.

        Args:
            func: The callable object decides whether the element should be kep

        Examples:
            ```python
            assert Option.none().filter(lambda n: n % 2 == 0) == Option.none()
            assert Option.some(3).filter(lambda n: n % 2 == 0) == Option.none()
            assert Option.some(4).filter(lambda n: n % 2 == 0) == Option.some(4)
            ```
        """
        ...

    @abstractmethod
    def and_then(self, func: Callable[[T], "Option[U]"]) -> "Option[U]":
        """Returns `None` if the option is `None`,
        otherwise calls `func` with the wrapped value and returns the result

        Args:
            func: A callable object to produce the next value.

        Examples:
            ```python
            assert Option.some(2).and_then(lambda x: Option.some(str(x))) == Option.some('2')
            assert Option.some(10).and_then(lambda _: Option.none()) == Option.none()
            assert Option.none().and_then(lambda x: Option.some(str(x))) == Option.none()
            ```
            Often used to chain fallible operations that may return `None`.
            ```python
            def get_from(l, i):
                try:
                    return Option.some(l[i])
                except IndexError:
                    return Option.none()

            arr_2d = [["A0", "A1"], ["B0", "B1"]]
            assert get_from(arr_2d, 0).and_then(lambda row: get_from(row, 1)) == Option.some('A1')
            assert get_from(arr_2d, 2).and_then(lambda row: get_from(row, 0)) == Option.none()
            ```
        """
        ...

    @abstractmethod
    def or_else(self, func: Callable[[], "Option[T]"]) -> "Option[T]":
        """Returns the option if it contains a value, otherwise calls `func` and returns the result

        Args:
            func: A callable object to produce the next value.

        Examples:
            ```python
            assert Option.some('foo').or_else(lambda: Option.some('bar')) == Option.some('foo')
            assert Option.none().or_else(lambda: Option.some('bar')) == Option.some('bar')
            assert Option.none().or_else(lambda: Option.none()) == Option.none()
            ```
        """
        ...

    def __add__(self, other: "Option[Any]") -> "Option[Any]":
        """Alias `self.__value.__add__`.

        Returns:
            If both value are `Some`, this will return `Some(self + other)`. Otherwise, return `None`.
        """
        if isinstance(other, Option):
            if self.is_some() and other.is_some():
                return Option.some(self.unwrap() + other.unwrap())
            else:
                return Option.none()
        else:
            raise TypeError("expect another Option")

    def __mul__(self, other: "Option[Any]") -> "Option[Any]":
        """Alias `self.__value.__mul__`.

        Returns:
            If both value are `Some`, this will return `Some(self * other)`. Otherwise, return `None`.
        """
        if isinstance(other, Option):
            if self.is_some() and other.is_some():
                return Option.some(self.unwrap() * other.unwrap())
            else:
                return Option.none()
        else:
            raise TypeError("expect another Option")

    def __and__(self, other: "Option[Any]"):
        if isinstance(other, Option):
            raise NotImplemented
        else:
            raise TypeError("expect another Option")

    def __or__(self, other: "Option[Any]"):
        if isinstance(other, Option):
            raise NotImplemented
        else:
            raise TypeError("expect another Option")

    def __xor__(self, other: "Option[Any]"):
        if isinstance(other, Option):
            raise NotImplemented
        else:
            raise TypeError("expect another Option")

    def __iter__(self) -> Iterator[T]:
        return iter(self.to_array())

    def to_iter(self) -> Iterator[T]:
        """Alias `iter(self.to_array())`."""
        return iter(self.to_array())


class OpSome(Generic[T], Option[T]):
    __value: T

    def __init__(self, value: T) -> None:
        self.__value = value

    def __bool__(self) -> bool:
        return True

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return f"Option<{self.__value}>"

    def __eq__(self, other):
        if isinstance(other, OpSome):
            return self.__value == other.__value
        else:
            return False

    def __hash__(self):
        return hash(self.__value)

    def is_some(self) -> bool:
        return True

    def is_none(self) -> bool:
        return False

    def is_some_and(self, func: Callable[[T], bool]) -> bool:
        return func(self.__value)

    def expect(self, msg: str) -> T:
        return self.__value

    def to_array(self) -> List[T]:
        return [self.__value]

    def unwrap(self) -> T:
        return self.__value

    def unwrap_or(self, default: T) -> T:
        return self.__value

    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        return self.__value

    def inspect(self, func: Callable[[T], None]) -> Option[T]:
        func(self.__value)
        return self

    def map(self, func: Callable[[T], U]) -> Option[U]:
        return Option.some(func(self.__value))

    def map_or(self, default: U, func: Callable[[T], U]) -> U:
        return func(self.__value)

    def map_or_else(self, default: Callable[[], U], func: Callable[[T], U]) -> U:
        return func(self.__value)

    def filter(self, func: Callable[[T], bool]) -> Option[T]:
        if func(self.__value):
            return self.clone()
        else:
            return OpNone()

    def and_then(self, func: Callable[[T], Option[U]]) -> Option[U]:
        return func(self.__value)

    def or_else(self, func: Callable[[], Option[T]]) -> Option[T]:
        return self.clone()


class OpNone(Generic[T], Option[T]):
    def __bool__(self):
        return False

    def __str__(self):
        return "None"

    def __repr__(self):
        return "Option<None>"

    def __eq__(self, other):
        return isinstance(other, OpNone)

    def __hash__(self):
        return hash(None)

    def is_some(self) -> bool:
        return False

    def is_none(self) -> bool:
        return True

    def is_some_and(self, func: Callable[[T], bool]) -> bool:
        return False

    def expect(self, msg: str) -> T:
        raise UnwrapException(msg)

    def to_array(self) -> List[T]:
        return []

    def unwrap(self) -> T:
        raise UnwrapException(
            "Option", "call `Option.unwrap` on an `Option<None>` object"
        )

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        return func()

    def inspect(self, func: Callable[[T], None]) -> Option[T]:
        return self

    def map(self, func: Callable[[T], U]) -> Option[U]:
        return Option.none()

    def map_or(self, default: U, func: Callable[[T], U]) -> U:
        return default

    def map_or_else(self, default: Callable[[], U], func: Callable[[T], U]) -> U:
        return default()

    def filter(self, func: Callable[[T], bool]) -> Option[T]:
        return self

    def and_then(self, func: Callable[[T], Option[U]]) -> Option[U]:
        return Option.none()

    def or_else(self, func: Callable[[], Option[T]]) -> Option[T]:
        return func()


class Mapper(ABC):
    def __call__(self, data: Option) -> Option:
        return self.map(data)

    @abstractmethod
    def map(self, data: Option) -> Option:
        raise NotImplemented
