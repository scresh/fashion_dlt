from sawtooth_sdk.processor.exceptions import InvalidTransaction

OWNER_ADDRESS_LENGTH = 70
SCANTRUST_ID_LENGTH = 256

# TODO: Item details validation
# ITEM_NAME_MAX_LENGTH = 128
# ITEM_COLOR_MAX_LENGTH = 16
# ITEM_SIZE_MAX_LENGTH = 16
# ITEM_DESC_MAX_LENGTH = 256
# ITEM_URL_MAX_LENGTH = 128
# ITEM_IMG_URL_MAX_LENGTH = 128
# ITEM_IMG_HASH_LENGTH = 32


class FashionPayload:
    def __init__(self, payload):
        try:
            # The payload is utf-8 encoded string
            scantrust_id, owner_address, item_details = payload.decode().split("\t")
            # item_name, item_color, item_size, item_description, ... = item_details.split('|')
        except ValueError:
            raise InvalidTransaction("Invalid payload serialization")

        # ScanTrust ID validation
        if not scantrust_id:
            raise InvalidTransaction('ScanTrust ID is required')

        if len(scantrust_id) != SCANTRUST_ID_LENGTH:
            raise InvalidTransaction(f'ScanTrust ID should consist of {SCANTRUST_ID_LENGTH} hex characters')

        try:
            int(scantrust_id, 16)
        except ValueError:
            raise InvalidTransaction('ScanTrust ID should contain only hexadecimal characters')

        # Owner address validation
        if not owner_address:
            raise InvalidTransaction('Owner address is required')

        if len(owner_address) != OWNER_ADDRESS_LENGTH:
            raise InvalidTransaction(f'Owner address should consist of {OWNER_ADDRESS_LENGTH} hex characters')

        try:
            int(owner_address, 16)
        except ValueError:
            raise InvalidTransaction('Owner address should contain only hexadecimal characters')

        self._scantrust_id = scantrust_id
        self._owner = owner_address
        self._item_details = item_details

    @staticmethod
    def from_bytes(payload):
        return FashionPayload(payload=payload)

    @property
    def scantrust_id(self):
        return self._scantrust_id

    @property
    def new_owner(self):
        return self._owner

