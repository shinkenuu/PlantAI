clean-cache:
	find . | grep pycache | xargs rm -r

test:
	pytest -vvv

lint:
	ruff check . --fix