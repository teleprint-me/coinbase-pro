# Messenger

## About

The `coinbase_pro.messenger` module is a lower level `requests` wrapper. You can use it avoid handling the nuances of creating authenticated requests while retaining fine-tuned control over those requests.

- This module defines the `API`, `Auth`, `Messenger`, and `Subscriber` classes. 
- The `Subscriber` class is used to define the `Client` interface. 
- The `Subscriber` class can also be used to inherit from the `Messenger` class to define an extension or plugin for the `Client` implentation.

## Import

```python
from coinbase_pro.messenger import API
from coinbase_pro.messenger import Auth
from coinbase_pro.messenger import Messenger
from coinbase_pro.messenger import Subscriber
```

## API

```python
API(settings: dict = None)
```

The API class defines the REST API URI path utilized by Messenger.

### API.settings

```python
API.settings -> dict
```

A read-only property containing the key, secret, passphrase, rest api, and feed api. This property defaults to a dict containing a empty str for key, secret, and passphrase. The rest and feed properties default to Coinbase Pro URI's.

_Note: 01-Quickstart.md shows how to implement this with an example._

### API.key

```python
API.key -> str
```

A read-only property representing the given Key.

### API.secret

```python
API.secret -> str
```

A read-only property representing the given Secret.

### API.passphrase

```python
API.passphrase -> str
```

A read-only property representing the given Passphrase.

### API.rest

```python
API.rest -> str
```

A read-only property that returns the root domain being used.

This property defaults to https://api.pro.coinbase.com

### API.feed

```python
API.feed -> str
```

A read-only property that returns the root domain being used.

This property defaults to wss://ws-feed.pro.coinbase.com

### API.verison

```python
API.version -> int
```

A read-only property that returns the REST API Version number.

### API.path

```python
API.path(value: str) -> str
```

A method that returns the URI path to be used.

### API.url

```python
API.url(value: str) -> str
```

A method that returns the full URL to be used during a request.

## Auth

```python
Auth(api: API = None)
```

The Auth class defines the REST API Authentication method utilized by Messenger.

### Auth.\_\_call__

```python
Auth.__call__(request: PreparedRequest) -> PreparedRequest
```

Auth is a callable object that returns a `PreparedRequest` instance object.

The callable instance `auth()` returns the authentication headers for the target REST API.

### Auth.api

```python
Auth.api -> API
```

A read-only property that returns the given API instance object.

### Auth.signature

```python
Auth.signature(message: str) -> bytes
```

A method that returns a signed message.

### Auth.header

```python
Auth.header(timestamp: str, message: str) -> dict
```

A method that returns the signed header which is injected into the given request.

## Messenger

```python
Messenger(auth: Auth = None)
```

The Messenger class defines the requests adapter.

_Warning: Do not abuse the REST API calls by polling requests. If you need to poll a request, then you should utilize the `coinbase_pro.sockets` module instead._

### Messenger.auth

```python
Messenger.auth -> Auth
```

A read-only property that returns the Auth instance object being used to authenticate requests.

### Messenger.api

```python
Messenger.api -> API
```

A read-only property that returns the API instance object being used to create requests.

### Messenger.session

```python
Messenger.session -> Session
```

A read-only property that returns the Session instance object being used to create requests.

### Messenger.timeout

```python
Messenger.timeout -> int
```

A read-only property that returns the number of seconds to wait before timing out a given request.

### Messenger.get

```python
Messenger.get(path: str, data: dict = None) -> Response
```

A method that returns a `Response` instance object created by `Messenger.session.get()`.

### Messenger.post

```python
Messenger.post(path: str, data: dict = None) -> Response
```

A method that returns a `Response` instance object created by `Messenger.session.post()`.

### Messenger.put

```python
Messenger.put(path: str, data: dict = None) -> Response
```

A method that returns a `Response` instance object created by `Messenger.session.put()`.

### Messenger.delete

```python
Messenger.delete(path: str, data: dict = None) -> Response
```

A method that returns a `Response` instance object created by `Messenger.session.delete()`.

### Messenger.page

```python
Messenger.page(path: str, data: dict = None) -> list
```

A method that returns a `Response` instance object created by `Messenger.session.get()`.

_Note: This method will always return a `list` of `Response` objects._

### Messenger.close

```python
Messenger.close()
```

A method that calls the `Messenger.session.close()` method.

## Subscriber

```python
Subscriber(messenger: Messenger)
```

The Subscriber is utilized by inheriting classes that define scoped methods utilized by the Client class.

_Note: 01-Quickstart.md shows how to implement this with an example._

### Subscriber.messenger

```python
Subscriber.messenger -> Messenger
```

A read-only property that returns the given Messenger instance object.

### Subscriber.error

```python
Subscriber.error(response: Response) -> bool
```

A method that returns `True` if the `response.status_code` is not `200`, otherwise it returns `False`.
