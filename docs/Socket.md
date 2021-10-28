# Socket

## About

The `coinbase_pro.socket` module is a `websocket-client` adapter. 

It simplifies websocket connections made to the WSS API by handling the nuances for you.


## Import

```python
from coinbase_pro.socket import WSS
from coinbase_pro.socket import Token
from coinbase_pro.socket import Stream
from coinbase_pro.socket import get_message
from coinbase_pro.socket import get_stream
```

## WSS

```python
WSS(settings: dict = None)
```

- The WSS class defines the WSS API URI path utilized by Stream.

### WSS.key

```python
WSS.key -> str
```

- A read-only property representing the given Key.

### WSS.secret

```python
WSS.secret -> str
```

- A read-only property representing the given Secret.

### WSS.passphrase

```python
WSS.passphrase -> str
```

- A read-only property representing the given Passphrase.

### WSS.url

```python
WSS.url -> str
```

- A read-only property that returns the root domain being used.
- This property defaults to wss://ws-feed.pro.coinbase.com

### WSS.verison

```python
WSS.version -> int
```

- A read-only property that returns the WSS API Version number.

## Token

```python
Token(wss: WSS)
```
- Create a Auth Token for receiving account related realtime data.

### Token.wss

```python
Token.wss -> WSS
```

- A read-only property that returns a WSS instance object.

### Token.\_\_call__

```python
Token.__call__() -> dict
```

- Return authentication information to be injected into the message during `websocket` initialization.

### Token.signature

```python
Token.signature(timestamp: str) -> bytes
```

- A method that returns a signed message.

### Token.header

```python
Token.header(timestamp: str, signature: bytes) -> dict
```

- A method that returns a signed header.

## Stream

```python
Stream(token: Token = none)
```

- The Stream class defines the websocket-client adapter.


### Stream.token

```python
Stream.token -> Token
```

- A read-only property that returns a Token instance object.

### Stream.wss

```python
Stream.wss -> WSS
```

- A read-only property that returns a WSS instance object.

### Stream.socket

```python
Stream.socket -> WebSocket
```

- A read-write property that returns a WebSocket instance object.

### Stream.auth

```python
Stream.auth -> bool
```

- A read-only property that returns `True` if `WSS.key`, `WSS.secret`, and `WSS.passphrase` are set else `False`.

### Stream.connected

```python
Stream.connected -> bool
```

- A read-only property that returns `True` if `Stream.socket` is connected else `False`

### Stream.connect

```python
Stream.connect(trace: bool = False) -> bool
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

### Stream.disconnect

```python
Stream.disconnect() -> bool
```

- A method that disconnects from the WSS Feed and returns `True` on success else `False` on failure.

## get_message

```python
get_message() -> dict
```

- Get the default message for websocket initialization.

## get_stream

```python
get_stream(settings: dict = None) -> dict
```

- A function that returns a Stream instance object based on the given `settings` argument.
