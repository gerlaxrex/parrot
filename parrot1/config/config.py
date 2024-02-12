import json
import logging
from typing import Optional

from pydantic.error_wrappers import ValidationError

from parrot1 import PARROT_CONFIG_FILE
from parrot1.config.config_model import ParrotConfigs


class ParrotConfigurationLoader:
    def __init__(self):
        self.parrot_configs: Optional[ParrotConfigs] = None
        self.__logger = logging.getLogger(__name__)

    def load_configurations(self):
        try:
            with open(PARROT_CONFIG_FILE, "r") as config_file:
                self.parrot_configs = ParrotConfigs(**json.load(config_file))
        except ValidationError as exc:
            self.__logger.error(
                "Something bad happened during the configurations loading."
                "Try running the 'parrot reload-configs' command in order to reset the configurations to a correct formatting."
            )
            self.__logger.error(exc)


PARROT_CONFIGS = ParrotConfigurationLoader()
