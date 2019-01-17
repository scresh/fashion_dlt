from django.http import JsonResponse
from django.views import View
import requests
import json
import hashlib
import random
from secp256k1 import PrivateKey
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch

FASHION_NAMESPACE = hashlib.sha512('fashion'.encode("utf-8")).hexdigest()[0:6]


def sign(message, private_key_hex):
    private_key = PrivateKey(bytes(bytearray.fromhex(private_key_hex)), raw=True)
    signature = private_key.ecdsa_sign(message)
    signature = private_key.ecdsa_serialize_compact(signature).hex()

    return signature.hex()


def sha512(data):
    return hashlib.sha512(data).hexdigest()


def get_address(scantrust_id):
    return FASHION_NAMESPACE + hashlib.sha512(scantrust_id.encode('utf-8')).hexdigest()[:64]


def create_batch_list(transactions, private_key_hex, public_key_hex):
    transaction_signatures = [t.header_signature for t in transactions]

    header = BatchHeader(
        signer_public_key=public_key_hex,
        transaction_ids=transaction_signatures
    ).SerializeToString()

    signature = sign(header, private_key_hex)

    batch = Batch(
        header=header,
        transactions=transactions,
        header_signature=signature)
    return BatchList(batches=[batch])


class GeneratorView(View):
    def post(self, request):
        url = 'http://127.0.0.1:4001'

        scantrust_id = request.POST['scantrust_id']
        owner = request.POST['owner']
        item_name = request.POST['item_name']
        item_info = request.POST['item_info']
        item_color = request.POST['item_color']
        item_size = request.POST['item_size']
        item_img = request.POST['item_img']
        item_img_md5 = request.POST['item_img_md5']

        public_key_hex = request.POST['public_key']
        private_key_hex = request.POST['private_key']

        payload = json.dumps(
            (scantrust_id, owner, item_name, item_info, item_color, item_size, item_img, item_img_md5)
        ).encode()

        address = get_address(scantrust_id)

        header = TransactionHeader(
            signer_public_key=public_key_hex,
            family_name="fashion",
            family_version="1.0",
            inputs=[address],
            outputs=[address],
            dependencies=[],
            payload_sha512=sha512(payload),
            batcher_public_key=public_key_hex,
            nonce=hex(random.randint(0, 2 ** 64))
        ).SerializeToString()

        signature = sign(header, private_key_hex)

        transaction = Transaction(
            header=header,
            payload=payload,
            header_signature=signature
        )

        batch_list = create_batch_list([transaction], private_key_hex, public_key_hex)
        data = batch_list.SerializeToString()

        headers = {'Content-Type': 'application/octet-stream'}

        try:
            result = requests.post(url, headers=headers, data=data)
            response = result.text
        except requests.ConnectionError:
            response = 'Connection fail'
        except BaseException:
            response = 'Incorrect data'

        return JsonResponse({'response': response})
