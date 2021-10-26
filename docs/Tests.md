# Tests

## About

Run tests on the coinbase_pro module

_Note: Some tests may be skipped.
The test may be private, not implemented, or the sandbox does not support it.
If the sandbox does not support the test, then the test results in a internal server error._

## Setup

First install pytest and dateutils packages

```sh
pip install pytest dateutils
```

Then copy the settings example provided in the tests dir

```sh
cp tests/settings.json.example settings.json

Add both your Sandbox and REST API keys to the settings file

```json
{
    "uri": {
        "sandbox": "https://api-public.sandbox.pro.coinbase.com",
        "restapi": "https://api.pro.coinbase.com",
        "websocket": "wss://ws-feed.pro.coinbase.com"
    },
    "sandbox": {
        "key": "sandbox_key",
        "secret": "sandbox_secret",
        "passphrase": "sandbox_passphrase"
    },
    "restapi": {
        "key": "restapi_key",
        "secret": "restapi_secret",
        "passphrase": "restapi_passphrase"
    }
}
```

Then edit the settings function in the tests/conftest.py file

```python
32 @pytest.fixture(scope='module')
33 def settings() -> dict:
34    data = dict()
# change line 35 from
35    with open('tests/settings.json.example', 'r') as file:
# to
35    with open('settings.json', 'r') as file:
```

Now you can run tests locally. 

The `.gitignore` file is set to ignore `main.py`, `settings.json`, and `settings.ini`.

## Run modular tests

To run a test on a individual module

```sh
pytest tests/test_public.py
```

Use the `-x` option to fail fast

```sh
pytest -x tests/test_public.py
```

To run a test on a individual module with private endpoints

```sh
pytest -x tests/test_private.py --private
```

## Run all tests

To run all tests with public endpoints

```sh
pytest
```

To run all tests with public and private endpoints

```sh
pytest --private
```
