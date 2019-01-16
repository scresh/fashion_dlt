from django.http import JsonResponse
from django.views import View
from secp256k1 import PrivateKey
from django.http import HttpResponse


class KeysView(View):
    def get(self, request):
        private_key = PrivateKey()
        private_key_hex = private_key.serialize()
        public_key_hex = private_key.pubkey.serialize().hex()

        result = {
            'private_key': private_key_hex,
            'public_key': public_key_hex,
        }
        return JsonResponse(result)

    def post(self, request):
        try:
            private_key_hex = request.POST['private_key']
            public_key_hex = request.POST['public_key']

            private_key = PrivateKey(bytes(bytearray.fromhex(private_key_hex)), raw=True)
            if public_key_hex == private_key.pubkey.serialize().hex():
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=401)

        except KeyError:
            return HttpResponse(status=400)
