from sanic import Blueprint
from sanic import response

from rest_api.data_common import transaction as data_transaction
from rest_api.consent_common import transaction as consent_transaction
from rest_api import general, security_messaging
from rest_api.errors import ApiInternalError, ApiBadRequest

ACADEMICS_BP = Blueprint('academic')


@ACADEMICS_BP.get('academic')
async def get_all_academics(request):
    """Fetches complete details of all Accounts in state"""
    client_key = general.get_request_key_header(request)
    academic_list = await security_messaging.get_academics(request.app.config.VAL_CONN, client_key)
    academic_list_json = []
    for address, pat in academic_list.items():
        academic_list_json.append({
            'public_key': pat.public_key,
            'name': pat.name
        })

    return response.json(body={'data': academic_list_json},
                         headers=general.get_response_headers())


# @ACADEMICS_BP.get('academic/consent_request_list')
# async def consent_request_list(request):
#     """Fetches complete details of all Accounts in state"""
#     client_key = general.get_request_key_header(request)
#     consent_list = \
#         await security_messaging.get_consent_request_list(request.app.config.VAL_CONN, client_key)
#     consent_list_json = []
#     for address, con in consent_list.items():
#         consent_list_json.append({
#             'src_pkey': con.src_pkey,
#             'dest_pkey': con.dest_pkey,
#             'action_type': con.action_type
#         })
#
#     return response.json(body={'data': consent_list_json},
#                          headers=general.get_response_headers())


@ACADEMICS_BP.post('academic')
async def register_academic(request):
    """Updates auth information for the authorized account"""
    # keyfile = common.get_keyfile(request.json.get['signer'])
    required_fields = ['name']
    general.validate_fields(required_fields, request.json)

    name = request.json.get('name')

    # private_key = common.get_signer_from_file(keyfile)
    # signer = CryptoFactory(request.app.config.CONTEXT).new_signer(private_key)
    academic_signer = request.app.config.SIGNER_ACADEMIC  # .get_public_key().as_hex()

    client_txn = consent_transaction.create_academic_client(
        txn_signer=academic_signer,
        batch_signer=academic_signer
    )

    academic_txn = data_transaction.create_academic(
        txn_signer=academic_signer,
        batch_signer=academic_signer,
        name=name)

    batch, batch_id = consent_transaction.make_batch_and_id([client_txn, academic_txn], academic_signer)

    await security_messaging.add_academic(
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


@ACADEMICS_BP.get('academic/request_consent/<consumer_pkey>')
async def request_consent(request, consumer_pkey):
    """Updates auth information for the authorized account"""
    client_key = general.get_request_key_header(request)
    client_signer = general.get_signer(request, client_key)
    request_consent_txn = consent_transaction.request_consumer_consent(
        txn_signer=client_signer,
        batch_signer=client_signer,
        consumer_pkey=consumer_pkey)

    batch, batch_id = consent_transaction.make_batch_and_id([request_consent_txn], client_signer)

    await security_messaging.request_consent(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], client_key)

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(sign_inform_consent
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())
