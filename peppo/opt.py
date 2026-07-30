import llvmlite.binding as llvm


def usual_optimize(target_machine: llvm.targets.TargetMachine,
                   module: llvm.ModuleRef,
                   speed_level: int = 2):
    """
    Applies a standard set of optimizations to `module`
    Mutates `module`
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
    mpm.run(module, pass_builder)

