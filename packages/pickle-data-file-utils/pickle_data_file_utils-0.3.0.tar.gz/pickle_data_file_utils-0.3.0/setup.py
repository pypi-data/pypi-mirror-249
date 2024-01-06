#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    "Rich"]

test_requirements = [ ]

setup(
    author="Jaideep Sundaram",
    author_email='jai.python3@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Collection of Python utility scripts for converting file formats to and from pickle files.",
    entry_points={
        'console_scripts': [
            'csv2pickle=pickle_data_file_utils.csv2pickle:main',
            'tsv2pickle=pickle_data_file_utils.tsv2pickle:main',
            'json2pickle=pickle_data_file_utils.json2pickle:main',
            'pickle2csv=pickle_data_file_utils.pickle2csv:main',
            'pickle2tsv=pickle_data_file_utils.pickle2tsv:main',
            'pickle2json=pickle_data_file_utils.pickle2json:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pickle_data_file_utils',
    name='pickle_data_file_utils',
    packages=find_packages(include=['pickle_data_file_utils', 'pickle_data_file_utils.*']),
    scripts=["scripts/generate_executables_and_aliases.py"],
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jai-python3/pickle_data_file_utils',
    version='0.3.0',
    zip_safe=False,
)
