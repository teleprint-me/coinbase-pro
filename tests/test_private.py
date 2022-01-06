# abstract
import pytest
from coinbase_pro.abstract import AbstractClient

# private
from coinbase_pro.client import (
    Account,
    Coinbase,
    CoinbasePro,
    Convert,
    Oracle,
    Order,
    Profile,
    Report,
    Transfer,
    User,
)

# core
from coinbase_pro.messenger import Subscriber

# custom
from tests.teardown import Teardown


@pytest.mark.private
class TestPrivateClient(object):
    def test_private_instance(self, private_client):
        assert isinstance(private_client, AbstractClient)
        assert isinstance(private_client, CoinbasePro)

    def test_private_attributes(self, private_client):
        assert hasattr(private_client, "account")
        assert hasattr(private_client, "coinbase")
        assert hasattr(private_client, "convert")
        assert hasattr(private_client, "transfer")
        assert hasattr(private_client, "order")
        assert hasattr(private_client, "oracle")
        assert hasattr(private_client, "profile")
        assert hasattr(private_client, "report")
        assert hasattr(private_client, "user")

    def test_private_account(self, private_client):
        account = private_client.account
        assert isinstance(account, Subscriber)
        assert isinstance(account, Account)
        assert callable(account.list)
        assert callable(account.get)
        assert callable(account.holds)
        assert callable(account.ledger)
        assert callable(account.transfers)

    def test_private_coinbase(self, private_client):
        coinbase = private_client.coinbase
        assert isinstance(coinbase, Subscriber)
        assert isinstance(coinbase, Coinbase)
        assert callable(coinbase.wallets)
        assert callable(coinbase.generate_address)
        assert callable(coinbase.deposit_from)
        assert callable(coinbase.withdraw_to)

    def test_private_convert(self, private_client):
        convert = private_client.convert
        assert isinstance(convert, Subscriber)
        assert isinstance(convert, Convert)
        assert callable(convert.post)
        assert callable(convert.get)

    def test_private_transfer(self, private_client):
        transfer = private_client.transfer
        assert isinstance(transfer, Subscriber)
        assert isinstance(transfer, Transfer)
        assert callable(transfer.deposit_from)
        assert callable(transfer.methods)
        assert callable(transfer.list)
        assert callable(transfer.get)
        assert callable(transfer.withdraw_to_address)
        assert callable(transfer.withdraw_estimate)
        assert callable(transfer.withdraw_to)

    def test_private_order(self, private_client):
        order = private_client.order
        assert isinstance(order, Subscriber)
        assert isinstance(order, Order)
        assert callable(order.fills)
        assert callable(order.list)
        assert callable(order.cancel_all)
        assert callable(order.post)
        assert callable(order.get)
        assert callable(order.cancel)

    def test_private_oracle(self, private_client):
        oracle = private_client.oracle
        assert isinstance(oracle, Subscriber)
        assert isinstance(oracle, Oracle)
        assert callable(oracle.prices)

    def test_private_profile(self, private_client):
        profiles = private_client.profile
        assert isinstance(profiles, Subscriber)
        assert isinstance(profiles, Profile)
        assert callable(profiles.list)
        assert callable(profiles.create)
        assert callable(profiles.transfer)
        assert callable(profiles.get)
        assert callable(profiles.rename)
        assert callable(profiles.delete)

    def test_private_report(self, private_client):
        report = private_client.report
        assert isinstance(report, Subscriber)
        assert isinstance(report, Report)
        assert callable(report.list)
        assert callable(report.create)
        assert callable(report.get)

    def test_private_user(self, private_client):
        user = private_client.user
        assert isinstance(user, Subscriber)
        assert isinstance(user, User)
        assert callable(user.limits)


@pytest.mark.private
class TestPrivateAccount(Teardown):
    def test_list(self, private_client):
        response = private_client.account.list()
        assert isinstance(response, list)
        assert "currency" in response[0]

    def test_get(self, private_client, account_id):
        response = private_client.account.get(account_id)
        assert isinstance(response, dict)
        assert "currency" in response

    def test_holds(self, private_client, account_id):
        response = private_client.account.holds(account_id)
        assert isinstance(response, list)
        if len(response) > 0:
            assert isinstance(response[0], dict)
            assert "amount" in response[0]
            assert "type" in response[0]
            assert "ref" in response[0]

    def test_ledger(self, private_client, account_id):
        response = private_client.account.ledger(account_id)
        assert isinstance(response, list)
        if len(response) > 0:
            assert isinstance(response[0], dict)
            assert "amount" in response[0]
            assert "details" in response[0]

    def test_transfers(self, private_client, account_id):
        response = private_client.account.transfers(account_id)
        assert isinstance(response, list)
        if len(response) > 0:
            assert isinstance(response[0], dict)
            assert "type" in response[0]
            assert "created_at" in response[0]
            assert "details" in response[0]


