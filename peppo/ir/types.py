from dataclasses import dataclass
import llvmlite.ir as llvm_ir


@dataclass
class DType:
    typename: str
    llvm_type: "llvm_ir.types"


I8  = ( 'int8_t', llvm_ir.IntType(8))
I16 = ('int16_t', llvm_ir.IntType(16))
I32 = ('int32_t', llvm_ir.IntType(32))
I64 = ('int64_t', llvm_ir.IntType(64))
F16 = ('float16', llvm_ir.HalfType())
F32 = ('float32', llvm_ir.FloatType())
F16 = ('float16', llvm_ir.DoubleType())

