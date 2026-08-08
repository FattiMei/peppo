# PEPPO
PEPPO is a framework designed to integrate the compiler infrastructure in the workflow of program optimization.

I often argue that program optimization is a matter of making appropriate **scheduling decisions**: assignments
of computational resources to tasks. Schedulings are:
  * **embedded in the source code** of traditional programming languages
  * **target dependent**: thus the need of specializing the assignment for many computing systems
  * **orthogonal to the domain code**: all valid schedulings are semantically equivalent

When a scheduling is embedded in the source code, exploring the space of design decisions require costly rewrites.
For this reason, scheduling languages like [exo](https://github.com/exo-lang/exo) and [RISE](https://rise-lang.org) have been developed.


## Who is this project for
This is a framework tailored to my needs, but you may find it useful if you are:
  * always writing many schedulings for your programs
  * curious about what code is fast for the compiler to optimize
  * willing to open the compiler black-box and write some custom passes yourself
  * interested in using the compile as **leverage** for writing better programs


## Technology choice
I choose Python and a jupyter notebook workflow because I need maximal interactivity.
With Python I can easily write glue code on the fly and compose the outputs of many command line programs (i.e `opt`, `mlir-opt`, ...)

In an ideal world, the domain specific user code and custom passes should be described in the python language via LLVM and MLIR bindings.
This is important because there is heavy coupling between the code description and the IR passes, for example the function names on which to apply the passes and some domain specific details.


The state of python bindings discourages me to develop in pure python. MLIR and LLVM are C++ native projects and it's simpler to work with the native API. They have really good support for command line programs, which will be the communication bottleneck between python and C++ parts of the codebase. This is just a technology problem: it's likely that in the future things will improve.


## Development phases
**Phase 1 - (code ingestion)**:
  1. support the users who have already code written in C/C++/FORTRAN.
  2. load the code into LLVM IR or MLIR and support the application of custom analysis and optimization passes.
  3. provide them with a JIT backend to perform the comparisons

**Phase 2 - (a new compiler toolchain)**:
  1. propose an embedded python DSL to support users in exploring global scheduling decisions (ones that cross function boundaries)
  2. (most probably) design an MLIR dialect to encode the scheduling decisions


## Use cases
The main protagonist is the domain specific user code, the framework is just a thin layer that makes it easier to compose passes.
For this reason I have compiled a list of use cases of PEPPO and each will have a dedicated folder:
  * `rng-throughput`: testing the random number generation of the C++ standard library
  * `munchhausen`: exploring the SIMD vectorization of a scalar function
  * `lapack-tridiag`: changing the data layout of input arguments of a LAPACK function without writing a single line of FORTRAN

