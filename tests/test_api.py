from coinbase_pro.abstract import AbstractAPI
from coinbase_pro.messenger import API

import requests


def test_api(api):
    assert 'sandbox' in api.url

    assert isinstance(api, AbstractAPI)
    assert isinstance(api, API)

    assert hasattr(api, 'url')
    assert hasattr(api, 'version')
    assert hasattr(api, 'endpoint')
    assert hasattr(api, 'path')

    assert isinstance(api.url, str)
    assert isinstance(api.version, int)

    assert api.endpoint('/time') == '/time'
    assert api.path('/time') == 'https://api-public.sandbox.pro.coinbase.com/time'

    response = requests.get(api.path('/time'), timeout=30)
    assert response.status_code == 200

    payload = response.json()
    assert 'iso' in payload and 'epoch' in payload
