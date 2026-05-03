WORKDIR="/home/shinkenuu/Projects/PlantAI/"
SENSOR_READING_FILE_PATH="sensor_readings.jsonl"

cd $WORKDIR
uv run plants/cli.py read-plants-sensors --pins-path="plants/pins.json"
