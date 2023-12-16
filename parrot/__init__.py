import pathlib as pl
import os
import shutil

PACKAGE_LOCATION = pl.Path(os.path.dirname(__file__))
ROOT_LOCATION = PACKAGE_LOCATION.parent

USER_HOME = pl.Path.home()
PARROT_DATA_FOLDER = USER_HOME / ".parrot"
PARROT_CACHED_MODELS = PARROT_DATA_FOLDER / "cached_models"
PARROT_CONFIG_FILE = PARROT_DATA_FOLDER / "config.json"

RESOURCES_LOCATION = PACKAGE_LOCATION / "resources"
DEFAULT_CONFIGS_PATH = RESOURCES_LOCATION / "default_configs.json"

if not os.path.exists(PARROT_CONFIG_FILE):
    shutil.copyfile(src=DEFAULT_CONFIGS_PATH, dst=PARROT_CONFIG_FILE)
