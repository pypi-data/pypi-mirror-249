from typing import Any
from dataclasses import dataclass


@dataclass
class R:
    _val: Any = None

    def __call__(self, x: Any) -> Any:
        self._val = x

    @property
    def val(self) -> Any:
        return self._val

    def is_none(self) -> bool:
        raise NotImplementedError(".is_none() method not implemented.")

    def is_some(self) -> bool:
        raise NotImplementedError(".is_some() method not implemented.")

    def is_ok(self) -> bool:
        raise NotImplementedError(".is_ok() method not implemented.")

    def is_err(self) -> bool:
        raise NotImplementedError(".is_err() method not implemented.")

    def unwrap(self) -> Any:
        raise NotImplementedError(".unwrap() method not implemented.")

    def unwrap_or(self, default: Any) -> Any:
        raise NotImplementedError(".unwrap_or() method not implemented.")


class Option(R):
    def is_none(self) -> bool:
        return self.val is None

    def is_some(self) -> bool:
        return not self.is_none()

    def unwrap(self) -> Any:
        return None if self.is_none() else self.val

    def unwrap_or(self, default: Any) -> Any:
        return default if self.is_none() else self.val


class Result(R):
    def is_err(self) -> bool:
        return self.val is None

    def is_ok(self) -> bool:
        return not self.is_err()

    def unwrap(self) -> Any:
        if self.is_ok():
            return self.val
        else:
            raise Exception("> Err: Value is None!")
