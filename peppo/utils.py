from peppo._env import *


ENV = {
    'CLANG_PATH'       : get_clang_path,
    'OPT_PATH'         : get_opt_path,
    'FLANG_PATH'       : get_flang_path,
    'MLIR_OPT_PATH'    : get_mlir_opt_path,
    'CLANGIR_PATH'     : get_clangir_path,
    'LLVM_INCLUDE_DIRS': get_llvm_include_dirs,
    'LLVM_DEFINITIONS' : get_llvm_definitions,
}


def dump_environment():
    for name, path_fun in ENV.items():
        print(name, ": ", path_fun())

