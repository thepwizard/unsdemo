import paho.mqtt.client as mqtt
import json
import time
import random

# MQTT Broker Configuration
BROKER = "emqx"
PORT = 1883

# Unified Namespace Topics
UNS_TOPICS = {
    "temperature": "cocacola/site_munich/filling_area_1/sensors/temperature",
    "pressure": "cocacola/site_munich/filling_area_1/sensors/pressure",
    "raw_materials": "cocacola/site_munich/filling_area_1/inventory/raw_materials",
    "orders": "cocacola/site_munich/filling_area_1/erp/orders",
    "machine_status": "cocacola/site_munich/filling_area_1/mes/machine_status"
}

def publish_temperature(client):
    """Publish temperature data."""
    temperature_data = {
        "sensor_id": "temp_001",
        "value": round(random.uniform(15.0, 25.0), 2),
        "unit": "C",
        "timestamp": time.time()
    }
    client.publish(UNS_TOPICS["temperature"], json.dumps(temperature_data))

def publish_pressure(client):
    """Publish pressure data."""
    pressure_data = {
        "sensor_id": "press_001",
        "value": round(random.uniform(1.0, 5.0), 2),
        "unit": "bar",
        "timestamp": time.time()
    }
    client.publish(UNS_TOPICS["pressure"], json.dumps(pressure_data))

def publish_raw_materials(client):
    """Publish raw material inventory data."""
    raw_materials_data = {
        "material_id": "rm_001",
        "quantity": random.randint(100, 1000),
        "unit": "kg",
        "timestamp": time.time()
    }
    client.publish(UNS_TOPICS["raw_materials"], json.dumps(raw_materials_data))

def publish_orders(client):
    """Publish ERP orders data."""
    orders_data = {
        "order_id": f"order_{random.randint(1000, 9999)}",
        "product": "bottles",
        "quantity": random.randint(500, 2000),
        "status": random.choice(["pending", "in_progress", "completed"]),
        "timestamp": time.time()
    }
    client.publish(UNS_TOPICS["orders"], json.dumps(orders_data))

def publish_machine_status(client):
    """Publish MES machine status data."""
    machine_status_data = {
        "machine_id": f"machine_{random.randint(1, 5)}",
        "status": random.choice(["running", "stopped", "breakdown"]),
        "timestamp": time.time()
    }
    client.publish(UNS_TOPICS["machine_status"], json.dumps(machine_status_data))

time.sleep(20)  # Wait 10 seconds before attempting to connect
# MQTT Client Setup
client = mqtt.Client()
client.connect(BROKER, PORT, 60)

# Simulate Continuous Publishing
try:
    print("Publishing Data.")
    while True:
        publish_temperature(client)
        publish_pressure(client)
        publish_raw_materials(client)
        publish_orders(client)
        publish_machine_status(client)
        time.sleep(5)
except KeyboardInterrupt:
    print("Publishing stopped.")
    client.disconnect()