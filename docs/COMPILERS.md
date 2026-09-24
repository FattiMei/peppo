For the code ingestion part, I need to access compilers for C, C++ and FORTRAN.
The compilers must produce LLVM IR (and in the future MLIR) that must be compatible with LLVM version used in PEPPO.

There are two ways of accessing the compilers:
  1. via an external tool call
  2. in memory via the C++ API


## External tool call
External tools are easy to use and produce LLVM assembly.
They are interacted with *stdin* and *stdout* and produce ascii output.

 - The user will be responsible of providing compilers that are compatible with PEPPO
 + new compilers can be added with ease


## In memory tool call
The compilers are invoked from the C++ runtime, and produce directly LLVM modules.
The LLVM modules could then be accessed by PEPPO without any parsing.

 - difficulties when supporting compilers other than clang and flang
 - requires dealing with irrelevant tasks like diagnostics
 + stronger guarantees on compatibility
 + occasion to couple C++ and python together


## Considerations
Since I'm planning to use the code ingestion only $O(1)$ per project, calling external tools is not performance critical.
As of 23/09/2026, I'm prioritizing code simplicity and full python inspectability.

