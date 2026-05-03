WORKDIR="/home/shinkenuu/Projects/PlantAI/"
SENSOR_READING_FILE_PATH="sensor_readings.jsonl"

cd $WORKDIR
uv run plants/cli.py --pins-path="plants/pins.json"
