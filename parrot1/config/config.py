import json
import logging

from pydantic.error_wrappers import ValidationError

from parrot1 import PARROT_CONFIG_FILE
from parrot1.config.config_model import ParrotConfigs

__logger = logging.getLogger(__name__)


def load_configurations():
    with open(PARROT_CONFIG_FILE, "r") as config_file:
        configs = ParrotConfigs(**json.load(config_file))
    return configs


PARROT_CONFIGS = None
try:
    PARROT_CONFIGS = load_configurations()
except ValidationError as exc:
    __logger.error(
        "Something bad happened during the configurations loading."
        "Try running the 'parrot1 reload-configs' command in order to reset the configurations to a correct formatting."
    )
    __logger.error(exc)
