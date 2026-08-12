# Performs a search of llvm tools like `opt`, `clang`, ...
# in the `LLVM_TOOLS_BINARY_DIR` directory
#
# Writes in `LLVM_TOOLS_DEFINES` the defines for the compilation
# of an external python module, which makes available to the
# python runtime the tool paths
#
#
# In the case the user wants to use specific tools, the `*_PATH`
# variables can be overriden at config time.
function(register_tool_path var_name prog_name)
	find_program(${var_name}
		NAMES ${prog_name}
		PATHS ${LLVM_TOOLS_BINARY_DIR}
		NO_DEFAULT_PATH)
endfunction()

register_tool_path(OPT_PATH      opt)
register_tool_path(CLANG_PATH    clang)
register_tool_path(FLANG_PATH    flang)
register_tool_path(MLIR_OPT_PATH mlir-opt)
register_tool_path(CLANGIR_PATH  xxx)

list(APPEND LLVM_TOOLS_PATHS
	OPT_PATH
	CLANG_PATH
	FLANG_PATH
	MLIR_OPT_PATH
	CLANGIR_PATH)

foreach(TOOL IN LISTS LLVM_TOOLS_PATHS)
	list(APPEND LLVM_TOOLS_DEFINES "${TOOL}=\"${${TOOL}}\"")
endforeach()

message(STATUS ${LLVM_TOOLS_DEFINES})

