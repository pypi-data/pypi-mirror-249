# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name="batch-none",
    version="1.0.0",
    description="Batch prediction recipe",
    author="Amit Boke",
    classifiers=["Programming Language :: Python :: 3.6"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["refractml", "refractio[local]"],
    # install_requires=[],
    python_requires=">=3.6,<3.10"
)
