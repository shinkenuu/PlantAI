clean-cache:
	find . | grep pycache | xargs rm -r

test-plants:
	uv run pytest -vvv tests/plants -m "not arduino"

test-agents:
	DEEPEVAL_TELEMETRY_OPT_OUT="YES" uv run deepeval test run tests/plantai/agents -vv

.PHONY: setup-cron
setup-cron:
	@(crontab -l 2>/dev/null | grep -v collector; echo "*/10 * * * * cd $(PWD) && uv run python plants/io/collector.py >> sensor_readings.log 2>&1") | crontab -
	@echo "Cron job installed (every 10 min):"
	@crontab -l | grep collector

.PHONY: remove-cron
remove-cron:
	@crontab -l 2>/dev/null | grep -v collector | crontab - 2>/dev/null
	@echo "Cron job removed"

.PHONY: view-log
view-log:
	@if [ -f sensor_readings.log ]; then tail -f sensor_readings.log; else echo "sensor_readings.log not found yet"; fi

lint:
	uv tool run ruff check . --fix
	uv tool run ruff format .
