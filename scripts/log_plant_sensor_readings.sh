WORKDIR="/home/shinkenuu/Projects/PlantAI/"
SENSOR_READING_FILE_PATH="sensor_readings.log"

cd $WORKDIR
uv run python plants/sensor_reader.py
