from abc import ABC, abstractmethod
import subprocess


class Compiler(ABC):
    """
    This class abstracts the compilation process for
    Clang-like compilers which are invoked as external programs

    A simple inheritance model is introduced as different
    compilers have slightly different command line parameters
    """
    def compile(self, src: str, language: str) -> str:
        cmd = self._get_compile_command(language)
        res = subprocess.run(
                cmd,
                input=src.encode(),
                capture_output=True,
                check=False)

        if res.returncode == 0:
            return res.stdout.decode()
        else:
            pass

    @abstractmethod
    def _get_compile_command(self, language: str) -> list[str]:
        pass


class Clang(Compiler):
    def _get_compile_command(self, language: str) -> list[str]:
        # https://discourse.llvm.org/t/better-way-to-get-no-optimisations-from-clang-than-o1-disable-llvm-passes/76859/8
        return [
                'clang',
                '-S', '-emit-llvm',
                '-O1',
                '-mllvm', '-disable-llvm-optzns', '-disable-llvm-passes',
                '-x', language, '-',
                '-o', '-'
                ]


class ClangIR(Compiler):
    def _get_compile_command(self, language: str) -> list[str]:
        pass


class Flang(Compiler):
    def _get_compile_command(self, language: str) -> list[str]:
        pass


class FlangNew(Compiler):
    def _get_compile_command(self, language: str) -> list[str]:
        pass

