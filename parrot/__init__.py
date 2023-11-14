import pathlib as pl
import os


PACKAGE_LOCATION = pl.Path(os.path.dirname(__file__))
ROOT_LOCATION = PACKAGE_LOCATION.parent

RESOURCES_LOCATION = PACKAGE_LOCATION / "resources"
