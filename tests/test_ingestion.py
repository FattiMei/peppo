import pytest
from peppo.ingest import ExtSource, Language, compile_snippet


def test_c_ingestion():
    hello_world_c = ExtSource(
        language=Language.C,
        src="""
            #include <stdio.h>

            int main() <%
                printf("Hello, World!\\n");
                return 0;
            %>
        """
    )

    print(hello_world_c.src)

    compile_snippet(hello_world_c)


def test_cpp_ingestion():
    hello_world_cpp = ExtSource(
        language=Language.CPP,
        src="""
            #include <iostream>

            int main() <%
                std::cout << "Hello, World" << std::endl;
                return 0;
            %>
        """
    )

    compile_snippet(hello_world_cpp)


def test_fortran_ingestion():
    hello_world_fortran = ExtSource(
        language=Language.F90,
        src="""
            program hello
            ! This is a comment line; it is ignored by the compiler
                print *, 'Hello, World!'
            end program hello
        """
    )

    compile_snippet(hello_world_fortran)

