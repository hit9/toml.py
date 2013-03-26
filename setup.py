from setuptools import setup

setup(
    name="toooml",
    version="0.1",
    author="hit9",
    author_email="nz2324@126.com",
    description=(
        """
        Python implementation for toml.
        Support both unicode string and raw string.
        An improved version of marksteve/toml-ply
        """
    ),
    license="MIT",
    keywords="toml, parser",
    url="https://github.com/hit9/toooml",
    py_modules=["toooml"],
    install_requires=["ply"]
)
