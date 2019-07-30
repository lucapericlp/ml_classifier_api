#Onfido Technical Task


Using Httpie, sending a request with a URL and classifier choice to endpoint 
```bash
http --json POST localhost:8080/api/v1/classify/numbers url=http://datawrangling.s3.amazonaws.com/sample_digit.png classifier=RNN
```

Sending a base64 image using Python3:
See local_image_request.py


API Docs
if __name__ == '__main__':
    assert sys.argv[-1] in ("run", "schema"), "Usage: example.py [run|schema]"

    if sys.argv[-1] == "run":
        uvicorn.run(app, host='0.0.0.0', port=8000)
    elif sys.argv[-1] == "schema":
        schema = schemas.get_schema(routes=app.routes)
        print(yaml.dump(schema, default_flow_style=False))