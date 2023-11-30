import os
import pathlib as pl
from typing import Union


def change_extension(filename: Union[str, os.PathLike], new_extension: str) -> pl.Path:
    return pl.Path(f"{filename.rsplit('.', 1)[0]}.{new_extension}")


def get_extension(filename: Union[str, os.PathLike]) -> str:
    return os.path.basename(filename).rsplit(".", 1)[1]


def get_filename(filepath: Union[str, os.PathLike]) -> str:
    return os.path.basename(filepath).rsplit(".", 1)[0]
