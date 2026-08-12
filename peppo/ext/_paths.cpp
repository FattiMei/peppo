#include <pybind11/pybind11.h>


// CMake should provide this translation unit with the paths of the LLVM/MLIR tools
// As a form of defensive programming, the missing entries are set to empty strings
//
// I hope this is a simple enough mechanism for registering the external tools
// It shouldn't be modified very much
#ifndef OPT_PATH
#define OPT_PATH ""
#endif

#ifndef CLANG_PATH
#define CLANG_PATH ""
#endif

#ifndef FLANG_PATH
#define FLANG_PATH ""
#endif

#ifndef MLIR_OPT_PATH
#define MLIR_OPT_PATH ""
#endif

#ifndef CLANGIR_PATH
#define CLANGIR_PATH ""
#endif


PYBIND11_MODULE(_paths, m) {
	m.doc() = "Bridge module to import the LLVM tool paths";

	// all these functions return an empty string when the program is not found
	m.def("get_clang_path",
	      []() { return std::string(CLANG_PATH); });

	m.def("get_opt_path",
	      []() { return std::string(OPT_PATH); });

	m.def("get_flang_path",
	      []() { return std::string(FLANG_PATH); });

	m.def("get_mlir_opt_path",
	      []() { return std::string(MLIR_OPT_PATH); });

	m.def("get_clangir_path",
	      []() { return std::string(CLANGIR_PATH); });
}
