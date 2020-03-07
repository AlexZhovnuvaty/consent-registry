from data_processor.data_common import helper
from data_processor.data_common.protobuf.data_payload_pb2 import Consumer, Academic, ConsumerData
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class ConsumerDataState(object):
    TIMEOUT = 3

    def __init__(self, context):
        """Constructor.
        Args:
            context (sawtooth_sdk.processor.context.Context): Access to
                validator state from within the transaction processor.
        """

        self._context = context

    def create_consumer(self, consumer):
        cn = self._load_consumer(public_key=consumer.public_key)

        if cn is None:
            self._store_consumer(consumer)

    def create_academic(self, academic):
        ac = self._load_academic(public_key=academic.public_key)

        if ac is None:
            self._store_academic(academic)

    def add_data(self, signer, data):
        data_obj = self._load_data(data.id)
        if data_obj is None:
            self._store_data(signer=signer, data=data)

    def get_consumer(self, public_key):
        consumer = self._load_consumer(public_key=public_key)
        return consumer

    def get_academic(self, public_key):
        academic = self._load_academic(public_key=public_key)
        return academic

    def get_data(self, data_id):
        data = self._load_data(data_id=data_id)
        return data

    def _load_consumer(self, public_key):
        consumer = None
        consumer_hex = helper.make_consumer_address(public_key)
        state_entries = self._context.get_state(
            [consumer_hex],
            timeout=self.TIMEOUT)
        if state_entries:
            consumer = Consumer()
            consumer.ParseFromString(state_entries[0].data)
        return consumer

    def _load_academic(self, public_key):
        academic = None
        academic_hex = helper.make_academic_address(public_key)
        state_entries = self._context.get_state(
            [academic_hex],
            timeout=self.TIMEOUT)
        if state_entries:
            academic = Academic()
            academic.ParseFromString(state_entries[0].data)
        return academic

    def _load_data(self, data_id):
        data = None
        data_hex = helper.make_data_address(data_id)
        state_entries = self._context.get_state(
            [data_hex],
            timeout=self.TIMEOUT)
        if state_entries:
            data = ConsumerData()
            data.ParseFromString(state_entries[0].data)
        return data

    def _store_consumer(self, consumer):
        address = helper.make_consumer_address(consumer.public_key)

        state_data = consumer.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)

    def _store_academic(self, academic):
        address = helper.make_academic_address(academic.public_key)

        state_data = academic.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)

    def _store_data(self, signer, data):
        data_address = helper.make_data_address(data.id)
        data_consumer_relation_address = helper.make_data_consumer__relation_address(data.id,
                                                                                     data.client_pkey)
        consumer_data_relation_address = helper.make_consumer_data__relation_address(data.client_pkey,
                                                                                     data.id)

        consumer_data = data.SerializeToString()
        states = {
            data_address: consumer_data,

            data_consumer_relation_address: str.encode(signer),
            consumer_data_relation_address: str.encode(data.id)

        }
        LOGGER.debug("_store_data: " + str(states))
        self._context.set_state(
            states,
            timeout=self.TIMEOUT)
