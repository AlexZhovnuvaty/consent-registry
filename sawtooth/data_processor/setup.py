from __future__ import print_function
from setuptools import setup, find_packages  # , Command

conf_dir = "/etc/sawtooth"

setup(
    name='data-processor',
    version='0.1',
    description='Sawtooth Consent Registry Project',
    author='Alexander Zhovnuvaty',
    url='https://github.com/AlexZhovnuvaty/consent-registry',
    packages=find_packages(),
    install_requires=[
        # 'aiohttp',
        'colorlog',
        'protobuf',
        'sawtooth-sdk',
        # 'sawtooth-signing',
        # 'PyYAML',
    ],
    # data_files=data_files,
    entry_points={
        'console_scripts': [
            'data-tp = data_processor.main:main',
        ]
    })
