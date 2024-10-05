clean-cache:
	find . | grep pycache | xargs rm -r

test:
	pytest -vvv -m "not arduino"

test-all:
	pytest -vvv

lint:
	ruff check . --fix