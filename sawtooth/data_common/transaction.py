import hashlib
import random
import logging
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader, Batch
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction, TransactionHeader
from . import helper as helper
from .protobuf.data_payload_pb2 import Academic, Consumer, DataPayload, ConsumerData

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


def create_academic(txn_signer, batch_signer, name):
    academic_pkey = txn_signer.get_public_key().as_hex()
    LOGGER.debug('academic_pkey: ' + str(academic_pkey))
    academic_hex = helper.make_academic_address(academic_pkey=academic_pkey)
    LOGGER.debug('academic_hex: ' + str(academic_hex))
    academic = Academic(
        public_key=academic_pkey,
        name=name)

    payload = DataPayload(
        payload_type=DataPayload.PAYLOAD_CREATE_ACADEMIC,
        create_academic=academic)

    LOGGER.debug('payload: ' + str(payload))

    return _make_transaction(
        payload=payload,
        inputs=[academic_hex],
        outputs=[academic_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def create_consumer(txn_signer, batch_signer, name):
    consumer_pkey = txn_signer.get_public_key().as_hex()
    LOGGER.debug('consumer_pkey: ' + str(consumer_pkey))
    inputs = outputs = helper.make_consumer_address(consumer_pkey=consumer_pkey)
    LOGGER.debug('inputs: ' + str(inputs))
    consumer = Consumer(
        public_key=consumer_pkey,
        name=name)

    payload = DataPayload(
        payload_type=DataPayload.PAYLOAD_CREATE_CONSUMER,
        create_consumer=consumer)

    return _make_transaction(
        payload=payload,
        inputs=[inputs],
        outputs=[outputs],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def add_data(txn_signer, batch_signer, uid, field1, field2, field3):
    consumer_pkey = txn_signer.get_public_key().as_hex()
    data_hex = helper.make_data_address(data_id=uid)
    data_consumer_rel_hex = helper.make_data_consumer__relation_address(uid, consumer_pkey)
    consumer_data_rel_hex = helper.make_consumer_data__relation_address(consumer_pkey, uid)
    current_times_str = helper.get_current_timestamp()

    data = ConsumerData(
        id=uid,
        client_pkey=consumer_pkey,
        field1=field1,
        field2=field2,
        field3=field3,
        event_time=str(current_times_str)
    )

    LOGGER.debug('data: ' + str(data))

    payload = DataPayload(
        payload_type=DataPayload.PAYLOAD_ADD_DATA,
        add_data=data)

    return _make_transaction(
        payload=payload,
        inputs=[data_hex, data_consumer_rel_hex, consumer_data_rel_hex],
        outputs=[data_hex, data_consumer_rel_hex, consumer_data_rel_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)
