import time
import random
import yaml
import json

def simulate_modbus_data():
    return {
        "voltage": round(random.uniform(220.0, 240.0), 2),
        "current": round(random.uniform(4.0, 6.0), 2),
        "power": round(random.uniform(0.8, 1.2), 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def load_config():
    with open("configs/device_config.yaml", "r") as file:
        return yaml.safe_load(file)

def read_and_print():
    config = load_config()
    while True:
        data = simulate_modbus_data()
        print(f"[{config['device_id']}] Data: {json.dumps(data)}")
        time.sleep(config["modbus"]["interval_seconds"])

if __name__ == "__main__":
    read_and_print()
