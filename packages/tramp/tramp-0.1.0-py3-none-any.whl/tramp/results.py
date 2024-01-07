from typing import Generic, NoReturn, TypeVar, Type


V = TypeVar("V")


class ResultException(Exception):
    """Base exception for errors raised by a result object."""


class ResultTypeCannotBeInstantiated(ResultException):
    """Raised when attempting to instantiate a result type that is not a value type."""


class ResultHasNoValueException(ResultException):
    """Raised when a result object has no value."""


class Result(Generic[V]):
    Value: "Type[Result[V]]"
    Nothing: "Result[V]"

    def __new__(cls, *_):
        if cls is Result:
            raise ResultTypeCannotBeInstantiated(
                "You cannot instantiate the base result type."
            )

        return super().__new__(cls)

    @property
    def value(self) -> V | NoReturn:
        raise ResultHasNoValueException(
            "You cannot Result directly, you must use either Result.Value or Result.Nothing"
        )

    def value_or(self, default: V) -> V:
        return self.value

    def __bool__(self):
        return False


class Value(Result):
    __match_args__ = ("value",)

    def __init__(self, value: V):
        self._value = value

    @property
    def value(self) -> V:
        return self._value

    def __bool__(self):
        return True


class Nothing(Result):
    def __new__(cls, *_):
        if not hasattr(Result, "Nothing"):
            return super().__new__(cls)

        return Result.Nothing

    @property
    def value(self) -> NoReturn:
        raise ResultHasNoValueException("No value was set, this is Nothing")

    def value_or(self, default: V) -> V:
        return default


Result.Value = Value
Result.Nothing = Nothing()
