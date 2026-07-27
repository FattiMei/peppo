import llvmlite
import subprocess


def clang_compile_command(language: str,
                          include_directories: list[str] = None) -> list[str]:
    """
    Returns the compilation command for clang compilers
    The command produces an unoptimized llvm ir
    """
    cmd = [
            compiler,
            '-S', '-emit-llvm',
            '-x', language, '-',
            '-o', '-'
            ]

    if include_directories is not None:
        for include_dir in include_directories:
            cmd.extend(('-I', include_dir))

    return cmd



def compile_snippet(src: str, language: str, compiler: str = 'clang') -> str:
    compile_command = clang_compile_command(language, compiler)

    res = subprocess.run(
            compile_command,
            input=src.encode(),
            capture_output=True,
            check=True,
            )

    llvm_ir = res.stdout.decode()
    return llvm_ir

