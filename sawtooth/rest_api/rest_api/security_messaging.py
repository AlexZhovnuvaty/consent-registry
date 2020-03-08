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
import logging

from sawtooth_rest_api.protobuf import client_state_pb2
from sawtooth_rest_api.protobuf import validator_pb2

from rest_api.data_common import helper as data_helper
from rest_api.data_common.protobuf.data_payload_pb2 import Consumer, Academic, ConsumerDataExt

from rest_api.consent_common import helper as consent_helper
from rest_api.consent_common.protobuf.consent_pb2 import Client, Permission, ActionOnAccess

from rest_api import messaging
from rest_api.errors import ApiForbidden, ApiUnauthorized, ApiBadRequest

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


async def _send(conn, timeout, batches):
    await messaging.send(conn, timeout, batches)


async def check_batch_status(conn, batch_ids):
    await messaging.check_batch_status(conn, batch_ids)


async def get_state_by_address(conn, address_suffix):
    status_request = client_state_pb2.ClientStateListRequest(address=address_suffix)
    validator_response = await conn.send(
        validator_pb2.Message.CLIENT_STATE_LIST_REQUEST,
        status_request.SerializeToString())

    status_response = client_state_pb2.ClientStateListResponse()
    status_response.ParseFromString(validator_response.content)
    # resp = status_response

    return status_response  # resp.entries


async def add_consumer(conn, timeout, batches):
    await _send(conn, timeout, batches)


async def get_consumers(conn, client_key):
    client = await get_client(conn, client_key)
    consumers_list = {}
    if Permission(type=Permission.GET_CONSUMERS_LIST) in client.permissions:
        list_consumer_address = data_helper.make_consumer_list_address()
        list_consumer_resources = await messaging.get_state_by_address(conn, list_consumer_address)
        for entity in list_consumer_resources.entries:
            cn = Consumer()
            cn.ParseFromString(entity.data)
            LOGGER.debug('consumer: ' + str(cn))
            consumers_list[entity.address] = cn
        return consumers_list
    raise ApiForbidden("Insufficient permission")


async def add_academic(conn, timeout, batches):
    await _send(conn, timeout, batches)


async def get_consent_request_list(conn, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.GET_REQUESTS_LIST) in client.permissions:
        LOGGER.debug('has GET_REQUESTS_LIST permission: ' + str(client_key))
        consent_request_list = await get_consent_request(conn, client_key)
        return consent_request_list
    raise ApiForbidden("Insufficient permission")


async def get_academics(conn, client_key):
    client = await get_client(conn, client_key)
    academic_list = {}
    if Permission(type=Permission.GET_ACADEMICS_LIST) in client.permissions:
        LOGGER.debug('has GET_ACADEMICS_LIST permission: ' + str(client_key))
        list_academic_address = data_helper.make_academic_list_address()
        # Get Data Processing Access
        # data_processing_access = await get_consent_by_consumer(consent_conn, client_key)
        # data_processing_access_list = {}
        # for address, pt in data_processing_access.items():
        #     LOGGER.debug('data_processing_access: ' + str(pt))
        #     patient = await get_patient(ehr_conn, pt.src_pkey)
        #     data_processing_access_list[pt.src_pkey] = patient

        # consent = await get_read_ehr_consent(conn, client_key)
        # consent_list = {}
        # for address, pt in consent.items():
        #     LOGGER.debug('consent: ' + str(pt))
        #     patient = await get_patient(conn, pt.src_pkey)
        #     consent_list[pt.src_pkey] = patient
        #
        academic_list_resources = await messaging.get_state_by_address(conn, list_academic_address)
        for entity in academic_list_resources.entries:
            ac = Academic()
            ac.ParseFromString(entity.data)
            academic_list[entity.address] = ac
            LOGGER.debug('academic: ' + str(ac))
        # Apply Access
        # for patient_address, pt in academic_list.items():
        #     LOGGER.debug('patient: ' + str(pt))
        #     if Permission(type=Permission.READ_OWN_PATIENT) in client.permissions and pt.public_key == client_key:
        #         pass
        #     elif pt.public_key not in data_processing_access_list:
        #         pat2 = Patient()
        #         patient_list[patient_address] = pat2
        return academic_list
    # elif Permission(type=Permission.READ_OWN_PATIENT) in client.permissions:
    #     LOGGER.debug('has READ_OWN_PATIENT: ' + str(client_key))
    #     # Get Data Processing Access
    #     data_processing_access = await get_consent_by_consumer(consent_conn, client_key)
    #     data_processing_access_list = {}
    #     for address, pt in data_processing_access.items():
    #         LOGGER.debug('data_processing_access: ' + str(pt))
    #         patient = await get_patient(ehr_conn, pt.src_pkey)
    #         data_processing_access_list[pt.src_pkey] = patient
    #     return data_processing_access_list
    raise ApiForbidden("Insufficient permission")


