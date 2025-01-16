from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
from datetime import datetime
import logging
import json
import os

debug_mode = os.getenv("DEBUG_DATA_FLOW") == "true"

# Configurare logger-ului pentru afisarea mesajelor in containerul adaptor
logging.basicConfig(
    level=logging.DEBUG if debug_mode else logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Conexiune baza de date InfluxDB folosind variabile de mediu
# Daca nu sunt setate, se folosesc valorile default (al doilea parametru)
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://influxdb:8086")
INFLUXDB_DB = os.getenv("INFLUXDB_DB", "iot_data")
influx_client = InfluxDBClient(host="influxdb", port=8086)
influx_client.create_database(INFLUXDB_DB)
influx_client.switch_database(INFLUXDB_DB)

# Functie de procesare a mesajelor MQTT, apleata la fiecare mesaj primit
def on_message(client, userdata, msg):
    logger.info(f"Received a message by topic [{msg.topic}]")
    
    # Decodare payload
    payload = json.loads(msg.payload.decode('utf-8'))
    timestamp = payload.get("timestamp", None)
    
    # Gestionare valorii timestamp daca nu este prezenta in payload
    if not timestamp:
        timestamp = datetime.utcnow().isoformat()

    logger.info(f"Data timestamp is: {timestamp}")

    # Datele ce vor fi introduse in baza de date
    data = []
    for key, value in payload.items():
        # Daca valoarea este un numar
        if isinstance(value, (int, float)):
            data.append({
                "measurement": f"{msg.topic.replace('/', '.')}.{key}",
                "time": timestamp,
                "fields": {"value": value} })
            logger.info(f"{msg.topic.replace('/', '.')}.{key} {value}")

    # Scrierea datelor in InfluxDB
    influx_client.write_points(data)

# Conexiune broker MQTT folosind variabile de mediu
BROKER_ADDRESS = os.getenv("BROKER_ADDRESS", "mqtt_broker")
BROKER_PORT = int(os.getenv("BROKER_PORT", 1883))
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT)
mqtt_client.subscribe("#")
mqtt_client.loop_forever()