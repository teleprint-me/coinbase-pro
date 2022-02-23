# Client

## About

The `coinbase_pro.client` module is a higher level wrapper that abstracts requests made by the `Auth` and `Messenger` objects. You can use it to avoid handling the nuances of the `Messenger` object while retaining fine-tuned control over requests.

- This module utilizes the strategy pattern to implement the REST API
- The `Subscriber` class is used to define the `CoinbasePro` properties interfaces. 
- The `Subscriber` class can also be used to inherit from the `Messenger` class to define an extension or plugin for the `CoinbasePro` implentation.

_Note: You will only need to instantiate a `CoinbasePro` object in most cases. You can do this by utilizing the `get_client` function. You can also create your own class by inheriting from the `Subscriber` class and utilizing the `CoinbasePro.plug` method to extend functionality._

## Import

You can manually create the `Messenger` and `CoinbasePro` instances

```python
from coinbase_pro.messenger import API
from coinbase_pro.messenger import Auth
from coinbase_pro.messenger import Messenger
from coinbase_pro.client import CoinbasePro
```

You can automate creating the `Messenger` and `CoinbasePro` instances

```python
from coinbase_pro.client import get_messenger
from coinbase_pro.client import get_client
```

## Account

```python
Account(messenger: Messenger)
```
### Account.list

```python
Account.list() -> list
```

A method that returns a list of accounts.

### Account.get

```python
Account.get(account_id: str) -> dict
```

A method that returns information for a single account. 

### Account.holds

```python
Account.holds(account_id: str, data: dict = None) -> list
```

A method that returns a list of holds on an account.

### Account.ledger

```python
Account.ledger(account_id: str, data: dict = None) -> list
```

A method that returns a list of ledger activity on an account.

### Account.transfers

```python
Account.transfers(account_id: str, data: dict = None) -> list
```

A method that returns a list of withdrawals and deposits for an account.

## Coinbase

