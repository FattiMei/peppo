from enum import Enum
from dataclasses import dataclass

import peppo.compiler
from peppo.ir import Language, IrType, Ir


@dataclass
class ExtSource:
    # There were also `defines` and `include_directories` fields.
    # I decided to delay the feature until the need for compiling
    # large projects emerges
    src: str
    language: Language

    def compile(self, ir_type: IrType) -> Ir:
        return peppo.compiler.compile(
                self.src,
                self.language,
                ir_type)

    def compile_to_llvm_ir(self) -> Ir:
        return self.compile(IrType.LLVM_IR)

    def compile_to_mlir(self) -> Ir:
        return self.compile(IrType.MLIR_IR)

