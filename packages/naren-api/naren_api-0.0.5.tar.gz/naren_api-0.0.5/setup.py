from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()


def get_requirements(file_path):
    requirements = []
    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if "-e ." in requirements:
            requirements.remove("-e .")
    return requirements


PROJECT_NAME = "naren_api"
VERSION = "0.0.5"
DESCRIPTION = "A small python package"
AUTHOR = "NarenBot"
AUTHOR_EMAIL = "narendas10@gmail.com"

setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},  # "src"
    packages=find_packages(where="src"),  # "where='src'"
    # install_requires=get_requirements("requirements.txt"),
)
