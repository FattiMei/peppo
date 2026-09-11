from peppo._env import (
    get_clang_path,
    get_clangxx_path,
    get_flang_path,
)


CLANG_PATH   = get_clang_path()
CLANGXX_PATH = get_clangxx_path()
FLANG_PATH   = get_flang_path()


def clang_compile_command(language: str) -> list[str]:
    assert(language == 'c')

    # https://discourse.llvm.org/t/better-way-to-get-no-optimisations-from-clang-than-o1-disable-llvm-passes/76859/8
    return [
        CLANG_PATH,
        '-S', '-emit-llvm',
        '-O1',
        '-mllvm', '-disable-llvm-optzns', '-disable-llvm-passes',
        '-x', language, '-',
        '-o', '-',
    ]


def clangxx_compile_command(language: str) -> list[str]:
    assert(language == 'c++')

    # https://discourse.llvm.org/t/better-way-to-get-no-optimisations-from-clang-than-o1-disable-llvm-passes/76859/8
    return [
        CLANGXX_PATH,
        '-S', '-emit-llvm',
        '-O1',
        '-mllvm', '-disable-llvm-optzns', '-disable-llvm-passes',
        '-x', language, '-',
        '-o', '-',
    ]


def flang_compile_command(language: str) -> list[str]:
    assert(language in ('f90',))

    return [
        FLANG_PATH,
        '-S', '-emit-llvm',
        '-x', language, '-',
        '-o', '-'
    ]

