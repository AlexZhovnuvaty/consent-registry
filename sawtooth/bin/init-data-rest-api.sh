#!/usr/bin/env bash
cp -R data_common rest_api/rest_api
cp -R consent_common rest_api/rest_api
cd rest_api || exit
python3 setup.py clean --all
python3 setup.py build
python3 setup.py install

if [[ ! -f /root/.sawtooth/keys/consumerWEB.priv ]]; then
    sawtooth keygen consumerWEB
fi;

if [[ ! -f /root/.sawtooth/keys/academicWEB.priv ]]; then
    sawtooth keygen academicWEB
fi;
