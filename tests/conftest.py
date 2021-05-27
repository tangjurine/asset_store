# following https://dev.to/po5i/how-to-add-basic-unit-test-to-a-python-flask-app-using-pytest-1m7a

import pytest

from app import create_app

@pytest.fixture()
def app():
    return create_app()

@pytest.fixture
def client(app):
    return app.test_client()