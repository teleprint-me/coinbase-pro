import pytest
import requests
from coinbase_pro.abstract import AbstractAuth
from coinbase_pro.messenger import Auth


class TestAuth:
    def test_type(self, auth: Auth):
        assert isinstance(auth, AbstractAuth)
        assert isinstance(auth, Auth)

    def test_attr(self, auth: Auth):
        assert hasattr(auth, "_Auth__api")
        assert hasattr(auth, "api")
        assert hasattr(auth, "signature")
        assert hasattr(auth, "header")

    def test_properties(self, auth: Auth):
        assert isinstance(auth.api.key, str)
        assert isinstance(auth.api.secret, str)
        assert isinstance(auth.api.passphrase, str)

    def test_callable(self, auth: Auth):
        assert callable(auth)
        assert callable(auth.signature)
        assert callable(auth.header)

    @pytest.mark.private
    def test_request(self, auth: Auth):
        assert "sandbox" in auth.api.rest, auth.api.rest
        response = requests.get(auth.api.url("/accounts"), auth=auth, timeout=30)
        assert response.status_code == 200, response.json()["message"]
