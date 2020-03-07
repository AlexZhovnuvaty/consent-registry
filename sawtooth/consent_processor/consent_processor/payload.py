from consent_processor.consent_common.protobuf import consent_pb2


class ConsentPayload(object):

    def __init__(self, payload):
        self._transaction = consent_pb2.ConsentPayload()
        self._transaction.ParseFromString(payload)

    def request_consent(self):
        return self._transaction.request_consent

    def is_request_consent(self):
        return self._transaction.payload_type == \
               consent_pb2.ConsentPayload.PAYLOAD_REQUEST_CONSENT

    def decline_consent(self):
        return self._transaction.decline_consent

    def is_decline_consent(self):
        return self._transaction.payload_type == \
               consent_pb2.ConsentPayload.PAYLOAD_DECLINE_CONSENT

    def approve_consent(self):
        return self._transaction.approve_consent

    def is_approve_consent(self):
        return self._transaction.payload_type == \
               consent_pb2.ConsentPayload.PAYLOAD_APPROVE_CONSENT

    def revoke_consent(self):
        return self._transaction.revoke_consent

    def is_revoke_consent(self):
        return self._transaction.payload_type == \
               consent_pb2.ConsentPayload.PAYLOAD_REVOKE_CONSENT

    def transaction_type(self):
        return self._transaction.payload_type

    def is_create_client(self):
        return self._transaction.payload_type == consent_pb2.ConsentPayload.PAYLOAD_ADD_CLIENT

    def create_client(self):
        return self._transaction.create_client
