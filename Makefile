env:
	virtualenv venv
	source venv/bin/activate

setup:
	pip install -r requirements.txt

test_public:
	pytest -x

test_private:
	pytest -x --private

build:
	python -m build .

install:
	python setup.py install

uninstall:
	pip uninstall coinbase-pro

clean:
	rm -rfv .pytest_cache/ dist/ coinbase_pro.egg-info/ coinbase_pro/__pycache__ tests/__pycache__
