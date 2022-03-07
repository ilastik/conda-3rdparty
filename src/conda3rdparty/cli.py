import json
import pathlib
import sys
from argparse import ArgumentParser
from subprocess import check_output
from typing import Iterable, Mapping, Union

from conda3rdparty import __version__

from .common import MISSING, CondaEnv, base_license_renderer


class CondaNotFound(Exception):
    pass


def parse_args():
    p = ArgumentParser(
        description="conda-3rdpart is a tool to gather license information about packages in a conda environment."
    )
    p.add_argument("-n", "--name", type=str, help="Env name", required=True)
    p.add_argument("--check", action="store_true", help="print a summary, exitcode indicates success")
    # p.add_argument("--json", action="store_true")
    # p.add_argument("-f", "--file", help="write 3rd party license file")
    p.add_argument("-t", "--template", type=str)
    p.add_argument("--fallback-file", type=str, help="path to json file pointing to fallback licenses for packages.")
    # p.add_argument("-v", "--verbose", action="count")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    args = p.parse_args()
    return args


def load_fallback(fallback_path: pathlib.Path) -> dict:
    assert fallback_path.exists()
    fallback = json.loads(fallback_path.read_text())
    for pkg in fallback:
        fallback[pkg]["license_file"] = [
            fallback_path.parent / license_file for license_file in fallback[pkg]["license_file"]
        ]
    return fallback


def make_check(env: CondaEnv, fallback_file) -> int:
    summary = []
    for info in env.license_infos(fallback_file):
        tmp = {"name": info["name"]}
        tmp.update(info["3rd_party_license_info"])
        tmp["ok"] = not any(x == MISSING for x in tmp["license_texts"])
        summary.append(tmp)

    missing = [x for x in summary if not x["ok"]]
    for info in missing:
        print(
            f"{info['name']} - {info['license_family']} - missing: {[x for x, y in zip(info['license_file'], info['license_texts']) if y == MISSING]  }"
        )

    return len(missing)


def main():
    args = parse_args()

    env = CondaEnv(args.name)

    fallback = None
    if args.fallback_file:
        fallback = load_fallback(pathlib.Path(args.fallback_file))

    if args.check:
        return make_check(env, fallback)

    template = pathlib.Path(args.template) if args.template else None

    print(base_license_renderer(env.license_infos(fallback), template_file=template))


if __name__ == "__main__":
    sys.exit(main())
