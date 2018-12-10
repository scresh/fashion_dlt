from sawtooth_sdk.processor.exceptions import InvalidTransaction

OWNER_ADDRESS_LENGTH = 70
SCANTRUST_ID_LENGTH = 256


class FashionPayload:
    def __init__(self, payload):
        try:
            # The payload is csv utf-8 encoded string
            scantrust_id, new_owner = payload.decode().split(",")
        except ValueError:
            raise InvalidTransaction("Invalid payload serialization")

        if not scantrust_id:
            raise InvalidTransaction('ScanTrust ID is required')

        if len(scantrust_id) != SCANTRUST_ID_LENGTH:
            raise InvalidTransaction(f'ScanTrust ID should consist of {SCANTRUST_ID_LENGTH} hex characters')

        try:
            int(scantrust_id, 16)
        except ValueError:
            raise InvalidTransaction('ScanTrust ID should contain only hexadecimal characters')

        if not new_owner:
            raise InvalidTransaction('New owner is required')

        if len(scantrust_id) != OWNER_ADDRESS_LENGTH:
            raise InvalidTransaction(f'Owner address should consist of {OWNER_ADDRESS_LENGTH} hex characters')

        try:
            int(scantrust_id, 16)
        except ValueError:
            raise InvalidTransaction('Owner address should contain only hexadecimal characters')

        self._scantrust_id = scantrust_id
        self._new_owner = new_owner

    @staticmethod
    def from_bytes(payload):
        return FashionPayload(payload=payload)

    @property
    def scantrust_id(self):
        return self._scantrust_id

    @property
    def new_owner(self):
        return self._new_owner

