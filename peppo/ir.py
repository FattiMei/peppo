from enum import Enum
from dataclasses import dataclass


class Language(Enum):
    C       = 'c'
    CPP     = 'c++'
    FORTRAN = 'fortran'


class IrType(Enum):
    LLVM_IR = 'llvm'
    MLIR_IR = 'mlir'


@dataclass
class Ir:
    ir_type: IrType
    src: str

    def __str__(self) -> str:
        return self.src

