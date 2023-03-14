import os
import tempfile

import pytest
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from blog_app_lite import create_app,db,it

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True
    })
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# @pytest.fixture
# def reset_security():
    # app.security = None

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self,login_credential):
        print('Hai')
        return self._client.post(
            '/login?include_auth_token',
            json=login_credential
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)