import requests
from coinbase_pro.abstract import AbstractAPI
from coinbase_pro.messenger import API


class TestAPI:
    def test_type(self, api: API):
        assert isinstance(api, AbstractAPI)
        assert isinstance(api, API)

    def test_attr(self, api: API):
        assert hasattr(api, "settings")
        assert hasattr(api, "key")
        assert hasattr(api, "secret")
        assert hasattr(api, "passphrase")
        assert hasattr(api, "rest")
        assert hasattr(api, "feed")
        assert hasattr(api, "version")

    def test_properties(self, api: API):
        assert isinstance(api.settings, dict)
        assert isinstance(api.key, str)
        assert isinstance(api.secret, str)
        assert isinstance(api.passphrase, str)
        assert isinstance(api.rest, str)
        assert isinstance(api.feed, str)
        assert isinstance(api.version, int)

    def test_callable(self, api: API):
        assert callable(api.path)
        assert callable(api.url)

        assert "sandbox" in api.rest

        assert api.path("/time") == "/time"
        assert api.url("/time") == "https://api-public.sandbox.pro.coinbase.com/time"

        response = requests.get(api.url("/time"), timeout=30)
        assert response.status_code == 200

        payload = response.json()
        assert "iso" in payload and "epoch" in payload
