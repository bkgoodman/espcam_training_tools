#!/usr/bin/python3

import tensorflow as tf
import datetime
import argparse
import json
import os
import pathlib

DATADIR='saved_images'
MODELNAME='bkgmodel'
HISTORYFILE=None
EPOCHS=50
CHECKPOINT=None
CLASSESFILENAME="bkgmodel_classes.json"
class CustomCallback(tf.keras.callbacks.Callback):
	def on_epoch_end(self, epoch, logs=None):
		keys = list(logs.keys())
		print("End epoch {} of training; got log keys: {}".format(epoch, keys))
		print ("LOGS",dir(logs))
		print ("SELF",dir(self))
		epoch += 1
		if ((CHECKPOINT is not None) and ((epoch % CHECKPOINT)==0) and (epoch != EPOCHS)):
			print ("CHECKPOINT")
			cpname = str(pathlib.Path(MODELNAME).with_suffix(''))+"_cp{0:05}.h5".format(epoch)
			self.model.save(cpname)
		if os.path.exists("stoptrain"):
			os.unlink("stoptrain")
			self.model.stop_training = True

if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Run Training")
	parser.add_argument('--data', dest='data', default=DATADIR,
                    help='Directory for training data')
	parser.add_argument('--model', dest='model', default=MODELNAME,
                    help='Resulting Module directory (or file if .h5)')
	parser.add_argument('--epochs', dest='epochs', default=EPOCHS,
                    help='Max epochs',type=int)
	parser.add_argument('--checkpoint', dest='checkpoint', default=None,
                    help='Checkpoint interval',type=int)
	parser.add_argument('--history', dest='history', default=None,
                    help='History File')
	parser.add_argument('--classes', dest='classes', default=None,
                    help='Classes File')
	args = parser.parse_args()
	DATADIR = args.data
	MODELNAME = args.model
	EPOCHS = args.epochs
	if args.history is None:
		HISTORYFILE = pathlib.Path(MODELNAME).stem+"_history.json"
	else:
		HISTORYFILE=args.history
	if args.classes is None:
		CLASSESFILENAME = pathlib.Path(MODELNAME).stem+"_classes.json"
	else:
		CLASSESFILENAME=args.classes
	CHECKPOINT = args.checkpoint

	image_size=(180,180)
	batch_size=4
	input_shape = image_size+(1,)

	train_ds = tf.keras.preprocessing.image.ImageDataGenerator(
					#rescale=1./255,
					shear_range=0.2,
					zoom_range=0.2,
					validation_split=0.2,
					rotation_range=20)
	val_ds = tf.keras.preprocessing.image.ImageDataGenerator(
					#rescale=1./255,
					shear_range=0.2,
					zoom_range=0.2,
					validation_split=0.2,
					rotation_range=20)
	train_ds = train_ds.flow_from_directory(
					DATADIR,
					target_size=image_size,
					subset='training',
					batch_size=batch_size,
					color_mode='grayscale',
					class_mode='sparse')
	val_ds = val_ds.flow_from_directory(
					DATADIR,
					target_size=image_size,
					batch_size=batch_size,
					color_mode='grayscale',
					subset='validation',
					class_mode='sparse')

	j = sorted(train_ds.class_indices,key=lambda y: y)
	json.dump (j,open(CLASSESFILENAME,'w'))
	"""
	train_ds = tf.keras.preprocessing.image_dataset_from_directory(
			"saved_images",
			validation_split=0.2,
			subset="training",
			seed=1337,
			color_mode="rgb",
			image_size=image_size,
			batch_size=batch_size,
	)
	val_ds = tf.keras.preprocessing.image_dataset_from_directory(
			"saved_images",
			validation_split=0.2,
			subset="validation",
			seed=1337,
			color_mode="rgb",
			image_size=image_size,
			batch_size=batch_size,
	)
	print (train_ds.class_names)
	"""
	model = tf.keras.Sequential([
	tf.keras.Input(shape=input_shape),
	tf.keras.layers.experimental.preprocessing.Rescaling(1./255),
	#tf.keras.layers.MaxPooling2D((2,2), strides=3, padding="same"),
	#tf.keras.layers.Conv2D(32, (2,2), padding="same"),
	#tf.keras.layers.MaxPooling2D((2,2), padding="same"),
	tf.keras.layers.Conv2D(8, (3,3), strides=1, padding="same"),
	tf.keras.layers.MaxPooling2D((2, 2)),
	tf.keras.layers.Conv2D(8, (3,3), strides=1),
	tf.keras.layers.MaxPooling2D((2, 2)),
	#x = tf.keras.layers.BatchNormalization()(x)
	#x = tf.keras.layers.Activation("relu")(x)
	tf.keras.layers.Flatten(),
	#tf.keras.layers.Dense(64, activation="relu"), #32
	tf.keras.layers.Dense(6, activation="softmax"),
	#x = tf.keras.layers.Dense(2, activation="softmax")(x)
	])
	#model = tf.keras.Model(inputs,x)


	log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
	tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

	model.compile(
			#optimizer=tf.keras.optimizers.Adam(1e-6), #5
			#optimizer=tf.keras.optimizers.SGD(lr=0.003, decay=1e-6, momentum=0.6, nesterov=True),
			optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.1),
			#loss="binary_crossentropy",
			loss="sparse_categorical_crossentropy",
			metrics=["sparse_categorical_accuracy"],
	)
	model.summary()
	history=	model.fit(train_ds, epochs=EPOCHS, validation_data=val_ds, callbacks=[tensorboard_callback,CustomCallback()])
	model.save(MODELNAME)
	print (train_ds.class_indices)
	#print ("MODEL",dir(model))
	#print ("HISOTRY KEYS",dir(history.history.keys()))
	#print ("FIT",dir(history))
	for x in history.history.keys():
		print ("HISTORY of ",x)
		print (history.history[x])
	print (", ".join(history.history.keys()))
	for x in range (0,len(history.history[list(history.history.keys())[0]])):
		t=[]
		for k in history.history.keys():
			t.append(str(history.history[k][x]))
		print (", ".join(t))
		
	
	json.dump(history.history,open(HISTORYFILE,"w"))

