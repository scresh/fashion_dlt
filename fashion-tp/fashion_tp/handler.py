import logging

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction

from .state import FashionItemState
from .state import FashionDLT
from .state import FASHION_NAMESPACE


LOGGER = logging.getLogger(__name__)


class FashionTransactionHandler(TransactionHandler):
    @property
    def family_name(self):
        return 'fashion'

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespaces(self):
        return [FASHION_NAMESPACE]

    def apply(self, transaction, context):
        header = transaction.header
        signer = header.signer_public_key
        new_item = FashionItemState.from_payload(transaction.payload)
        fashion_dlt = FashionDLT(context)

        current_item_payload = fashion_dlt.get_item_last_payload(new_item)

        if current_item_payload is None:
            # TODO: Add authentication
            if signer != new_item.owner:
                raise InvalidTransaction(
                    'Invalid action: New item owner must be transaction signer')

            fashion_dlt.add_item_state(new_item)
            _display(new_item, signer, new_item.owner)

        else:
            current_item = FashionItemState.from_payload(current_item_payload)

            if signer != current_item.owner:
                raise InvalidTransaction(
                    'Invalid action: Item does not belong to transaction signer')

            if new_item.owner == current_item.owner:
                raise InvalidTransaction(
                    'Invalid action: Can not sent owned item to yourself')

            if new_item.item_name != current_item.item_name:
                raise InvalidTransaction(
                    'Invalid action: Invalid item name')

            if new_item.item_info != current_item.item_info:
                raise InvalidTransaction(
                    'Invalid action: Invalid item info')

            if new_item.item_color != current_item.item_color:
                raise InvalidTransaction(
                    'Invalid action: Invalid item color')

            if new_item.item_size != current_item.item_size:
                raise InvalidTransaction(
                    'Invalid action: Invalid item size')

            if new_item.item_img != current_item.item_img:
                raise InvalidTransaction(
                    'Invalid action: Invalid item image')

            if new_item.item_img_md5 != current_item.item_img_md5:
                raise InvalidTransaction(
                    'Invalid action: Invalid item image MD5')

            item_first_payload = fashion_dlt.get_item_first_payload(new_item)
            first_item = FashionItemState.from_payload(item_first_payload)
            fashion_dlt.add_item_state(new_item)
            _display(first_item, signer, new_item.owner)


def _display(item, sender, receiver):
    col_left, col_right = 12, 81

    border = '+-' + '-' * col_left + '-+-' + '-' * col_right + '-+'
    row = '| {} | {} |'
    lines = ['']

    item_dict = {
        'ScanTrust ID': item.scantrust_id,
        'Name': f'{item.item_name} ({item.item_color}) [{item.item_size}]',
        'Info': [item.item_info, f'{item.item_info[:col_right-3]}...'][len(item.item_info) > col_right],
        'Image URL': item.item_img,
        'Image MD5': item.item_img_md5,
        'Sender': sender,
        'Receiver': receiver,

    }

    lines.append(border)
    for key, value in item_dict.items():
        lines.append(row.format(key.center(col_left, ' '), value.center(col_right, ' ')))
        lines.append(border)

    LOGGER.debug('\n'.join(lines))

