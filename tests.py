import unittest, requests, base64, json

domain = 'localhost:8080'

class TestDataValidation(unittest.TestCase):
	def test_data_validation(self):
		with open("sample_images/4.png","rb") as image_file:
			encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
			
			# Valid b64 request works as intended?
			r = requests.post('http://'+domain+'/api/v1/classify/digits',
    				data = json.dumps({"classifier":"KNN" ,"b64":encoded_string}))
			result = r.json()
			assert result["predictions"]

			# Valid url request works as intended?
			r = requests.post('http://'+domain+'/api/v1/classify/digits',
    				data = json.dumps({"classifier":"KNN" ,"url":"http://datawrangling.s3.amazonaws.com/sample_digit.png"}))
			result = r.json()
			assert result["predictions"]

			# Invalid URL?
			r = requests.post('http://'+domain+'/api/v1/classify/digits',
    				data = json.dumps({"classifier":"KNN" ,"url":"http://datawrangling.s3.amazonaws.com/sample_digit123dfaf"}))
			result = r.json()
			assert result["errors"]["code"]

			# Invalid classifier?
			r = requests.post('http://'+domain+'/api/v1/classify/digits',
    				data = json.dumps({"classifier":"TNN" ,"url":"http://datawrangling.s3.amazonaws.com/sample_digit.png"}))
			result = r.json()
			assert result["errors"]["code"]

			# Invalid b64?
			r = requests.post('http://'+domain+'/api/v1/classify/digits',
    				data = json.dumps({"classifier":"CNN" ,"b64":"123"}))
			result = r.json()
			assert result["errors"]["code"]

			# No b64 or url?
			r = requests.post('http://'+domain+'/api/v1/classify/digits',
    				data = json.dumps({"classifier":"CNN"}))
			result = r.json()
			assert result["errors"]["code"]

			# No classifier?
			r = requests.post('http://'+domain+'/api/v1/classify/digits',
    				data = json.dumps({"url":"http://datawrangling.s3.amazonaws.com/sample_digit.png"}))
			result = r.json()
			assert result["errors"]["code"]

class TestModelClassification(unittest.TestCase):
	def test_model_classification(self):
		# TODO: Add more in depth error handling for model classification to be able 
		# to ensure API durability

		r = requests.post('http://'+domain+'/api/v1/classify/digits',
    				data = json.dumps({"classifier":"KNN" ,"url":"http://datawrangling.s3.amazonaws.com/sample_digit.png"}))
		result = r.json()
		assert result["predictions"][0][0] == '4'

		r = requests.post('http://'+domain+'/api/v1/classify/digits',
    				data = json.dumps({"classifier":"RNN" ,"url":"http://datawrangling.s3.amazonaws.com/sample_digit.png"}))
		result = r.json()
		assert result["predictions"][0][0] == '4'

if __name__ == "__main__":
	unittest.main()