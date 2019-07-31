from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.schemas import SchemaGenerator
from io import BytesIO
import asyncio, base64, uvicorn
from fastai.vision import *

import factory
from utilities import *

# Define the valid classifiers and create the relative models.
global VALID_CLASSIFIERS
VALID_CLASSIFIERS = {
    "RNN":factory.create_rnn(),
    "CNN":None,
    "SVM":None
}

schemas = SchemaGenerator({"openapi": "3.0.0", "info": {"title": "ML classifier API", "version": "0.1"}})
app = Starlette()

@app.route("/api/v1/classify/digits", methods=["POST"])
async def classify_numbers(request):
    """
    responses:
      200:
        description: Return list of class predictions for input image.
        parameters:
          [{"classifier": "RNN"}, {"url": "http://datawrangling.s3.amazonaws.com/sample_digit.png"}]
        example: |
          {'predictions': [['4', 0.9999681711196899], ['6', 2.6835603421204723e-05], ['1', 2.648422423590091e-06], ['7', 1.2625563385881833e-06], ['2', 4.2422348656145914e-07], ['9', 2.9029823167547875e-07], ['0', 1.704291605619801e-07], ['8', 1.5085298343819886e-07], ['3', 3.132079839929247e-08], ['5', 4.936829611779103e-09]]}  
      400:
        description: Invalid data provided.
        example:
          Error retrieving and opening image via URL. Please try with another image.
    """
    try:
        # get the correct classifier and input data then use them to perform inference and 
        # return accordingly.
        data = await parse_request(request)
        chosen_classifier, img_bytes = await validate_and_extract(data,VALID_CLASSIFIERS.keys())

        learner,response = VALID_CLASSIFIERS[chosen_classifier],None
        response = learner.predict(img_bytes)
        return JSONResponse(response, 200)
    except ValidationException as e:
        return JSONResponse(e.json(), e.status_code)

@app.route("/schema", methods=["GET"], include_in_schema=False)
def openapi_schema(request):
    return schemas.OpenAPIResponse(request=request)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
