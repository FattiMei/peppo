from enum import Enum
from subprocess import run
from dataclasses import dataclass

from peppo.ingest.compiler import (
    clang_compile_command,
    clangxx_compile_command,
    flang_compile_command,
)

import llvmlite.binding as llvm


class Language(Enum):
    C   = 'c'
    CPP = 'c++'
    F90 = 'f90'


@dataclass
class ExtSource:
    language: Language
    src: str


LANGUAGE_TO_COMPILE_COMMAND_TABLE = {
    Language.C  : clang_compile_command('c'),
    Language.CPP: clangxx_compile_command('c++'),
    Language.F90: flang_compile_command('f90'),
}


def compile_snippet(snippet: ExtSource) -> llvm.ModuleRef:
    cmd = LANGUAGE_TO_COMPILE_COMMAND_TABLE[snippet.language]
    res = run(
        cmd,
        input=snippet.src.encode(),
        capture_output=True,
        check=False
    )

    returncode = res.returncode
    if returncode == 0:
        ir = res.stdout.decode()
        return llvm.parse_assembly(ir)
    else:
        err = res.stderr.decode()
        raise RuntimeError(
            f'Command {cmd} failed with exit {returncode}: \n{err}'
        )

