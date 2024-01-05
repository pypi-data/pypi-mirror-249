from pip._internal.req.req_file import ParsedRequirement
from setuptools import setup, find_packages
from pip._internal.req import req_file

VERSION = '0.0.3.21'
DESCRIPTION = 'airclick 相关python包'
requirments = req_file.parse_requirements('requirements.txt', session='hack')
instll_requires = [req.requirement for req in requirments]

print(instll_requires)

setup(
    name="airclick",
    version=VERSION,
    author="aojoy",
    author_email="aojoytec@163.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding="UTF8").read(),
    packages=find_packages(),
    keywords=['python', "airclick"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/itisl2220/airscript",
    install_requires = instll_requires,
)
