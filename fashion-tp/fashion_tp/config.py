import collections
import logging
import os

import toml

from sawtooth_sdk.processor.exceptions import LocalConfigurationError

LOGGER = logging.getLogger(__name__)


def load_default_fashion_config():
    """
    Returns the default FashionConfig
    """
    return FashionConfig(
        connect='tcp://localhost:4004',
    )


def load_toml_fashion_config(filename):
    """Returns a FashionConfig created by loading a TOML file from the
    filesystem.

    Args:
        filename (string): The name of the file to load the config from

    Returns:
        config (FashionConfig): The FashionConfig created from the stored
            toml file.

    Raises:
        LocalConfigurationError
    """
    if not os.path.exists(filename):
        LOGGER.info(
            "Skipping transaction proccesor config loading from non-existent"
            " config file: %s", filename)
        return FashionConfig()

    LOGGER.info("Loading transaction fashion-tp information from config: %s",
                filename)

    try:
        with open(filename) as fd:
            raw_config = fd.read()
    except IOError as e:
        raise LocalConfigurationError(
            "Unable to load transaction fashion-tp configuration file:"
            " {}".format(str(e)))

    toml_config = toml.loads(raw_config)
    invalid_keys = set(toml_config.keys()).difference(
        ['connect'])
    if invalid_keys:
        raise LocalConfigurationError(
            "Invalid keys in transaction fashion-tp config: "
            "{}".format(", ".join(sorted(list(invalid_keys)))))

    config = FashionConfig(
        connect=toml_config.get("connect", None)
    )

    return config


def merge_fashion_config(configs):
    """
    Given a list of FashionConfig objects, merges them into a single
    FashionConfig, giving priority in the order of the configs
    (first has highest priority).

    Args:
        configs (list of FashionConfigs): The list of fashion configs that
            must be merged together

    Returns:
        config (FashionConfig): One FashionConfig that combines all of the
            passed in configs.
    """
    connect = None

    for config in reversed(configs):
        if config.connect is not None:
            connect = config.connect

    return FashionConfig(
        connect=connect
    )


class FashionConfig:
    def __init__(self, connect=None):
        self._connect = connect

    @property
    def connect(self):
        return self._connect

    def __repr__(self):
        # not including  password for opentsdb
        return \
            "{}(connect={})".format(
                self.__class__.__name__,
                repr(self._connect),
            )

    def to_dict(self):
        return collections.OrderedDict([
            ('connect', self._connect),
        ])

    def to_toml_string(self):
        return str(toml.dumps(self.to_dict())).strip().split('\n')
