# Abstract

## Globals

The `coinbase_pro` library has a few abstract types and global variables which are utilized by the API implementations as well as the python `setuptools` package. These variables are defined in the `coinbase_pro.__init__` module.

## Variables

- `__agent__` defines who the request is made by
- `__source__` defines the URI pointing to the public repository
- `__version__` defines the library version
- `__limit__` defines the amount of time to block a given request

## Classes

### Overview

The Abstract Base Interfaces implemented for the modules `messenger`, `client`, and `socket` respectively. There are nuances in each of the REST API and WSS API implementations which cause some differences to occur. Any differences that do occur will be noted and or outlined to clarify what they are based on implementation.

### AbstractAPI


```python
AbstractAPI()
```

AbstractAPI defines the REST API Key and URI utilized by AbstractMessenger.

### AbstractAuth

```python
AbstractAuth(api: AbstractAPI = None)
```

AbstractAuth defines the REST API Authentication methods utilized by AbstractMessenger.

### AbstractMessenger

```python
AbstractMessenger(auth: AbstractAuth = None)
```

AbstractMessenger defines the requests adapter utilized to facilitate communication with the REST API.

### AbstractSubscriber

```python
AbstractSubscriber(messenger: AbstractMessenger)
```

AbstractSubscriber is utilized by inheriting classes that define scoped methods utilized by AbstractClient.

### AbstractClient

```python
AbstractClient(messenger: AbstractMessenger)
```

AbstractClient defines the AbstractMessenger adapter utilized to facilitate communication with the REST API. 

### AbstractWSS

```python
AbstractWSS()
```

AbstractWSS defines the WSS API Key and URI utilized by WSS API.

### AbstractToken

```python
AbstractToken(wss: AbstractWSS = None)
```

AbstractToken defines the WSS API Authentication methods utilized by AbstractStream.

### AbstractStream

```python
AbstractStream(token: AbstractToken = None)
```

AbstractStream defines the websocket-client adapter utilized to facilitate communication with the WSS API.
