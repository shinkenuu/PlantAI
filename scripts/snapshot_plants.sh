#!/usr/bin/env bash
set -euo pipefail

PINOUT_FILE="plants/plants.json"
PLANT_LOG="plants/sensors.jsonl"

LOCKFILE="/tmp/plantai-snapshot.lock"
ERROR_LOG="snapshot-errors.log"

ARDUINO_POWER="uhubctl -l 1-1 -p 3"

export PATH="$HOME/.local/bin:$PATH"

cleanup() {
    $ARDUINO_POWER -a off >> "$ERROR_LOG" 2>&1
}
trap cleanup EXIT

exec 200>"$LOCKFILE"
flock -n 200 || {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Snapshot already running, skipping" >> "$ERROR_LOG"
    exit 0
}

if [ ! -f "$PINOUT_FILE" ]; then
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ERROR: $PINOUT_FILE not found" >> "$ERROR_LOG"
    exit 1
fi

if ! $ARDUINO_POWER -a on >> "$ERROR_LOG" 2>&1; then
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ERROR: Failed to power on Arduino" >> "$ERROR_LOG"
    exit 1
fi
sleep 3

if ! timeout 60 uv run plants/cli.py --pinout-path="$PINOUT_FILE" --log-path="$PLANT_LOG" 2>> "$ERROR_LOG"; then
    exit_code=$?
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ERROR: Snapshot failed (exit $exit_code)" >> "$ERROR_LOG"
    exit "$exit_code"
fi

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Snapshot completed" >> "$ERROR_LOG"
