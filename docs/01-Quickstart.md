# Quickstart

For those who are impatient and want to start experimenting right away :smile:

## About

This is a quick tutorial on how to install the library and get up and running with the REST and WSS API's.

## Setup

We need to create a working directory and setup our project.

```sh
mkdir -p cbot/cbot
cd cbot
touch settings.json cbot/__main__.py
virtualenv venv
source venv/bin/activate
pip install -U pip
```

Expected output

```sh
$ pip list --format=columns
Package    Version
---------- -------
pip        21.3.1
setuptools 60.1.0
wheel      0.37.1
```

Expected contents

```sh
$ pwd     
/home/teleprint-me/documents/code/python/cbot
$ ls -l
total 12K
drwxr-xr-x 2 teleprint-me teleprint-me 4.0K Jan  6 02:53 cbot/
-rw-r--r-- 1 teleprint-me teleprint-me    0 Jan  6 02:58 settings.json
drwxr-xr-x 4 teleprint-me teleprint-me 4.0K Jan  6 02:54 venv/
```

## Authentication

We'll use `json` to feed our API Key to our project to keep things simple.

This is the template that the module utilizes when `pytest` is executed.
You can use this template in your projects as well if you'd like.

```json
{
    "box": {
        "key": "",
        "secret": "",
        "passphrase": "",
        "rest": "https://api-public.sandbox.pro.coinbase.com",
        "feed": "wss://ws-feed.pro.coinbase.com"
    },
    "api": {
        "key": "",
        "secret": "",
        "passphrase": "",
        "rest": "https://api.pro.coinbase.com",
        "feed": "wss://ws-feed.pro.coinbase.com"
    }
}
```

We will have to add our API Keys to our `settings.json` source file as we go.
You will not be able to see your Secret and Passphrase again once they are set.

