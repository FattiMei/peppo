import os
import glob
import subprocess
from abc import ABC, abstractmethod


DEFAULT_SEARCH_DIR = '/usr/bin'


def search_tool_in_directory(tool_name: str, directory: str):
    # here I'm matching any name that starts with the tool name
    # because there may be only versioned tools
    candidates = glob.glob(
        f'{tool_name}*',
        root_dir=directory,
        recursive=False
    )

    if len(candidates) > 0:
        # I make the assumption that the shortest name
        # is also the right one
        return sorted(
            candidates,
            key=str.__len__
        )[0]

    return None


class Tool(ABC):
    """
    This class abstracts the external tool calling.

    Tools are called as external processes,
    they must communicate with stdin and stdout.
    """
    def __init__(self, path: str = None):
        if path is None:
            path = os.environ.get(
                self._get_env_var_name()
            )

        if path is None:
            path = search_tool_in_directory(
                tool_name=self._get_tool_name(),
                directory=DEFAULT_SEARCH_DIR
            )

        if path is None:
            raise FileNotFoundError()

        self.path = path

    @abstractmethod
    def _get_env_var_name(self) -> str:
        pass

    @abstractmethod
    def _get_tool_name(self) -> str:
        pass

    def call(self, cmd: list[str], input: str) -> str:
        res = subprocess.run(
            cmd,
            input=input.encode(),
            capture_output=True,
            check=False
        )

        if res.returncode == 0:
            return res.stdout.decode()
        else:
            err = res.stderr.decode()
            raise RuntimeError(
                f'Command {cmd} failed with exit {res.returncode}: \n{err}'
            )

