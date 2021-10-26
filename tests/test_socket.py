from coinbase_pro.socket import Token
from coinbase_pro.socket import Stream
from coinbase_pro.socket import get_message

import pytest


def test_message():
    message: dict = get_message()

    assert isinstance(message, dict)
    assert isinstance(message['product_ids'], list)
    assert isinstance(message['channels'], list)

    assert message['type'] == 'subscribe'
    assert message['product_ids'] == ['BTC-USD']
    assert message['channels'] == ['ticker']


def test_token(token: Token):
    assert hasattr(token, '_Token__key')
    assert hasattr(token, '_Token__secret')
    assert hasattr(token, '_Token__passphrase')
    assert hasattr(token, 'signature')
    assert hasattr(token, 'header')

    assert isinstance(token._Token__key, str)
    assert isinstance(token._Token__secret, str)
    assert isinstance(token._Token__passphrase, str)

    assert callable(token)
    assert callable(token.signature)
    assert callable(token.header)


def test_public_stream(public_stream: Stream):
    assert 'wss://ws-feed.pro.coinbase.com' == public_stream.url

    message: dict = get_message()

    assert public_stream.connect() is True
    public_stream.send(message)
    assert public_stream.connected is True

    init = public_stream.receive()
    response = public_stream.receive()
    assert init['type'] == 'subscriptions'
    assert init['channels'][0] == {'name': 'ticker', 'product_ids': ['BTC-USD']}
    assert response['type'] == 'ticker'
    assert response['product_id'] == 'BTC-USD'
    assert 'side' in response
    assert 'time' in response
    assert public_stream.disconnect() is True


@pytest.mark.private
def test_private_stream(token: Token, private_stream: Stream):
    assert 'wss://ws-feed.pro.coinbase.com' == private_stream.url

    message: dict = get_message()

    private_stream.connect()
    private_stream.send(message)
    assert private_stream.connected is True

    init = private_stream.receive()
    response = private_stream.receive()
    assert init['type'] == 'subscriptions'
    assert init['channels'][0] == {'name': 'ticker', 'product_ids': ['BTC-USD']}
    assert response['type'] == 'ticker'
    assert response['product_id'] == 'BTC-USD'
    assert 'side' in response
    assert 'time' in response
    assert private_stream.disconnect() is True
