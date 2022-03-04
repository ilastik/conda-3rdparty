import json
import pathlib
from argparse import ArgumentParser
from subprocess import check_output
from typing import Iterable, Mapping, Union

from conda3rdparty import __version__


class CondaNotFound(Exception):
    pass


def parse_args():
    p = ArgumentParser(
        description="conda-3rdpart is a tool to gather license information about packages in a conda environment."
    )
    p.add_argument("-n", "--name", type=str, help="Env name", required=True)
    p.add_argument("--json", action="store_true")
    p.add_argument("-f", "--file", help="write license file")
    p.add_argument("-t", "--template")
    p.add_argument("--fallback-file")
    p.add_argument("-v", "--verbose", action="count")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    args = p.parse_args()
    return args


def main():
    args = parse_args()


if __name__ == "__main__":
    main()
