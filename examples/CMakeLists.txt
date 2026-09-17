cmake_minimum_required(VERSION 3.20)
project(peppo-examples)


# this is the same standard llvm is compiled with
set(CMAKE_CXX_STANDARD 17 CACHE STRING "")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")


find_package(LLVM REQUIRED)
message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
list(APPEND CMAKE_MODULE_PATH "${LLVM_CMAKE_DIR}")


# every example will need these
include_directories(SYSTEM ${LLVM_INCLUDE_DIRS})
link_directories(${LLVM_LIBRARY_DIRS})
add_definitions(${LLVM_DEFINITIONS})


include(AddLLVM)
add_subdirectory(strength-reduction)
add_subdirectory(addition)
add_subdirectory(lapack)

