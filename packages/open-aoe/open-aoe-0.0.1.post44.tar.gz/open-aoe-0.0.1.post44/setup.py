#!/usr/bin/env python
# Copyright (c) didigo. All rights reserved.
from setuptools import find_packages, setup
import openaoe.backend.util.file as utils
import os

def recursive_files(base_dir):
    file_list = []
    for dirpath, dirnames, filenames in os.walk(base_dir):
        for filename in filenames:
            file_list.append(os.path.join(dirpath, filename))
    return file_list

setup(
    name='open-aoe',
    version='0.0.1-post44',
    description='AOE (All yOu nEed) retrieves answers from different LLM in parallel',
    long_description=utils.get_file_content("README_OUT.md"),
    long_description_content_type='text/markdown',
    author='arkmon',
    author_email='',
    keywords='openaoe',
    url='https://github.com/opensealion/aoe',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'openaoe': ['frontend/dist/*', 'frontend/dist/**/*']
    },
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
    license='Apache License 2.0',
    install_requires=utils.parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
              'open-aoe=openaoe.main:main'
        ]
    },
    ext_modules=[],

)
