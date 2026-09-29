from peppo.ext.tool import Tool


class MlirTranslate(Tool):
    def __init__(self, path: str = None):
        super().__init__(path)

    def _get_env_var_name(self) -> str:
        return 'MLIR_TRANSLATE_PATH'

    def _get_tool_name(self) -> str:
        return 'mlir-translate'

    def translate_llvm_to_mlir(self, src: str) -> str:
        cmd = [
            self.path,
            '--import-llvm',
            '--mlir-print-op-generic', # otherwise xDSL has problems parsing the IR
            '-o', '-',
        ]

        return self._call(cmd, src)
    
    def translate_mlir_to_llvm(self, src: str) -> str:
        cmd = [
            self.path,
            '--mlir-to-llvmir',
            '-o', '-'
        ]

        return self._call(cmd, src)


class FirOpt(Tool):
    def __init__(self, path: str = None):
        super().__init__(path)

    def _get_env_var_name(self) -> str:
        return 'FIR_OPT_PATH'

    def _get_tool_name(self) -> str:
        return 'fir-opt'

    def optimize_fir(self, src: str) -> str:
        cmd = [
            self.path,
            '--mlir-print-op-generic',
            '-o', '-',
        ]

        return self._call(cmd, src)


class MlirOpt(Tool):
    def __init__(self, path: str = None):
        super().__init__(path)

    def _get_env_var_name(self) -> str:
        return 'MLIR_OPT_PATH'

    def _get_tool_name(self) -> str:
        return 'mlir-opt'

    def canonicalize(self, src: str) -> str:
        cmd = [
            self.path,
            '--canonicalize',
            '-o', '-',
        ]

        return self._call(cmd, src)