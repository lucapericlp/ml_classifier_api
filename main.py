from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.schemas import SchemaGenerator
from io import BytesIO
import asyncio, base64, uvicorn
from fastai.vision import *

import factory
from utilities import *

app = Starlette(debug=True)

@app.route("/api/v1/classify/numbers", methods=["POST"])
async def classify_numbers(request):
	"""
    responses:
      200:
        description: Return list of class predictions for input image.
        examples:
          [{"classifier": "RNN"}, {"url": "http://datawrangling.s3.amazonaws.com/sample_digit.png"}]
    """
    
    # Validate and extract fields of interest from the POST request
	data = await request.json()
	chosen_classifier, img_bytes = None, None
	try:
		chosen_classifier, img_bytes = await validate_and_extract(data,VALID_CLASSIFIERS.keys())

		learner,response = VALID_CLASSIFIERS[chosen_classifier],None
		response = learner.predict(img_bytes)
		return JSONResponse(response)
	except ValidationException as e:
		return JSONResponse(str(e), e.status_code)

if __name__ == '__main__':
	global VALID_CLASSIFIERS
	VALID_CLASSIFIERS = {
		"RNN":factory.create_rnn(),
		"CNN":None,
		"SVM":None
	}

	uvicorn.run(app, host='0.0.0.0', port=8080)