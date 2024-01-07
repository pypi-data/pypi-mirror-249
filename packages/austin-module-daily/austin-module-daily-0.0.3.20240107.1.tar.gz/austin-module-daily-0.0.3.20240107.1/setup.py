# coding: utf8
""" 
@File: setup.py
@Editor: PyCharm
@Author: Austin (From Chengdu.China) https://fairy.host
@HomePage: https://github.com/AustinFairyland
@OperatingSystem: Windows 11 Professional Workstation 23H2 Canary Channel
@CreatedTime: 2024-01-07
"""
from __future__ import annotations

import os
import sys
import warnings
import platform
import asyncio

sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import time
import random

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="austin-module-daily",
    version="0.0.3.20240107.01",
    author="Austin D",
    author_email="fairylandhost@outlook.com",
    description="Austin personally developed Python library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com.AustinFairyland/AustinModulesDaily",
    # packages=setuptools.find_packages(),
    packages=["tools"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)"
    ],
    python_requires=">=3.7",
    
)