async def get_academic(conn, academic_key):
    list_academic_address = data_helper.make_academic_address(academic_key)
    academic_resources = await messaging.get_state_by_address(conn, list_academic_address)
    for entity in academic_resources.entries:
        ac = Academic()
        ac.ParseFromString(entity.data)
        return ac
    raise ApiBadRequest("No such academic exist: " + str(academic_key))


async def add_data(conn, timeout, batches, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.ADD_DATA) in client.permissions:
        LOGGER.debug('has ADD_DATA permission: True')
        # Has consent from patient
        # access = await has_data_processing_access(ehr_conn, dest_pkey, src_pkey)
        # if not access:
        #     LOGGER.debug('no data processing access')
        #     raise ApiForbidden("Insufficient permission")
        #
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


async def approve_request(conn, timeout, batches, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.ADD_DATA) in client.permissions:
        LOGGER.debug('has permission: True')
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


async def revoke_consent(conn, timeout, batches, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.REVOKE_CONSENT) in client.permissions:
        LOGGER.debug('has permission: True')
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


async def request_consent(conn, timeout, batches, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.REQUEST_CONSENT) in client.permissions:
        LOGGER.debug('has permission: True')
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


async def decline_request(conn, timeout, batches, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.DECLINE_CONSENT) in client.permissions:
        LOGGER.debug('has permission: True')
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


async def get_client(conn, client_key):
    client_address = consent_helper.make_client_address(client_key)
    LOGGER.debug('client_address: ' + str(client_address))
    client_resources = await messaging.get_state_by_address(conn, client_address)
    LOGGER.debug('client_resources: ' + str(client_resources))
    for entity in client_resources.entries:
        cl = Client()
        cl.ParseFromString(entity.data)
        LOGGER.debug('client: ' + str(cl))
        return cl
    raise ApiUnauthorized("No such client registered")


# async def has_data_processing_access(conn, dest_pkey, src_pkey):  # dest_pkey - doctor, src_pkey - patient
#     access_list = await get_consent_by_consumer(conn, dest_pkey)
#     for address, data in access_list.items():
#         LOGGER.debug('address: data -> ' + str(data) + '; src_key -> ' + str(src_pkey))
#         if data.src_pkey == src_pkey:
#             LOGGER.debug('has consent!')
#             return True
#     return False


async def get_consent_request(conn, client_key):
    consent_list_address = \
        consent_helper.make_consent_list_address_by_destination_client(client_key)
    LOGGER.debug('consent_list_address: ' + str(consent_list_address))
    consent_list_resources = \
        await messaging.get_state_by_address(conn, consent_list_address)
    LOGGER.debug('consent_list_resources: ' + str(consent_list_resources))
    consent_list = {}
    for entity in consent_list_resources.entries:
        aoa = ActionOnAccess()
        aoa.ParseFromString(entity.data)
        consent_list[entity.address] = aoa
        LOGGER.debug('request inform consent: ' + str(aoa))
    return consent_list


