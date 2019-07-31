from setup import *
import pickle

def create_rnn():
	# Residual Neural Network with 18 layers
	# Defining the properties that the model was trained with in order to correctly perform
	# inference. Load weights into learner and create fast.ai implementation of learner.
	tfms = get_transforms(do_flip=False, max_lighting=None, 
		max_zoom=1.2, p_affine=0.5, max_warp=0.2, max_rotate=5.0)
	classes = [str(i) for i in range(0,10)]
	data = ImageDataBunch.single_from_classes('.', classes, ds_tfms=tfms, size=24).normalize(imagenet_stats)
	learner = cnn_learner(data, models.resnet18)
	learner.load('rnn_18_onfido_1')
	return FastAILearner(learner)

def create_cnn():
	# VGG with 16 layers
	tfms = get_transforms(do_flip=False, max_lighting=None, 
		max_zoom=1.2, p_affine=0.5, max_warp=0.2, max_rotate=5.0)
	classes = [str(i) for i in range(0,10)]
	data = ImageDataBunch.single_from_classes('.', classes, ds_tfms=tfms, size=28).normalize(imagenet_stats)
	learner = cnn_learner(data, models.vgg16_bn)
	learner.load('vgg_16_bn_onfido')
	return FastAILearner(learner)	

def create_svm():
	# Linear Support Vector Machine
	learner = pickle.load(open('models/SVM_onfido.sav','rb'))
	return ScikitLearner(learner)

def create_knn():
	# K-Nearest Neighbours
	learner = pickle.load(open('models/KNearest_onfido.sav','rb'))
	return ScikitLearner(learner)

def create_rf():
	# Random Forest
	learner = pickle.load(open('models/RF_onfido.sav','rb'))
	return ScikitLearner(learner)