@pytest.mark.private
class TestPrivateCoinbase(Teardown):
    def test_wallets(self, private_client):
        response = private_client.coinbase.wallets()
        assert isinstance(response, list)
        if len(response) > 0:
            assert isinstance(response[0], dict)
            assert "available_on_consumer" in response[0]
            assert "balance" in response[0]
            assert "currency" in response[0]

    @pytest.mark.skip
    def test_generate_address(self, private_client):
        # NOTE: The generated address is for the Coinbase account.
        # ERROR: generates a 500 response in sandbox
        pass

    @pytest.mark.skip
    def test_deposit_from(self, private_client):
        # NOTE: This is to deposit from Coinbase.
        # ERROR: generates a 500 response in sandbox
        pass

    @pytest.mark.skip
    def test_withdraw_to(self, private_client):
        # NOTE: This is to withdraw to Coinbase.
        # ERROR: generates a 500 response in sandbox
        pass


@pytest.mark.private
class TestPrivateConvert(Teardown):
    def test_post(self, private_client):
        data = {"from": "USD", "to": "USDC", "amount": 10.0}
        response = private_client.convert.post(data)
        assert isinstance(response, dict)
        assert "from" in response and response["from"] == "USD"
        assert "to" in response and response["to"] == "USDC"

    def test_get(self, private_client, conversion_id):
        response = private_client.convert.get(conversion_id)
        assert isinstance(response, dict)
        assert "from_account_id" in response
        assert "to_account_id" in response


@pytest.mark.private
class TestPrivateTransfer(Teardown):
    @pytest.mark.skip
    def test_methods(self, private_client):
        pass

    @pytest.mark.skip
    def test_list(self, private_client):
        pass

    @pytest.mark.skip
    def test_get(self, private_client):
        pass

    @pytest.mark.skip
    def test_withdraw_estimate(self, private_client):
        pass


@pytest.mark.private
class TestPrivateOrder(Teardown):
    def test_post_limit_order(self, private_client):
        response = private_client.order.post(
            {
                "side": "buy",
                "product_id": "BTC-USD",
                "type": "limit",
                "price": 40000.0,
                "size": 0.001,
            }
        )
        assert isinstance(response, dict)
        assert "status" in response
        assert response["type"] == "limit"

    def test_post_market_order(self, private_client):
        response = private_client.order.post(
            {"side": "buy", "product_id": "BTC-USD", "type": "market", "size": 0.001}
        )
        assert isinstance(response, dict)
        assert "status" in response
        assert response["type"] == "market"

    @pytest.mark.parametrize("stop", ["entry", "loss"])
    def test_post_stop_order(self, private_client, stop):
        response = private_client.order.post(
            {
                "side": "buy",
                "product_id": "BTC-USD",
                "type": "limit",
                "price": 50000.0,
                "size": 0.01,
                "stop": stop,
                "stop_price": 40000.0,
            }
        )
        print(response)
        assert isinstance(response, dict)
        assert response["type"] == "limit"
        assert response["stop"] == stop

    def test_cancel(self, private_client):
        order = private_client.order.post(
            {
                "side": "buy",
                "product_id": "BTC-USD",
                "type": "limit",
                "price": 40000.0,
                "size": 0.001,
            }
        )
        response = private_client.order.cancel(order["id"], {"product_id": "BTC-USD"})
        assert isinstance(response, str)
        assert response == order["id"]

    def test_list(self, private_client):
        response = private_client.order.list(
            {"status": "pending", "product_id": "BTC-USD"}
        )
        assert isinstance(response, list)
        if len(response) > 0:
            assert "created_at" in response[0]

    def test_get(self, private_client):
        order = private_client.order.post(
            {
                "side": "buy",
                "product_id": "BTC-USD",
                "type": "limit",
                "price": 40000.0,
                "size": 0.01,
            }
        )
        response = private_client.order.get(order["id"])
        assert response["id"] == order["id"]

    def test_fills(self, private_client):
        response = private_client.order.fills({"product_id": "BTC-USD", "limit": 20})
        assert isinstance(response, list)
        assert isinstance(response[0], dict)
        assert "product_id" in response[0]
        assert "order_id" in response[0]
        assert "price" in response[0]
        assert "size" in response[0]
        assert "created_at" in response[0]


@pytest.mark.private
class TestPrivateOracle(Teardown):
    def test_prices(self, private_client):
        response = private_client.oracle.prices()
        assert isinstance(response, dict)
        assert "messages" in response
        assert "prices" in response
        assert "signatures" in response


@pytest.mark.skip
class TestPrivateProfile(Teardown):
    pass


@pytest.mark.skip
class TestPrivateReport(Teardown):
    pass


@pytest.mark.skip
class TestPrivateUser(Teardown):
    pass
