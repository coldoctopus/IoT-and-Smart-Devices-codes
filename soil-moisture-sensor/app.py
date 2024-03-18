#need to open ur browsers and go to "http://localhost:5000" or "http://127.0.0.1:5000".
#won't open automatically for u :v
#if not look like (nightlight) PS D:/... then run "activate" to activate venv
#this uses another folder's python
"""
Python 3.9.13
Flask 2.1.2 (pip install flask==2.1.2)
Werkzeug 2.2.2 (pip isntall werkzeug==2.2.2)
"""
import time, json
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
import paho.mqtt.client as mqtt
from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

adc = ADC()
relay = GroveRelay(5)

id = 'coldoctopus'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'soilmoisturesensor_client'

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,client_name) #changed cuz iuse paho-mqtt 2.0.0 || teacher rcm 1.5.1
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    if payload['relay_on']:
        relay.on()
    else:
        relay.off()

mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command

while True:
    soil_moisture = adc.read(0)
    print("Soil moisture:", soil_moisture)
    mqtt_client.publish(client_telemetry_topic, json.dumps({'soil_moisture' : soil_moisture}))

    time.sleep(10)
    