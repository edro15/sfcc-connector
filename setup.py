#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pathlib import Path

project_dir = Path(__file__).parent

about = {}
with open(project_dir.joinpath("sfcc_connector", "__main__.py"), "r") as f:
    exec(f.read(), about)

setup(
    name = about["__title__"],
    version = about["__version__"],
    description = about["__description__"],
    # Use UTF-8 encoding for README even on Windows by using the encoding argument.
    long_description = project_dir.joinpath("README.md").read_text(encoding="utf-8"),
    long_description_content_type = "text/markdown",
    author = about["__author__"],
    author_email=about["__author_email__"],
    maintainer=about["__maintainer__"],
    maintainer_email=about["__maintainer_email__"],
    license=about["__license__"],
    url = about["__url__"],
    keywords = about["__keywords__"],
    packages = find_packages(),
    install_requires = project_dir.joinpath("requirements.in").read_text().split("\n"),
    python_requires = ">=3.6",
    include_package_data = True,
    zip_safe = False,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
