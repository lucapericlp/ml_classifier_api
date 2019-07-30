from setup import *

def create_rnn():
	tfms = get_transforms(do_flip=False, max_lighting=None, 
		max_zoom=1.2, p_affine=0.5, max_warp=0.2, max_rotate=5.0)
	classes = [str(i) for i in range(0,10)]
	data = ImageDataBunch.single_from_classes('.', classes, ds_tfms=tfms, size=24).normalize(imagenet_stats)
	learn = cnn_learner(data, models.resnet18)
	learn.load('rnn_18_onfido_1')
	return FastAILearner(learn)
