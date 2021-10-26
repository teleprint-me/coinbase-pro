from coinbase_pro.messenger import API
from coinbase_pro.messenger import Auth
from coinbase_pro.messenger import Messenger
from coinbase_pro.socket import Token
from coinbase_pro.socket import Stream
from coinbase_pro.client import Client

import pytest
import json


def pytest_addoption(parser):
    parser.addoption(
        "--private", action="store_true", default=False, help="test private endpoints"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "private: test private endpoints")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--private"):
        # --no-skip given: do not skip tests
        return
    private = pytest.mark.skip(reason="need --private option to run")
    for item in items:
        if "private" in item.keywords:
            item.add_marker(private)


@pytest.fixture(scope='module')
def settings() -> dict:
    data = dict()
    with open('tests/settings.json.example', 'r') as file:
        data = json.load(file)
    return data


@pytest.fixture(scope='module')
def api(settings: dict) -> API:
    return API(settings['uri']['sandbox'])


@pytest.fixture(scope='module')
def auth(settings: dict) -> Auth:
    key = settings['sandbox']['key']
    secret = settings['sandbox']['secret']
    passphrase = settings['sandbox']['passphrase']
    return Auth(key, secret, passphrase)


@pytest.fixture(scope='module')
def token(settings: dict) -> Token:
    key = settings['restapi']['key']
    secret = settings['restapi']['secret']
    passphrase = settings['restapi']['passphrase']
    return Token(key, secret, passphrase)


@pytest.fixture(scope='module')
def public_messenger(api: API) -> Messenger:
    return Messenger(api)


@pytest.fixture(scope='module')
def private_messenger(api: API, auth: Auth) -> Messenger:
    return Messenger(api, auth)


@pytest.fixture(scope='module')
def public_client(public_messenger: Messenger) -> Client:
    return Client(public_messenger)


@pytest.fixture(scope='module')
def private_client(private_messenger: Messenger) -> Client:
    return Client(private_messenger)


@pytest.fixture(scope='module')
def public_stream() -> Stream:
    return Stream()


@pytest.fixture(scope='module')
def private_stream(token: Token) -> Stream:
    return Stream(token)


@pytest.fixture(scope='module')
def account_id(private_client: Client) -> str:
    accounts = private_client.account.list()
    account = [a for a in accounts if a['currency'] == 'BTC']
    return account[0]['id']


@pytest.fixture(scope='module')
def conversion_id(private_client: Client) -> str:
    data = {'from': 'USD', 'to': 'USDC', 'amount': 10.0}
    conversion = private_client.convert.post(data)
    return conversion['id']
