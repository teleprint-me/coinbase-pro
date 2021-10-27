from coinbase_pro.abstract import AbstractAPI
from coinbase_pro.messenger import API

import requests


def test_api(api):
    assert isinstance(api, AbstractAPI)
    assert isinstance(api, API)

    assert hasattr(api, 'key')
    assert hasattr(api, 'secret')
    assert hasattr(api, 'passphrase')
    assert hasattr(api, 'authority')
    assert hasattr(api, 'version')

    assert isinstance(api.key, str)
    assert isinstance(api.secret, str)
    assert isinstance(api.passphrase, str)
    assert isinstance(api.authority, str)
    assert isinstance(api.version, int)

    assert callable(api.path)
    assert callable(api.url)

    assert 'sandbox' in api.authority

    assert api.path('/time') == '/time'
    assert api.url('/time') == 'https://api-public.sandbox.pro.coinbase.com/time'

    response = requests.get(api.url('/time'), timeout=30)
    assert response.status_code == 200

    payload = response.json()
    assert 'iso' in payload and 'epoch' in payload
