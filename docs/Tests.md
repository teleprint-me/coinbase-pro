# Tests

## About

Run tests on the coinbase_pro module

_Note: Some tests may be skipped.
The test may be private, not implemented, or the sandbox does not support it.
If the sandbox does not support the test, then the test results in a internal server error._

## Run modular tests

To run a test on a individual module

```sh
pytest -x tests/test_api.py
```

To run a test on a individual module with private endpoints

```sh
pytest -x tests/test_auth.py --private
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
