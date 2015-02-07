from setuptools import setup

setup(
    name="toml.py",
    version="0.1.7",
    author="hit9",
    author_email="nz2324@126.com",
    description=(
        """
          Tested Toml's Python implementation.
          An improved version of marksteve/toml-ply with friendly
          support for unicode, raw and common strings.
        """
    ),
    license="MIT",
    keywords="toml, parser",
    url="https://github.com/hit9/toml.py",
    py_modules=["toml"],
    install_requires=["ply", "six"]
)
