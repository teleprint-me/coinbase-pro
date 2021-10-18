# Client

## About

The `coinbase_pro.client` module is a higher level wrapper that abstracts requests made by the `Auth` and `Messenger` objects. You can use it to avoid handling the nuances of the `Messenger` object while retaining fine-tuned control over requests.

- This module utilizes the strategy pattern to implement the REST API
- The `Subscriber` class is used to define the `Client` properties interfaces. 
- The `Subscriber` class can also be used to inherit from the `Messenger` class to define an extension or plugin for the `Client` implentation.

## Import

You can manually create the `Messenger` and `Client` instances

```python
from coinbase_pro.client import Auth
from coinbase_pro.client import Messenger
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
Account.list() -> Dict
```

- A method that returns a list of accounts.

### Account.get

```python
Account.get(account_id: str) -> Dict
```

- A method that returns information for a single account. 

### Account.holds

```python
Account.holds(account_id: str, data: dict = None) -> Dict
```

- A method that returns a list of holds on an account.

### Account.ledger

```python
Account.ledger(account_id: str, data: dict = None) -> Dict
```

- A method that returns a list of ledger activity on an account.

### Account.transfers

```python
Account.transfers(account_id: str, data: dict = None) -> Dict
```

- A method that returns a list of withdrawals and deposits for an account.

## Coinbase

```python
Coinbase(messenger: Messenger)
```
- A class definition for communicating with [Coinbase](https://coinbase.com)

### Coinbase.wallets

```python
Coinbase.wallets() -> Dict
```

- A method that returns a list of Coinbase wallets.

### Coinbase.generate_address

```python
Coinbase.generate_address(account_id: str) -> Dict
```

- A method that returns a one-time crypto deposit address.

### Coinbase.deposit_from

```python
Coinbase.deposit_from(data: dict) -> Dict
```

- Deposit funds from a Coinbase wallet to a specified `profile_id`.

### Coinbase.withdraw_to

```python
Coinbase.withdraw_to(data: dict) -> Dict
```

- Withdraw funds from a specified `profile_id` to a Coinbase wallet.

## Convert
## Currency
## Transfer
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
