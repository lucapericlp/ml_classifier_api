from fastai.vision import *
from io import BytesIO
from abc import ABC, abstractmethod
from errors import ValidationException, ERROR_CODES
from PIL import Image
import numpy as np
from sklearn.preprocessing import scale

'''
We use ABC and abstractmethod here since the implementation of the prediction and the output
is going to have to be different according to which third party library is being used since 
we're going to be using both fast.ai and scikit learn but we abstract that complexity away so that
the learner can be treated in a uniform way in the API route.
'''

class GeneralLearner(ABC):
	def __init__(self):
		super().__init__()

	@abstractmethod
	def predict(self, data):
		pass

	@abstractmethod
	def output(self):
		pass

class ScikitLearner(GeneralLearner):
	def __init__(self, learner):
		self.learner = learner

	def predict(self, img_bytes):
		img = None
		try:
			# Perform image preprocessing to achieve target characteristics before predicting
			img = Image.open(BytesIO(img_bytes)).convert("L").resize((28,28),Image.ANTIALIAS)
			img = np.array(img, dtype="float64").flatten()
			assert img.shape == (784,)
			img = img.reshape(1,-1)
			img = scale(img,axis=1)
			
			losses = (self.learner.predict_proba(img)).flatten()
			return self.output(losses)
		except:
			err = 5
			raise ValidationException({
				"error":{"code":err, "message":ERROR_CODES[err]},
				"status_code":400
			})

	def output(self, losses):
		classes = [i for i in range(0,10)]
		return {"predictions": sorted(
				zip(classes, map(float, losses)),
				key=lambda p: p[1],
				reverse=True
		)}


class FastAILearner(GeneralLearner):
	def __init__(self,learner):
		self.learner = learner

	def predict(self, img_bytes):
		img = None
		try: 
			img = open_image(BytesIO(img_bytes))
		except:
			err = 5
			raise ValidationException({
				"error":{"code":err, "message":ERROR_CODES[err]},
				"status_code":400
			})

		_,_,losses = self.learner.predict(img)
		return self.output(losses)

	def output(self,losses):
		return {"predictions": sorted(
			zip(self.learner.data.classes, map(float, losses)),
			key=lambda p: p[1],
			reverse=True
		)}