## Onfido Technical Task

### API Specification
```yaml
info:
  title: ML classifier API
  version: '0.1'
openapi: 3.0.0
paths:
  /api/v1/classify/digits:
    post:
      responses:
        200:
          description: Returns JSON ordered list of class predictions for input image.
          example_requests:
          - - classifier: RNN
            - url: http://datawrangling.s3.amazonaws.com/sample_digit.png
          - or
          - - classifier: RNN
            - b64: AAAN4AAADfCAYAAACZO20SAAAABmJLR0QA/wD/AP+...
          example_response: "{\"predictions\": [[\"4\", 0.9999681711196899], [\"6\"\
            , 2.6835603421204723e-05], [\"1\", 2.648422423590091e-06], [\"7\", 1.2625563385881833e-06],\
            \ [\"2\", 4.2422348656145914e-07], [\"9\", 2.9029823167547875e-07], [\"\
            0\", 1.704291605619801e-07], [\"8\", 1.5085298343819886e-07], [\"3\",\
            \ 3.132079839929247e-08], [\"5\", 4.936829611779103e-09]]}  \n"
          parameters:
          - classifier: RNN|CNN|SVM|RF|KNN
          - url
          - b64
        400:
          description: Returns JSON with custom error code and relative description.
          example: "{\n  \"errors\": {\n    \"code\": 1,\n    \"message\": \"Invalid\
            \ or no classifier-type provided.\"\n  }\n}\n"
```

### Example usage:
First run server using Docker (and ensure port 8080 is open):
```bash
docker build -t api .
docker run -p 8080:8080 api
```

Using Httpie, sending a request with a URL and classifier choice to the local endpoint:
```bash
http --json POST localhost:8080/api/v1/classify/digits url=http://datawrangling.s3.amazonaws.com/sample_digit.png classifier=RNN
```

Using Python3, sending a request with an encoded image and classifier choice to the local endpoint: 

[local\_image\_request.py](/examples/local_image_request.py)

### Using the notebooks
Use jupyter to open and view the notebooks.

### Generate API Spec
Send a GET request to /schema endpoint. An example:

[get\_api\_spec.py](/scripts/get_api_spec.py)