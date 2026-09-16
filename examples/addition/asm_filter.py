#!/usr/bin/python
import sys
import tabulate
import pandas as pd


def process_functions(lines: list[str]) -> dict[str, list[str]]:
    res = {}

    function_name_pos = []
    for (i,line) in enumerate(lines):
        if line.startswith('add_'):
            function_name_pos.append(i)
    function_name_pos.append(len(lines))

    for (i,j) in zip(function_name_pos[:-1], function_name_pos[1:]):
        function_name = lines[i][:-1]
        res[function_name] = '\n'.join(map(lambda s: s.expandtabs().strip(), lines[i+1:j]))

    return res


if __name__ == '__main__':
    asm_str = sys.stdin.read()

    # filtering phase
    lines = []
    for line in asm_str.splitlines():
        stripped = line.strip()

        if not stripped.startswith('.'):
            lines.append(line)

    # separation into targets
    header_pos = []
    for (i,line) in enumerate(lines):
        if line.startswith('#'):
            header_pos.append(i)
    header_pos.append(len(lines))

    targets = {}
    for (i,j) in zip(header_pos[:-1], header_pos[1:]):
        header = lines[i]
        triple = header.split()[1]

        targets[triple] = process_functions(lines[i+1:j])

    table_headers = ["type"] + list(targets.keys())

    df = pd.DataFrame(targets)
    table = tabulate.tabulate(
        df,
        headers=table_headers,
        tablefmt='grid'
    )
    print(table)

