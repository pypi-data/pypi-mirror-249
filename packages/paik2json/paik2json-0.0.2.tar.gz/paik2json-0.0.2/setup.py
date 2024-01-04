import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="paik2json",
    version="0.0.2",
    description="convert paik to json",
    author="paikwiki",
    author_email="paikwiki@gmail.com",
    long_description=long_description,
    url="https://github.com/paikwiki/paik2json",
    packages=find_packages(include=["paik2json", "paik2json.*"]),
    install_requires=[],
    tests_require=["unittest"],
)
