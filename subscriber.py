import paho.mqtt.client as mqtt
import json
import tkinter as tk
from datetime import datetime
import time


# MQTT setup for subscriber
def setup():
    brokers = ["broker.hivemq.com"]
    broker_address = brokers[0]
    client = mqtt.Client("HeartRateSubscriber_IOT_FinalProject")
    print("Connecting to broker ", broker_address)
    port = 1883
    client.connect(broker_address, port)
    sub_topic = "IOT/FinalProject/HeartRate"
    client.subscribe(sub_topic)
    return client


def create_gui():
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Heart Rate Monitor")
    listbox = tk.Listbox(root)
    listbox.config(width=100, height=100, font=("Courier 11", 15), fg="white", bg="brown")
    current_date = datetime.today().strftime('%B %d, %Y')
    listbox.insert(tk.END, "Heart Rate Monitoring on " + current_date + " - Stay Alert for Heart Rate Above 80 BPM")
    listbox.insert(tk.END, "")
    listbox.pack()
    return root, listbox


# Callback function for incoming messages of all clients
def on_message_for_clients(client, userdata, message, listbox):
    data = json.loads(message.payload.decode())
    for id, content in data.items():
        rate = int(content[0])
        sample_time = content[1]
        if rate > 80:
            listbox.insert(tk.END,
                           "ID: " + str(id) + " has a high heart rate: " + str(rate) + " | on time: " + sample_time)
        time.sleep(2)


# Callback function for incoming messages of specific client
def on_message_for_specific_client(client, userdata, message, client_id, listbox):
    data = json.loads(message.payload.decode())
    for id, content in data.items():
        rate = int(content[0])
        sample_time = content[1]
        if id == str(client_id):
            if rate > 80:
                listbox.insert(tk.END,
                               "ID: " + str(id) + " has a high heart rate: " + str(rate) + " | on time: " + sample_time)
                # Create alert by changing the color
                listbox.itemconfig(listbox.size() - 1, {'bg': 'khaki3'})
            else:
                listbox.insert(tk.END,
                               "ID: " + str(id) + " has a high heart rate: " + str(rate) + " | on time: " + sample_time)
                listbox.itemconfig(listbox.size() - 1, {'bg': 'brown'})
        time.sleep(2)


# Continuously listen for incoming data
def subscribe(client_id):
    client = setup()
    root, listbox = create_gui()
    print("Starts displaying the heart rate dashboard")
    if client_id == 0:
        client.on_message = lambda c, u, m: on_message_for_clients(c, u, m, listbox)
    else:
        listbox.insert(tk.END,
                       "Dashboard of ID number: " + str(client_id), "")
        client.on_message = lambda c, u, m: on_message_for_specific_client(c, u, m, client_id, listbox)
    client.loop_start()
    root.mainloop()

