import llvmlite.binding as llvm


def get_closest_function_name(module: llvm.ModuleRef,
                              name: str) -> list[str]:
    """
    Returns the name of functions defined in `module`
    that match `name`

    This is useful when the C++ compiler performs name
    mangling. Note that multiple functions could match
    `name`, so we return a list
    """
    res = []
    for func in module.functions:
        if func.name.find(name) != -1:
            res.append(func.name)

    return res
