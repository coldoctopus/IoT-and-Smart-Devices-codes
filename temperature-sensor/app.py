#need to open ur browsers and go to "http://localhost:5000" or "http://127.0.0.1:5000".
#won't open automatically for u :v
#if not look like (nightlight) PS D:/... then run "activate" to activate venv

"""
Python 3.9.13
Flask 2.1.2 (pip install flask==2.1.2)
Werkzeug 2.2.2 (pip isntall werkzeug==2.2.2)
"""
import time, json
from counterfit_shims_seeed_python_dht import DHT
import paho.mqtt.client as mqtt

from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

sensor = DHT("11", 5)

id = 'coldoctopus'
client_name = id + 'temperature_sensor_client'
client_telemetry_topic = id + '/telemetry'
#server_command_topic = id + '/commands'

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

"""
def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    if payload['led_on']:
        led.on()
    else:
        led.off()

mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command
"""
print("MQTT connected!")

while True:
    _, temp = sensor.read()
    print(f'Temperature {temp}°C')
    
    telemetry = json.dumps({'temperature' : temp})
    print("Sending telemetry ", telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)
    
    time.sleep(60*2)

    
    

    

    

