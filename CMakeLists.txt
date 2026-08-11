cmake_minimum_required(VERSION 3.20)
project(${SKBUILD_PROJECT_NAME}
	VERSION ${SKBUILD_PROJECT_VERSION}
	LANGUAGES CXX)

find_package(pybind11 CONFIG REQUIRED)

set(PATHS_MODULE "_paths")
add_library(${PATHS_MODULE} MODULE peppo/ext/_paths.cpp)
target_link_libraries(${PATHS_MODULE} PUBLIC pybind11::module)
# TODO: add the defines discovered from LLVM tools

# TODO: needs an installation, which must be seen from python
