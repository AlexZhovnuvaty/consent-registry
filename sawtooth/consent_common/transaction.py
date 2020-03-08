import hashlib
import random
import logging

from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader, Batch
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction, TransactionHeader

from . import helper as helper
from .protobuf.consent_pb2 import Permission, ConsentPayload, Client, ActionOnAccess

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


def _make_transaction(payload, inputs, outputs, txn_signer, batch_signer):
    txn_header_bytes, signature = _transaction_header(txn_signer, batch_signer, inputs, outputs, payload)

    txn = Transaction(
        header=txn_header_bytes,
        header_signature=signature,
        payload=payload.SerializeToString()
    )

    return txn


def make_batch_and_id(transactions, batch_signer):
    batch_header_bytes, signature = _batch_header(batch_signer, transactions)

    batch = Batch(
        header=batch_header_bytes,
        header_signature=signature,
        transactions=transactions
    )

    return batch, batch.header_signature


def _make_header_and_batch(payload, inputs, outputs, txn_signer, batch_signer):
    txn_header_bytes, signature = _transaction_header(txn_signer, batch_signer, inputs, outputs, payload)

    txn = Transaction(
        header=txn_header_bytes,
        header_signature=signature,
        payload=payload.SerializeToString()
    )

    transactions = [txn]

    batch_header_bytes, signature = _batch_header(batch_signer, transactions)

    batch = Batch(
        header=batch_header_bytes,
        header_signature=signature,
        transactions=transactions
    )

    return batch, batch.header_signature


def _transaction_header(txn_signer, batch_signer, inputs, outputs, payload):
    txn_header_bytes = TransactionHeader(
        family_name=helper.TP_FAMILYNAME,
        family_version=helper.TP_VERSION,
        inputs=inputs,
        outputs=outputs,
        signer_public_key=txn_signer.get_public_key().as_hex(),  # signer.get_public_key().as_hex(),
        # In this example, we're signing the batch with the same private key,
        # but the batch can be signed by another party, in which case, the
        # public key will need to be associated with that key.
        batcher_public_key=batch_signer.get_public_key().as_hex(),  # signer.get_public_key().as_hex(),
        # In this example, there are no dependencies.  This list should include
        # an previous transaction header signatures that must be applied for
        # this transaction to successfully commit.
        # For example,
        # dependencies=['540a6803971d1880ec73a96cb97815a95d374cbad5d865925e5aa0432fcf1931539afe10310c122c5eaae15df61236079abbf4f258889359c4d175516934484a'],
        dependencies=[],
        nonce=random.random().hex().encode(),
        payload_sha512=hashlib.sha512(payload.SerializeToString()).hexdigest()
    ).SerializeToString()

    signature = txn_signer.sign(txn_header_bytes)
    return txn_header_bytes, signature


def _batch_header(batch_signer, transactions):
    batch_header_bytes = BatchHeader(
        signer_public_key=batch_signer.get_public_key().as_hex(),
        transaction_ids=[txn.header_signature for txn in transactions],
    ).SerializeToString()

    signature = batch_signer.sign(batch_header_bytes)

    return batch_header_bytes, signature


def create_consumer_client(txn_signer, batch_signer):
    permissions = [Permission(type=Permission.GET_CONSUMERS_LIST),
                   Permission(type=Permission.ADD_DATA),
                   Permission(type=Permission.READ_OWN_DATA),
                   Permission(type=Permission.GET_REQUESTS_LIST),
                   Permission(type=Permission.APPROVE_CONSENT),
                   Permission(type=Permission.DECLINE_CONSENT),
                   Permission(type=Permission.REVOKE_CONSENT)
                   ]
    return create_client(txn_signer, batch_signer, permissions)


def create_academic_client(txn_signer, batch_signer):
    permissions = [Permission(type=Permission.GET_CONSUMERS_LIST),
                   Permission(type=Permission.GET_ACADEMICS_LIST),
                   Permission(type=Permission.GET_REQUESTS_LIST),
                   Permission(type=Permission.REQUEST_CONSENT),
                   Permission(type=Permission.READ_DATA)
                   ]
    return create_client(txn_signer, batch_signer, permissions)


