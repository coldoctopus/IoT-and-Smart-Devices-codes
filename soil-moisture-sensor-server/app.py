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
import threading


id = 'coldoctopus'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'soilmoisturesensor_server'

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,client_name) #changed cuz iuse paho-mqtt 2.0.0 || teacher rcm 1.5.1
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

water_time = 5
wait_time = 20

def send_relay_command(client, state):
    command = { 'relay_on' : state }
    print("Sending message:", command)
    client.publish(server_command_topic, json.dumps(command))

def control_relay(client):
    print("Unsubscribing from telemetry")
    mqtt_client.unsubscribe(client_telemetry_topic)

    send_relay_command(client, True)
    time.sleep(water_time)

    send_relay_command(client, False)
    time.sleep(wait_time)

    print("Subscribing to telemetry")
    mqtt_client.subscribe(client_telemetry_topic)

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    if payload['soil_moisture'] > 450:
        threading.Thread(target=control_relay, args=(client,)).start()

""" old version!!!
def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    command = { 'relay_on' : payload['soil_moisture'] > 450 }
    print("Sending message:", command)

    client.publish(server_command_topic, json.dumps(command))
"""

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)