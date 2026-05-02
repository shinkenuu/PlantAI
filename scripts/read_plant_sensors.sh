WORKDIR="/home/shinkenuu/Projects/PlantAI/"
SENSOR_READING_FILE_PATH="sensor_readings.log"

cd $WORKDIR
uv run python plants/io/collector.py >> $SENSOR_READING_FILE_PATH 2>&1
