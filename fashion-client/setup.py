from __future__ import print_function
from setuptools import setup, find_packages
import os

conf_dir = "/etc/sawtooth"

data_files = [
    (conf_dir, ['packaging/fashion.toml'])
]

if os.path.exists("/etc/default"):
    data_files.append(
        ('/etc/default', ['packaging/systemd/fashion-client-python'])
    )

if os.path.exists("/lib/systemd/system"):
    data_files.append(
        ('/lib/systemd/system', ['packaging/systemd/fashion-client-python.service'])
    )

setup(
    name='fashion-client',
    version='1.0',
    description='Fashion Client',
    author='scresh',
    url='https://github.com/scresh/fashion_dlt',
    packages=find_packages(),
    install_requires=[
        'certifi',
        'cffi',
        'chardet',
        'colorlog',
        'idna',
        'protobuf',
        'pycparser',
        'PyYAML',
        'pyzmq',
        'requests',
        'sawtooth-sdk',
        'sawtooth-signing',
        'secp256k1',
        'six',
        'toml',
        'urllib3',
    ],
    data_files=data_files,
    entry_points={
        'console_scripts': [
            'fashion-client = fashion_client.main:main',
        ]
    })
