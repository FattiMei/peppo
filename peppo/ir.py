import inspect
from enum import Enum
from collections.abc import Callable
from dataclasses import dataclass


class DType:
    pass


class Value:
    def __init__(self, name: str = None, dtype: DType = None):
        self.name = name
        self.dtype = dtype


class Constant(Value):
    def __init__(self, value, name: str = None):
        super().__init__(name=name)
        self.value = value


class BinExpr(Value):
    def __init__(self, left: Value, right: Value, name: str = None):
        super().__init__(name=name)
        self.left = left
        self.right = right


# this is not part of the ir, but it's necessary to define procedures as decorated python functions
class Function:
    """
    This class makes possible to write DSL functions as decorated python functions.
    With this class one should be able to produce a LLVM module
    """
    def __init__(self, signature: tuple[DType], body: Callable[..., Value], name: str = None):
        self.signature = signature
        self.body = body
        self.name = name

    def __call__(self, *args):
        """
        This method is used when a DSL function is called within a DSL function
        We just return an IR node that doesn't expand the function body

        This call should validate the arguments against the signature
        """
        return FunctionCall(self, *args)


class FunctionCall(Value):
    # this should add the `name` argument
    def __init__(self, func: Function, *args):
        self.func = func


def proc(f):
    """
    This decorator makes the embedded DSL possible.
    With a clever trick we can capture the body of the function and decorate it at the same time.
    The result is a callable Function object that can be transformed as the user requires
    """
    return Function(
        signature=inspect.signature(f),
        body=f,
        name=f.__name__)

