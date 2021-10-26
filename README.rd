This project creates a web UI that lets you snap and view photos from a ESP-CAM on a Linux Apache CGI script, then place and manipulate them into folder for use in TensorFlow Keras training for Tensorflow Lite Micro model creation from user-collected data.

It works by connecting to an ESP-CAM (or similar) project from the default sample camera firmware from the ESP-WHO project, and both previews the images on the web browser, and gives options to categorize by saving to folders.

An example Keras training script `ml.py` builds a model from these images.

Work TBD involved saving the model as TensorFlow Lite Micro for incluion back into ESP-WHO project


train.py  - builds model
quantize.py - Converts Tensorflow float model to TensorflowLite 8-bit model
infer.py - Infernce server  - because infer.cgi takes a while to load, but infers fast
infer.cgi - Runs inference from build bkgmodel.h5 - requires infer.py to be running (chown the socket unix-domain socket it creates so apache2 can read it!)
liteinfer.py - Runs inference form the TFLite 8-bit model
