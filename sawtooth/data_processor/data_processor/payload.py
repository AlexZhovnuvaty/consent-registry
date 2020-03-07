from data_processor.data_common.protobuf.data_payload_pb2 import DataPayload


class ConsumerDataPayload(object):

    def __init__(self, payload):
        self._transaction = DataPayload()
        self._transaction.ParseFromString(payload)

    def create_consumer(self):
        return self._transaction.create_consumer

    def create_academic(self):
        return self._transaction.create_academic

    def add_data(self):
        return self._transaction.add_data

    def is_create_consumer(self):
        return self._transaction.payload_type == DataPayload.PAYLOAD_CREATE_CONSUMER

    def is_create_academic(self):
        return self._transaction.payload_type == DataPayload.PAYLOAD_CREATE_ACADEMIC

    def is_add_data(self):
        return self._transaction.payload_type == DataPayload.PAYLOAD_ADD_DATA

    def transaction_type(self):
        return self._transaction.payload_type
