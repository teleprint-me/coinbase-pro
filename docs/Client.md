# Client

## About

The `coinbase_pro.client` module is a higher level wrapper that abstracts requests made by the `Auth` and `Messenger` objects. You can use it to avoid handling the nuances of the `Messenger` object while retaining fine-tuned control over requests.

- This module utilizes the strategy pattern to implement the REST API
- The `Subscriber` class is used to define the `Client` properties interfaces. 
- The `Subscriber` class can also be used to inherit from the `Messenger` class to define an extension or plugin for the `Client` implentation.

_Note: Plugins are currently unsupported at the moment.  I plan on adding a `Client.plug` method to the class to attach custom objects to the `client` instance._

## Import

You can manually create the `Messenger` and `Client` instances

```python
from coinbase_pro.messenger import API
from coinbase_pro.messenger import Auth
from coinbase_pro.messenger import Messenger
from coinbase_pro.client import Client
```

You can automate creating the `Messenger` and `Client` instances

```python
from coinbase_pro.client import get_messenger
from coinbase_pro.client import get_client
```

_Note: You will only need to instantiate a `Client` object in most cases. You can do this by utilizing the `get_client` function._

## Account

```python
Account(messenger: Messenger)
```
### Account.list

```python
Account.list() -> list
```

- A method that returns a list of accounts.

### Account.get

```python
Account.get(account_id: str) -> dict
```

- A method that returns information for a single account. 

### Account.holds

```python
Account.holds(account_id: str, data: dict = None) -> list
```

- A method that returns a list of holds on an account.

### Account.ledger

```python
Account.ledger(account_id: str, data: dict = None) -> list
```

- A method that returns a list of ledger activity on an account.

### Account.transfers

```python
Account.transfers(account_id: str, data: dict = None) -> list
```

- A method that returns a list of withdrawals and deposits for an account.

## Coinbase

```python
Coinbase(messenger: Messenger)
```
- A class definition for communicating with [Coinbase](https://coinbase.com)

### Coinbase.wallets

```python
Coinbase.wallets() -> list
```

- A method that returns a list of Coinbase wallets.

### Coinbase.generate_address

```python
Coinbase.generate_address(account_id: str) -> dict
```

- A method that returns a one-time crypto deposit address.

### Coinbase.deposit_from

```python
Coinbase.deposit_from(data: dict) -> dict
```

- Deposit funds from a Coinbase wallet to a specified `profile_id`.

### Coinbase.withdraw_to

```python
Coinbase.withdraw_to(data: dict) -> dict
```

- Withdraw funds from a specified `profile_id` to a Coinbase wallet.

## Convert

### Convert.post

```python
Convert.post(data: dict) -> dict
```

- Converts funds from `from` currency to `to` currency. Funds are converted on the `from` account in the `profile_id` profile.

### Convert.get

```python
Convert.get(conversion_id: str) -> dict
```

- Gets a currency conversion by id (i.e. USD -> USDC).

## Currency

### Currency.list

```python
Currency.list() -> list
```

- Gets a list of all known currencies.

### Currency.get

```python
Currency.get(currency_id: str) -> dict
```

- Gets a single currency by id.

## Transfer

### Transfer.deposit_from

```python
Transfer.deposit_from(data: dict) -> dict
```

- Deposits funds from a linked external payment method to the specified profile_id.

### Transfer.methods

```python
Transfer.methods() -> list
```

- Gets a list of the user's linked payment methods.

### Transfer.list

```python
Transfer.list() -> list
```

- Gets a list of in-progress and completed transfers of funds in/out of any of the user's accounts.

### Transfer.get

```python
Transfer.get(transfer_id: str) -> dict
```

- Get information on a single transfer.

### Transfer.withdraw_to_address

```python
Transfer.withdraw_to_address(data: dict) -> dict
```

- Withdraws funds from the specified profile_id to an external crypto address.

### Transfer.withdraw_estimate

```python
Transfer.withdraw_estimate(data: dict = None) -> dict
```

- Gets the fee estimate for the crypto withdrawal to crypto address.

### Transfer.withdraw_to

```python
Transfer.withdraw_to(data: dict = None) -> dict
```

- Withdraws funds from the specified profile_id to a linked external payment method.

## Order
## Oracle
## Product
## Profile
## Report
## User
## Time

## Client

```python
Client(messenger: Messenger)
```

- The `Client` class defines the `Messenger` adapter and it's associated property objects.

_Warning: Do not abuse the REST API calls by polling requests. If you need to poll a request, then you should utilize the `coinbase_pro.socket` module instead._

_Note: Coinbase Exchange users will need to modify the `Messenger.api.url` property to point to https://api.exchange.coinbase.com_.

### Client.account

```python
Client.account -> Account
```

- A property that returns the `Account` instance object.

### Client.coinbase

```python
Client.coinbase -> Coinbase
```

- A property that returns the `Coinbase` instance object.

### Client.convert

```python
Client.convert -> Convert
```

- A property that returns the `Convert` instance object.

### Client.currency

```python
Client.currency -> Currency
```

- A property that returns the `Currency` instance object.

### Client.transfer

```python
Client.transfer -> Transfer
```

- A property that returns the `Transfer` instance object.

### Client.order

```python
Client.order -> Order
```

- A property that returns the `Order` instance object.

### Client.oracle

```python
Client.oracle -> Oracle
```

- A property that returns the `Oracle` instance object.

### Client.product

```python
Client.product -> Product
```

- A property that returns the `Product` instance object.

### Client.profile

```python
Client.profile -> Profile
```

- A property that returns the `Profile` instance object.

### Client.report

```python
Client.report -> Report
```

- A property that returns the `Report` instance object.

### Client.user

```python
Client.user -> User
```

- A property that returns the `User` instance object.

### Client.time

```python
Client.time -> Time
```

- A property that returns the `Time` instance object.

## get_messenger

```python
get_messenger(key: str = None,
              secret: str = None,
              passphrase: str = None) -> Messenger
```

- Return a `Messenger` a instance object.

## get_client

```python
get_client(key: str = None,
           secret: str = None,
           passphrase: str = None) -> Client
```

- Return a `Client` a instance object.
