import json

from parrot import PARROT_CONFIG_FILE
from parrot.config.config_model import ParrotConfigs


def load_configurations():
    with open(PARROT_CONFIG_FILE, "r") as config_file:
        configs = ParrotConfigs(**json.load(config_file))
    return configs


PARROT_CONFIGS = load_configurations()
