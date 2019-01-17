from django.http import JsonResponse
from django.views import View
from secp256k1 import PrivateKey


class ValidatorView(View):
    def get(self, request):
        try:
            private_key_hex = request.GET.get('private_key')
            public_key_hex = request.GET.get('public_key')

            private_key = PrivateKey(bytes(bytearray.fromhex(private_key_hex)), raw=True)
            if public_key_hex == private_key.pubkey.serialize().hex():
                return JsonResponse({'result': 'OK'})

            else:
                return JsonResponse({'result': 'Key pair does not match'})
        except:
            return JsonResponse({'result': 'Incorrect values'})


1
