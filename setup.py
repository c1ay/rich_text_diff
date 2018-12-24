# -*- coding: utf-8 -*-
from setuptools import setup


with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='rich_text_diff',
    version='0.0.6',
    author='liukai',
    author_email='liukai@zhihu.com',
    description='support rich text diff',
    packages=['rich_text_diff'],
    test_suite='nose.collector',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/c1ay/rich_text_diff',
    tests_require=['nose'],
    install_requires=[
        'lxml',
        'diff_match_patch',
        'bidict',
    ]
)
