from enum import Enum
from dataclasses import dataclass


class Type(Enum):
    SCALAR = 0


class Value:
    pass


class Constant(Value):
    def __init__(self, value, dtype: Type = None):
        self.value = value
        self.dtype = dtype


@dataclass
class Mul(Value):
    left:  Value
    right: Value
    dtype: Type = None
    name:  str = None


@dataclass
class Add(Value):
    left:  Value
    right: Value
    dtype: Type = None
    name:  str = None


@dataclass
class Function(Value):
    signature: tuple[Type]
    body: Value = None

