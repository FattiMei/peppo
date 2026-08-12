cmake_minimum_required(VERSION 3.20)
project(${SKBUILD_PROJECT_NAME}
	VERSION ${SKBUILD_PROJECT_VERSION}
	LANGUAGES CXX)


find_package(LLVM REQUIRED)
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(FindLlvmTools)


cmake_policy(SET CMP0148 NEW)
find_package(pybind11 CONFIG REQUIRED)

set(PATHS_MODULE "_paths")
pybind11_add_module(${PATHS_MODULE} MODULE peppo/ext/_paths.cpp)
target_compile_definitions(${PATHS_MODULE} PRIVATE ${LLVM_TOOLS_DEFINES})
install(TARGETS ${PATHS_MODULE} DESTINATION peppo/ext)
