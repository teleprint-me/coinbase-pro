# abstract
import datetime

import pytest
from coinbase_pro.abstract import AbstractClient

# public
from coinbase_pro.client import CoinbasePro, Currency, Product, Time

# core
from coinbase_pro.messenger import Subscriber

# calc dates
from dateutil.relativedelta import relativedelta

# custom
from tests.teardown import Teardown


class TestPublicClient(object):
    def test_public_instance(self, public_client):
        assert isinstance(public_client, AbstractClient)
        assert isinstance(public_client, CoinbasePro)

    def test_public_attributes(self, public_client):
        assert hasattr(public_client, "product")
        assert hasattr(public_client, "currency")
        assert hasattr(public_client, "time")

    def test_public_product(self, public_client):
        product = public_client.product
        assert isinstance(product, Subscriber)
        assert isinstance(product, Product)
        assert callable(product.list)
        assert callable(product.get)
        assert callable(product.book)
        assert callable(product.ticker)
        assert callable(product.trades)
        assert callable(product.candles)
        assert callable(product.stats)

    def test_public_currency(self, public_client):
        currency = public_client.currency
        assert isinstance(currency, Subscriber)
        assert isinstance(currency, Currency)
        assert callable(currency.list)
        assert callable(currency.get)

    def test_public_time(self, public_client):
        time = public_client.time
        assert isinstance(time, Subscriber)
        assert isinstance(time, Time)
        assert callable(time.get)


class TestPublicProduct(Teardown):
    def test_list(self, public_client):
        response = public_client.product.list()
        assert isinstance(response, list)
        assert "id" in response[0]

    def test_get(self, public_client):
        response = public_client.product.get("BTC-USD")
        assert isinstance(response, dict)
        assert "id" in response
        assert response["id"] == "BTC-USD"
        assert response["base_currency"] == "BTC"
        assert response["quote_currency"] == "USD"

    @pytest.mark.parametrize("level", [None, 1, 2, 3])
    def test_book(self, public_client, level):
        if level is None:
            response = public_client.product.book("BTC-USD")
        else:
            response = public_client.product.book("BTC-USD", {"level": level})
        assert isinstance(response, dict)
        assert "sequence" in response
        assert "asks" in response
        assert "bids" in response

    def test_ticker(self, public_client):
        response = public_client.product.ticker("BTC-USD")
        assert isinstance(response, dict)
        assert "trade_id" in response
        assert "price" in response
        assert "size" in response

    def test_trades(self, public_client):
        response = public_client.product.trades("BTC-USD")
        assert isinstance(response, list)
        assert "trade_id" in response[0]

    current_time = datetime.datetime.now()

    @pytest.mark.parametrize(
        "start,end,granularity",
        [(current_time - relativedelta(months=1), current_time, 86400)],
    )
    def test_candles(self, public_client, start, end, granularity):

        data = {"start": start, "end": end, "granularity": granularity}
        response = public_client.product.candles("BTC-USD", data)
        assert isinstance(response, list)
        for ticker in response:
            assert all([type(tick) in (int, float) for tick in ticker])

    def test_stats(self, public_client):
        response = public_client.product.stats("BTC-USD")
        assert isinstance(response, dict)
        assert "volume_30day" in response


class TestPublicCurrency(Teardown):
    def test_list(self, public_client):
        response = public_client.currency.list()
        assert isinstance(response, list)
        assert "name" in response[0]
        assert "details" in response[0]

    def test_get(self, public_client):
        response = public_client.currency.get("BTC")
        assert isinstance(response, dict)
        assert "id" in response
        assert response["id"] == "BTC"


class TestPublicTime(Teardown):
    def test_get(self, public_client):
        response = public_client.time.get()
        assert isinstance(response, dict)
        assert "iso" in response