# # TODO Invalid package?
# async def get_signed_inform_consent(conn, client_key):
#     signed_inform_consent_list_address = \
#         consent_helper.make_sign_inform_document_consent_list_address_by_destination_client(client_key)
#     LOGGER.debug('signed_inform_consent_list_address: ' + str(signed_inform_consent_list_address))
#     signed_inform_consent_list_resources = \
#         await messaging.get_state_by_address(conn, signed_inform_consent_list_address)
#     LOGGER.debug('signed_inform_consent_list_resources: ' + str(signed_inform_consent_list_resources))
#     signed_inform_consent_list = {}
#     for entity in signed_inform_consent_list_resources.entries:
#         aoa = ActionOnAccess()
#         aoa.ParseFromString(entity.data)
#         signed_inform_consent_list[entity.address] = aoa
#         LOGGER.debug('signed inform consent: ' + str(aoa))
#     return signed_inform_consent_list


async def get_consent_by_consumer(conn, client_key):
    consent = consent_helper.make_consent_list_address_by_destination_client(client_key)
    LOGGER.debug('consent: ' + str(consent))
    consent_resources = await messaging.get_state_by_address(conn, consent)
    LOGGER.debug('consent_resources: ' + str(consent_resources))
    consent_list = {}
    for entity in consent_resources.entries:
        aoa = ActionOnAccess()
        aoa.ParseFromString(entity.data)
        if aoa.action_type == ActionOnAccess.APPROVED:
            consent_list[entity.address] = aoa
            LOGGER.debug('consent approved i: ' + str(aoa))
        else:
            LOGGER.debug('consent not approved i: ' + str(aoa))
    return consent_list

# async def get_shared_ehrs(ehr_conn, consent_conn, investigator_pkey):
#     investigator_access_address = \
#         ehr_helper.make_investigator_access_list_address_by_destination_client(investigator_pkey)
#     LOGGER.debug('investigator_access_address: ' + str(investigator_access_address))
#     investigator_access_resources = await messaging.get_state_by_address(ehr_conn, investigator_access_address)
#     LOGGER.debug('investigator_access_resources: ' + str(investigator_access_resources))
#     ehrs_list = {}
#     for entity in investigator_access_resources.entries:
#         aoa = ActionOnAccess()
#         aoa.ParseFromString(entity.data)
#         ehrs = await get_ehrs(ehr_conn, consent_conn, aoa.src_pkey)
#         ehrs_list.update(ehrs)
#         LOGGER.debug('ehrs: ' + str(ehrs))
#     return ehrs_list


