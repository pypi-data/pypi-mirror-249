import pathlib
from setuptools import setup, find_packages

setup(
    name="paik2json",
    version="0.2.1",
    description="convert paik to json",
    author="paikwiki",
    author_email="paikwiki@gmail.com",
    long_description='일반 문자열(plain text)로 작성한 메모 파일을 JSON 형태로 변환하는 데 사용하는 패키지입니다. 패키지 이름 "paik2json"은 확장자가 ".paik"인 일반 텍스트를 ".json" 파일로 바꿔준다는 의미로 지었습니다.',
    url="https://github.com/paikwiki/paik2json",
    packages=find_packages(include=["paik2json", "paik2json.*"]),
    install_requires=[],
    tests_require=["unittest"],
)
