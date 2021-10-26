#!/usr/bin/python3
# -*- coding: utf-8 -*-


import tensorflow as tf
import argparse
import numpy as np
print (tf.__version__)

#!rm -rf bkgmodel_cp* bkgmodel.h5 bkgmode.png
#!/usr/bin/python3

import datetime
import json
import os
import pathlib
CHECKPOINT=250
EPOCHS=2000
MODELNAME="bkgmodel"
IMAGE_DIRECTORY="saved_images"
INITIAL_EPOCH=1
class CustomCallback(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
                keys = list(logs.keys())
                #print("End epoch {} of training; got log keys: {}".format(epoch, keys))
                if os.path.exists("stoptrain"):
                        os.unlink("stoptrain")
                        self.model.stop_training = True
                        cpname = str("{}_cp{0:05}.h5".format(MODELNAME,epoch))
                        self.model.save(cpname)
                epoch += 1
                if ((CHECKPOINT is not None) and ((epoch % CHECKPOINT)==0) and (epoch != EPOCHS)):
                  print ("CHECKPOINT")
                  cpname = str("{}_cp{0:05}.h5".format(MODELNAME,epoch))
                  self.model.save(cpname)
                  """
                  try:
                      response = s3_client.upload_file(cpname, "bradgoodman-aiml", cpname)
                  except ClientError as e:
                      logging.error(e)
                  """
def plot_confusion_matrix(cm, class_names):
  """
  Returns a matplotlib figure containing the plotted confusion matrix.

  Args:
    cm (array, shape = [n, n]): a confusion matrix of integer classes
    class_names (array, shape = [n]): String names of the integer classes
  """
  figure = plt.figure(figsize=(8, 8))
  plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
  plt.title("Confusion matrix")
  plt.colorbar()
  tick_marks = np.arange(len(class_names))
  plt.xticks(tick_marks, class_names, rotation=45)
  plt.yticks(tick_marks, class_names)

  # Compute the labels from the normalized confusion matrix.
  labels = np.around(cm.astype('float') / cm.sum(axis=1)[:, np.newaxis], decimals=2)

  # Use white text if squares are dark; otherwise black.
  threshold = cm.max() / 2.
  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    color = "white" if cm[i, j] > threshold else "black"
    plt.text(j, i, labels[i, j], horizontalalignment="center", color=color)

  plt.tight_layout()
  plt.ylabel('True label')
  plt.xlabel('Predicted label')
  return figure




def log_confusion_matrix(epoch, logs):
  print ("Build Conf Matrix EPOCH {}".format(epoch))
  val_pred = model.predict(val_ds)
  """
  print ("VAL_PRED is", val_pred.shape)
  print (val_pred)

  print ("VAL_DS is", val_ds)
  print (dir(val_ds))
  for (i,x) in enumerate(val_ds):
        if (i==0):
            print ("FIRST VAL IS",x)
            print (dir(x))
  """
  for (i,x) in enumerate(val_pred):
        if (i%13)==0:
            print ("VAL PREDICT {:>3.0f} category {}: ".format(i,val_ds.classes[i]),end='')
            for z in range(len(class_names)):
                print ("{: >6.2f} ".format(x[z]*100),end='')
            print ("file {}".format(val_ds.filenames[i]))
  print ("DONE Conf Matrix")
  """
  # Use the model to predict the values from the validation dataset.
  test_pred_raw = model.predict(val_ds)
  test_pred = np.argmax(test_pred_raw, axis=1)

  # Calculate the confusion matrix.
  cm = sklearn.metrics.confusion_matrix(test_labels, test_pred)
  # Log the confusion matrix as an image summary.
  figure = plot_confusion_matrix(cm, class_names=class_names)
  cm_image = plot_to_image(figure)

  # Log the confusion matrix as an image summary.
  with file_writer_cm.as_default():
    tf.summary.image("Confusion Matrix", cm_image, step=epoch)
  """

# Define the per-epoch callback.
# Clear out prior logging data.
def model_summary_output(s):
    with open('{}_model.txt'.format(MODELNAME),'w+') as f:
        print(s, file=f)

parser = argparse.ArgumentParser(description='Run training on images.')
parser.add_argument('--model', default=MODELNAME, help='Base name for model files')
parser.add_argument('--epochs', default=EPOCHS, type=int, help='Number of Epochs to run')
parser.add_argument('--checkpoint', default=CHECKPOINT, type=int, help='Checkpoint every # epochs')
parser.add_argument('--batch_size', default=320, type=int, help='Batch Size')
parser.add_argument('--contfile', help='Checkpoint file to continue training from')
parser.add_argument('--images', default=IMAGE_DIRECTORY, help='root directory of categorized images')
parser.add_argument('--tbdebug', help='Enable Tensorboard Debug Data',action="store_true")
parser.add_argument('--initial_epoch', default=INITIAL_EPOCH, help='Starting epoc number (used for continuing)')
args = parser.parse_args()
EPOCHS=args.epochs
INITIAL_EPOCH=args.initial_epoch
MODELNAME=args.model
CHECKPOINT=args.checkpoint
IMAGE_DIRECTORY=args.images
batch_size=args.batch_size
image_size=(180,180)
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
        IMAGE_DIRECTORY,
        target_size=image_size,
        subset='training',
        batch_size=batch_size,
                                color_mode='grayscale',
        class_mode='sparse')
