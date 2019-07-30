import base64
import requests
import json

with open("sample_images/4.png" , "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    r = requests.post('http://localhost:8080/api/v1/classify/numbers',
    	data = json.dumps({"classifier":"RNN" ,"b64":encoded_string}))
    result = r.json()
    print(result)
