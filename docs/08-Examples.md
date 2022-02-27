# Examples

_Note: For clarification, `Client` is the abstract reference, `client` is the instance reference, and `CoinbasePro` is the implementation reference. I use the terms `client`, `Client`, and `CoinbasePro` interchangably. Treat them as synonyms for the sake of simplicity._

## Did you read the Quickstart?
Recommended Prerequisites in the following order:

1) `docs/01-Quickstart.md`
2) `docs/03-Messenger.md` 
3) `docs/04-Client.md`

### API Key Authentication
The `docs/01-Quickstart -> Setup` section covers how to setup your API Key for Authentication. Reference the `Setup` section if you have not setup an API Key for Authentication seeing as some of the following examples will require them.

### REST API Documentation
You must read the [Official Coinbase Documentation](https://docs.cloud.coinbase.com/exchange/docs) in order to understand the Python implementation of the API. You will need to study both the REST API, and the Python API, in order to maximize the API's full potential.

### REST API Reference
You should have the [Official Coinbase Reference](https://docs.cloud.coinbase.com/exchange/reference) open and available in order to understand what arguments are being made and why. 

In most cases, the `data` argument will be a `dict`, the keys will be the `Param`, and the values are the `Query`. This will become clearer as we go through the examples. 

## Example 1: Setting up a Messenger or Client instance

### The Messenger Instance
The `Messenger` instance is an object that wraps `requests` and returns a `requests.Response` instance. Use this object if you want full control over your requests and responses.

```python
import json

from coinbase_pro.client import get_messenger


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, "r") as file:
        data = json.load(file)
    return data


messenger = get_messenger(get_settings("settings.json")["box"])
```

_Note: This guide will soley use the `CoinbasePro` client instance object in the following examples. Referencing the `Messenger` instance directly is for developers that understand what they're doing and just want a jump start._

### The Client Instance
The client instance is a `CoinbasePro` object that can be located in the `coinbase_pro.client` module. We can start making API requests once we have a `client` instance.

```python
import json

from coinbase_pro.client import get_client
from pprint import pprint


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, "r") as file:
        data = json.load(file)
    return data


client = get_client(get_settings("settings.json")["box"])
```

## Example 2: Client is a Composition of Strategy
The `client` object is a composition of the strategy pattern. All other classes are independently defined and reference their respective scope via a method or property. The default `Subscriber` instances that make up the composition of `CoinbasePro` are defined in `docs/04-Client.md`. This means we can access a section of the API by simply referencing its identifier.

### The Client, Subscriber, and Method model
Let's say we're interested in procuring our order history as our first example.

The `client` object is implementing the idea that we have the following structure: `<Client>.<Subscriber>.<Method>`. The `client` instance is referencing the `order` instance. The `order` instance references the `fills` method. We are effectively implementing a structure that's easy for our brains to follow.

```python
# <Client>.<Subscriber>.<Method>
>>> client.order.fills
<bound method Order.fills of <coinbase_pro.client.Order object at 0x7fa405d60400>>
```

### The `data` parameter is always a `dict`
The `fills` method is defined in the Python API Reference as `Order.fills(data: dict) -> list[dict]`. This means that the `Order` is the `Subscriber`, `fills` is the `Method`, and `fills` requires some argument that is type `dict`. The `fills` method should also return a `list` of objects that are type `dict`. The `data` object will be a `dict` that holds a parameter and query as a set of key and value pairs.

```python
# product_id is the parameter
# "BTC-USD" is the query
# fills is the response as a list[dict]
fills = client.order.fills(dict(product_id="BTC-USD"))
```

### Reference and Implementation comparisons
This methodology makes it easy for us to compare the Python API to the actual REST API. If we go to the [Orders API Reference](https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getfills) and compare the results, then we can see that `data` is a makeup of the `Query Params` table which means that the `Responses 200` section also gives you a list of expected results. This means that the `response` instance is a `list` of `dict`'s that fit our "list of expected results".

These general ideas apply to the entire core library. It will all click into place once you get the hang of it.

### Implementing the abstract
Let's actually apply these abstract ideas and see what they do now that we have an idea of how they work.

```python
import json

from coinbase_pro.client import get_client
from pprint import pprint


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, "r") as file:
        data = json.load(file)
    return data

# set the query parameters
data = {"product_id": "BTC-USD"}

# set the client instance object
client = get_client(get_settings("settings.json")["box"])

# get the order history for fills
response = client.order.fills(data)

# output the response
pprint(response)
```

## Example 3: Putting the pieces together

### Understanding the REST API Reference
Let's say we want to get candle sticks as our next example. 

We would have to reference the `Product.candles` in order to get the information we were looking for. If we take a look at the [Get Product Candles Reference](https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproductcandles), then we can see what to expect.

On the left hand side of the page you'll see the `Products` category with `Get Product Candles` section highlighted. On the right, you'll see the following definition.

> Historic rates for a product. Rates are returned in grouped buckets. Candle schema is of the form [timestamp, price_low, price_high, price_open, price_close]

If we scroll down to the `Response Items` section and look at the `Params` sections we'll see that a `product_id` is required. We also see that we need to supply some other information as well to define the scope of our request. 

That information follows as `granularity`, `start`, and `end`. The `Details` section specifies that `if either one of the start or end fields are not provided then both fields will be ignored`, which means they're most likely optional.

Let's see if we can piece the puzzle together to get the picture we're looking for. First lets decide on our `product_id` argument. The API Reference states that it is type `str`.

```python
product_id = "BTC-USD"
```

Then we can define our params. While `start` and `end` are assumed to be optional, the API Reference explicitly states that `granularity` is required.

> The granularity field must be one of the following values: {60, 300, 900, 3600, 21600, 86400}. Otherwise, your request will be rejected.

These values can be assumed to be seconds. 60 seconds, 300 seconds, and so on. This means we have access to 1 min, 5 min, 15 min, 1 hour, 1 day, and 1 week candle sticks respectively. We also can see that the API Reference states that `granularity` is type `int`. Let's say we want the daily candle sticks.

```python
data = {"granularity": 21600}
```

### Understanding the Python API Reference
If we look at the Python API Reference, we can see that `Product.candles(product_id: str, data: dict) -> list[list]` is what we need to use and tells us what to expect in return. 

Keep in mind that the `client` instance is a composition of the REST API. It follows the form `<Client>.<Subscriber>.<Method>`. We use `client` to reference `product` and we can use `product` to reference `candles`. This gives us `client.product.candles` as a result.

We can now put the pieces to gether to finally make our request.

```python
import json

from coinbase_pro.client import get_client
from pprint import pprint


def get_settings(filename: str) -> dict:
    data = None
    with open(filename, "r") as file:
        data = json.load(file)
    return data


# set the required product id and granularity arguments
product_id = "BTC-USD"
data = {"granularity": 21600}

# get the CoinbasePro client instance object
client = get_client(get_settings("settings.json")["box"])

# make the request for getting the defined products candle sticks
candles = client.product.candles(product_id, data)

# output the response
pprint(candles)
```

## Summary
This entire process is a skill that is developed over time. Don't feel bad or stupid if you don't understand this process. It takes time, practice, and effort. Give your self credit where credit is due. The majority of people never make it to the end of any form of documentation. Make sure to experiment with snippets like these to make sure your expectations are correct. You'll eventually get the hang of it. Understanding documentation and code are the hardest parts of coding. 

So, just keep at it.

> [Give a man a fish, and you feed him for a day. Teach a man to fish, and you feed him for a lifetime.](https://quoteinvestigator.com/2015/08/28/fish/)
