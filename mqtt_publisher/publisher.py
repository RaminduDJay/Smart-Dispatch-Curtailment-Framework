import time
import json
import yaml
import random
import paho.mqtt.client as mqtt

def load_config():
    with open("configs/device_config.yaml", "r") as file:
        return yaml.safe_load(file)

def simulate_modbus_data():
    return {
        "voltage": round(random.uniform(220.0, 240.0), 2),
        "current": round(random.uniform(4.0, 6.0), 2),
        "power": round(random.uniform(0.8, 1.2), 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def main():
    config = load_config()
    client = mqtt.Client()
    client.connect(config["mqtt"]["broker"], config["mqtt"]["port"], 60)

    while True:
        data = simulate_modbus_data()
        payload = {
            "device_id": config["device_id"],
            "data": data
        }
        client.publish(config["mqtt"]["topic"], json.dumps(payload))
        print(f"Published: {json.dumps(payload)}")
        time.sleep(config["modbus"]["interval_seconds"])

if __name__ == "__main__":
    main()
