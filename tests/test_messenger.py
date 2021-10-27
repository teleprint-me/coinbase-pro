from coinbase_pro.abstract import AbstractMessenger

from coinbase_pro.messenger import API
from coinbase_pro.messenger import Auth
from coinbase_pro.messenger import Messenger
from coinbase_pro.messenger import Subscriber

from requests import Session
from requests import Response

from tests.teardown import Teardown

import pytest


class TestMessenger(Teardown):
    def test_messenger_attributes(self, private_messenger):
        assert hasattr(private_messenger, 'auth')
        assert hasattr(private_messenger, 'api')
        assert hasattr(private_messenger, 'session')
        assert hasattr(private_messenger, 'timeout')

    def test_messenger_methods(self, private_messenger):
        assert callable(private_messenger.get)
        assert callable(private_messenger.post)
        assert callable(private_messenger.put)
        assert callable(private_messenger.delete)
        assert callable(private_messenger.page)

    def test_messenger_instance(self, private_messenger):
        assert isinstance(private_messenger, AbstractMessenger)
        assert isinstance(private_messenger.api, API)
        assert isinstance(private_messenger.auth, Auth)
        assert isinstance(private_messenger.session, Session)
        assert isinstance(private_messenger.timeout, int)

    def test_messenger_get(self, public_messenger):
        response = public_messenger.get('/time')
        assert isinstance(response, Response)
        assert response.status_code == 200
        payload = response.json()
        assert isinstance(payload, dict)
        assert 'iso' in payload and 'epoch' in payload

    @pytest.mark.private
    def test_messenger_post(self, private_messenger):
        order = {
            'product_id': 'BTC-USD',
            'type': 'market',
            'side': 'buy',
            'funds': 10.0
        }

        response = private_messenger.post('/orders', order)
        assert isinstance(response, Response)

        payload = response.json()
        assert 'message' not in payload
        assert 'side' in payload
        assert 'product_id' in payload
        assert payload['side'] == 'buy'
        assert payload['product_id'] == 'BTC-USD'

    @pytest.mark.private
    def test_messenger_page(self, private_messenger):
        data = {'product_id': 'BTC-USD'}
        responses = private_messenger.page('/fills', data)

        assert isinstance(responses, list)

        assert 0 < len(responses) <= 20

        for response in responses:
            assert isinstance(response, Response)
            assert response.status_code == 200


class Dummy(Subscriber):
    pass


def test_subscriber(public_messenger):
    dummy = Dummy(public_messenger)

    assert isinstance(dummy, Subscriber)
    assert isinstance(dummy, Dummy)
    assert isinstance(dummy.messenger, Messenger)

    assert hasattr(dummy, 'messenger')
    assert hasattr(dummy, 'error')

    assert callable(dummy.error)
