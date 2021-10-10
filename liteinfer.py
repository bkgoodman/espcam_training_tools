#!/usr/bin/python3

# https://towardsdatascience.com/a-basic-introduction-to-tensorflow-lite-59e480c57292
import tensorflow as tf
import os,sys,json
import datetime
import cgi
import argparse
import numpy as np

filename=None
#filename="saved_images/five/img-004efa84b919487aa1ff507e4d25b4eb.jpg"

def infer(filename,classes):
	img = tf.keras.preprocessing.image.load_img(
			filename, target_size=image_size, grayscale=True
	)
	#print (img)
	#print (dir(img))
	img_array = tf.keras.preprocessing.image.img_to_array(img)
	#print (img_array)
	#print (dir(img_array))
	print ("ORIG",img_array.shape)
	#img_array = tf.expand_dims(img_array /1.0, 0)  # Create batch axis
	img_array= np.array(np.expand_dims(img_array/1.0,0), dtype=np.uint8)
	print ("IMAGE_ARRAY type",img_array.dtype)
	print ("EXPANDED",img_array.shape)

	#predictions = model.predict(img_array)
	interpreter = tf.lite.Interpreter(model_path="bkgmodel_quant.tflite")
	interpreter.resize_tensor_input(0, [1, 180, 180, 1])
	interpreter.allocate_tensors()
	print ("INPUT TENSOR",interpreter.get_input_details())
	print ("OUTPUT TENSOR",interpreter.get_output_details())
	input = interpreter.tensor(interpreter.get_input_details()[0]["index"])
	output = interpreter.tensor(interpreter.get_output_details()[0]["index"])
	#input().fill(1.)
	print ("IMAGE_ARRAY type",img_array.dtype)
	interpreter.set_tensor(0, img_array)
	v=interpreter.invoke()
	answers = output()
	print ()
	print (filename)
	for i in range(0,len(classes)):
		print ("{} {}".format(classes[i],answers[0][i]))
	"""
	print (v)
	print (dir(v))
	print (type(v))
	"""
	#print (dir(model))
	#print(filename,predictions)
	#print (predictions[0])
	#print (len(predictions[0]))
	"""
	j = {}
	#print (predictions[0][1])
	for (i,x) in enumerate(predictions[0]):
		j[classes[i]] = round(float(x)*100,2)
	return json.dumps(j)
	"""


classes=json.load(open("bkgmodel_classes.json"))
for filename in sys.argv[1:]:

	"""
	"""

	image_size=(180,180)
	batch_size=2
	input_shape = image_size+(3,)

	infer(filename,classes)

#for filename in sys.argv[1:]:
