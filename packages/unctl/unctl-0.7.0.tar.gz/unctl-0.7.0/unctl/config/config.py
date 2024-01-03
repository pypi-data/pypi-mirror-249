import os
import yaml
from .app_config import AppConfig


def load_config(config_path: str) -> AppConfig:
    """
    The `load_config` function loads a YAML configuration file and returns an instance
    of the `AppConfig` class.

    :param config_path: The `config_path` parameter is a string that represents the path
    to the YAML configuration file
    :type config_path: str
    :return: The function `load_config` returns an instance of the `AppConfig` class.
    """

    if config_path is not None and not os.path.isfile(config_path):
        raise Exception(f"config file not found by --config path {config_path}")

    # If `config_path` is not specified, then `config_path` fallbacks to the
    # user default configuration file path `~/.config/unctl/config.yaml`.
    if config_path is None:
        config_path = os.path.join(os.path.expanduser("~"), ".config/unctl/config.yaml")

        # If `config_path` is not found in user default configuration path,
        # then `config_path` fallbacks to the default configuration file
        # `config_default.yaml` in the current folder.
        if not os.path.isfile(config_path):
            config_path = os.path.join(os.path.dirname(__file__), "config_default.yaml")

    with open(config_path, "r") as config_file:
        config_data = yaml.safe_load(config_file)

    config = AppConfig(**config_data)
    return config
