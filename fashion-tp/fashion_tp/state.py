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


def hex_verify(hex_str, name, length):
    if not hex_str:
        raise InvalidTransaction(f'Item {name} is required')

    if not isinstance(hex_str, str):
        raise InvalidTransaction(f'Item {name} must be string')

    if not all([*map(lambda c: (ord('0') <= ord(c) <= ord('9')) or (ord('a') <= ord(c) <= ord('f')), hex_str)]):
        raise InvalidTransaction(f'Item {name} should only consist of lowercase hexadecimal characters')

    if not (len(hex_str) == length):
        raise InvalidTransaction(f'Item {name} length should be {length} characters')


def img_verify(url, md5):
    if not url:
        raise InvalidTransaction(f'Item image url is required')

    if not md5:
        raise InvalidTransaction(f'Item image MD5 is required')

    if not isinstance(url, str):
        raise InvalidTransaction(f'Item image url must be string')

    if not (len(url) <= ITEM_IMG_MAX_LENGTH):
        raise InvalidTransaction(f'Item image url length can not be grater than {ITEM_IMG_MAX_LENGTH} characters')

    try:
        img = request.urlopen(url, timeout=ITEM_IMG_TIMEOUT).read()
        if hashlib.md5(img).hexdigest() != md5:
            raise InvalidTransaction(f'Incorrect image MD5 hash')
    except (error.URLError, socket.timeout, ValueError):
        raise InvalidTransaction('Incorrect image URL')


def text_verify(text, name, max_length):
    if not text:
        raise InvalidTransaction(f'Item {name} is required')

    if not isinstance(name, str):
        raise InvalidTransaction(f'Item {name} must be string')

    if not text.isprintable():
        raise InvalidTransaction(f'Item {name} should only consist of printable characters')

    if not (len(text) <= max_length):
        raise InvalidTransaction(f'Item {name} length can not be grater than {max_length} characters')


def serialize_batch(deserialized_batch):
    """Takes a dictionary of FashionItemState objects and serializes it into bytes.
    Args:
        deserialized_batch (dict): ScanTrust ID of item (str) keys, FashionItemState values
    Returns:
        (bytes): The encoded string, witch is JSON representation of array of decoded payloads
    """
    decoded_payloads = []
    for _, item_state in deserialized_batch.items():
        decoded_payloads.append(item_state.payload.decode())

    return json.dumps(decoded_payloads).encode()


def deserialize_batch(serialized_batch):
    """Take bytes and deserialize them into dictionary of FashionItemState objects.
    Args:
        serialized_batch (bytes): The encoded string, witch is JSON representation of array of decoded payloads
    Returns:
        (dict): ScanTrust ID of item (str) keys, FashionItemState values
    """
    deserialized_batch = {}
    try:
        for decoded_payload in json.loads(serialized_batch.decode()):
            item = FashionItemState.from_payload(decoded_payload.encode())
            deserialized_batch[item.scantrust_id] = item
    except ValueError:
        raise InternalError("Failed to deserialize item data")

    return deserialized_batch


class FashionItemState:
    def __init__(self, scantrust_id, owner, item_name, item_info, item_color, item_size, item_img, item_img_md5):

        hex_verify(scantrust_id, 'ScanTrust ID', SCANTRUST_ID_LENGTH)
        hex_verify(owner, 'owner', OWNER_LENGTH)
        text_verify(item_name, 'name', ITEM_NAME_MAX_LENGTH)
        text_verify(item_info, 'info', ITEM_INFO_MAX_LENGTH)
        text_verify(item_color, 'color', ITEM_COLOR_MAX_LENGTH)
        text_verify(item_size, 'size', ITEM_SIZE_MAX_LENGTH)
        img_verify(item_img, item_img_md5)

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
        item_batch = self._get_item_last_batch(item_address)

        # Update item block
        item_batch[item_state.scantrust_id] = item_state
        self._store_item(item_address, item_batch)

    def get_item_last_payload(self, item):
        address = item.address
        scantrust_id = item.scantrust_id
        if self._get_item_last_batch(address).get(scantrust_id):
            return self._get_item_last_batch(address).get(scantrust_id).payload
        else:
            return None

    def get_item_first_payload(self, item):
        address = item.address
        scantrust_id = item.scantrust_id
        if self._get_item_first_batch(address).get(scantrust_id):
            return self._get_item_last_batch(address).get(scantrust_id).payload
        else:
            return None

    def _store_item(self, item_address, item_batch):
        state_data = serialize_batch(item_batch)

        if self._address_cache.get(item_address):
            self._address_cache[item_address].insert(0, state_data)
        else:
            self._address_cache[item_address] = [state_data, ]

        self._context.set_state(
            {item_address: state_data},
            timeout=self.TIMEOUT)

    def _get_item_all_batches(self, item_address):
        if self._address_cache.get(item_address):
            serialized_batches = self._address_cache[item_address]
            deserialized_batches = [*map(lambda x: deserialize_batch(x), serialized_batches)]

        else:
            state_entries = self._context.get_state([item_address], timeout=self.TIMEOUT)

            if state_entries:
                self._address_cache[item_address] = [*map(lambda x: x.data, state_entries)]
                serialized_batches = self._address_cache[item_address]
                deserialized_batches = [*map(lambda x: deserialize_batch(x), serialized_batches)]
            else:
                self._address_cache[item_address] = []
                deserialized_batches = []

        return deserialized_batches

    def _get_item_last_batch(self, item_address):
        try:
            return self._get_item_all_batches(item_address)[0]
        except IndexError:
            return {}

    def _get_item_first_batch(self, item_address):
        try:
            return self._get_item_all_batches(item_address)[-1]
        except IndexError:
            return {}
