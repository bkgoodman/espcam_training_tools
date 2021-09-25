This project creates a web UI that lets you snap and view photos from a ESP-CAM on a Linux Apache CGI script, then place and manipulate them into folder for use in TensorFlow Keras training for Tensorflow Lite Micro model creation from user-collected data.

  It works by connecting to an ESP-CAM (or similar) project from the default sample camera firmware from the ESP-WHO project, and both previews the images on the web browser, and gives options to categorize by saving to folders.

An example Keras training script `ml.py` builds a model from these images.

Work TBD involved saving the model as TensorFlow Lite Micro for incluion back into ESP-WHO project
