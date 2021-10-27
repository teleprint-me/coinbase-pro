from coinbase_pro.abstract import AbstractAuth

from coinbase_pro.messenger import Auth

import pytest
import requests


def test_auth(auth: Auth):
    assert isinstance(auth, AbstractAuth)

    assert hasattr(auth, '_Auth__api')
    assert hasattr(auth, 'api')
    assert hasattr(auth, 'signature')
    assert hasattr(auth, 'header')

    assert isinstance(auth.api.key, str)
    assert isinstance(auth.api.secret, str)
    assert isinstance(auth.api.passphrase, str)

    assert callable(auth)
    assert callable(auth.signature)
    assert callable(auth.header)


@pytest.mark.private
def test_auth_request(auth: Auth):
    assert 'sandbox' in auth.api.authority
    response = requests.get(auth.api.url('/accounts'), auth=auth, timeout=30)
    assert response.status_code == 200
