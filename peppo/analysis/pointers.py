import xdsl
from xdsl.dialects import llvm
from enum import Enum


"""
This file is meant for analysis passes on pointer usage.
The analysis are motivated by the fact that FORTRAN functions
take arguments by untyped pointers.


# POINTER USAGE PASS:
    1. determine if the corresponding variable is scalar or a vector
    2. determine the underlying type, based on the usage of the pointer
    3. determine if a pointer to an array has been used canonically,
       that is:
           * only used by load and stores and getelementptr
           * the result of getelementptr only used in load and stores


The xdsl features (which are mirrors of MLIR ones) should be able to easily
support this analysis


# ARGUMENT POINTER TO SCALAR -> SCALAR
I could also write a pass that transforms those pointers to scalars into
scalar arguments if some conditions are met:
    * the pointer is only used in loads
    * (redundant) no pointer arithmetic is performed on it


# POINTER ACCESS BOUNDS
For pointers that are associated to a buffer, we could find the access bounds.

I expect to find the getelementptr operations that use the pointer and retrieve the indices
I expect those indices to be somewhat related to an induction variable
We can retrieve, maybe with some already existing analyis the induction variables ranges

NOTE: induction variables ranges should be very easy to access in the scf dialect,
do we have access to it? Does FIR lower to scf?
"""


class PointerAnalysisResult:
    class Kind(Enum):
        SCALAR           = 0
        AMBIGUOUS_SCALAR = 1
        BUFFER           = 2
        UNMATCHED        = 3

    def __init__(self, ptr, kind, types: list = None):
        self.ptr = ptr
        self.kind = kind
        self.types = types

        if kind == PointerAnalysisResult.Kind.SCALAR:
            assert(len(types) == 1)
        elif kind == PointerAnalysisResult.Kind.BUFFER:
            assert(len(types) == 1)

    def __repr__(self) -> str:
        return f'PointerAnalysisResult(ptr={self.ptr}, kind={self.kind}, types={self.types}'


def run_pointer_analysis(ptr) -> PointerAnalysisResult:
    """
    This implementation assumes to be working at the `llvm` dialect
    Also I'm assuming that `ptr` is a pointer, I can't yet enforce it
    """

    could_be_scalar = True
    could_be_buffer = False

    types = []

    for use in ptr.uses:
        op = use.operation

        if isinstance(op, llvm.LoadOp):
            result_type = op.result_types[0]
            types.append(result_type)

        elif isinstance(op, llvm.StoreOp):
            store_type = op.operand_types[0]
            types.append(store_type)

        elif isinstance(op, llvm.GEPOp):
            could_be_scalar = False
            could_be_buffer = True

            # for me a proper buffer is a pointer that
            # gets indexed by getelementptr, but that
            # pointer is only used in load and stores
            #   <=> is a SCALAR
            res = run_pointer_analysis(op.result)
            if res.kind == PointerAnalysisResult.Kind.SCALAR:
                types.extend(res.types)
            else:
                could_be_buffer = False

        else:
            could_be_scalar = False
            could_be_buffer = False
            break

    # the pointer could be dereferenced with different types,
    # I need to detect that and in principle inform the user
    types = list(set(types))

    # here the two conditions can never be true at the same time
    assert(not (could_be_scalar and could_be_buffer))

    if could_be_scalar:
        if len(types) == 1:
            kind = PointerAnalysisResult.Kind.SCALAR
        else:
            kind = PointerAnalysisResult.Kind.AMBIGUOUS_SCALAR

    elif could_be_buffer and len(types) == 1:
        kind = PointerAnalysisResult.Kind.BUFFER

    else:
        kind = PointerAnalysisResult.Kind.UNMATCHED

    return PointerAnalysisResult(ptr, kind, types)

