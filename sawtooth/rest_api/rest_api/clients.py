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
from sanic import Blueprint
from sanic import response

from rest_api import general

CLIENTS_BP = Blueprint('clients')


@CLIENTS_BP.get('clients')
async def get_all_clients(request):
    """Fetches complete details of all Accounts in state"""
    consumer_pkey = request.app.config.SIGNER_CONSUMER.get_public_key().as_hex()
    academic_pkey = request.app.config.SIGNER_ACADEMIC.get_public_key().as_hex()
    clients = {'consumer': consumer_pkey, 'academic': academic_pkey}
    return response.json(body={'data': clients},
                         headers=general.get_response_headers())
