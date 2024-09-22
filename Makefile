clean-cache:
	find . | grep pycache | xargs rm -r

tests:
	pytest -vvv -m "not arduino"

tests-all:
	pytest -vvv

lint:
	ruff check . --fix