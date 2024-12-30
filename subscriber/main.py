import paho.mqtt.client as mqtt
import pymongo
import json
import time


# MongoDB Configuration
# MONGO_URI = "mongodb+srv://uns:uns123@unifiednamespace.zzmac.mongodb.net/?retryWrites=true&w=majority&appName=unifiednamespace"
MONGO_URI="mongodb://admin:password@mongodb:27017"
DB_NAME = "unified_namespace"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

# MQTT Broker Configuration
BROKER = "emqx"
PORT = 1883

# MQTT Callback Functions
def on_connect(mqtt_client, userdata, flags, rc):
    print("Connected with result code", rc)
    mqtt_client.subscribe("cocacola/#")

def on_message(mqtt_client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload.decode())
    collection_name = topic.split("/")[-1]  # Use the last part of the topic as the collection name
    print(topic)
    print(payload)
    print(collection_name)
    
    db[collection_name].insert_one(payload)
    print(f"Data stored in MongoDB collection: {collection_name}")

# MQTT Client Setup
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
time.sleep(20)  # Wait 10 seconds before attempting to connect
mqtt_client.connect(BROKER, PORT, 60)
mqtt_client.loop_forever()