1. [Create the Sandbox API Key](https://public.sandbox.pro.coinbase.com/profile/api) on Coinbase Pro Sandbox.
2. [Create the REST API Key](https://pro.coinbase.com/profile/api) on Coinbase Pro.
3. Add the API Keys to our `settings.json` file.

We will use our Sandbox Key for experimenting and testing purposes.
We avoid experimenting with our live account this way and can mitigate mistakes that may have been preventable otherwise.

_Obligatory Warning: Never share your API Key with any one for any reason.
If you think your API Key is compromised in any way, then you should delete it and generate a new one immediately._

### Coinbase Exchange

- Exchange users will need to generate their own API Key on their respective platform.
- Use https://api-public.sandbox.exchange.coinbase.com for sandbox 
- Use https://api.exchange.coinbase.com for rest
- Use wss://ws-feed.exchange.coinbase.com for feed

## Install

We can now install the coinbase-pro library.

```sh
$ pip install git+https://github.com/teleprint-me/coinbase-pro.git#egg=coinbase-pro
```

We can run a pip command to see if it shows up once it's installed.

```sh
$ pip list --format=columns
Package      Version
------------ -------
coinbase-pro 2.2.1
pip          21.3.1
setuptools   60.1.0
wheel        0.37.1
```

We can also test importing the library version and see if it outputs the right version number.

```sh
$ bpython            
bpython version 0.22.1 on top of Python 3.10.1
>>> from coinbase_pro import __version__
>>> print(__version__)
2.2.1
>>> 
```

### Missing `websocket-client` dependency

There is a known bug that prevents the `websocket-client` package from being installed. 
I am looking into this issue and will release a patch once I've discoverd the bug.

If you receive a `ModuleNotFoundError: No module named 'websocket'` error message, then you will have to manually install `websocket-client` instead. 

If the `websocket-client` package dependency is missing and your project requires it, then you can issue the following command to resolve the missing dependency.

```sh
pip install websocket-client
```

If you want to install a specific version (recommended), then you can issue a similar command. You can check the current `requirements.txt` in the repository to verify the package version.

```sh
$ pip install websocket-client==1.2.3
```

## Messenger

Messenger is just a fancy requests wrapper. 
It takes care of all the little nuances you would have to normally worry about if it didn't exist.
You'll want to use Messenger if you're intent on staying as close as possible to requests and want full control over the responses.

### API, Auth, and Messenger

Example code for manual instantiation of Messenger.

```python
#!/usr/bin/env python
# cbot/__main__.py
import json

from coinbase_pro.messenger import API, Auth, Messenger


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, "r") as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    settings = get_settings("settings.json")
    sandbox = settings["box"]
    messenger = Messenger(Auth(API(sandbox)))
    response = messenger.get("/time")
    data = response.json()
    print("[Response]", response)
    print("[Data]", data)
```

We the get the following results when we execute our sample program.

```sh
$ python cbot
[Response] <Response [200]>
[Data] {'iso': '2022-01-06T08:19:55.646Z', 'epoch': 1641457195.646}
```

More information on API, Auth, and Messenger can be found in docs/Messenger.md.

### get_messenger

The `coinbase_pro.client` module provides a pair of functions for instantiating Messenger or CoinbasePro objects.

You can always use the `get_messenger` function wrapper instead of manually building the Messenger instance yourself. 

We will refactor the example code we previously wrote to utilize the `get_messenger` function instead.

```python
from coinbase_pro.client import get_messenger

import json


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


settings = get_settings('settings.json')
sandbox = settings['sandbox']
messenger = get_messenger(sandbox)
response = messenger.get('/time')
data = response.json()

print('[Response]', response)
print('[Data]', data)
```

We should get the same result as before when we execute our sample program.

More information for `get_messenger` can be found in docs/Client.md.

### Rate Limiting

Rate Limiting is built into the `Messenger` class and is available at the modules base import level.

```sh
$ bpython
bpython version 0.22.1 on top of Python 3.10.1
>>> from coinbase_pro import __limit__
>>> print(__limit__)
0.2857142857142857
>>> 
```

If you run the above code, you should see that the timeout is set to a `float` value of `0.2857142857142857`. This value is calculated by taking a fractional ratio between 1 second and a `float` value of `f` representing the fractional value of `f` seconds. 

That expression is simply `__limit__ = 1 / 3.5` which results in a number between `1/4` and `1/3` of a second. I've found this value to be ideal in most cases.

This basically means that a request will be blocked for `__limit__` seconds for each request we make.

_Note: You may find that your program looks like it's hanging while it's making requests. If this is the case, then you should refactor your approach because it can most likely be rewritten to be more efficient._

## Client

The CoinbasePro class is a Messenger wrapper. 

The `coinbase_pro.client` module allows us to create the API, Auth, Messenger, and CoinbasePro instances all in just one line of code. 

We'll see if we can get the time from the server again and this time we'll do it with the `client` instance.

```python
#!/usr/bin/env python
# cbot/__main__.py
import json

from coinbase_pro.client import get_client


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, "r") as file:
        data = json.load(file)
    return data


client = get_client(get_settings("settings.json")["box"])
time = client.time.get()

print("[Response]", time)
```

Expected Output

```sh
$ python cbot
[Response] {'iso': '2022-01-06T18:47:32.678Z', 'epoch': 1641494852.678}
```

The `client` instance is a composition of other objects that delegate responsibility to the Messenger class and handles the minutia of dealing with paths and responses for you. 

All you have to do is reference the appropriate object and associated method to get the end result your expecting.

```python
#!/usr/bin/env python
# cbot/__main__.py
import json
from pprint import pprint

from coinbase_pro.client import get_client


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, "r") as file:
        data = json.load(file)
    return data


client = get_client(get_settings("settings.json")["box"])

# here we get a list of available products
products = client.product.list()
# and then we get a list of our accounts
accounts = client.account.list()

print("[Products]")
pprint(products[0])
print("[Accounts]")
pprint(accounts[0])
```

Expected Output

```sh
$ python cbot
[Products]
{'auction_mode': False,
 'base_currency': 'LINK',
 'base_increment': '1',
 'base_max_size': '55000',
 'base_min_size': '0.03',
 'cancel_only': False,
 'display_name': 'LINK/USD',
 'fx_stablecoin': False,
 'id': 'LINK-USD',
 'limit_only': False,
 'margin_enabled': False,
 'max_market_funds': '1800000',
 'max_slippage_percentage': '0.10000000',
 'min_market_funds': '1',
 'post_only': False,
 'quote_currency': 'USD',
 'quote_increment': '0.01',
 'status': 'online',
 'status_message': '',
 'trading_disabled': False}
[Accounts]
{'available': '0',
 'balance': '0.0000000000000000',
 'currency': 'BAT',
 'hold': '0.0000000000000000',
 'id': '14b3d08b-348b-4231-84b3-2c75b03f6913',
 'profile_id': 'fcada388-d6f6-47fe-8826-5afbceaf197c',
 'trading_enabled': True}
```

I'm sure you can see why something like this would be useful.

More information on CoinbasePro can be found in docs/Client.md.

## Socket

There will be times when you'll want to inspect and utilize realtime data. 
This can be done with the WSS, Token, and Stream classes. 

- WSS handles the url and API Key information.
- Token is used to sign a message. 
- Stream is a websocket-client wrapper. 

This is especially useful for watching fill orders or even using live order-book information.

Let's create a `stream` instance and see how it works.

```python
#!/usr/bin/env python
# cbot/__main__.py
import json
from pprint import pprint
from time import sleep

from coinbase_pro.socket import WSS, Stream, Token, get_message


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, "r") as file:
        data = json.load(file)
    return data


print("[Init] Initializing")
ticks = 0
message = get_message()
stream = Stream(Token(WSS(get_settings("settings.json")["api"])))
print("[Init] Initialized Stream")
print("[Connected]", stream.connect())
stream.send(message)
print("[Info] Press ^C to stop receiving")
print("[Info] Starting stream in 10 seconds")
sleep(10)

while True:
    try:
        print("[Ticks]", ticks)
        response = stream.receive()
        pprint(response)
        print("*" * 20)
        ticks += 1
        sleep(0.5)
    except (KeyboardInterrupt,):
        print("[Exit] Stop receiving")
        break

print("[Disconnected]", stream.disconnect())
```

Once we have our source ready, we can then execute it.

```sh
$ python cbot
[Init] Initializing
[Init] Initialized Stream
[Connected] True
[Info] Press ^C to stop receiving
[Info] Starting stream in 10 seconds
[Ticks] 0
{'channels': [{'name': 'ticker', 'product_ids': ['BTC-USD']}],
 'type': 'subscriptions'}
********************
[Ticks] 1
{'best_ask': '43473.92',
 'best_bid': '43470.28',
 'high_24h': '44828.74',
 'last_size': '0.00221994',
 'low_24h': '42432.99',
 'open_24h': '44665',
 'price': '43473.92',
 'product_id': 'BTC-USD',
 'sequence': 32818623264,
 'side': 'buy',
 'time': '2022-01-06T19:47:07.454980Z',
 'trade_id': 260239946,
 'type': 'ticker',
 'volume_24h': '28589.68639442',
 'volume_30d': '445085.36439028'}
********************
[Disconnected] True
```

More information on WSS, Token, and Stream can be found in docs/Socket.md

### get_stream

You can use the `get_stream` method to shortcut building the Stream instance manually.

This is the same general idea that was applied to `get_messenger` and `get_client`.

We'll refactor our Stream sample to reflect this.

```python
#!/usr/bin/env python
# cbot/__main__.py
import json
from pprint import pprint
from time import sleep

from coinbase_pro.socket import get_message, get_stream


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, "r") as file:
        data = json.load(file)
    return data


print("[Init] Initializing")
ticks = 0
message = get_message()
stream = get_stream(get_settings("settings.json")["api"])
print("[Init] Initialized Stream")
print("[Connected]", stream.connect())
stream.send(message)
print("[Info] Press ^C to stop receiving")
print("[Info] Starting stream in 5 seconds")
sleep(5)

while True:
    try:
        print("[Ticks]", ticks)
        response = stream.receive()
        pprint(response)
        print("*" * 20)
        ticks += 1
        sleep(0.5)
    except (KeyboardInterrupt,):
        print("[Exit] Stop receiving")
        break

print("[Disconnected]", stream.disconnect())
```

We should get the same result as before when we execute the sample code.

## Subscriber and CoinbasePro.plug

The `Subscriber` and `CoinbasePro` class allow you to create your own extensible classes. If we find there is not a class or method that supports a particular pattern or solution, then we can create out own instead and easily attach it to a `client` instance.

```python
#!/usr/bin/env python
# cbot/__main__.py
import json
from pprint import pprint
from time import sleep

from coinbase_pro.client import get_client
from coinbase_pro.messenger import Subscriber


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, "r") as file:
        data = json.load(file)
    return data


class History(Subscriber):
    def list_(self, data: dict) -> list:
        responses = self.messenger.page("/fills", data)
        return [r.json() for r in responses if "message" not in r.json()]


client = get_client(get_settings("settings.json")["box"])
client.plug("history", History(client.messenger))
responses = client.history.list_({"product_id": "BTC-USD", "limit": 25})
print("[History]")
pprint(responses[0][0])
```

_Note: The `CoinbasePro.plug` method is currently experimental and should improve over time. Changes should be expected as the methods implementation is improved._

## Notes

This was only meant to be primer to showcase the tools available and how they might be utilized in extremely simple scenarios.
There's more that it can do and that just depends on what you're planning on building.

If you want to learn more, then be sure to dive deeper into the docs/.

It's also highly recommended that you go over the [Official Documentation](https://docs.cloud.coinbase.com/exchange/docs) for better familiarity. 
Without it, you won't know how to properly supply arguments for the Messenger, CoinbasePro, or Stream object instances.

I may add a longer tutorial series on implementing a averaging bot at some point in the future. Until then, enjoy!
