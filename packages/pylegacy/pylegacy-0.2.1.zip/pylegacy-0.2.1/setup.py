#! /usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa: E122
"""pylegacy -- Backports for abandoned Python versions."""

import io
import os
import re
from setuptools import setup
from setuptools import find_packages


def get_content(name, splitlines=False):
    """Return the file contents with project root as root folder."""

    here = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(here, name)
    with io.open(path, "r", encoding="utf-8") as fd:
        content = fd.read()
    if splitlines:
        content = [row for row in content.splitlines() if row]
    return content


def get_version(pkgname):
    """Return package version without importing the file."""

    here = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(*[here, "src"] + pkgname.split(".") + ["__init__.py"])
    with io.open(path, "r", encoding="utf-8") as fd:
        pattern = r"""\n__version__[ ]*=[ ]*["']([^"]+)["']"""
        return re.search(pattern, fd.read()).group(1)


setup(**{
    "name":
        "pylegacy",
    "version":
        get_version("pylegacy"),
    "license":
        "MIT",
    "description":
        "Backports for abandoned Python versions",
    "long_description":
        get_content("README.md"),
    "long_description_content_type":
        "text/markdown",
    "url":
        "https://github.com/pylegacy/pylegacy",
    "maintainer":
        "Víctor Molina García",
    "maintainer_email":
        "molinav@users.noreply.github.com",
    "classifiers": [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    "keywords": [
        "compatibility",
        "backports",
        "legacy",
    ],
    "package_dir":
        {"": "src"},
    "packages":
        find_packages(where="src"),
    "python_requires":
        ", ".join([
            ">=2.6",
            "!=3.0.*",
            "!=3.1.*",
            "<3.13",
        ]),
    "extras_require": {
        "lint":
            get_content("requirements-lint.txt", splitlines=True),
        "test":
            get_content("requirements-test.txt", splitlines=True),
    },
    "project_urls": {
        "Bug Tracker":
            "https://github.com/pylegacy/pylegacy/issues",
        "Source":
            "https://github.com/pylegacy/pylegacy",
    },
})
