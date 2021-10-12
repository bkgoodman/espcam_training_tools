#!/usr/bin/python3

# https://neuralet.com/article/quantization-of-tensorflow-object-detection-api-models/?fbclid=IwAR2N_SvDHVURAwouQQgOidwpIJ17coTjs2XwsZNQoDMTguRtyeCsOyUfQvc
import tensorflow as tf
import cv2,os
import numpy as np

def representative_dataset_gen():
    """
    # Generating representative data sets
    :return:
    """
    image_dir = 'saved_images/five'
    input_size = [180, 180]
    imgSet = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    for img_path in imgSet:
        orig_image = cv2.imread(img_path)
        rgb_image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2GRAY)
        image_tensor = cv2.resize(rgb_image, dsize=tuple(input_size))
        image_tensor = np.asarray(image_tensor / 1.0, dtype=np.float32)
        image_tensor = image_tensor[np.newaxis, :]
        image_tensor = image_tensor.reshape(1,180,180,1)
        yield [image_tensor]

model = tf.keras.models.load_model("bkgmodel.h5")

converter = tf.lite.TFLiteConverter.from_keras_model(model)

converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.uint8  
converter.inference_output_type = tf.uint8  

tflite_model = converter.convert()

# Save the model.
with open('bkgmodel_quant.tflite', 'wb') as f:
  f.write(tflite_model)


