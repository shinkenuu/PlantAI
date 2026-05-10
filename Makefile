clean-cache:
	find . | grep pycache | xargs rm -r

test-plants:
	uv run pytest -vvv tests/plants -m "not arduino"

test-agents:
	DEEPEVAL_TELEMETRY_OPT_OUT="YES" uv run deepeval test run tests/plantai/agents -vv

.PHONY: setup-cron
setup-cron:
	@(crontab -l 2>/dev/null | grep -v snapshot_plants; echo "*/10 * * * * cd $(PWD) && scripts/snapshot_plants.sh") | crontab -
	@echo "Cron job installed (every 10 min):"
	@crontab -l | grep snapshot_plants

.PHONY: remove-cron
remove-cron:
	@crontab -l 2>/dev/null | grep -v snapshot_plants | crontab - 2>/dev/null
	@echo "Cron job removed"

.PHONY: view-log
view-log:
	@if [ -f plants/sensors.jsonl ]; then tail -f plants/sensors.jsonl; else echo "plants/sensors.jsonl not found yet"; fi

lint:
	uv tool run ruff check . --fix
	uv tool run ruff format .
	uv tool run ty check .
