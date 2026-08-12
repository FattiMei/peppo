cmake_minimum_required(VERSION 3.20)
project(${SKBUILD_PROJECT_NAME}
	VERSION ${SKBUILD_PROJECT_VERSION}
	LANGUAGES CXX)


find_package(LLVM REQUIRED)
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(FindLlvmTools)


cmake_policy(SET CMP0148 NEW)
find_package(pybind11 CONFIG REQUIRED)

set(ENV_MODULE "_env")
pybind11_add_module(${ENV_MODULE} MODULE peppo/_env.cpp)
target_compile_definitions(${ENV_MODULE} PRIVATE ${LLVM_TOOLS_DEFINES})
target_compile_definitions(${ENV_MODULE} PRIVATE
	"LLVM_INCLUDE_DIRS=\"${LLVM_INCLUDE_DIRS}\"")
target_compile_definitions(${ENV_MODULE} PRIVATE
	"LLVM_DEFINITIONS=\"${LLVM_DEFINITIONS}\"")

install(TARGETS ${ENV_MODULE} DESTINATION peppo/_env)


