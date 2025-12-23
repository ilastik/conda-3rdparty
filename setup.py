from setuptools import find_packages, setup

setup(
    name="conda-3rdparty",
    version="0.0.6",
    author="ilastik-team",
    license="MIT",
    license_files=("LICENSE",),
    description="Command line tool to summarize 3rd party licenses of conda environments.",
    package_dir={"": "src"},
    packages=find_packages("./src"),
    include_package_data=True,
    install_requires=["jinja2", "conda>=25.11.1"],
    entry_points={"console_scripts": ["conda-3rdparty = conda3rdparty.cli:main"]},
)
