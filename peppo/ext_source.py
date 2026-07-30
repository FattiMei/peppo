from enum import Enum
from subprocess import run, CalledProcessError
from dataclasses import dataclass


import llvmlite.binding as llvm


def _clang_compile_command(language: str,
                           defines: list[str] = None,
                           include_directories: list[str] = None) -> list[str]:
    """
    Returns the clang command for an unoptimized build
    that outputs llvm ir

    An unoptimized build will automatically insert function
    attributes like `noopt` and `noinline` which interfere
    with later optimization passes
    """
    cmd = [
            'clang',
            '-S', '-emit-llvm',
            '-O1', '-mllvm', '-disable-llvm-optzns', '-disable-llvm-passes',
            '-x', language, '-',
            '-o', '-'
            ]

    if include_directories is not None:
        for include_dir in include_directories:
            cmd.extend(('-I', include_dir))

    if defines is not None:
        for define in defines:
            cmd.extend(('-D', define))

    return cmd


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

    def compile_to_llvm_ir(self) -> llvm.ModuleRef:
        clang_compile_cmd = _clang_compile_command(
                self.language.value,
                self.defines,
                self.include_directories)

        res = run(
                clang_compile_cmd,
                input=self.src.encode(),
                capture_output=True,
                check=True)

        llvm_ir = res.stdout.decode()
        module = llvm.parse_assembly(llvm_ir)
        module.verify()

        return module

