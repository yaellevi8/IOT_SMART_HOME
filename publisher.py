import paho.mqtt.client as mqtt
import random
import json
from datetime import datetime
import time


# MQTT setup for publisher
def setup():
    brokers = ["broker.hivemq.com"]
    broker_address = brokers[0]
    client = mqtt.Client("HeartRateClient_IOT_FinalProject")
    port = 1883
    print("Starts publishing data to broker ", broker_address)
    client.connect(broker_address, port)
    return client


# Generate random heart rate data
def generate_heart_rate(id):
    data = {}
    time.sleep(2)
    current_time = datetime.today().strftime('%H:%M:%S')
    if id == 0:
        id = random.randint(100000000, 999999999)
    rate = random.randint(50, 180)
    data[id] = [rate, current_time]
    return data


# Send data dictionary via MQTT
def send_data(topic, data, client):
    json_data = json.dumps(data)
    client.publish(topic, json_data)


def generate_heart_rate_and_publish(client_id):
    client = setup()
    # Continuously generate and send data
    while True:
        sub_topic = "IOT/FinalProject/HeartRate"
        data = generate_heart_rate(client_id)
        send_data(sub_topic, data, client)

