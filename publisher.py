import paho.mqtt.client as mqtt
import random
import json
from datetime import datetime

# MQTT setup for publisher
brokers = ["broker.hivemq.com"]
broker_address = brokers[0]
client = mqtt.Client("HeartRateClient_IOT_FinalProject")
port = 1883
client.connect(broker_address, port)
sub_topic = "IOT/FinalProject/HeartRate"


# Dictionary containing ID and heart rate data
data = {}


# Generate random heart rate data
def generate_heart_rate():
    for i in range(20):
        current_time = datetime.today().strftime('%H:%M:%S')
        id = random.randint(10000000, 999999999)
        rate = random.randint(55, 180)
        data[id] = [rate, current_time]
    return data


# Send data dictionary via MQTT
def send_data(topic, data):
    json_data = json.dumps(data)
    client.publish(topic, json_data)


# Continuously generate and send data
# while True:

print("Start publishing data to broker ", broker_address)
data = generate_heart_rate()
send_data(sub_topic, data)
