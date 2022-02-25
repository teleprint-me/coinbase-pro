# Development

## Issues
- Open an issue if you find a bug or error.
- Open an issue if you want to start a discussion for a proposal or make a proposal
- Report as much information as is relavent to the issue you're experiencing.
- Remember to omit your API Key information. 

_Note: It's good practice to store your API Key externally from your environment._

## Contributions
- Anyone can help with the Documentation or Code Base.
- A [GPG Signature](https://docs.github.com/en/authentication/managing-commit-signature-verification) is required to make a Pull Request.
- If a test is missing or a modification is not accounted for in a test, then a test should be added to challenge the integrity of that modification.
- All public and private tests must pass before a PR is accepted. Breaking changes will not be accepted or merged into the main branch until tests are accounted for and passing.

## Pull Requests

### Community Input
A stricter approach will be applied when it comes to the core `coinbase_pro` module while a more relaxed approach will be applied to plugins. If a valid argument with a concrete model is proposed, then steps can be taken to make adjustments as needed.

### Plugin
Plugins were added to compensate for extensibility. You are free to make a pull request if you want to publish your plugin and make it available with the module. 

If your plugin is a single file, then you're free to add it to the plugin module as is with the name of the module being the name of your plugin. 

If your plugin is more than one file, then you should create a self contained module with the name of the directory being the name of your plugin and all other source files located within that module.

### Guidlines

- The code should be consice, clean, and readable
- The class, its methods and properties, should be self contained
- Prefer composition over inheritence when possible
- Tests must be added to challenge the integrity of the plugin
- You are expected to maintain your own plugin module as well as tracking issues that are related to your plugin module
- (Optional) Add your name or handle to the Contributors.md
- All tests should be passing before sumbitting a PR. You may submit a broken PR if you're looking for community feedback or help with your plugin.
- Treat everyone respectfully; We're all human beings too.

## Setup

```sh
git clone git@github.com:teleprint-me/coinbase-pro.git
cd coinbase-pro
pip install --user pipx
pipx install poetry
poetry shell         # run virtualenv
poetry install       # install deps and dev-deps
touch main.py        # create a scratch pad
cp tests/settings.json.example settings.json
pytest -x            # run public tests
pytest -x --private  # run public and private tests
poetry build         # create a build
deactivate           # exit virtualenv
```

_Note: You can find more information about [poetry commands](https://python-poetry.org/docs/cli/) at their [official docs](https://python-poetry.org/docs/)._

### Requirements
- Use `flake8` for linting
- Use `black` for formatting
- Use `pytest` for testing
- Use `poetry` for building and packaging
- Use `git` for Branches, Tags, and Pull Requests
- Add your handle to Contributors.md

_Note: `flake8`, `black`, and `pytest` are included in the `pyproject.toml`. They are installed automatically as dependecies when `poetry install` is executed. A `.flake8` config is included with the repository for local development._