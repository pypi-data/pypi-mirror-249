# coding: utf8
"""
@ File: __init__.py
@ Editor: PyCharm
@ Author: Austin (From Chengdu.China) https://fairy.host
@ HomePage: https://github.com/AustinFairyland
@ OS: Linux Ubuntu 22.04.4 Kernel 6.2.0-36-generic 
@ CreatedTime: 2024/1/8
"""
from __future__ import annotations

import sys
import warnings
import platform
import asyncio

sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

__name__ = "austin-core"
__version__ = "0.0.1"

from .core.Base import Base
from .core.DefaultData import DefaultData

__all__ = [
    "Base",
    "DefaultData",
]
