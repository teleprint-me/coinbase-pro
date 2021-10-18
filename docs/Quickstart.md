# Quickstart

For those who are impatient and want to start experimenting right away :smile:

## About

This is a quick tutorial on how to install the library and get up and running with the REST and WSS API's.

## Setup

We need to create a working directory and setup our project.

```sh
mkdir -p cryptobot/cryptobot
cd cryptobot
touch settings.ini main.py cryptobot/__init__.py
virtualenv venv
source venv/bin/activate
```

## Authentication

The fist thing we need to do is [Create our API Key](https://pro.coinbase.com/profile/api) on Coinbase Pro.

_Note: Coinbase Exchange users will need to generate their own API Key on their respective platform._

Then we can add the API Key to our `settings.ini` file.

```ini
# settings.ini
[coinbase_pro]
key = MY_API_KEY
secret = MY_API_SECRET
passphrase = MY_API_PASSPHRASE
```

We'll use `configparser` to feed our API Key to our project. This is just to keep things simple considering there are a myriad of methods for securing your Keys. 

Keep in mind that it's probably a good idea to use GPG to encrypt and decrypt your Keys; There is no good method for storing your Keys locally. That's why it's important to protect it the best you can. If you're especially paranoid, then you can probably use some type of device to store your keys in cold storage and only apply usage when required.

_Obligatory Warning: Never share your API Key with any one for any reason. If you think your API Key is compromised in any way, then you should delete it and generate a new one immediately._

## Install

We can now install our library.

```sh
pip install git+https://github.com/teleprint-me/coinbase-pro.git#egg=coinbase-pro
```

We can run a pip command to see if it shows up once it's installed.

```sh
pip list --format=columns

# output
Package            Version
------------------ ---------
build              0.7.0
certifi            2021.10.8
charset-normalizer 2.0.7
coinbase-pro       1.0.8
idna               3.3
packaging          21.0
pep517             0.11.1
pip                21.2.4
pyparsing          2.4.7
requests           2.26.0
setuptools         58.0.4
tomli              1.2.1
urllib3            1.26.7
websocket-client   1.2.1
wheel              0.37.0
```

We can also test importing the library version and see if it outputs the right version number.

```python
# main.py
from coinbase_pro import __version__
print(__version__)
```

Then execute our script and see if it works as expected.

```sh
python main.py

# output
1.0.8
```

## Messenger

The lower level `requests` adapters can always be used in place of the `Client` class if you want to be as close as possible to the `requests` library. This library is nothing more than a not-so-fancy `requests` wrapper to make developing a bit easier.

Rate Limiting is built into the `Messenger` class and is available at the modules base import level.

```python
# main.py
from coinbase_pro import __timeout__
print(__timeout__)
```

If you run the above code, you should see that the timeout is set to a `float` value of `0.2857142857142857`. This value is calculated by taking a fractional ratio between 1 second and a `float` value of `f` representing the fractional value of `f` seconds. 

That expression is simply `__timeout__ = 1 / 3.5` which results in a number between `1/4` and `1/3` of a second. I've found this value to be ideal in most cases.

This basically means that a request will be blocked for `__timeout__` seconds for each request we make.

In our `main.py` source file, we can start importing and creating our `Auth` and `Messenger` instances. We'll also need to create a wrapper function for easy importing with `configparser`.

_Note: You may find that your program looks like it's hanging while it's making requests. If this is the case, then you should refactor your approach because you're most likely doing it in a very inefficient way._

```python
# main.py
from coinbase_pro.messenger import Auth
from coinbase_pro.messenger import Messenger

from configparser import SectionProxy
from configparser import ConfigParser


def get_proxy(section: str) -> SectionProxy:
    config = ConfigParser()
    config.read('settings.ini')
    return config[section]


proxy = get_proxy('coinbase_pro')
messenger = Messenger(Auth(proxy['key'], proxy['secret'], proxy['passphrase']))
response = messenger.get('/time')
print(response)
result = dict() if response.status_code != 200 else response.json()
print(result)
```

You should get output that looks like `<Response [200]>` from the `print(response)` expression.

```sh
# python interpreter
>>> response = messenger.get('/time')
>>> response
<Response [200]>
>>> result = response.json()
>>> result
{'iso': '2021-10-18T19:20:28.557Z', 'epoch': 1634584828.557}
```

All you'll need to supply is the `endpoint` and `data`, if any, as arguments and you'll always receive a `Response` object which is defined as type `response.Response`. The only exception to this is the `Messenger.page` method which also always returns a `Response` object and is redefined as type `list[response.Response]`.

More information on `Auth` and `Messenger` can be found in docs/Messenger.md.

_Note: You can always use the `get_messenger` function wrapper instead of manually building the `Messenger` instance yourself. This is documented in docs/Client.md._

## Client

If you prefer all the grunt work to be taken care of for you so you can focus all of your mental energy into your project, then the `Client` class is made just for you.

The `coinbase_pro.client` module allows us to create the `Auth`, `Messenger`, and `Client` instances all in just one line of code. Wait. We could do that already. It's just less typing. You can use the `get_messenger` and `get_client` functions as a shortcut to instantiate the desired object.

We'll see if we can get the time from the server again and this time we'll do it with the `Client` instance.

```python
# main.py
from configparser import SectionProxy
from configparser import ConfigParser

from coinbase_pro.client import get_client


def get_proxy(section: str) -> SectionProxy:
    config = ConfigParser()
    config.read('settings.ini')
    return config[section]


proxy = get_proxy('coinbase_pro')
client = get_client(proxy['key'], proxy['secret'], proxy['passphrase'])
time = client.time.get()
print(time)
```

The `client` object is a composition of other objects that delegate responsibility to the `Messenger` class and handles the minutia of dealing with endpoints and responses for you. 

All you have to do is reference the appropriate object and associated method to get the end result your expecting.

```python
# main.py
#
# ...code we already wrote...
#

# here we get a list of available products
products = client.product.list()
# and then we get a list of our accounts
accounts = client.account.list()
```

I'm sure you can see why something like this would be useful.

More information on `Client` can be found in docs/Client.md.

## Socket

There will be times where you'll want to inspect and utilize realtime data. This can be done with the `Token` and `Stream` classes. `Token` is used to sign a message. `Stream` is a `websocket-client` adapter that uses a optional `Token` instance to create signed messages for initializing connections.

This is especially useful for watching fill orders or even using live order-book information.

Let's create a `Token` and `Stream` instance and see what it does.

```python
# main.py
from configparser import SectionProxy
from configparser import ConfigParser

from pprint import pprint
from time import sleep

from coinbase_pro.socket import Token
from coinbase_pro.socket import Stream
from coinbase_pro.socket import get_message


def get_proxy(section: str) -> SectionProxy:
    config = ConfigParser()
    config.read('settings.ini')
    return config[section]


print('[Init] Initializing stream')

proxy = get_proxy('coinbase_pro')
stream = Stream(Token(proxy['key'], proxy['secret'], proxy['passphrase']))
message = get_message()

print('[Message]')
pprint(message)

count = 0
print('[Connected]', stream.connect())
stream.send(message)

print('[Info] Press ^C to stop receiving')
print('[Info] Starting stream in 10 seconds')
sleep(10)

while True:
    try:
        print('[Ticks]', count)
        response = stream.receive()
        pprint(response)
        print('*' * 20)
        count += 1
    except (KeyboardInterrupt,):
        print('[Exit] Stop receiving')
        break

print('[Disconnected]', stream.disconnect())
```

Once we have our source ready, we can then execute it.

```sh
python main.py
```

More information on `Token` and `Stream` can be found in docs/Socket.md

## Notes

This was only meant to be primer to showcase the tools available and how they might be utilized in extremely simple scenarios. There's more that it can do and that just depends on what you're planning on building.

If you want to learn more, then be sure to dive deeper into the docs/. 

It's also highly recommended that you go over the [Official Documentation](https://docs.cloud.coinbase.com/exchange/docs) for better familiarity. Without it, you won't know how to properly supply arguments for either of the `Messenger` or `Client` object instances.

I may add a longer tutorial series on implementing a averaging bot at some point in the future. Until then, enjoy!