async def get_data(conn, client_key):
    client = await get_client(conn, client_key)
    data_list = {}
    if Permission(type=Permission.READ_DATA) in client.permissions:
        LOGGER.debug('has READ_DATA permission: ' + str(client_key))
        # Get Consumers with Consent
        consumers_with_consent = await get_consent_by_consumer(conn, client_key)
        for address, cn in consumers_with_consent.items():
            LOGGER.debug('consumer with consent: ' + str(cn))

            data_id_list_address = data_helper.make_data_list_by_consumer_address(cn.src_pkey)
            data_id_list_resources = await messaging.get_state_by_address(conn, data_id_list_address)
            for entity in data_id_list_resources.entries:
                data_id = entity.data.decode()
                data_address = data_helper.make_data_address(data_id)
                LOGGER.debug('get data: ' + str(data_address))
                data_resources = await messaging.get_state_by_address(conn, data_address)
                for entity2 in data_resources.entries:
                    entity_data_decode = entity2.data.decode()
                    LOGGER.debug('entity_data_decode: ' + str(entity_data_decode))
                    cde = ConsumerDataExt()
                    cde.ParseFromString(entity2.data)
                    LOGGER.debug('data: ' + str(cde))
                    data_list[entity2.address] = cde

        # data_list_resources = await messaging.get_state_by_address(conn, data_list_address)
        # for entity in data_list_resources.entries:
        #     cde = ConsumerDataExt()
        #     cde.ParseFromString(entity.data)
        #
        #     data_list[entity.address] = cde
        #     LOGGER.debug('data: ' + str(cde))
        # # Apply Consent
        # for patient_address, pt in patient_list.items():
        #     LOGGER.debug('patient: ' + str(pt))
        #     for claim_address, e in ehr_list.items():
        #         LOGGER.debug('ehr: ' + str(e))
        #         if patient_address == e.client_pkey:
        #             LOGGER.debug('match!')
        #             pt_local = patient_list[patient_address]
        #             e.name = pt_local.name
        #             e.surname = pt_local.surname
        #             ehr_list[claim_address] = e
        return data_list
    elif Permission(type=Permission.READ_OWN_DATA) in client.permissions:
        data_id_list_address = data_helper.make_data_list_by_consumer_address(client_key)
        LOGGER.debug('has READ_OWN_DATA permission: ' + str(client_key))
        data_id_list_resources = await messaging.get_state_by_address(conn, data_id_list_address)
        for entity in data_id_list_resources.entries:
            data_id = entity.data.decode()
            data_address = data_helper.make_data_address(data_id)
            LOGGER.debug('get data: ' + str(data_address))
            data_resources = await messaging.get_state_by_address(conn, data_address)
            for entity2 in data_resources.entries:
                entity_data_decode = entity2.data.decode()
                LOGGER.debug('entity_data_decode: ' + str(entity_data_decode))
                cde = ConsumerDataExt()
                cde.ParseFromString(entity2.data)
                LOGGER.debug('data: ' + str(cde))
                data_list[entity2.address] = cde
        return data_list
    # elif Permission(type=Permission.READ_OWN_PATIENT_DATA) in client.permissions:
    #     ehr_list_ids_address = ehr_helper.make_ehr_list_by_patient_address(client_key)
    #     LOGGER.debug('has READ_OWN_PATIENT_DATA permission: ' + str(ehr_list_ids_address))
    #     ehr_list_ids = await messaging.get_state_by_address(ehr_conn, ehr_list_ids_address)
    #     for entity in ehr_list_ids.entries:
    #         ehr_id = entity.data.decode()
    #         ehr_address = ehr_helper.make_ehr_address(ehr_id)
    #         LOGGER.debug('get ehr: ' + str(ehr_address))
    #         ehr_resources = await messaging.get_state_by_address(ehr_conn, ehr_address)
    #         for entity2 in ehr_resources.entries:
    #             LOGGER.debug('get ehr entity2: ' + str(entity2.address))
    #             e = EHRWithUser()
    #             e.ParseFromString(entity2.data)
    #             ehr_list[entity2.address] = e
    #     return ehr_list
    else:
        LOGGER.debug('neither READ_DATA permissions')
    raise ApiForbidden("Insufficient permission")


