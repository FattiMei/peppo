import subprocess
import llvmlite.binding as llvm


def _clang_compile_command(language: str,
                           defines: list[str] = None,
                           include_directories: list[str] = None) -> list[str]:
    """
    Returns the clang command for an unoptimized build
    that outputs llvm ir
    """
    cmd = [
            'clang',
            '-S', '-emit-llvm',
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


def compile(src: str, language: str, compiler: str = 'clang') -> llvm.ModuleRef:
    """
    An unoptimized build by clang produces annotations
    that will interfere with the optimization process:
      * noopt
      * noinline

    One may manually remove those annotations in the
    string representation or edit the attributes in
    the llvm.Module. I haven't decided yet
    """
    compile_command = clang_compile_command(language)

    try:
        llvm_ir = subprocess.run(
                compile_command,
                input=src.encode(),
                capture_output=True,
                check=True,
                ).stdout

    except subprocess.CalledProcessError as err:
        return err.stderr.decode()

    module = llvm.parse_assembly(llvm_ir)
    module.verify()

    return module

