from enum import Enum
from dataclasses import dataclass

from peppo.ir import IrType, Ir
from peppo.compilers import Clang, ClangIR, Flang, FlangNew


class Language(Enum):
    C       = 'c'
    CPP     = 'c++'
    FORTRAN = 'fortran'


# this table encodes the logic for which compiler
# to use given the language and IR requirements
COMPILE_LOGIC_TABLE = {
        (Language.C      , IrType.LLVM_IR): Clang,
        (Language.CPP    , IrType.LLVM_IR): Clang,
        (Language.FORTRAN, IrType.LLVM_IR): Flang,

        (Language.C      , IrType.MLIR_IR): ClangIR,
        (Language.CPP    , IrType.MLIR_IR): ClangIR,
        (Language.FORTRAN, IrType.MLIR_IR): FlangNew,
        }


@dataclass
class ExtSource:
    # There were also `defines` and `include_directories` fields.
    # I decided to delay the feature until the need for compiling
    # large projects emerges
    src: str
    language: Language

    def compile(self, ir_type: IrType) -> Ir:
        compiler = COMPILE_LOGIC_TABLE[
                (self.language, IrType.LLVM_IR)
                ]()

        src = compiler.compile(
                self.src,
                self.language.value)
        return Ir(ir_type, src)

    def compile_to_llvm_ir(self) -> Ir:
        return self.compile(IrType.LLVM_IR)

    def compile_to_mlir(self) -> Ir:
        return self.compile(IrType.MLIR_IR)

