from __future__ import print_function

import os
import subprocess

from setuptools import setup, find_packages

conf_dir = "/etc/sawtooth"

data_files = [
    (conf_dir, ['packaging/fashion.toml'])
]

if os.path.exists("/etc/default"):
    data_files.append(
        ('/etc/default', ['packaging/systemd/fashion-tp-python']))

if os.path.exists("/lib/systemd/system"):
    data_files.append(('/lib/systemd/system',
                       ['packaging/systemd/fashion-tp-python.service']))

setup(
    name='sawtooth-fashion',
    version='0.1',
    description='Sawtooth Fashion',
    author='scresh',
    url='https://github.com/scresh/fashion_dlt',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'colorlog',
        'protobuf',
        'sawtooth-sdk',
        'sawtooth-signing',
        'PyYAML',
    ],
    data_files=data_files,
    entry_points={
        'console_scripts': [
            'fashion = fashion_transaction_family.fashion_cli:main_wrapper',
            'fashion-tp-python = fashion_transaction_family.processor.main:main',
        ]
    })
