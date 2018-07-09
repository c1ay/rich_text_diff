# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='rich_text_diff',
    version='0.0.2',
    author='liukai',
    author_email='liukai@zhihu.com',
    description='rich_text_diff rich text',
    packages=['rich_text_diff'],
    test_suite='nose.collector',
    url='https://github.com/c1ay/rich_text_diff',
    tests_require=['nose'],
    install_requires=[
        'lxml',
        'diff_match_patch',
        'bidict',
    ]
)
