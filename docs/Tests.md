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
```

Add both your Sandbox and REST API keys to the settings file

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


- The `.gitignore` file is set to ignore `main.py`, `settings.json`, and `settings.ini`.
- If a `settings.json` file does not exist, then the test suite will default to the `tests/settings.json.example` file.
- If a `settings.json` file does exist, then the test suite will use that file instead.
- You can run tests locally once you have configured your `settings.json` file. 

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
