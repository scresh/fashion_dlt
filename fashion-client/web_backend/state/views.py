import base64

from django.http import JsonResponse
from django.views import View
import urllib.request
import json
import hashlib

FASHION_NAMESPACE = hashlib.sha512('fashion'.encode("utf-8")).hexdigest()[0:6]


def from_payload(payload):
    scantrust_id, owner, item_name, item_info, item_color, item_size, item_img, item_img_md5 = \
        json.loads(payload)

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


def get_address(scantrust_id):
    return FASHION_NAMESPACE + hashlib.sha512(scantrust_id.encode('utf-8')).hexdigest()[:64]


def get_json(url):
    try:
        with urllib.request.urlopen(url) as data:
            json_data = json.loads(data.read().decode())
            return json_data
    except:
        return {}


class StateView(View):
    def get(self, request):
        scantrust_id = request.GET.get('scantrust_id')
        address = request.GET.get('address')

        state_url = 'http://127.0.0.1:8008/state'

        result = []
        if scantrust_id:
            state_url += '/' + get_address(scantrust_id)
            base64_payload = get_json(state_url).get('data')
            if base64_payload:
                batch_payload = base64.b64decode(base64_payload)
                payload = json.loads(batch_payload)[0]

                result = [
                    from_payload(payload)
                ]

        else:
            state_url += '?address=' + FASHION_NAMESPACE

            states = get_json(state_url).get('data')
            for state in states:
                base64_payload = state.get('data')
                batch_payload = base64.b64decode(base64_payload)
                payload = json.loads(batch_payload)[0]
                result.append(from_payload(payload))

            if address:
                print(type(result[0]))

                result = list(filter(lambda x: x.get('owner') == address, result))

        return JsonResponse({'data': result})
