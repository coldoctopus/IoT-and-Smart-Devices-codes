#need to open ur browsers and go to "http://localhost:5000" or "http://127.0.0.1:5000".
#won't open automatically for u :v
#if not look like (nightlight) PS D:/... then run "activate" to activate venv
#this uses another folder's python (u might want to use previous classes' interpreter)
"""
Python 3.9.13
Flask 2.1.2 (pip install flask==2.1.2)
Werkzeug 2.2.2 (pip isntall werkzeug==2.2.2)
"""

from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import io
from counterfit_shims_picamera import PiCamera

from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

camera = PiCamera()
camera.resolution = (640, 480)
camera.rotation = 0

image = io.BytesIO()
camera.capture(image, 'jpeg')
image.seek(0)

with open('image.jpg', 'wb') as image_file:
    image_file.write(image.read())


prediction_url = 'https://fruit-quality-detector-prediction-1.cognitiveservices.azure.com/customvision/v3.0/Prediction/9f50b41e-da61-40e6-892a-0ad0476a584a/classify/iterations/Iteration2/image'
prediction_key = '24e1973e721d4b63aa74185885d2b251'

parts = prediction_url.split('/')
endpoint = 'https://' + parts[2]
project_id = parts[6]
iteration_name = parts[9]

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(endpoint, prediction_credentials)

image.seek(0)
results = predictor.classify_image(project_id, iteration_name, image)

for prediction in results.predictions:
    print(f'{prediction.tag_name}:\t{prediction.probability * 100:.2f}%')
