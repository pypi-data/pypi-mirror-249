#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/3
# @Author  : alan
# @File    : setup.py

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LoggerX",
    version="0.2",
    author="alan",
    author_email="al6nlee@gmail.com",
    description="自定义日志模块",
    long_description=long_description,  # 会显示在PyPI的项目描述页面。必须是rst(reStructuredText) 格式的
    long_description_content_type="text/markdown",
    url="https://github.com/al6nlee/LoggerX",
    packages=setuptools.find_packages(),  # 指定最终发布的包中要包含的packages
    classifiers=[  # 其他信息，一般包括项目支持的Python版本，License，支持的操作系统
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development"
    ],
    install_requires=[],  # 项目依赖哪些库，这些库会在pip install的时候自动安装
    python_requires='>=3.6',
    license='Apache-2.0'
)
