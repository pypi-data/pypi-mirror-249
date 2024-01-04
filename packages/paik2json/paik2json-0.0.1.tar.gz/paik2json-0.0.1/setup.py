from setuptools import setup, find_packages

setup(
    name="paik2json",
    version="0.0.1",
    description="convert paik to json",
    author="paikwiki",
    author_email="paikwiki@gmail.com",
    packages=find_packages(include=["paik2json", "paik2json.*"]),
    install_requires=[],
    tests_require=["unittest"],
)
