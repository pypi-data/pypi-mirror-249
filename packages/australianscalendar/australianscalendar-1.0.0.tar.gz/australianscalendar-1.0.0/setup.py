# -*- coding: utf-8 -*-
from setuptools import setup

import australians_calendar

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="australianscalendar",
    version=australians_calendar.__version__,
    description="check if some day is holiday in Australia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hack Fang",
    author_email="kaifang.1995@gmail.com",
    url="https://github.com/hack-fang/australian-calendar",
    license="MIT License",
    packages=["australians_calendar"],
    install_requires=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
