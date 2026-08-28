import numpy as np
from peppo.ir import *


# We can call this a macro. Takes the value `x` and a numeric constant
# and returns the IR for the multiplication
#
# The user can then apply rewrites and ultimately convert this to LLVM IR
# using llvmlite bindings. At this stage the types have to be fully determined
def mult_by_constant(x, CONST):
    return Mul(x, CONST)


def foo(dtype, const_value: int):
    x = Value(dtype)
    CONST = Constant(dtype, const_value)

    func = Function()
    llvm_ir = lower_to_llvm(func)

    return llvm_ir


if __name__ == '__main__':

    pass
