import os

import pytest

import audio_converter.adapters.uuid


TEST_MEDIA_PATH = './tests/media'


@pytest.fixture
def detour_media_path():
    old_path = os.environ['MEDIA_PATH']
    os.environ['MEDIA_PATH'] = TEST_MEDIA_PATH
    yield
    os.environ['MEDIA_PATH'] = old_path


@pytest.fixture
def uuid_provider():
    return audio_converter.adapters.uuid.DefaultUUIDProvider()
