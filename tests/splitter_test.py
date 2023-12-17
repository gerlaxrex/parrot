import pytest
from parrot1 import PARROT_CONFIG_FILE
from parrot1.utils.file_utils import get_filename


@pytest.fixture
def url():
    return PARROT_CONFIG_FILE


def test_extract_filename(url):
    fname = get_filename(url)
    assert fname is not None
