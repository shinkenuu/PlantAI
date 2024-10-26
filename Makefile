clean-cache:
	find . | grep pycache | xargs rm -r

test:
	pytest -vvv -m "not arduino"

test-carie:
	DEEPEVAL_TELEMETRY_OPT_OUT="YES" deepeval test run tests/plantai/agents/test_carie.py -vv

lint:
	ruff check . --fix