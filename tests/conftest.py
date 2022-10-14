from app import app
import pytest


@pytest.fixture
def client():
    """Providess a client to test with"""
    with app.test_client() as app_client:

        with app.app_context():
            # None
            temp = 1
        yield app_client