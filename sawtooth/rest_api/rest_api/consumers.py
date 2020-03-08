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

from rest_api.data_common import transaction as data_transaction
from rest_api.consent_common import transaction as consent_transaction
from rest_api import general, security_messaging
from rest_api.errors import ApiBadRequest, ApiInternalError

CONSUMERS_BP = Blueprint('consumer')


@CONSUMERS_BP.get('consumer')
async def get_all_consumers(request):
    """Fetches complete details of all Accounts in state"""
    client_key = general.get_request_key_header(request)
    consumer_list = await security_messaging.get_consumers(request.app.config.VAL_CONN, client_key)

    consumer_list_json = []
    for address, con in consumer_list.items():
        consumer_list_json.append({
            'public_key': con.public_key,
            'name': con.name
        })
    return response.json(body={'data': consumer_list_json},
                         headers=general.get_response_headers())


@CONSUMERS_BP.post('consumer')
async def register_consumer(request):
    """Updates auth information for the authorized account"""
    required_fields = ['name']
    general.validate_fields(required_fields, request.json)

    name = request.json.get('name')

    consumer_signer = request.app.config.SIGNER_CONSUMER  # .get_public_key().as_hex()

    client_txn = consent_transaction.create_consumer_client(
        txn_signer=consumer_signer,
        batch_signer=consumer_signer
    )

    consumer_txn = data_transaction.create_consumer(
        txn_signer=consumer_signer,
        batch_signer=consumer_signer,
        name=name
    )

    batch, batch_id = consent_transaction.make_batch_and_id([client_txn, consumer_txn], consumer_signer)

    await security_messaging.add_consumer(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch])

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())


@CONSUMERS_BP.get('consumer/approve_request/<academic_pkey>')
async def approve_academic_request(request, academic_pkey):
    """Updates auth information for the authorized account"""
    consumer_key = general.get_request_key_header(request)
    client_signer = general.get_signer(request, consumer_key)
    approve_request_txn = consent_transaction.approve_academic_request(
        txn_signer=client_signer,
        batch_signer=client_signer,
        academic_pkey=academic_pkey)

    batch, batch_id = consent_transaction.make_batch_and_id([approve_request_txn], client_signer)

    await security_messaging.approve_request(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], consumer_key)

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())


@CONSUMERS_BP.get('consumer/decline_request/<academic_pkey>')
async def decline_academic_request(request, academic_pkey):
    """Updates auth information for the authorized account"""
    consumer_key = general.get_request_key_header(request)
    client_signer = general.get_signer(request, consumer_key)
    decline_request_txn = consent_transaction.decline_academic_request(
        txn_signer=client_signer,
        batch_signer=client_signer,
        academic_pkey=academic_pkey)

    batch, batch_id = consent_transaction.make_batch_and_id([decline_request_txn], client_signer)

    await security_messaging.decline_request(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], consumer_key)

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())


@CONSUMERS_BP.get('consumer/revoke_request/<academic_pkey>')
async def revoke_academic_request(request, academic_pkey):
    """Updates auth information for the authorized account"""
    consumer_key = general.get_request_key_header(request)
    client_signer = general.get_signer(request, consumer_key)
    revoke_request_txn = consent_transaction.revoke_academic_request(
        txn_signer=client_signer,
        batch_signer=client_signer,
        academic_pkey=academic_pkey)

    batch, batch_id = consent_transaction.make_batch_and_id([revoke_request_txn], client_signer)

    await security_messaging.revoke_consent(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], consumer_key)

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())