val_ds = val_ds.flow_from_directory(
        IMAGE_DIRECTORY,
        target_size=image_size,
        batch_size=batch_size,
                                color_mode='grayscale',
        subset='validation',
        class_mode='sparse' # TODO "categorical" ??
        )

class_names = sorted(train_ds.class_indices,key=lambda y: y)
json.dump (class_names,open('{}_classes.json'.format(MODELNAME),'w'))
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
# Tensorboard debug - disable if too big??
if args.tbdebug:
    tf.debugging.experimental.enable_dump_debug_info(log_dir, tensor_debug_mode="FULL_HEALTH", circular_buffer_size=-1)
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
file_writer_cm = tf.summary.create_file_writer(log_dir + '/cm')
cm_callback = tf.keras.callbacks.LambdaCallback(on_epoch_end=log_confusion_matrix)

model.compile(
    #optimizer=tf.keras.optimizers.Adam(1e-6), #5
    optimizer=tf.keras.optimizers.SGD(lr=0.005, decay=1e-6, momentum=0.6, nesterov=True),
    #optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.1),
    #loss="binary_crossentropy",
    loss="sparse_categorical_crossentropy",
    metrics=["sparse_categorical_accuracy"],
)
model.summary()
model.summary(print_fn=model_summary_output)
with open("{}_model.json".format(MODELNAME),"w+") as fd:
    fd.write(model.to_json())
if os.path.isfile("{}_continue.h5".format(MODELNAME)):
    os.rename("{}_continue.h5".format(MODELNAME),"{}_lastcontinue.h5".format(MODELNAME))
    model = tf.keras.models.load_model("{}_lastcontinue.h5".format(MODELNAME))
    print ("Continuing training....")
if args.contfile is not None:
    os.rename(args.contfile,"{}_lastcontinue.h5".format(MODELNAME))
    model = tf.keras.models.load_model("{}_lastcontinue.h5".format(MODELNAME))
    print ("Continuing training from {}....".format(args.contfile))
history=model.fit(train_ds, epochs=EPOCHS, validation_data=val_ds, initial_epoch=INITIAL_EPOCH,callbacks=[tensorboard_callback,cm_callback,CustomCallback()])
model.save("{}.h5".format(MODELNAME),save_format='h5')
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
fig.savefig("{}_training.png".format(MODELNAME))
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

model.save("{}.h5".format(MODELNAME))
#json.dump (class_names,open('{}_classes.json'.format(MODELNAME),'w'))


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
