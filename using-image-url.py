#using image url
import os
import sys
import time
from PIL import Image
from array import array
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

API_KEY = "YOUR_API_KEY"
ENDPOINT = "YOUR_ENDPOINT_LINK"
computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

print("===== START - Read File - remote =====")
read_image_url = "IMAGE_URL"
read_response = computervision_client.read(read_image_url,  raw=True)
read_operation_location = read_response.headers["Operation-Location"]
operation_id = read_operation_location.split("/")[-1]

while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
print()
print("===== END - Read File - remote =====")
