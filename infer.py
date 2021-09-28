#!/usr/bin/python3

import tensorflow as tf
import os,sys,json
import datetime
import cgi
import socket

filename=None
socket_name = "./infer_socket"
#filename="saved_images/five/img-004efa84b919487aa1ff507e4d25b4eb.jpg"

def infer(filename):
	img = tf.keras.preprocessing.image.load_img(
			filename, target_size=image_size
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
	for (i,x) in enumerate(predictions[0]):
		j[classes[i]] = float(x)
	return json.dumps(j)

if len(sys.argv) > 1:
	filename = sys.argv[1]

form = cgi.FieldStorage()

if 'filename' in form:
	filename = form['filename'].value
image_size=(180,180)
batch_size=2
input_shape = image_size+(3,)

model = tf.keras.models.load_model("bkgmodel")
#model.summary()
classes=json.load(open("classes.json"))

if filename is None:
	print("Sercing")
	# Make sure the socket does not already exist
	try:
			os.unlink(socket_name)
	except OSError:
			if os.path.exists(socket_name):
					raise
	# Create a UDS socket
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	sock.bind(socket_name)

	# Listen for incoming connections
	sock.listen(1)

	while True:
			# Wait for a connection
			print ("Awiating connection")
			connection, client_address = sock.accept()
			try:
				data = connection.recv(256)
				print ("GOT",data)
				try:
					result=infer(data)
				except BaseException as e:
					result=str(e)
				connection.sendall(result.encode('utf-8'))
				connection.close()
				print ("Sent: {}".format(result))
			except BaseException as e:
				print ("ERROR",e)
				pass
		
else:
	infer(filename)

#for filename in sys.argv[1:]:
