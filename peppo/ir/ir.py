from peppo.ir.types import DType
from dataclasses import dataclass


@dataclass
class Value:
    name: str = None
    dtype: DType = None


class Constant(Value):
    def __init__(self, value, dtype: DType, name: str = None):
        super().__init__(dtype=dtype, name=name)
        self.value = value

    def lower_to_llvm(self) -> "":
        # this only works for scalar types for now...
        return dtype.llvm_type(self.value)


class Argument(Value):
    def __init__(self, dtype: DType, name: str = None):
        super().__init__(dtype=dtype, name=name)


class Function:
    def __init__(self, signature: tuple[Argument], body: Value = None, name: str = None):
        self.signature = signature
        self.name = name

        if body is not None:
            self.set_body(body)

    def set_body(self, body: Value):
        """
        This function could potentially check the correctness of the function body.
        In particular I can check that every value is either a constant or depends on an argument
        """
        self.body = body

    def __call__(self, *args) -> "FunctionCall":
        return FunctionCall(self, args)

    def lower_to_llvm(self) -> "":
        return None


@dataclass
class FunctionCall(Value):
    function: Function
    args: tuple[Value]


@dataclass
class BinExpr(Value):
    left: Value
    right: Value


@dataclass
class Mul(BinExpr):
    def lower_to_llvm(self, builder):
        pass

