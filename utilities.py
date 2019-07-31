from errors import *
import aiohttp, asyncio, base64

'''
Raising of errors should be delegated to any dedicated functions like parse_request()
(since they can be used in multiple places). Be frugal with function wrapping for the purpose
of error raising (depends on where the function is most likely to be used and how frequently). 
Also prioritise logical symmetry like how try block could be delegated to get_bytes()
but was not to maintain logical symmetry within the validate_and_extract 'if' block and 
it is unlikely for it to be used outside of the parent function.
'''

async def get_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

async def parse_request(request):
	try:
		return await request.json()
	except:
		err = 6
		raise ValidationException({
				"error":{"code":err, "message":ERROR_CODES[err]},
				"status_code":400
			})

async def validate_and_extract(data,valid_classifiers):
	if "classifier" in data and data["classifier"] is not None and data["classifier"] in valid_classifiers:
		chosen_classifier = data["classifier"]
	else:
		err = 1
		raise ValidationException({
			"error":{"code":err, "message":ERROR_CODES[err]},
			"status_code":400
		})

	img_bytes = None
	if "b64" in data and data["b64"] is not None:
		try:
			img_b64 = bytes(data["b64"],"utf-8")
			img_bytes = base64.b64decode(img_b64)
		except:
			err = 2
			raise ValidationException({
				"error":{"code":err, "message":ERROR_CODES[err]},
				"status_code":400
			})
	elif "url" in data and data["url"] is not None:
		try:
			img_bytes = await get_bytes(data["url"])
		except:
			err = 3
			raise ValidationException({
				"error":{"code":err, "message":ERROR_CODES[err]},
				"status_code":400
			})

	else:
		err = 4
		raise ValidationException({
			"error":{"code":err, "message":ERROR_CODES[err]},
			"status_code":400
		})

	return chosen_classifier, img_bytes