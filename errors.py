ERROR_CODES = {
	1:"Invalid or no classifier-type provided.",
	2:"Invalid base64 string provided.",
	3:"Error retrieving and opening image via URL. Please try with another image.",
	4:"Invalid or no image URL/source provided. Valid options: base64 encoded image or full image source URL.",
	5:"Image data could not be parsed due to invalid or corrupt image data. Please try with another image.",
	6:"Invalid JSON provided and could not be parsed."
}

class ValidationException(Exception):
	def __init__(self, errors):
		self.errors = errors["error"]
		self.status_code = errors["status_code"]
	def json(self):
		return {"errors":self.errors}