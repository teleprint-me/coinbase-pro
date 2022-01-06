# README

## Contents

- 00-README.md
- 01-Quickstart.md
- 02-Abstract.md
- 03-Messenger.md
- 04-Client.md
- 05-Socket.md
- 06-Tests.md

## Install

### Local

```sh
pip install --user git+https://github.com/teleprint-me/coinbase-pro.git#egg=coinbase-pro
```

### Global

```sh
pip install git+https://github.com/teleprint-me/coinbase-pro.git#egg=coinbase-pro
```

### Development

```sh
git clone git@github.com:teleprint-me/coinbase-pro.git
cd coinbase-pro
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
touch main.py
cp tests/settings.json.example settings.json
pytest -x            # run public tests
pytest -x --private  # run public and private tests
```

- Use `flake8` for linting
- Use `black` for formatting
- Use `pytest` for testing
- Use `make` for building
- Use `git` for Branches, Tags, and Pull Requests
- Add your handle to Contributors.md

## Notes

- This library is intentionally minimalistic
- It's recommended that you familiarize your self with the [Official Documentation](https://docs.cloud.coinbase.com/exchange/docs).
- There is NO WARRANTY, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE.

## Issues

- Open an issue If you find a bug or error. 
- Report as much information as is relavent to issue you're experiencing.
- Remember to omit your API Key information.
- It's good practice to store your API Key externally from your environment.

## Contributions

- Leave a Tip
    - Every Satoshi goes a long way!
- Anyone can help with the Documentation or Code Base.
    - A [GPG Signature](https://docs.github.com/en/authentication/managing-commit-signature-verification) is required to make a Pull Request.

## Coinbase Exchange

- Pro and Exchange are identical interfaces and only require you to modify the API URL.
- More information can be found in 01-Quickstart.md.
