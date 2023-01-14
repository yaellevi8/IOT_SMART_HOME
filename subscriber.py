import paho.mqtt.client as mqtt
import json
import tkinter as tk
from datetime import datetime
import time


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
listbox.config(width=100, height=100, font=("Courier 11", 15), fg="white", bg="brown")
current_date = datetime.today().strftime('%B %d, %Y')
listbox.insert(tk.END, "Heart Rate Monitoring on " + current_date + " - Stay Alert for Heart Rate Above 80 BPM")
listbox.insert(tk.END, "")
listbox.pack()


# Callback function for incoming messages
def on_message(client, userdata, message):
    data = json.loads(message.payload.decode())
    for id, content in data.items():
        rate = int(content[0])
        sample_time = content[1]
        if rate > 80:
            listbox.insert(tk.END,
                           "ID: " + str(id) + " has a high heart rate: " + str(rate) + " | on time: " + sample_time)
        time.sleep(2)



client.on_message = on_message

# Continuously listen for incoming data
client.loop_start()
root.mainloop()