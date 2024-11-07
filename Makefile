clean-cache:
	find . | grep pycache | xargs rm -r

test-plants:
	pytest -vvv tests/plants -m "not arduino"

test-agents:
	DEEPEVAL_TELEMETRY_OPT_OUT="YES" deepeval test run tests/plantai/agents -vv

lint:
	ruff check . --fix