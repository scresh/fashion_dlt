import json
import hashlib
import socket
from urllib import request
from urllib import error
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.exceptions import InvalidTransaction

FASHION_NAMESPACE = hashlib.sha512('fashion'.encode("utf-8")).hexdigest()[0:6]

OWNER_LENGTH = 66
SCANTRUST_ID_LENGTH = 70
ITEM_NAME_MAX_LENGTH = 64
ITEM_INFO_MAX_LENGTH = 160
ITEM_COLOR_MAX_LENGTH = 8
ITEM_SIZE_MAX_LENGTH = 4
ITEM_IMG_MAX_LENGTH = 128
ITEM_IMG_HASH_LENGTH = 32
ITEM_IMG_TIMEOUT = 1.0


def remove_control_chars(text):
    return ''.join([*map(lambda x: [x, ''][ord(x) < ord(' ')], text)])


def get_serialized_block(deserialized_block):
    """Takes a dict of FashionItemState objects and serializes them into bytes.
    Args:
        deserialized_block (dict): ScanTrust ID of item (str) keys, FashionItemState values.
    Returns:
        (string): The UTF-8 encoded string stored in state.
    """
    decoded_payloads = []
    for _, item_state in deserialized_block.items():
        decoded_payloads.append(item_state.payload.decode())

    return json.dumps(decoded_payloads).encode()


def get_deserialized_block(serialized_block):
    """Take bytes stored in state and deserialize them into FashionItemState objects.
    Args:
        serialized_block (bytes): The UTF-8 encoded string stored in state.
    Returns:
        (dict): ScanTrust ID of item (str) keys, FashionItemState values.
    """
    deserialized_block = {}
    try:
        for decoded_payload in json.loads(serialized_block.decode()):
            item = FashionItemState.from_payload(decoded_payload.encode())
            deserialized_block[item.scantrust_id] = item
    except ValueError:
        raise InternalError("Failed to deserialize item data")

    return deserialized_block


class FashionItemState:
    def __init__(self, scantrust_id, owner, item_name, item_info, item_color, item_size, item_img, item_img_md5):

        scantrust_id = remove_control_chars(scantrust_id)
        owner = remove_control_chars(owner)
        item_name = remove_control_chars(item_name)
        item_info = remove_control_chars(item_info)
        item_color = remove_control_chars(item_color)
        item_size = remove_control_chars(item_size)
        item_img = remove_control_chars(item_img)
        item_img_md5 = remove_control_chars(item_img_md5)

        if not scantrust_id:
            raise InvalidTransaction('Item ScanTrust ID is required')

        if len(scantrust_id) != SCANTRUST_ID_LENGTH:
            raise InvalidTransaction('Item ScanTrust ID incorrect length')

        try:
            int(scantrust_id, 16)
        except ValueError:
            raise InvalidTransaction('Item ScanTrust ID should contain only hexadecimal characters')

        if not owner:
            raise InvalidTransaction('Item owner address is required')

        if len(owner) != OWNER_LENGTH:
            raise InvalidTransaction('Item owner address incorrect length')

        try:
            int(owner, 16)
        except ValueError:
            raise InvalidTransaction('Owner address should contain only hexadecimal characters')

        if len(item_name) > ITEM_NAME_MAX_LENGTH:
            raise InvalidTransaction('Item name too long')

        if len(item_info) > ITEM_INFO_MAX_LENGTH:
            raise InvalidTransaction('Item info too long')

        if len(item_color) > ITEM_COLOR_MAX_LENGTH:
            raise InvalidTransaction('Item color too long')

        if len(item_size) > ITEM_SIZE_MAX_LENGTH:
            raise InvalidTransaction('Item size too long')

        if len(item_img) > ITEM_IMG_MAX_LENGTH:
            raise InvalidTransaction('Item image url too long')

        if len(item_img_md5) != 0:
            if len(item_img_md5) != ITEM_IMG_HASH_LENGTH:
                raise InvalidTransaction(f'Image MD5 incorrect length')

            try:
                int(item_img_md5, 16)
            except ValueError:
                raise InvalidTransaction('Image MD5 should contain only hexadecimal characters')

            try:
                img = request.urlopen(item_img, timeout=ITEM_IMG_TIMEOUT).read()
                if hashlib.md5(img).hexdigest() != item_img_md5:
                    raise InvalidTransaction(f'Incorrect image MD5 hash')
            except (error.URLError, socket.timeout):
                raise InvalidTransaction('Incorrect image URL')

        self._scantrust_id = scantrust_id
        self._owner = owner
        self._item_name = item_name
        self._item_info = item_info
        self._item_color = item_color
        self._item_size = item_size
        self._item_img = item_img
        self._item_img_md5 = item_img_md5

    @property
    def scantrust_id(self):
        return self._scantrust_id

    @property
    def owner(self):
        return self._owner

    @property
    def item_name(self):
        return self._item_name

    @property
    def item_info(self):
        return self._item_info

    @property
    def item_color(self):
        return self._item_color

    @property
    def item_size(self):
        return self._item_size

    @property
    def item_img(self):
        return self._item_img

    @property
    def item_img_md5(self):
        return self._item_img_md5

    @property
    def address(self):
        return FASHION_NAMESPACE + hashlib.sha512(self.scantrust_id.encode('utf-8')).hexdigest()[:64]

    @property
    def payload(self):
        return json.dumps(
            (self.scantrust_id, self.owner, self.item_name, self.item_info,
             self.item_color, self.item_size, self.item_img, self.item_img_md5)
        ).encode()

    @staticmethod
    def from_payload(payload):
        try:
            scantrust_id, owner, item_name, item_info, item_color, item_size, item_img, item_img_md5 = json.loads(
                payload.decode())
        except (ValueError, json.JSONDecodeError):
            raise InvalidTransaction('Incorrect payload structure')

        return FashionItemState(scantrust_id, owner, item_name, item_info, item_color, item_size, item_img,
                                item_img_md5)


class FashionDLT:
    TIMEOUT = 3

    def __init__(self, context):
        self._context = context
        self._address_cache = {}

    def add_item_state(self, item_state):
        item_address = item_state.address

        # Get current item block
        item_block = self._get_item_block(item_address)

        # Update item block
        item_block[item_state.scantrust_id] = item_state
        self._store_item(item_address, item_block)

    def get_item_payload(self, item):
        address = item.address
        scantrust_id = item.scantrust_id
        if self._get_item_block(address).get(scantrust_id):
            return self._get_item_block(address).get(scantrust_id).payload
        else:
            return None

    def _store_item(self, item_address, item_block):
        state_data = get_serialized_block(item_block)

        self._address_cache[item_address] = state_data

        self._context.set_state(
            {item_address: state_data},
            timeout=self.TIMEOUT)

    def _get_item_block(self, item_address):
        if item_address in self._address_cache:
            if self._address_cache[item_address]:
                serialized_block = self._address_cache[item_address]
                block = get_deserialized_block(serialized_block)
            else:
                block = {}

        else:
            state_entries = self._context.get_state([item_address], timeout=self.TIMEOUT)

            if state_entries:
                self._address_cache[item_address] = state_entries[0].data
                block = get_deserialized_block(state_entries[0].data)
            else:
                self._address_cache[item_address] = None
                block = {}

        return block
