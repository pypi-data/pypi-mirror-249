# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name="batch-none",
    version="1.0.1",
    description="Batch prediction recipe",
    author="Amit Boke",
    classifiers=["Programming Language :: Python :: 3.6"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    # install_requires=[],
    python_requires=">=3.6,<3.10"
)
