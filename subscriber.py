import paho.mqtt.client as mqtt
import json
import tkinter as tk
from datetime import datetime

# MQTT setup for subscriber
brokers = ["broker.hivemq.com"]
broker_address = brokers[0]
client = mqtt.Client("HeartRateSubscriber_IOT_FinalProject")
print("Connecting to broker ", broker_address)
port = 1883
client.connect(broker_address, port)
sub_topic = "IOT/FinalProject/HeartRate"
client.subscribe(sub_topic)

# Create GUI
root = tk.Tk()
root.geometry("800x600")
root.title("Heart Rate Monitor")

# Create listbox
listbox = tk.Listbox(root)
listbox.pack()
listbox.config(width=100, height=100,font=("calibri",20),fg="white",bg="brown")
listbox.insert(tk.END, "Heart Rate of "+ str(datetime.today().strftime('%Y-%m-%d')))
listbox.insert(tk.END, "----------------------------------------------------------------------")
listbox.insert(tk.END, "Remember - a high heart rate is a heart rate over 80")
listbox.insert(tk.END, "----------------------------------------------------------------------")


# Callback function for incoming messages
def on_message(client, userdata, message):
    data = json.loads(message.payload.decode())
    for id, rate in data.items():
        if rate > 80:
            listbox.insert(tk.END, "Id: " + str(id) + " has a HIGH heart rate: " + str(rate))


client.on_message = on_message

# Continuously listen for incoming data
client.loop_start()
root.mainloop()