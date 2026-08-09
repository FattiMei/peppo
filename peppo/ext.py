from enum import Enum
from dataclasses import dataclass


class Language(Enum):
    C       = 'c'
    CPP     = 'c++'
    FORTRAN = 'fortran'


@dataclass
class ExtSource:
    src: str
    language: Language
    defines: list[str] = None
    include_directories: list[str] = None

    def compile_to_llvm_ir(self) -> str:
        pass

    def compile_to_mlir(self) -> str:
        pass

