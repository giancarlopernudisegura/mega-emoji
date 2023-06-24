#!/usr/bin/env python

from setuptools import setup

setup(
    author="Giancarlo Pernudi Segura",
    author_email="pernudig@gmail.com",
    description="Split images into square grids",
    entry_points={
        "console_scripts": [
            "split-image = split_image:cli"
        ]
    },
    install_requires=[
        "Pillow>=9.5.0,<10.0.0",
        "click>=8.1.3,<9.0"
    ]
)
