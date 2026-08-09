from peppo.ir import Language, IrType, Ir

import subprocess


def clang_compile_command(language: str) -> list[str]:
    # https://discourse.llvm.org/t/better-way-to-get-no-optimisations-from-clang-than-o1-disable-llvm-passes/76859/8
    return [
            'clang',
            '-S', '-emit-llvm',
            '-O1',
            '-mllvm', '-disable-llvm-optzns', '-disable-llvm-passes',
            '-x', language, '-',
            '-o', '-'
            ]


flang_compile_command = [
        'flang',
        '-S', '-emit-llvm',
        '-x', 'f90', '-',
        '-o', '-'
        ]


# this table encodes the logic for which compiler
# to use given the language and IR requirements
COMPILE_LOGIC_TABLE = {
        (Language.C      , IrType.LLVM_IR): clang_compile_command('c'),
        (Language.CPP    , IrType.LLVM_IR): clang_compile_command('c++'),
        (Language.FORTRAN, IrType.LLVM_IR): flang_compile_command,

        (Language.C      , IrType.MLIR_IR): None,
        (Language.CPP    , IrType.MLIR_IR): None,
        (Language.FORTRAN, IrType.MLIR_IR): None,
        }


def compile(src: str, language: Language, ir_type: IrType) -> Ir:
    cmd = COMPILE_LOGIC_TABLE[(language, ir_type)]
    res = subprocess.run(
            cmd,
            input=src.encode(),
            capture_output=True,
            check=False)

    returncode = res.returncode
    if returncode == 0:
        ir = res.stdout.decode()
        return Ir(ir_type, ir)
    else:
        err = res.stderr.decode()
        raise RuntimeError(f"Command {cmd} failed with exit {returncode}:\n{err}")

