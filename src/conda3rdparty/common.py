import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List

from jinja2 import Template

MISSING = object()


class CondaPackageFileNotFound(Exception):
    pass


def conda_info() -> Dict[str, Any]:
    return json.loads(subprocess.check_output(["conda", "info", "-e", "--json"]))


def conda_envs() -> List[Path]:
    return [Path(x) for x in json.loads(subprocess.check_output(["conda", "env", "list", "--json"]))["envs"]]


def gather_license_info(package_info: dict, fallback_info: dict = None) -> dict:
    fallback_info = fallback_info or {}
    package_path = Path(package_info["extracted_package_dir"])
    about_file = package_path / "info" / "about.json"
    if not about_file.exists():
        raise CondaPackageFileNotFound(f"Couldn't find `about.json` in {package_path}")

    about_content = json.loads(about_file.read_text())

    def ensure_list(x):
        if not x:
            return []
        if isinstance(x, str):
            return [x]
        else:
            return x

    license_info = {
        "license": about_content.get("license", ""),
        "license_family": about_content.get("license_family", ""),
        "license_file": [
            package_path / "info" / "licenses" / x for x in ensure_list(about_content.get("license_file"))
        ],
    }

    license_texts = [
        license.read_text(encoding="latin-1") if license.exists() else MISSING
        for license in license_info["license_file"]
    ]

    if MISSING not in license_texts:
        # treat as invalid
        license_info["license_source"] = "package"
    elif package_info["name"] in fallback_info:
        license_info["license_source"] = "fallback"
        license_texts = [
            license.read_text(encoding="latin-1") for license in fallback_info[package_info["name"]]["license_file"]
        ]

    license_info["license_texts"] = license_texts

    package_info["3rd_party_license_info"] = license_info
    return package_info


class CondaEnv:
    def __init__(self, env_name: str):
        self._name = env_name

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> Path:
        return Path(conda_info()["envs_dirs"][0]) / self.name

    @property
    def exists(self) -> bool:
        return self.path in conda_envs()

    @property
    def conda_meta_path(self) -> Path:
        return self.path / "conda-meta"

    @property
    def package_list(self) -> List[Dict[str, Any]]:
        return sorted([json.loads(x.read_text()) for x in self.conda_meta_path.glob("*.json")], key=lambda x: x["name"])

    def license_infos(self, fallback_info=None) -> List[Dict[str, Any]]:
        out = []
        for package in self.package_list:
            out.append(gather_license_info(package, fallback_info))

        return out


_base_template = """
3rd-party licenses

{% for info in license_infos %}
License for {{ info['name'] }} {{ info['version'] }}
    {% for license_text in info['3rd_party_license_info']['license_texts'] %}
{{ license_text }}
{% endfor %}
{% endfor %}

"""


def base_license_renderer(license_infos: List[Dict[str, Any]], template_file: Path = None):
    if not template_file:
        template = Template(_base_template)
    else:
        template = Template(template_file.read_text())
    return template.render(license_infos=license_infos)