# async def get_ehr_by_id(ehr_conn, consent_conn, client_key, ehr_id):
#     client = await get_client(consent_conn, client_key)
#     ehr_list = {}
#     if Permission(type=Permission.READ_PATIENT_DATA) in client.permissions:
#         # ehr_list_address = ehr_helper.make_ehr_list_address()
#         ehr_address = ehr_helper.make_ehr_address(ehr_id)
#         LOGGER.debug('has READ_PATIENT_DATA permission: ' + str(client_key))
#         # Get Consent
#         access = await get_consent_by_consumer(ehr_conn, client_key)
#         patient_list = {}
#         for address, pt in access.items():
#             LOGGER.debug('patient access: ' + str(pt))
#             patient = await get_patient(ehr_conn, pt.src_pkey)
#             patient_list[pt.src_pkey] = patient
#         #
#         ehr_resources = await messaging.get_state_by_address(ehr_conn, ehr_address)
#         for entity in ehr_resources.entries:
#             cl = EHRWithUser()
#             cl.ParseFromString(entity.data)
#
#             ehr_list[entity.address] = cl
#             LOGGER.debug('ehr: ' + str(cl))
#         # Apply Consent
#         for patient_address, pt in patient_list.items():
#             LOGGER.debug('patient: ' + str(pt))
#             for claim_address, e in ehr_list.items():
#                 LOGGER.debug('ehr: ' + str(e))
#                 if patient_address == e.client_pkey:
#                     LOGGER.debug('match!')
#                     pt_local = patient_list[patient_address]
#                     e.name = pt_local.name
#                     e.surname = pt_local.surname
#                     ehr_list[claim_address] = e
#         if not ehr_list:
#             raise ApiForbidden("Cat not get EHR having '" + str(ehr_id) + "' id")
#         return list(ehr_list.values())[0]
#     elif Permission(type=Permission.READ_OWN_PATIENT_DATA) in client.permissions:
#         # ehr_list_ids_address = ehr_helper.make_ehr_list_by_patient_address(client_key)
#         LOGGER.debug('has READ_OWN_PATIENT_DATA permission: ' + str(client_key))
#         # ehr_list_ids = await messaging.get_state_by_address(conn, ehr_list_ids_address)
#         # for entity in ehr_list_ids.entries:
#         #     ehr_id = entity.data.decode()
#         ehr_address = ehr_helper.make_ehr_address(ehr_id)
#         LOGGER.debug('get ehr: ' + str(ehr_address))
#         ehr_resources = await messaging.get_state_by_address(ehr_conn, ehr_address)
#         for entity in ehr_resources.entries:
#             LOGGER.debug('get ehr entity: ' + str(entity.address))
#             e = EHRWithUser()
#             e.ParseFromString(entity.data)
#             ehr_list[entity.address] = e
#         if not ehr_list:
#             raise ApiForbidden("Cat not get EHR having '" + str(ehr_id) + "' id")
#         return list(ehr_list.values())[0]
#     else:
#         LOGGER.debug('neither READ_PATIENT_DATA nor READ_OWN_PATIENT_DATA permissions')
#     raise ApiForbidden("Insufficient permission")

# def _get_int(value):
#     return int(value)
#
#
# # Used
# def _match_incl_excl_criteria(data, inc_excl_criteria):
#     for criteria, value in inc_excl_criteria.items():
#         LOGGER.debug('_match_incl_excl_criteria -> criteria: ' + criteria + '; value: ' + value + ';')
#         v = _get_int(value)
#         if criteria == "excl_height_less":
#             if _get_int(data.height) < v:
#                 return False
#         elif criteria == "excl_height_more":
#             if _get_int(data.height) > v:
#                 return False
#         elif criteria == "incl_height_less":
#             if _get_int(data.height) > v:
#                 return False
#         elif criteria == "incl_height_more":
#             if _get_int(data.height) < v:
#                 return False
#         else:
#             raise ApiForbidden("Invalid excl/incl criteria specified. "
#                                "Only {excl_height_less,excl_height_more,incl_height_less,incl_height_more} allowed")
#     return True


# # Used
# async def get_pre_screening_data(ehr_conn, consent_conn, investigator_pkey, inc_excl_criteria):
#     client = await get_client(consent_conn, investigator_pkey)
#     if Permission(type=Permission.READ_PATIENT_DATA) in client.permissions:
#         ehr_list = await get_shared_ehrs(ehr_conn, consent_conn, investigator_pkey)
#         ehr_screening_list = {}
#         for address, ehr in ehr_list.items():
#             if _match_incl_excl_criteria(ehr, inc_excl_criteria):
#                 ehr_screening_list[address] = ehr
#         return ehr_screening_list
#     else:
#         LOGGER.debug('has permission: False')
#     raise ApiForbidden("Insufficient permission")

# async def has_signed_inform_consent(conn, patient_pkey, investigator_pkey):
#     LOGGER.debug('patient_pkey: ' + str(patient_pkey) + '; investigator_pkey: ' + str(investigator_pkey))
#     signed_inform_consent_list = await get_signed_inform_consent(conn, investigator_pkey)
#     for address, value in signed_inform_consent_list.items():
#         LOGGER.debug('address: ' + str(address) + '; value: ' + str(value))
#         if value.src_pkey == patient_pkey:
#             LOGGER.debug('signed inform consent: True')
#             return True
#     return False
