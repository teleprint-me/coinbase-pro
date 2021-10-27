# Quickstart

For those who are impatient and want to start experimenting right away :smile:

## About

This is a quick tutorial on how to install the library and get up and running with the REST and WSS API's.

## Setup

We need to create a working directory and setup our project.

```sh
mkdir -p cbot/cbot
cd cbot
touch main.py settings.json cbot/__init__.py
virtualenv venv
source venv/bin/activate
```

## Authentication

We'll use `json` to feed our API Key to our project to keep things simple.

This is the template that the module utilizes when `pytest` is executed.
You can use this template in your projects as well if you'd like.

```json
{
    "sandbox": {
        "key": "",
        "secret": "",
        "passphrase": "",
        "authority": "https://api-public.sandbox.pro.coinbase.com"
    },
    "restapi": {
        "key": "",
        "secret": "",
        "passphrase": "",
        "authority": "https://api.pro.coinbase.com"
    },
    "websocket": {
        "authority": "wss://ws-feed.pro.coinbase.com"
    }
}
```

We will have to add our API Keys to our `settings.json` source file as we go.
Once the Secret and Passphrase are set, you will not be able to see them again.

1. [Create the Sandbox API Key](https://public.sandbox.pro.coinbase.com/profile/api) on Coinbase Pro Sandbox.
2. [Create the REST API Key](https://pro.coinbase.com/profile/api) on Coinbase Pro.
3. Add the API Keys to our `settings.json` file.

We will use our Sandbox Key for experimenting and testing purposes.
We avoid experimenting with our live account this way and can mitigate mistakes that may have been preventable otherwise.

_Obligatory Warning: Never share your API Key with any one for any reason.
If you think your API Key is compromised in any way, then you should delete it and generate a new one immediately._

_Note: Coinbase Exchange users will need to generate their own API Key on their respective platform._

## Install

We can now install the coinbase-pro library.

```sh
pip install git+https://github.com/teleprint-me/coinbase-pro.git#egg=coinbase-pro
```

We can run a pip command to see if it shows up once it's installed.

```sh
$ pip list --format=columns
Package      Version
------------ -------
coinbase-pro 2.1.1
pip          21.3.1
setuptools   58.1.0
wheel        0.37.0
```

We can also test importing the library version and see if it outputs the right version number.

```sh
$ bpython
bpython version 0.21 on top of Python 3.9.7
>>> from coinbase_pro import __version__
>>> print(__version__)
2.1.1
>>>
```

## Messenger

Messenger is just a fancy requests wrapper. 
It takes care of all the little nuances you would have to normally worry about if it didn't exist.
You'll want to use Messenger if you're intent on staying as close as possible to requests and want full control over the responses.

### API, Auth, and Messenger

Example code for manual instantiation of Messenger.

```python
from coinbase_pro.messenger import API
from coinbase_pro.messenger import Auth
from coinbase_pro.messenger import Messenger

import json


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


settings = get_settings('settings.json')
sandbox = settings['sandbox']

messenger = Messenger(Auth(API(sandbox)))

response = messenger.get('/time')
data = response.json()
print('[Response]', response)
print('[Data]', data)
```

We the get the following results when we execute our sample program.

```sh
$ python main.py
[Response] <Response [200]>
[Data] {'iso': '2021-10-27T18:00:24.216Z', 'epoch': 1635357624.216}
```

More information on API, Auth, and Messenger can be found in docs/Messenger.md.

### get_messenger

The `coinbase_pro.client` module provides a pair of functions for instantiating Messenger or Client objects.

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
bpython version 0.21 on top of Python 3.9.7
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

The Client class is a Messenger wrapper. 

The `coinbase_pro.client` module allows us to create the API, Auth, Messenger, and Client instances all in just one line of code. 

We'll see if we can get the time from the server again and this time we'll do it with the `client` instance.

```python
from coinbase_pro.client import get_client

import json


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


settings = get_settings('settings.json')
sandbox = settings['sandbox']
client = get_client(sandbox)

time = client.time.get()

print('[Response]', time)
```

We should see this output from the shell after executing our sample program.

```sh
$ python main.py
[Response] {'iso': '2021-10-27T18:15:29.194Z', 'epoch': 1635358529.194}
```

The `client` instance is a composition of other objects that delegate responsibility to the Messenger class and handles the minutia of dealing with paths and responses for you. 

All you have to do is reference the appropriate object and associated method to get the end result your expecting.

```python
from coinbase_pro.client import get_client
from pprint import pprint

import json


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


settings = get_settings('settings.json')
sandbox = settings['sandbox']
client = get_client(sandbox)

# here we get a list of available products
products = client.product.list()
# and then we get a list of our accounts
accounts = client.account.list()

print('[Products]')
pprint(products[0])
print('[Accounts]')
pprint(accounts[0])
```

The results for products after executing our sample program.

```sh
$ python main.py
[Products]
{'auction_mode': False,
 'base_currency': 'LINK',
 'base_increment': '1',
 'base_max_size': '800000',
 'base_min_size': '1',
 'cancel_only': False,
 'display_name': 'LINK/USDC',
 'fx_stablecoin': False,
 'id': 'LINK-USDC',
 'limit_only': False,
 'margin_enabled': False,
 'max_market_funds': '100000',
 'max_slippage_percentage': '0.10000000',
 'min_market_funds': '10',
 'post_only': False,
 'quote_currency': 'USDC',
 'quote_increment': '0.000001',
 'status': 'online',
 'status_message': '',
 'trading_disabled': False}
```

I'm sure you can see why something like this would be useful.

More information on Client can be found in docs/Client.md.

## Socket

There will be times when you'll want to inspect and utilize realtime data. 
This can be done with the WSS, Token, and Stream classes. 

- WSS handles the url and API Key information.
- Token is used to sign a message. 
- Stream is a websocket-client wrapper. 

This is especially useful for watching fill orders or even using live order-book information.

Let's create a `stream` instance and see how it works.

```python
from coinbase_pro.socket import WSS
from coinbase_pro.socket import Token
from coinbase_pro.socket import Stream
from coinbase_pro.socket import get_message

from pprint import pprint
from time import sleep

import json


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


print('[Init] Initializing Stream')

ticks = 0
print('[Init] Initialized Ticks')

settings = get_settings('settings.json')
restapi = settings['restapi']
restapi['authority'] = settings['websocket']['authority']
print('[Init] Initialized Settings')

message = get_message()
print('[Init] Initialized Message')

stream = Stream(Token(WSS(restapi)))
print('[Init] Initialized Stream')

print('[Connected]', stream.connect())
stream.send(message)

print('[Info] Press ^C to stop receiving')
print('[Info] Starting stream in 10 seconds')
sleep(10)

while True:
    try:
        print('[Ticks]', ticks)
        response = stream.receive()
        pprint(response)
        print('*' * 20)
        ticks += 1
    except (KeyboardInterrupt,):
        print('[Exit] Stop receiving')
        break

print('[Disconnected]', stream.disconnect())
```

Once we have our source ready, we can then execute it.

```sh
$ python main.py
[Init] Initializing Stream
[Init] Initialized Ticks
[Init] Initialized Settings
[Init] Initialized Message
[Init] Initialized Stream
[Connected] True
[Info] Press ^C to stop receiving
[Info] Starting stream in 10 seconds
[Ticks] 0
{'channels': [{'name': 'ticker', 'product_ids': ['BTC-USD']}],
 'type': 'subscriptions'}
********************
[Ticks] 1
{'best_ask': '58839.04',
 'best_bid': '58837.28',
 'high_24h': '62368.29',
 'last_size': '0.00253306',
 'low_24h': '58100',
 'open_24h': '62331.17',
 'price': '58837.28',
 'product_id': 'BTC-USD',
 'sequence': 30567736753,
 'side': 'sell',
 'time': '2021-10-27T18:51:35.465118Z',
 'trade_id': 227606504,
 'type': 'ticker',
 'volume_24h': '20278.96487655',
 'volume_30d': '423243.17814882'}
```

More information on WSS, Token, and Stream can be found in docs/Socket.md

### get_stream

You can use the `get_stream` method to shortcut building the Stream instance manually.

This is the same general idea that was applied to `get_messenger` and `get_client`.

We'll refactor our Stream sample to reflect this.

```python
from coinbase_pro.socket import get_stream
from coinbase_pro.socket import get_message

from pprint import pprint
from time import sleep

import json


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


print('[Init] Initializing Stream')

ticks = 0
print('[Init] Initialized Ticks')

settings = get_settings('settings.json')
restapi = settings['restapi']
restapi['authority'] = settings['websocket']['authority']
print('[Init] Initialized Settings')

message = get_message()
print('[Init] Initialized Message')

stream = get_stream(restapi)
print('[Init] Initialized Stream')

print('[Connected]', stream.connect())
stream.send(message)

print('[Info] Press ^C to stop receiving')
print('[Info] Starting stream in 10 seconds')
sleep(10)

while True:
    try:
        print('[Ticks]', ticks)
        response = stream.receive()
        pprint(response)
        print('*' * 20)
        ticks += 1
    except (KeyboardInterrupt,):
        print('[Exit] Stop receiving')
        break

print('[Disconnected]', stream.disconnect())
```

We should get the same result as before when we execute the sample code.

## Notes

This was only meant to be primer to showcase the tools available and how they might be utilized in extremely simple scenarios.
There's more that it can do and that just depends on what you're planning on building.

If you want to learn more, then be sure to dive deeper into the docs/.

It's also highly recommended that you go over the [Official Documentation](https://docs.cloud.coinbase.com/exchange/docs) for better familiarity. 
Without it, you won't know how to properly supply arguments for the Messenger, Client, or Stream object instances.

I may add a longer tutorial series on implementing a averaging bot at some point in the future. Until then, enjoy!
