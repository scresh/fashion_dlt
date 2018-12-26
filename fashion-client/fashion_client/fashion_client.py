import hashlib
import base64
from base64 import b64encode
import time
import random
import requests
import yaml
import json

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import ParseError
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch

from .fashion_exceptions import FashionException

FASHION_NAMESPACE = hashlib.sha512('fashion'.encode("utf-8")).hexdigest()[0:6]


def _sha512(data):
    return hashlib.sha512(data).hexdigest()


class FashionClient:
    def __init__(self, base_url, keyfile=None):

        self._base_url = base_url

        if keyfile is None:
            self._signer = None
            return

        try:
            with open(keyfile) as fd:
                private_key_str = fd.read().strip()
        except OSError as err:
            raise FashionException(
                'Failed to read private key {}: {}'.format(
                    keyfile, str(err)))

        try:
            private_key = Secp256k1PrivateKey.from_hex(private_key_str)
        except ParseError as e:
            raise FashionException(
                'Unable to load private key: {}'.format(str(e)))

        self._signer = CryptoFactory(create_context('secp256k1')) \
            .new_signer(private_key)

    def create_item(self, scantrust_id, item_name, item_info, item_color, item_size, item_img, item_img_md5,
                    wait=None, auth_user=None, auth_password=None):
        return self._send_fashion_txn(
            scantrust_id,
            self._signer.get_public_key().as_hex(),
            item_name, item_info, item_color, item_size, item_img, item_img_md5,
            wait=wait,
            auth_user=auth_user,
            auth_password=auth_password)

    def send_item(self, scantrust_id, recipient, item_name, item_info, item_color, item_size, item_img, item_img_md5,
                  wait=None, auth_user=None, auth_password=None):
        return self._send_fashion_txn(
            scantrust_id,
            recipient,
            item_name, item_info, item_color, item_size, item_img, item_img_md5,
            wait=wait,
            auth_user=auth_user,
            auth_password=auth_password)

    def list_transactions(self, scantrust_id, user_address, auth_user=None, auth_password=None):
        result = self._send_request(
            "transactions",
            auth_user=auth_user,
            auth_password=auth_password)

        try:
            encoded_entries = yaml.safe_load(result)['data']
            transaction_list = []
            if encoded_entries:
                for entry in encoded_entries:
                    if entry['header']['family_name'] != 'fashion':
                        continue
                    sender = entry['header']['signer_public_key']
                    payload = base64.b64decode(entry['payload'])
                    item_dict = self.from_payload(payload)
                    receiver = item_dict['owner']
                    item_id = item_dict['scantrust_id']

                    if scantrust_id:
                        if scantrust_id == item_id:
                            transaction_list.append(item_dict)

                    elif user_address:
                        if (user_address == sender) or (user_address == receiver):
                            transaction_list.append(item_dict)
                    else:
                        transaction_list.append(item_dict)

            return transaction_list

        except BaseException:
            return []

    def show(self, scantrust_id, auth_user=None, auth_password=None):
        address = self._get_address(scantrust_id)

        result = self._send_request(
            "state/{}".format(address),
            name=scantrust_id,
            auth_user=auth_user,
            auth_password=auth_password)
        try:
            return base64.b64decode(yaml.safe_load(result)["data"])

        except BaseException:
            return None

    def _get_status(self, batch_id, wait, auth_user=None, auth_password=None):
        try:
            result = self._send_request(
                'batch_statuses?id={}&wait={}'.format(batch_id, wait),
                auth_user=auth_user,
                auth_password=auth_password)
            return yaml.safe_load(result)['data'][0]['status']
        except BaseException as err:
            raise FashionException(err)

    @staticmethod
    def _get_prefix():
        return _sha512('fashion'.encode('utf-8'))[0:6]

    @staticmethod
    def _get_address(scantrust_id):
        return FASHION_NAMESPACE + hashlib.sha512(scantrust_id.encode('utf-8')).hexdigest()[:64]

    @staticmethod
    def from_payload(payload):
        scantrust_id, owner, item_name, item_info, item_color, item_size, item_img, item_img_md5 = \
            json.loads(payload.decode())

        return {
            'scantrust_id': scantrust_id,
            'owner': owner,
            'item_name': item_name,
            'item_info': item_info,
            'item_color': item_color,
            'item_size': item_size,
            'item_img': item_img,
            'item_img_md5': item_img_md5,
        }

    def _send_request(self,
                      suffix,
                      data=None,
                      content_type=None,
                      name=None,
                      auth_user=None,
                      auth_password=None):
        if self._base_url.startswith("http://"):
            url = "{}/{}".format(self._base_url, suffix)
        else:
            url = "http://{}/{}".format(self._base_url, suffix)

        headers = {}
        if auth_user is not None:
            auth_string = "{}:{}".format(auth_user, auth_password)
            b64_string = b64encode(auth_string)
            auth_header = 'Basic {}'.format(b64_string)
            headers['Authorization'] = auth_header

        if content_type is not None:
            headers['Content-Type'] = content_type

        try:
            if data is not None:
                result = requests.post(url, headers=headers, data=data)
            else:
                result = requests.get(url, headers=headers)

            if result.status_code == 404:
                raise FashionException("No such item: {}".format(name))

            elif not result.ok:
                raise FashionException("Error {}: {}".format(
                    result.status_code, result.reason))

        except requests.ConnectionError as err:
            raise FashionException(
                'Failed to connect to {}: {}'.format(url, str(err)))

        except BaseException as err:
            raise FashionException(err)

        return result.text

    def _send_fashion_txn(self,
                          scantrust_id, owner, item_name, item_info, item_color, item_size, item_img, item_img_md5,
                          wait=None,
                          auth_user=None,
                          auth_password=None):
        # Serialization is just a delimited utf-8 encoded string
        payload = json.dumps(
            (scantrust_id, owner, item_name, item_info, item_color, item_size, item_img, item_img_md5)
        ).encode()
        # Construct the address
        address = self._get_address(scantrust_id)

        header = TransactionHeader(
            signer_public_key=self._signer.get_public_key().as_hex(),
            family_name="fashion",
            family_version="1.0",
            inputs=[address],
            outputs=[address],
            dependencies=[],
            payload_sha512=_sha512(payload),
            batcher_public_key=self._signer.get_public_key().as_hex(),
            nonce=hex(random.randint(0, 2 ** 64))
        ).SerializeToString()

        signature = self._signer.sign(header)

        transaction = Transaction(
            header=header,
            payload=payload,
            header_signature=signature
        )

        batch_list = self._create_batch_list([transaction])
        batch_id = batch_list.batches[0].header_signature

        if wait and wait > 0:
            wait_time = 0
            start_time = time.time()
            response = self._send_request(
                "batches", batch_list.SerializeToString(),
                'application/octet-stream',
                auth_user=auth_user,
                auth_password=auth_password)
            while wait_time < wait:
                status = self._get_status(
                    batch_id,
                    wait - int(wait_time),
                    auth_user=auth_user,
                    auth_password=auth_password)
                wait_time = time.time() - start_time

                if status != 'PENDING':
                    return response

            return response

        return self._send_request(
            "batches", batch_list.SerializeToString(),
            'application/octet-stream',
            auth_user=auth_user,
            auth_password=auth_password)

    def _create_batch_list(self, transactions):
        transaction_signatures = [t.header_signature for t in transactions]

        header = BatchHeader(
            signer_public_key=self._signer.get_public_key().as_hex(),
            transaction_ids=transaction_signatures
        ).SerializeToString()

        signature = self._signer.sign(header)

        batch = Batch(
            header=header,
            transactions=transactions,
            header_signature=signature)
        return BatchList(batches=[batch])
