from coinbase_pro.abstract import AbstractAuth

from coinbase_pro.messenger import API
from coinbase_pro.messenger import Auth

import pytest
import requests


def test_auth(auth: Auth):
    assert isinstance(auth, AbstractAuth)

    assert hasattr(auth, '_Auth__key')
    assert hasattr(auth, '_Auth__secret')
    assert hasattr(auth, '_Auth__passphrase')
    assert hasattr(auth, 'signature')
    assert hasattr(auth, 'headers')

    assert isinstance(auth._Auth__key, str)
    assert isinstance(auth._Auth__secret, str)
    assert isinstance(auth._Auth__passphrase, str)

    assert callable(auth)
    assert callable(auth.signature)
    assert callable(auth.headers)


@pytest.mark.private
def test_auth_request(api: API, auth: Auth):
    assert 'sandbox' in api.url

    url = api.path('/accounts')
    response = requests.get(url, auth=auth, timeout=30)

    assert response.status_code == 200
