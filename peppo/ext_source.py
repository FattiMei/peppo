from enum import Enum
from dataclasses import dataclass

import peppo.clang
import llvmlite.binding as llvm


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

    def compile(self) -> llvm.ModuleRef:
        return peppo.clang.compile(
                self.src,
                self.language.value,
                self.defines,
                self.include_directories)
