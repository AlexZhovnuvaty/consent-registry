# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

from __future__ import print_function
from setuptools import setup, find_packages  # , Command

setup(
    name='rest-api',
    version='0.1',
    description='Sawtooth Consent Registry Project',
    author='Alexander Zhovnuvaty',
    url='https://github.com/AlexZhovnuvaty/consent-registry',
    # packages=find_packages(include=['rest_api*', 'common*']),
    packages=find_packages(),
    # package_dir={'': 'processor'},
    install_requires=[
        # 'aiohttp',
        'colorlog',
        'protobuf',
        'sawtooth-sdk',
        'secp256k1',
        # 'Crypto',
        'requests',
        'sanic',
        'sanic_cors',
        'pyzmq',
    ],
    # cmdclass={
    #     'clean': CleanCommand,
    # },
    # data_files=data_files,
    entry_points={
        'console_scripts': [
            # 'xo = sawtooth_xo.xo_cli:main_wrapper',
            'rest-api = rest_api.main:main',
        ]
    })
