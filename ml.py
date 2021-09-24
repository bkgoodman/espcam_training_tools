#!/usr/bin/python3

import tensorflow as tf
import datetime

image_size=(180,180)
batch_size=2
input_shape = image_size+(3,)

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
model = tf.keras.Sequential([
tf.keras.Input(shape=input_shape),
tf.keras.layers.experimental.preprocessing.Rescaling(1./255),
#tf.keras.layers.MaxPooling2D((2,2), strides=3, padding="same"),
#tf.keras.layers.Conv2D(32, (2,2), padding="same"),
tf.keras.layers.Conv2D(32, (2,2), strides=3, padding="same"),
tf.keras.layers.MaxPooling2D((2,2), padding="same"),
#x = tf.keras.layers.BatchNormalization()(x)
#x = tf.keras.layers.Activation("relu")(x)
tf.keras.layers.Flatten(),
tf.keras.layers.Dense(32, activation="relu"), #32
tf.keras.layers.Dense(16, activation="relu"), #32
tf.keras.layers.Dense(64, activation="relu"), #32
tf.keras.layers.Dense(2, activation="softmax"),
#x = tf.keras.layers.Dense(2, activation="softmax")(x)
])
#model = tf.keras.Model(inputs,x)


log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

model.compile(
    #optimizer=tf.keras.optimizers.Adam(1e-6), #5
    optimizer=tf.keras.optimizers.SGD(lr=0.01, decay=1e-5, momentum=0.6, nesterov=True),
    #loss="binary_crossentropy",
    loss="sparse_categorical_crossentropy",
    metrics=["sparse_categorical_accuracy"],
)
model.summary()
model.fit(train_ds, epochs=5, validation_data=val_ds, callbacks=[tensorboard_callback])
model.save("bkgmodel")

