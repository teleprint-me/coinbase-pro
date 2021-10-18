# Socket

## About

The `coinbase_pro.socket` module is a `websocket-client` wrapper. It simplifies websocket connections made to the WSS API by handling the nuances for you.


## Import

```python
from coinbase_pro.socket import Token
from coinbase_pro.socket import Stream
```

## Token

```python
Token(key: str, secret: str, passphrase: str)
```

- Create a Auth Token for receiving realtime account related information.

_Note: Auth `Token` is not required to create a `Stream` instance._

### Token.\_\_call\_\_

```python
Token.__call__() -> dict
```

- Return authentication information to be injected into the message during `websocket` initialization.

### Token.signature

```python
Token.signature(message: str) -> bytes
```

- Sign the given message and return the signed message as a `bytes` instance

## Stream

```python
Stream(auth: Token = none, url: str = None, trace: bool = False)
```

- The `Stream` class defines the `websocket-client` adapter.

_Note: Stream.url defaults to wss://ws-feed.pro.coinbase.com._

### Stream.connected

```python
Stream.connected -> bool
```

- A read-only property that returns `True` if the `websocket` is connected else `False`

### Stream.connect

```python
Stream.connect -> bool
```

- A method that creates a `websocket` connection and returns `True` on success else `False` on failure.

### Stream.send

```python
Stream.send(message: dict) -> None
```

- A method that sends the `websocket` initialization message to the WSS Feed.

### Stream.receive

```python
Stream.receive() -> dict
```

- A method that receives responses from the WSS Feed.

_Note: You'll want to poll this method while you have an active connection._

### Stream.ping

```python
Stream.ping() -> None
```

- A method that keeps the connection alive.

_Note: This method blocks and should not be polled._

### Stream.disconnect

```python
Stream.disconnect() -> bool
```

- A method that disconnects from the WSS Feed and returns `True` if the connection is closed, else `False`.

## get_default_message

```python
get_default_message() -> dict
```

- Get the default message for websocket initialization

## get_message

```python
get_message(value: dict = None) -> dict
```

- Get the default message for websocket initialization or return the given value as message
