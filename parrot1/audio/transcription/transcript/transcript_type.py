"""A utility module for handling different transcript formats"""
# pylint: disable=C0103
import enum


class TranscriptType(str, enum.Enum):
    """An enum of supported transcript formats"""

    microsoftstream = "microsoftstream"
