import pytest
from peppo.ext.compilers import (
    Clang,
    Flang
)


HELLO_WORLD_C = """
    #include <stdio.h>

    int main() <%
        printf("Hello, World!\\n");
        return 0;
    %>
"""


HELLO_WORLD_CPP = """
    #include <iostream>

    int main() <%
        std::cout << "Hello, World" << std::endl;
        return 0;
    %>
"""


HELLO_WORLD_FORTRAN = """
    program hello
    ! This is a comment line; it is ignored by the compiler
        print *, 'Hello, World!'
    end program hello
"""


# if the appropriate environment variable is not selected,
# the tool is searched in the default search path
CLANG_TOOL = Clang()
FLANG_TOOL = Flang()


@pytest.mark.skipif(CLANG_TOOL.path is None, reason="can't find clang")
class TestClang:
    def test_llvm(self):
        llvm_ir = CLANG_TOOL.compile_to_llvm(HELLO_WORLD_C, language='c')

    # this test is not that important because it relies on clang being
    # compiled with clangir support
    def test_clang_cir(self):
        try:
            cir = CLANG_TOOL.compile_to_cir(HELLO_WORLD_CPP, language='c++')
        except RuntimeError:
            pytest.skip("this installation of clang doesn't support cir")


@pytest.mark.skipif(FLANG_TOOL.path is None, reason="can't find flang")
class TestFlang:
    def test_llvm(self):
        llvm_ir = FLANG_TOOL.compile_to_llvm(HELLO_WORLD_FORTRAN)

    def test_fir(self):
        fir = FLANG_TOOL.compile_to_fir(HELLO_WORLD_FORTRAN)

