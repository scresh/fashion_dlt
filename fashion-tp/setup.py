from __future__ import print_function
from setuptools import setup, find_packages
import os

conf_dir = "/etc/sawtooth"

data_files = [
    (conf_dir, ['packaging/fashion.toml'])
]

if os.path.exists("/etc/default"):
    data_files.append(
        ('/etc/default', ['packaging/systemd/fashion-tp-python'])
    )

if os.path.exists("/lib/systemd/system"):
    data_files.append(
        ('/lib/systemd/system', ['packaging/systemd/fashion-tp-python.service'])
    )

setup(
    name='fashion-tp',
    version='1.0',
    description='Fashion Transaction Processor',
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
            'fashion-tp = fashion-tp.main:main',
        ]
    })
