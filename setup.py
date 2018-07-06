# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='rich_text_diff',
    version='0.0.1',
    author='liukai',
    author_email='liukai@zhihu.com',
    description='diff rich text',
    packages=['diff'],
    test_suite='nose.collector',
    url='https://github.com/c1ay/diff',
    tests_require=['nose'],
    install_requires=[
        'lxml',
        'diff_match_patch',
        'bidict',
    ]
)
