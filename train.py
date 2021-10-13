#!/usr/bin/python3
# -*- coding: utf-8 -*-


import tensorflow as tf
print (tf.__version__)

#!rm -rf bkgmodel_cp* bkgmodel.h5 bkgmode.png
#!/usr/bin/python3

import datetime
import json
import os
import pathlib
CHECKPOINT=250
EPOCHS=2000
class CustomCallback(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
                keys = list(logs.keys())
                #print("End epoch {} of training; got log keys: {}".format(epoch, keys))
                if os.path.exists("stoptrain"):
                        os.unlink("stoptrain")
                        self.model.stop_training = True
                        cpname = str("bkgmodel_cp{0:05}.h5".format(epoch))
                        self.model.save(cpname)
                epoch += 1
                if ((CHECKPOINT is not None) and ((epoch % CHECKPOINT)==0) and (epoch != EPOCHS)):
                  print ("CHECKPOINT")
                  cpname = str("bkgmodel_cp{0:05}.h5".format(epoch))
                  self.model.save(cpname)
                  """
                  try:
                      response = s3_client.upload_file(cpname, "bradgoodman-aiml", cpname)
                  except ClientError as e:
                      logging.error(e)
                  """

image_size=(180,180)
batch_size=320
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
        'saved_images',
        target_size=image_size,
        subset='training',
        batch_size=batch_size,
                                color_mode='grayscale',
        class_mode='sparse')
val_ds = val_ds.flow_from_directory(
        'saved_images',
        target_size=image_size,
        batch_size=batch_size,
                                color_mode='grayscale',
        subset='validation',
        class_mode='sparse')

j = sorted(train_ds.class_indices,key=lambda y: y)
json.dump (j,open('bkgmodel_classes.json','w'))
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
#tf.keras.layers.Dropout(0.1),
tf.keras.layers.Conv2D(32, (3,3), strides=2, padding="same"),
tf.keras.layers.MaxPooling2D((2, 2)),
tf.keras.layers.Conv2D(32, (3,3), strides=2),
tf.keras.layers.MaxPooling2D((2, 2)),
#tf.keras.layers.Conv2D(32, (3,3), strides=2),
#tf.keras.layers.MaxPooling2D((2, 2)),
#x = tf.keras.layers.BatchNormalization()(x)
#x = tf.keras.layers.Activation("relu")(x)
tf.keras.layers.Flatten(),
#tf.keras.layers.Dropout(0.05),
tf.keras.layers.Dense(32, activation="relu"), #32
tf.keras.layers.Dense(6, activation="softmax"),
#x = tf.keras.layers.Dense(2, activation="softmax")(x)
])
#model = tf.keras.Model(inputs,x)

"""
Original ESPCam Fashion MINST model
        layers.Conv2D(6, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(6, kernel_size=(3, 3), activation="relu"),
        layers.Flatten(), 

        # Output- Layer
        layers.Dense(num_classes, activation="softmax"),
"""

log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

model.compile(
    #optimizer=tf.keras.optimizers.Adam(1e-6), #5
    optimizer=tf.keras.optimizers.SGD(lr=0.005, decay=1e-6, momentum=0.6, nesterov=True),
    #optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.1),
    #loss="binary_crossentropy",
    loss="sparse_categorical_crossentropy",
    metrics=["sparse_categorical_accuracy"],
)
model.summary()
if os.path.isfile("bkgmodel_continue.h5"):
    os.rename("bkgmodel_continue.h5","bkgmodel_lastcontinue.h5")
    model = tf.keras.models.load_model("bkgmodel_lastcontinue.h5")
    print ("Continuing training....")
history=model.fit(train_ds, epochs=EPOCHS, validation_data=val_ds, callbacks=[tensorboard_callback,CustomCallback()])
model.save("bkgmodel.h5",save_format='h5')
print (train_ds.class_indices)

"""# Plot Results"""

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
print (history.history.keys())
# summarize history for accuracy
fig, axs = plt.subplots(2)
fig.suptitle("Accuracy and Loss - No Dropout")
axs[0].plot(history.history['sparse_categorical_accuracy'])
axs[0].plot(history.history['val_sparse_categorical_accuracy'])
#axs[0].set_title('model accuracy')
axs[0].set_ylabel('accuracy')
axs[0].set_xlabel('epoch')
axs[0].legend(['train', 'test'], loc='upper left')
#axs[0].savefig("accuracy.png")
#axs[0].show()
# summarize history for loss
axs[1].plot(history.history['loss'])
axs[1].plot(history.history['val_loss'])
#axs[1].set_title('model loss')
axs[1].set_ylabel('loss')
axs[1].set_xlabel('epoch')
axs[1].legend(['train', 'test'], loc='upper left')
#axs[1].show()
fig.savefig("bkgmodel.png")
fig.show()


for x in history.history.keys():
  print ("HISTORY of ",x)
  print (history.history[x])
  print (", ".join(history.history.keys()))
  for x in range (0,len(history.history[list(history.history.keys())[0]])):
    t=[]
    for k in history.history.keys():
      t.append(str(history.history[k][x]))
    print (", ".join(t))

model.save("bkgmodel.h5")
json.dump (j,open('bkgmodel_classes.json','w'))


"""# Quantize the model
The next step is to quantize the model so that we can use it on the ESP32-CAM. This step is very important. Therefore, we will generate a representative dataset. In this way, we can classify images directly on the ESP32-CAM:

    Use the "quantize.py" script instead 
"""

"""
def representative_data_gen():
  for input_value in tf.data.Dataset.from_tensor_slices(train_images).batch(1).take(100):
    yield [input_value]


converter = tf.lite.TFLiteConverter.from_saved_model('./bkgmodel')
converter.optimizations = [tf.lite.Optimize.DEFAULT]

converter.representative_dataset = representative_data_gen
tflite_model = converter.convert()
tflite_model_size = open('./bkgmodel.tflite', "wb").write(tflite_model)
print("Quantized model is %d bytes" % tflite_model_size)
"""

"""You can find more details about how to use quantization with Tensroflow here. Now our machine learning model is ready and we can use it with ESP32-CAM. Before using it, it is necessary to export it:"""

#!apt-get -qq install xxd
#!xxd -i "./bkgmodel.tflite" > "./bkgmodel_quant.cc"
#!cat "./mnist_model_quant.cc"
