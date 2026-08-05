import llvmlite.binding as llvm


def usual_optimize(target_machine: llvm.targets.TargetMachine,
                   module: llvm.ModuleRef,
                   speed_level: int = 2) -> llvm.ModuleRef:
    """
    Applies a standard set of optimizations to `module`
    Returns an optimized module

    Originally mutated `module` but some use cases need
    to compare original and optimized modules.
    """

    pto = llvm.create_pipeline_tuning_options(
            speed_level=speed_level)

    pass_builder = llvm.create_pass_builder(
            target_machine,
            pto)

    # we can add a rich selection of optimization
    # passes to the module pass manager e.g:
    #   * aggressive_dce
    #   * dead_arg_elimination
    #   * loop_deletion
    mpm = pass_builder.getModulePassManager()
    cloned_module = module.clone()
    mpm.run(cloned_module, pass_builder)

    return cloned_module