def create_client(txn_signer, batch_signer, permissions):
    client_pkey = txn_signer.get_public_key().as_hex()
    LOGGER.debug('client_pkey: ' + str(client_pkey))
    inputs = outputs = helper.make_client_address(public_key=client_pkey)
    LOGGER.debug('inputs: ' + str(inputs))
    client = Client(
        public_key=client_pkey,
        permissions=permissions)

    payload = ConsentPayload(
        payload_type=ConsentPayload.PAYLOAD_ADD_CLIENT,
        create_client=client)

    LOGGER.debug('payload: ' + str(payload))

    return _make_transaction(
        payload=payload,
        inputs=[inputs],
        outputs=[outputs],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def request_consumer_consent(txn_signer, batch_signer, consumer_pkey):
    academic_pkey = txn_signer.get_public_key().as_hex()
    consent_hex = \
        helper.make_consent_address(dest_pkey=academic_pkey, src_pkey=consumer_pkey)
    consent_vice_versa_hex = \
        helper.make_consent_address(dest_pkey=consumer_pkey, src_pkey=academic_pkey)

    access = ActionOnAccess(
        dest_pkey=academic_pkey,
        src_pkey=consumer_pkey,
        action_type=ActionOnAccess.REQUESTED
    )

    payload = ConsentPayload(
        payload_type=ConsentPayload.PAYLOAD_REQUEST_CONSENT,
        request_consent=access)

    return _make_transaction(
        payload=payload,
        inputs=[consent_hex, consent_vice_versa_hex],
        outputs=[consent_hex, consent_vice_versa_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def approve_academic_request(txn_signer, batch_signer, academic_pkey):
    consumer_pkey = txn_signer.get_public_key().as_hex()
    consent_hex = \
        helper.make_consent_address(dest_pkey=academic_pkey, src_pkey=consumer_pkey)
    consent_vice_versa_hex = \
        helper.make_consent_address(dest_pkey=consumer_pkey, src_pkey=academic_pkey)

    access = ActionOnAccess(
        dest_pkey=academic_pkey,
        src_pkey=consumer_pkey,
        action_type=ActionOnAccess.APPROVED
    )

    payload = ConsentPayload(
        payload_type=ConsentPayload.PAYLOAD_APPROVE_CONSENT,
        approve_consent=access)

    return _make_transaction(
        payload=payload,
        inputs=[consent_hex, consent_vice_versa_hex],
        outputs=[consent_hex, consent_vice_versa_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def decline_academic_request(txn_signer, batch_signer, academic_pkey):
    consumer_pkey = txn_signer.get_public_key().as_hex()
    consent_hex = \
        helper.make_consent_address(dest_pkey=academic_pkey, src_pkey=consumer_pkey)
    consent_vice_versa_hex = \
        helper.make_consent_address(dest_pkey=consumer_pkey, src_pkey=academic_pkey)

    access = ActionOnAccess(
        dest_pkey=academic_pkey,
        src_pkey=consumer_pkey,
        action_type=ActionOnAccess.DECLINED
    )

    payload = ConsentPayload(
        payload_type=ConsentPayload.PAYLOAD_DECLINE_CONSENT,
        decline_consent=access)

    return _make_transaction(
        payload=payload,
        inputs=[consent_hex, consent_vice_versa_hex],
        outputs=[consent_hex, consent_vice_versa_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def revoke_academic_request(txn_signer, batch_signer, academic_pkey):
    consumer_pkey = txn_signer.get_public_key().as_hex()
    consent_hex = \
        helper.make_consent_address(dest_pkey=academic_pkey, src_pkey=consumer_pkey)
    consent_vice_versa_hex = \
        helper.make_consent_address(dest_pkey=consumer_pkey, src_pkey=academic_pkey)

    access = ActionOnAccess(
        dest_pkey=academic_pkey,
        src_pkey=consumer_pkey
    )

    payload = ConsentPayload(
        payload_type=ConsentPayload.PAYLOAD_REVOKE_CONSENT,
        revoke_consent=access)

    return _make_transaction(
        payload=payload,
        inputs=[consent_hex, consent_vice_versa_hex],
        outputs=[consent_hex, consent_vice_versa_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)
