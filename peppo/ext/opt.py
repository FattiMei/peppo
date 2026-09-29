from peppo.ext.tool import Tool


class Opt(Tool):
    def __init__(self, path: str = None):
        super().__init__(path)

    def _get_env_var_name(self) -> str:
        return 'OPT_PATH'

    def _get_tool_name(self) -> str:
        return 'opt'
    
    def apply_mem2reg(self, src: str) -> str:
        cmd = [
            self.path,
            '-S',
            '--passes=mem2reg',
            '-o', '-'
        ]

        return self._call(cmd, src)
    
    def apply_O2(self, src: str) -> str:
        cmd = [
            self.path,
            '-S',
            '-O2',
            '-o', '-'
        ]

        return self._call(cmd, src)
