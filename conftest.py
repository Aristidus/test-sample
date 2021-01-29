import pytest

from src.client import Client
from src.config import Configuration

ENDPOINT = "http://localhost"

@pytest.fixture(scope="session")
def api(request):
    config = Configuration(endpoint=ENDPOINT)
    api = Client(config)
    yield api
    del api
