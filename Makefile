clean-cache:
	find . | grep pycache | xargs rm -r

test-plants:
	uv run pytest -vvv tests/plants -m "not arduino"

test-agents:
	DEEPEVAL_TELEMETRY_OPT_OUT="YES" uv run deepeval test run tests/plantai/agents -vv

lint:
	uv tool run ruff check . --fix
	uv tool run ruff format .
