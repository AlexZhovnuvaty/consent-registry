#!/usr/bin/env bash
bin/consent-registry-protogen make_consent_protobuf
cp -R consent_common consent_processor/consent_processor
cd consent_processor || exit
python3 setup.py clean --all
python3 setup.py build
python3 setup.py install