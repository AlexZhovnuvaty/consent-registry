import logging

from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.handler import TransactionHandler

import data_processor.data_common.helper as helper
from data_processor.payload import ConsumerDataPayload
from data_processor.state import ConsumerDataState

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class DataTransactionHandler(TransactionHandler):
    def __init__(self, namespace_prefix):
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
        return helper.TP_FAMILYNAME

    @property
    def family_versions(self):
        return [helper.TP_VERSION]

    @property
    def namespaces(self):
        return [self._namespace_prefix]

    def apply(self, transaction, context):
        try:

            _display("i'm inside handler _display")
            # print("i'm inside handler print")

            header = transaction.header
            signer = header.signer_public_key
            LOGGER.debug("signer_public_key: " + str(signer))
            LOGGER.debug("transaction payload: " + str(transaction.payload))
            payload = ConsumerDataPayload(payload=transaction.payload)

            state = ConsumerDataState(context)

            if payload.is_create_consumer():
                consumer = payload.create_consumer()

                cn = state.get_consumer(signer)
                if cn is not None:
                    raise InvalidTransaction(
                        'Invalid action: Consumer already exists: ' + consumer.name)

                state.create_consumer(consumer)

            elif payload.is_create_academic():
                academic = payload.create_academic()

                ac = state.get_academic(signer)
                if ac is not None:
                    raise InvalidTransaction(
                        'Invalid action: Academic already exists: ' + academic.name)

                state.create_academic(academic)

            elif payload.is_add_data():
                data = payload.add_data()
                state.add_data(signer, data)

            else:
                raise InvalidTransaction('Unhandled action: {}'.format(payload.transaction_type()))
        except Exception as e:
            # print("Error: {}".format(e))
            logging.exception(e)
            raise InvalidTransaction(repr(e))


def _display(msg):
    n = msg.count("\n")

    if n > 0:
        msg = msg.split("\n")
        length = max(len(line) for line in msg)
    else:
        length = len(msg)
        msg = [msg]

    # pylint: disable=logging-not-lazy
    LOGGER.debug("+" + (length + 2) * "-" + "+")
    for line in msg:
        LOGGER.debug("+ " + line.center(length) + " +")
    LOGGER.debug("+" + (length + 2) * "-" + "+")
