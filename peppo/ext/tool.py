import subprocess


class Tool:
    """
    This class abstracts the external tool calling.

    Tools are called as external processes,
    they must communicate with stdin and stdout.
    """
    def __init__(self, path: str = ''):
        self.path = path

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

