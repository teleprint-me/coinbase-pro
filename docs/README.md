# README

## Notes

- This library is intentionally minimalistic
- It's recommended that you familiarize your self with the [Official Documentation](https://docs.cloud.coinbase.com/exchange/docs).
- There is NO WARRANTY, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE.

## Install

```sh
virtualenv venv 
source venv/bin/activate
pip install git+https://github.com/teleprint-me/coinbase-pro.git#egg=coinbase-pro
```

## Abstract

### Overview

```sh
$ tree coinbase-pro
coinbase-pro
├── coinbase_pro
│   ├── abstract.py
│   ├── client.py
│   ├── __init__.py
│   ├── messenger.py
│   └── socket.py
├── docs
│   ├── Client.md
│   ├── Messenger.md
│   ├── Quickstart.md
│   ├── README.md
│   └── Socket.md
├── LICENSE
├── README.md
├── setup.cfg
└── setup.py

2 directories, 14 files
```

### Globals

The `coinbase_pro` library has a few abstract types and global variables which are utilized by the API implementations as well as the python `setuptools` package. These variables are defined in the `coinbase_pro.__init__` module.

### Variables

- `__agent__` defines who the request is made by
- `__source__` defines the URI pointing to the public repository
- `__version__` defines the library version
- `__timeout__` defines how long to wait before the request fails

### Types

- `List` is defined as type `list` and `list[dict]`
- `Dict` is defined as type `dict` and `List`
- `Response` is defined as type `requests.Response` and `list[requests.Response]`

_Note: All other data types utilized are built-in._


## Issues

- If you find a bug or error, then you should open an issue and report as much information as is relavent to issue you're experiencing.
- Remember to omit your API Key information.
- It's good practice to store your API Key externally from your environment.

## Contributions

- Anyone can help with the Documentation or Code Base.
    - A [GPG Signature](https://docs.github.com/en/authentication/managing-commit-signature-verification) is required to make a Pull Request.
- Leave a Tip if you would like to support this project financially.
    - I put a lot of time, effort, and energy into creating and maintaining this project.
    - Every Sat, Gwei, or Litoshi goes a long way!

## Coinbase Exchange

- Pro and Exchange are identical interfaces and only require you to modify the API URL.
- More information can be found in docs/Messenger.md.