```python
Coinbase(messenger: Messenger)
```
A class definition for communicating with [Coinbase](https://coinbase.com)

### Coinbase.wallets

```python
Coinbase.wallets() -> list
```

A method that returns a list of Coinbase wallets.

### Coinbase.generate_address

```python
Coinbase.generate_address(account_id: str) -> dict
```

A method that returns a one-time crypto deposit address.

### Coinbase.deposit_from

```python
Coinbase.deposit_from(data: dict) -> dict
```

Deposit funds from a Coinbase wallet to a specified `profile_id`.

### Coinbase.withdraw_to

```python
Coinbase.withdraw_to(data: dict) -> dict
```

Withdraw funds from a specified `profile_id` to a Coinbase wallet.

## Convert

### Convert.post

```python
Convert.post(data: dict) -> dict
```

Converts funds from `from` currency to `to` currency. Funds are converted on the `from` account in the `profile_id` profile.

### Convert.get

```python
Convert.get(conversion_id: str, data: dict = None) -> dict
```

Gets a currency conversion by id (i.e. USD -> USDC).

## Currency

### Currency.list

```python
Currency.list() -> list
```

Gets a list of all known currencies.

### Currency.get

```python
Currency.get(currency_id: str) -> dict
```

Gets a single currency by id.

## Transfer

### Transfer.deposit_from

```python
Transfer.deposit_from(data: dict) -> dict
```

Deposits funds from a linked external payment method to the specified profile_id.

### Transfer.methods

```python
Transfer.methods() -> list
```

Gets a list of the user's linked payment methods.

### Transfer.list

```python
Transfer.list() -> list
```

Gets a list of in-progress and completed transfers of funds in/out of any of the user's accounts.

### Transfer.get

```python
Transfer.get(transfer_id: str) -> dict
```

Get information on a single transfer.

### Transfer.withdraw_to_address

```python
Transfer.withdraw_to_address(data: dict) -> dict
```

Withdraws funds from the specified profile_id to an external crypto address.

### Transfer.withdraw_estimate

```python
Transfer.withdraw_estimate(data: dict = None) -> dict
```

Gets the fee estimate for the crypto withdrawal to crypto address.

### Transfer.withdraw_to

```python
Transfer.withdraw_to(data: dict) -> dict
```

Withdraws funds from the specified profile_id to a linked external payment method.

## Fee

### Fee.get

```python
Fee.get() -> dict
```

Get fees rates and 30 days trailing volume.

## Order

### Order.fills

```python
Order.fills(data: dict) -> dict
```

Get a list of fills. A fill is a partial or complete match on a specific order.

### Order.list

```python
Order.list(data: dict) -> list
```

List your current open orders.

### Order.cancel_all

```python
Order.cancel_all(data: dict = None) -> list
```

With best effort, cancel all open orders.

### Order.post

```python
Order.post(data: dict) -> dict
```

Create an order. You can place two types of orders: limit and market.

### Order.get

```python
Order.get(order_id: str) -> dict
```

Get a single order by `id`.

### Order.cancel

```python
Order.cancel(order_id: str, data: dict = None) -> str
```

Cancel a single open order by `{id}`.

## Oracle

### Oracle.prices

```python
Oracle.prices() -> dict
```

Get cryptographically signed prices ready to be posted on-chain using Compound's Open Oracle smart contract.

## Product

### Product.list

```python
Product.list() -> list
```

Gets a list of available currency pairs for trading.

### Product.get

```python
Product.get(product_id: str) -> dict
```

Get information on a single product.

### Product.book

```python
Product.book(product_id: str, data: dict = None) -> dict
```

Get a list of open orders for a product.

### Product.ticker

```python
Product.ticker(product_id: str) -> dict
```

Gets snapshot information about the last trade (tick), best bid/ask and 24h volume.

### Product.trades

```python
Product.trades(product_id: str, data: dict = None) -> list
```

Gets a list the latest trades for a product.

### Product.candles

```python
Product.candles(product_id: str, data: dict = None) -> list
```

Historic rates for a product.

### Product.stats

```python
Product.stats(product_id: str) -> dict
```

Gets 30day and 24hour stats for a product.

## Profile

### Profile.list

```python
Profile.list(data: dict = None) -> list
```

### Profile.create

```python
Profile.create(data: dict) -> dict
```

### Profile.transfer

```python
Profile.transfer(data: dict) -> dict
```

### Profile.get

```python
Profile.get(profile_id: str, data: dict) -> dict
```

### Profile.rename

```python
Profile.rename(profile_id: str, data: dict) -> dict
```

### Profile.delete

```python
Profile.delete(profile_id: str, data: dict) -> dict
```

## Report

### Report.list

```python
Report.list(user_id: str) -> dict
```

### Report.limits

```python
Report.create(data: dict) -> dict
```

### Report.limits

```python
Report.get(report_id: str) -> dict
```

## User

### User.limits

```python
User.limits(user_id: str) -> dict
```

## Time

### Time.get

```python
Time.get() -> dict
```

## CoinbasePro

```python
CoinbasePro(messenger: Messenger)
```

The `CoinbasePro` class defines the `Messenger` adapter and it's associated property objects.

_Warning: Do not abuse the REST API calls by polling requests. If you need to poll a request, then you should utilize the `coinbase_pro.socket` module instead._

### CoinbasePro.account

```python
CoinbasePro.account -> Account
```

A property that returns the `Account` instance object.

### CoinbasePro.coinbase

```python
CoinbasePro.coinbase -> Coinbase
```

A property that returns the `Coinbase` instance object.

### CoinbasePro.convert

```python
CoinbasePro.convert -> Convert
```

A property that returns the `Convert` instance object.

### CoinbasePro.currency

```python
CoinbasePro.currency -> Currency
```

A property that returns the `Currency` instance object.

### CoinbasePro.transfer

```python
CoinbasePro.transfer -> Transfer
```

A property that returns the `Transfer` instance object.

### CoinbasePro.fee

```python
CoinbasePro.fee -> Fee
```

A property that returns the `Fee` instance object.

### CoinbasePro.order

```python
CoinbasePro.order -> Order
```

A property that returns the `Order` instance object.

### CoinbasePro.oracle

```python
CoinbasePro.oracle -> Oracle
```

A property that returns the `Oracle` instance object.

### CoinbasePro.product

```python
CoinbasePro.product -> Product
```

A property that returns the `Product` instance object.

### CoinbasePro.profile

```python
CoinbasePro.profile -> Profile
```

A property that returns the `Profile` instance object.

### CoinbasePro.report

```python
CoinbasePro.report -> Report
```

A property that returns the `Report` instance object.

### CoinbasePro.user

```python
CoinbasePro.user -> User
```

A property that returns the `User` instance object.

### CoinbasePro.time

```python
CoinbasePro.time -> Time
```

A property that returns the `Time` instance object.

### CoinbasePro.key

```python
CoinbasePro.key -> str
```

A property that returns the given `API.key` property.

### CoinbasePro.name

```python
CoinbasePro.name -> str
```

A property that returns the client label.

### CoinbasePro.plug

```python
CoinbasePro.plug(cls: object, name: str)
```

A method used to attach 3rd party classes to extend the clients functionality.

_Note: This method is experimental and is subject to change._

## get_messenger

```python
get_messenger(settings: dict = None) -> Messenger
```

Return a `Messenger` a instance object.

## get_client

```python
get_client(settings: dict = None) -> CoinbasePro
```

Return a `CoinbasePro` a instance object.
