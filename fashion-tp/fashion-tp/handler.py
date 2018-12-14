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

        current_item_payload = fashion_dlt.get_item_payload(new_item)

        if current_item_payload is None:
            # TODO: Add authentication
            if signer != new_item.owner:
                raise InvalidTransaction(
                    'Invalid action: New item owner must be transaction signer')

            fashion_dlt.add_item_state(new_item)
            _display(f'User {signer} created a new item [{new_item.scantrust_id}]')

        else:
            current_item = FashionItemState.from_payload(current_item_payload)

            if signer != current_item.owner:
                raise InvalidTransaction(
                    'Invalid action: Item does not belong to transaction signer')

            if new_item.owner != current_item.owner:
                raise InvalidTransaction(
                    'Invalid action: Can not sent owned item to yourself')

            fashion_dlt.add_item_state(new_item)
            _display(f'User {signer} sent item [{new_item.scantrust_id}] to {new_item.owner}')


def _display(msg):
    n = msg.count("\n")

    if n > 0:
        msg = msg.split("\n")
        length = max(len(line) for line in msg)
    else:
        length = len(msg)
        msg = [msg]

    # pylint: disable=logging-not-lazy
    LOGGER.debug("+" + (length + 2) * "-" + "+")
    for line in msg:
        LOGGER.debug("+ " + line.center(length) + " +")
    LOGGER.debug("+" + (length + 2) * "-" + "+")
