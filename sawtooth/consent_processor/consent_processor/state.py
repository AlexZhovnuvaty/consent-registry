from consent_processor.consent_common import helper
from consent_processor.consent_common.protobuf import consent_pb2

import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class ConsentState(object):
    TIMEOUT = 3

    def __init__(self, context):
        """Constructor.
        Args:
            context (sawtooth_sdk.processor.context.Context): Access to
                validator state from within the transaction processor.
        """

        self._context = context

    def request_consent(self, dest_pkey, src_pkey):
        self._store_request_consent(dest_pkey, src_pkey)

    def approve_consent(self, dest_pkey, src_pkey):
        self._store_approve_consent(dest_pkey, src_pkey)

    def decline_consent(self, dest_pkey, src_pkey):
        self._store_decline_consent(dest_pkey, src_pkey)

    def revoke_consent(self, dest_pkey, src_pkey):
        self._revoke_consent(dest_pkey, src_pkey)

    # def has_signed_inform_consent(self, dest_pkey, src_pkey):
    #     return self._load_inform_consent(dest_pkey=dest_pkey, src_pkey=src_pkey)

    def _load_consent(self, dest_pkey, src_pkey):
        access_hex = [helper.make_consent_address(dest_pkey=dest_pkey, src_pkey=src_pkey)]
        state_entries = self._context.get_state(
            access_hex,
            timeout=self.TIMEOUT)
        if state_entries:
            access = consent_pb2.ActionOnAccess()
            access.ParseFromString(state_entries[0].data)
            return access
        return None

    def _store_request_consent(self, dest_pkey, src_pkey):
        consent_address = helper.make_consent_address(dest_pkey=dest_pkey, src_pkey=src_pkey)
        consent_address_vice_versa = helper.make_consent_address(dest_pkey=src_pkey, src_pkey=dest_pkey)

        consent = consent_pb2.ActionOnAccess()
        consent.dest_pkey = dest_pkey
        consent.src_pkey = src_pkey
        consent.action_type = consent_pb2.ActionOnAccess.REQUESTED

        state_data = consent.SerializeToString()
        self._context.set_state(
            {consent_address: state_data,
             consent_address_vice_versa: state_data},
            timeout=self.TIMEOUT)

    def _store_approve_consent(self, dest_pkey, src_pkey):
        consent_address = \
            helper.make_consent_address(dest_pkey=dest_pkey, src_pkey=src_pkey)
        consent_address_vice_versa = \
            helper.make_consent_address(dest_pkey=src_pkey, src_pkey=dest_pkey)

        consent = consent_pb2.ActionOnAccess()
        consent.dest_pkey = dest_pkey
        consent.src_pkey = src_pkey
        consent.action_type = consent_pb2.ActionOnAccess.APPROVED

        state_data = consent.SerializeToString()
        self._context.set_state(
            {consent_address: state_data,
             consent_address_vice_versa: state_data},
            timeout=self.TIMEOUT)

    def _store_decline_consent(self, dest_pkey, src_pkey):
        consent_address = \
            helper.make_consent_address(dest_pkey=dest_pkey, src_pkey=src_pkey)
        consent_address_vice_versa = \
            helper.make_consent_address(dest_pkey=src_pkey, src_pkey=dest_pkey)

        consent = consent_pb2.ActionOnAccess()
        consent.dest_pkey = dest_pkey
        consent.src_pkey = src_pkey
        consent.action_type = consent_pb2.ActionOnAccess.DECLINED

        state_data = consent.SerializeToString()
        self._context.set_state(
            {consent_address: state_data,
             consent_address_vice_versa: state_data},
            timeout=self.TIMEOUT)

    def _revoke_consent(self, dest_pkey, src_pkey):
        consent_address = \
            helper.make_consent_address(dest_pkey=dest_pkey, src_pkey=src_pkey)

        consent_address_vice_versa = \
            helper.make_consent_address(dest_pkey=src_pkey, src_pkey=dest_pkey)

        self._context.delete_state(
            [consent_address,
             consent_address_vice_versa],
            timeout=self.TIMEOUT)

    def create_client(self, client):
        address = helper.make_client_address(public_key=client.public_key)

        state_data = client.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)
