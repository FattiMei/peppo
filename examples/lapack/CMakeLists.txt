add_llvm_executable(lapack main.cpp)

# this example needs the LLVM IR representation of the lapack fortran source code
# there are two main strategies for code ingestion, and each has its own drawbacks:
#   A. compile the source code with an external flang-18
#   B. runtime compile the code with the llvm API
#
# A is easy and fast, especially since we won't ever need to modify the original source
# however, it assumes the compiler used is compatible with the PEPPO LLVM version
#
# B is harder and I don't know if the LLVM CMake package can automatically detect
# clang or flang compilers, but if so it would solve the coupling problem
#
# for now I'm choosing (A)
set(LAPACK_IR_FILE dtgsv.ll)

cmake_path(ABSOLUTE_PATH LAPACK_IR_FILE
    BASE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
    NORMALIZE
    OUTPUT_VARIABLE LAPACK_IR_PATH
)

target_compile_definitions(lapack
	PUBLIC
	LAPACK_IR_PATH="${LAPACK_IR_PATH}"
)

