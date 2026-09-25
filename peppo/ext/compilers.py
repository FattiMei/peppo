from peppo.ext.tool import Tool


class Clang(Tool):
    def __init__(self, path: str = None):
        super().__init__(path)

    def _get_env_var_name(self) -> str:
        return 'CLANG_PATH'

    def _get_tool_name(self) -> str:
        return 'clang'

    def compile_to_llvm(self, src: str, language: str = 'c++') -> str:
        cmd = [
            self.path,
            '-S', '-emit-llvm',
            '-O1',
            '-mllvm', '-disable-llvm-optzns', '-disable-llvm-passes',
            '-x', language, '-',
            '-o', '-',
        ]

        return self.call(cmd, src)

    def compile_to_cir(self, src: str, language: str = 'c++') -> str:
        cmd = [
            self.path,
            '-fclangir', '-emit-cir',
            '-x', language, '-',
            '-o', '-',
        ]

        return self.call(cmd, src)


class Flang(Tool):
    def __init__(self, path: str = None):
        super().__init__(path)

    def _get_env_var_name(self) -> str:
        return 'FLANG_PATH'

    def _get_tool_name(self) -> str:
        return 'flang'

    def compile_to_llvm(self, src: str) -> str:
        cmd = [
            self.path,
            '-fc1', '-emit-llvm',
            '-x', 'f95', '-',
            '-o', '-'
        ]

        return self.call(cmd, src)

    def compile_to_fir(self, src: str) -> str:
        cmd = [
            self.path,
            '-fc1', '-emit-mlir',
            '-x', 'f95', '-',
            '-o', '-'
        ]

        return self.call(cmd, src)

