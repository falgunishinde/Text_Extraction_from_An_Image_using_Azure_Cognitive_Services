#using local image file
import os
import io
import json
import time
from array import array
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import requests
from PIL import Image, ImageDraw, ImageFont


API_KEY = "YOUR_API_KEY"
ENDPOINT = "YOUR_ENDPOINT_LINK"
computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

print("===== START - Read File - remote =====")
local_image  = './images/img1.jpg'
read_response = computervision_client.read_in_stream(open(local_image, 'rb'), language ='en', raw=True)
read_operation_location = read_response.headers["Operation-Location"]
operation_id = read_operation_location.split("/")[-1]

while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

if read_result.status == OperationStatusCodes.succeeded:
    text = ''
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
                text += line.text + ' '
                text += '\n'
        open('output.txt', 'w').write(text)
        print()
    print("Text successfully written in output file")
print()
print("===== END - Read File - remote =====")
