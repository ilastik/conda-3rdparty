import sys
from argparse import ArgumentParser
from pathlib import Path

from conda3rdparty import __version__

from .common import MISSING, CondaEnv, load_fallback, render_license_info


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
    p.add_argument("-i", "--ignore", action="append")

    args = p.parse_args()
    return args


def make_check(env_name: str, fallback_file: Path) -> int:
    env = CondaEnv(env_name)
    fallback_info = load_fallback(fallback_file) if fallback_file else None
    summary = []
    for info in env.license_infos(fallback_info):
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
    template = Path(args.template) if args.template else None

    fallback = Path(args.fallback_file) if args.fallback_file else None

    ignore = args.ignore if args.ignore else None

    if args.check:
        return make_check(args.name, fallback)

    print(render_license_info(args.name, template_file=template, fallback_file=fallback, ignore_packages=ignore))


if __name__ == "__main__":
    sys.exit(main())
