# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='diff',
    version='0.1',
    author='liukai',
    author_email='liukai@zhihu.com',
    packages=['diff'],
    install_requires=[
        'lxml',
        'diff_match_patch',
        'bidict',
    ]
)
