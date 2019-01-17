from django.http import JsonResponse
from django.views import View
from secp256k1 import PrivateKey


class GeneratorView(View):
    def get(self, request):
        private_key = PrivateKey()
        private_key_hex = private_key.serialize()
        public_key_hex = private_key.pubkey.serialize().hex()

        result = {
            'private_key': private_key_hex,
            'public_key': public_key_hex,
        }
        return JsonResponse(result)
