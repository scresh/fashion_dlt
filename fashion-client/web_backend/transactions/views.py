import base64

from django.http import JsonResponse
from django.views import View
import urllib.request
import json
import hashlib

FASHION_NAMESPACE = hashlib.sha512('fashion'.encode("utf-8")).hexdigest()[0:6]


def from_payload(payload, signer):
    scantrust_id, owner, item_name, item_info, item_color, item_size, item_img, item_img_md5 = \
        json.loads(payload)

    return {
        'scantrust_id': scantrust_id,
        'sender': signer,
        'receiver': owner,
        'item_name': item_name,
        'item_info': item_info,
        'item_color': item_color,
        'item_size': item_size,
        'item_img': item_img,
        'item_img_md5': item_img_md5,
    }


def get_address(scantrust_id):
    return FASHION_NAMESPACE + hashlib.sha512(scantrust_id.encode('utf-8')).hexdigest()[:64]


def get_json(url):
    try:
        with urllib.request.urlopen(url) as data:
            json_data = json.loads(data.read().decode())
            return json_data
    except:
        return {}


class TransactionsView(View):
    def get(self, request):
        scantrust_id = request.GET.get('scantrust_id')
        address = request.GET.get('address')
        # TODO: change url domain to rest-api-0
        transactions_url = 'http://127.0.0.1:4000/transactions'
        transactions = get_json(transactions_url).get('data')
        result = []

        for transaction in transactions:
            if transaction.get('header').get('family_name') != 'fashion':
                continue

            signer = transaction.get('header').get('signer_public_key')

            base64_payload = transaction.get('payload')
            payload = base64.b64decode(base64_payload)
            result.append(from_payload(payload, signer))

        if address:
            result = list(filter(lambda x: (x.get('sender') == address) or (x.get('receiver') == address), result))

        if scantrust_id:
            result = list(filter(lambda x: x.get('scantrust_id') == scantrust_id, result))

        return JsonResponse({'data': result})
