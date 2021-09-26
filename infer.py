#!/usr/bin/python3

import tensorflow as tf
import os,sys
import datetime

filename="saved_images/five/img-004efa84b919487aa1ff507e4d25b4eb.jpg"
if len(sys.argv) > 1:
	filename = sys.argv[1]

image_size=(180,180)
batch_size=2
input_shape = image_size+(3,)

model = tf.keras.models.load_model("bkgmodel")
model.summary()

for filename in sys.argv[1:]:
	img = tf.keras.preprocessing.image.load_img(
			filename, target_size=image_size
	)
	#print (img)
	#print (dir(img))
	img_array = tf.keras.preprocessing.image.img_to_array(img)
	#print (img_array)
	#print (dir(img_array))
	print ("ORIG",img_array.shape)
	img_array = tf.expand_dims(img_array, 0)  # Create batch axis
	print ("EXPANDED",img_array.shape)

	predictions = model.predict(img_array)
	print(filename,predictions)
