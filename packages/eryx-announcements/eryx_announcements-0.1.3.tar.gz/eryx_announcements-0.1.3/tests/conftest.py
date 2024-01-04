import pytest

from src.announcer import Announcer


@pytest.fixture
def announcer():
    return Announcer.new()
