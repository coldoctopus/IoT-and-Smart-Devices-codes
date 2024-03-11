#need to open ur browsers and go to "http://localhost:5000" or "http://127.0.0.1:5000".
#won't open automatically for u :v
#if not look like (nightlight) PS D:/... then run "activate" to activate venv

"""
Python 3.9.13
Flask 2.1.2 (pip install flask==2.1.2)
Werkzeug 2.2.2 (pip isntall werkzeug==2.2.2)
"""
import json
import time

import paho.mqtt.client as mqtt

from os import path
import csv
from datetime import datetime

id = 'coldoctopus'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'temperature_sensor_server'

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,client_name) #changed cuz iuse paho-mqtt 2.0.0 || teacher rcm 1.5.1
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

temperature_file_name = 'temperature.csv'
fieldnames = ['date', 'temperature']

if not path.exists(temperature_file_name):
    with open(temperature_file_name, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    with open(temperature_file_name, mode='a') as temperature_file:        
        temperature_writer = csv.DictWriter(temperature_file, fieldnames=fieldnames)
        temperature_writer.writerow({'date' : datetime.now().astimezone().replace(microsecond=0).isoformat(), 'temperature' : payload['temperature']})


mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(1)