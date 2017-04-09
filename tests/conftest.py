import pytest
from elaster.server import main as elaster_app


@pytest.fixture(scope='session')
def app():
    return elaster_app
    