#!/usr/bin/python3

import tensorflow as tf
import os,sys,json
import datetime
import glob
import argparse
import numpy as np


def infer(filename):
	img = tf.keras.preprocessing.image.load_img(
			filename, target_size=image_size, grayscale=True
	)
	#print (img)
	#print (dir(img))
	img_array = tf.keras.preprocessing.image.img_to_array(img)
	#print (img_array)
	#print (dir(img_array))
	#print ("ORIG",img_array.shape)
	img_array = tf.expand_dims(img_array, 0)  # Create batch axis
	#print ("EXPANDED",img_array.shape)

	predictions = model.predict(img_array)
	#print (dir(model))
	#print(filename,predictions)
	#print (predictions[0])
	#print (len(predictions[0]))
	j = {}
	#print (predictions[0][1])

	return (predictions[0])
	"""
	for (i,x) in enumerate(predictions[0]):
	j[classes[i]] = round(float(x)*100,2)
	return json.dumps(j)
"""

def max_index(l):
    max=0
    idx=None
    for (i,v) in enumerate(l):
        if idx is None or v>max:
            max=v
            idx = i
    return i


parser = argparse.ArgumentParser(description='Run training on images.')
parser.add_argument('--model', default="bkgmodel", help='Base name for model files')
parser.add_argument('--imagedir', default="saved_images", help='root directory of categorized images')
args = parser.parse_args()
image_size=(180,180)
batch_size=2
input_shape = image_size+(3,)

model = tf.keras.models.load_model("{}.h5".format(args.model))
classes=json.load(open("{}_classes.json".format(args.model)))
idxes = {}
for (i,c) in enumerate(classes):
    idxes[c] = i


cm = np.zeros(shape=(len(classes),len(classes)))

counts = np.zeros(shape=(len(classes)))

for (ci,c) in enumerate(classes):  
    for f in glob.glob(os.path.join(args.imagedir,c,"img-z*.jpg")):
        #print (ci,c,f)
        scores =  infer(f)
        #print (scores)
        #print (cm)
        cm[ci] += scores
        #print ()
        counts[ci] +=1

cm /= counts
cm *= 100
print (cm)

print ("{:15s} ".format(""),end="")
for i in range(len(classes)):
        print ("{: >8s} ".format(classes[i]),end="")
print ("")
for i in range(len(classes)):
    print ("{:15s} ".format(classes[i]),end="")
    for x in range(len(classes)):
        print ("{: >8.2f} ".format(cm[i][x]),end="")
    print ("")


