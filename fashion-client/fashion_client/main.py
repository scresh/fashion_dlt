from __future__ import print_function

import argparse
import getpass
import logging
import os
import traceback
import sys
import pkg_resources

from colorlog import ColoredFormatter

from .fashion_client import FashionClient
from .fashion_exceptions import FashionException

DISTRIBUTION_NAME = 'fashion-cli'

DEFAULT_URL = 'http://127.0.0.1:8008'


def create_console_handler(verbose_level):
    clog = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s[%(asctime)s %(levelname)-8s%(module)s]%(reset)s "
        "%(white)s%(message)s",
        datefmt="%H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        })

    clog.setFormatter(formatter)

    if verbose_level == 0:
        clog.setLevel(logging.WARN)
    elif verbose_level == 1:
        clog.setLevel(logging.INFO)
    else:
        clog.setLevel(logging.DEBUG)

    return clog


def setup_loggers(verbose_level):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(create_console_handler(verbose_level))


def add_create_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'create',
        help='Creates a new fashion item',
        description='Sends a transaction to create a fashion item with the identifier <scantrust_id> and '
                    '<item_name>, <item_info> <item_color> <item_size> <item_img> <item_img_md5>'
                    'This transaction will fail if the specified item already exists.',
        parents=[parent_parser]
    )

    parser.add_argument(
        'scantrust_id',
        type=str,
        help='unique identifier for the new item')

    parser.add_argument(
        'item_name',
        type=str,
        help='fashion item name')
    
    parser.add_argument(
        'item_info',
        type=str,
        help='fashion item info')
    
    parser.add_argument(
        'item_color',
        type=str,
        help='fashion item color')
    
    parser.add_argument(
        'item_size',
        type=str,
        help='fashion item size')
    
    parser.add_argument(
        'item_img',
        type=str,
        help='fashion item img')
    
    parser.add_argument(
        'item_img_md5',
        type=str,
        help='fashion item img md5')

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    parser.add_argument(
        '--username',
        type=str,
        help="identify name of user's private key file")

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")

    parser.add_argument(
        '--auth-user',
        type=str,
        help='specify username for authentication if REST API '
             'is using Basic Auth')

    parser.add_argument(
        '--auth-password',
        type=str,
        help='specify password for authentication if REST API '
             'is using Basic Auth')

    parser.add_argument(
        '--disable-client-validation',
        action='store_true',
        default=False,
        help='disable client validation')

    parser.add_argument(
        '--wait',
        nargs='?',
        const=sys.maxsize,
        type=int,
        help='set time, in seconds, to wait for item to commit')


def add_send_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'send',
        help='Send item to other user',
        description='Sends a transaction to send a specific fashion item '
                    'with the identifier <scantrust_id> to user with'
                    'address <recipient>',
        parents=[parent_parser]
    )

    parser.add_argument(
        'scantrust_id',
        type=str,
        help='identifier for the fashion item')

    parser.add_argument(
        'recipient',
        type=str,
        help='Recipient public key')

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    parser.add_argument(
        '--username',
        type=str,
        help="identify name of user's private key file")

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")

    parser.add_argument(
        '--auth-user',
        type=str,
        help='specify username for authentication if REST API '
             'is using Basic Auth')

    parser.add_argument(
        '--auth-password',
        type=str,
        help='specify password for authentication if REST API '
             'is using Basic Auth')

    parser.add_argument(
        '--wait',
        nargs='?',
        const=sys.maxsize,
        type=int,
        help='set time, in seconds, to wait for take transaction '
             'to commit')


def create_parent_parser(script_name):
    parent_parser = argparse.ArgumentParser(prog=script_name, add_help=False)
    parent_parser.add_argument(
        '-v', '--verbose',
        action='count',
        help='enable more verbose output'
    )

    try:
        version = pkg_resources.get_distribution(DISTRIBUTION_NAME).version
    except pkg_resources.DistributionNotFound:
        version = 'UNKNOWN'

    parent_parser.add_argument(
        '-V', '--version',
        action='version',
        version=(DISTRIBUTION_NAME + ' (Hyperledger Sawtooth) version {}').format(version),
        help='display version information'
    )

    return parent_parser


def create_parser(script_name):
    parent_parser = create_parent_parser(script_name)

    parser = argparse.ArgumentParser(
        description='Provides subcommands to send transactions in distributed ledger storing fashion items',
        parents=[parent_parser]
    )

    subparsers = parser.add_subparsers(title='subcommands', dest='command')

    subparsers.required = True

    add_create_parser(subparsers, parent_parser)
    add_send_parser(subparsers, parent_parser)

    return parser


def do_create(args):
    scantrust_id = args.scantrust_id
    item_name = args.item_name
    item_info = args.item_info
    item_color = args.item_color
    item_size = args.item_size
    item_img = args.item_img
    item_img_md5 = args.item_img_md5

    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user, auth_password = _get_auth_info(args)

    client = FashionClient(base_url=url, keyfile=keyfile)

    if args.wait and args.wait > 0:
        response = client.create_item(
            scantrust_id, item_name, item_info, item_color, item_size, item_img, item_img_md5,
            wait=args.wait,
            auth_user=auth_user,
            auth_password=auth_password)
    else:
        response = client.create_item(
            scantrust_id, item_name, item_info, item_color, item_size, item_img, item_img_md5,
            auth_user=auth_user,
            auth_password=auth_password)

    print("Response: {}".format(response))


def do_send(args):
    scantrust_id = args.scantrust_id
    recipient = args.recipient

    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user, auth_password = _get_auth_info(args)

    client = FashionClient(base_url=url, keyfile=keyfile)

    if args.wait and args.wait > 0:
        response = client.send_item(
            scantrust_id, recipient, wait=args.wait,
            auth_user=auth_user,
            auth_password=auth_password)
    else:
        response = client.send_item(
            scantrust_id, recipient,
            auth_user=auth_user,
            auth_password=auth_password)

    print("Response: {}".format(response))


def _get_url(args):
    return DEFAULT_URL if args.url is None else args.url


def _get_keyfile(args):
    username = getpass.getuser() if args.username is None else args.username
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")

    return '{}/{}.priv'.format(key_dir, username)


def _get_auth_info(args):
    auth_user = args.auth_user
    auth_password = args.auth_password
    if auth_user is not None and auth_password is None:
        auth_password = getpass.getpass(prompt="Auth Password: ")

    return auth_user, auth_password


def main(script_name=os.path.basename(sys.argv[0]), args=None):
    if args is None:
        args = sys.argv[1:]
    parser = create_parser(script_name)
    args = parser.parse_args(args)

    if args.verbose is None:
        verbose_level = 0
    else:
        verbose_level = args.verbose

    setup_loggers(verbose_level=verbose_level)

    if args.command == 'create':
        do_create(args)
    elif args.command == 'take':
        do_send(args)
    else:
        raise FashionException("invalid command: {}".format(args.command))


def main_wrapper():
    try:
        main()
    except FashionException as err:
        print("Error: {}".format(err), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
