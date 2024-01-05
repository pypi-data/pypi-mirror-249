#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2024/1/4 18:11
# @Author:boyizhang
from setuptools import setup, find_packages

setup(
    name='pytoolkit1',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # 项目依赖
    ],
    entry_points={
        'console_scripts': [
            # 可执行脚本
        ],
    },
    # 其他元数据
    author='boyi.zhang',
    author_email='15813380401@163.com',
    description='pytoolkit',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/your_package_name',
    # ...
)