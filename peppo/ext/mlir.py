from peppo.ext.tool import Tool


class MlirTranslate(Tool):
    def __init__(self, path: str = None):
        super().__init__(path)

    def _get_env_var_name(self) -> str:
        return 'MLIR_TRANSLATE_PATH'

    def _get_tool_name(self) -> str:
        return 'mlir-translate'

    def translate_llvm_to_mlir(src: str) -> str:
        cmd = [
            self.path,
            '--import-llvm',
            '-o', '-',
        ]

        return self.call(cmd, src)

