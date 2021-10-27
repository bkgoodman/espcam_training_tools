# Project
This project creates a web UI that lets you snap and view photos from a ESP-CAM on a Linux Apache CGI script, then place and manipulate them into folder for use in TensorFlow Keras training for Tensorflow Lite Micro model creation from user-collected data.

It works by connecting to an ESP-CAM (or similar) project from the default sample camera firmware from the ESP-WHO project, and both previews the images on the web browser, and gives options to categorize by saving to folders.

Work TBD involved saving the model as TensorFlow Lite Micro for incluion back into ESP-WHO project

It is kind of a giant experimental mess right now - but it is a start-to-finish flow that lets you:

1. Acquire images directly from ESP32-CAM (Web GUI)
2. Save and categorize them (on a host computer) (Web GUI)
3. Manually (human) Crop/Resize, review, recategorized, reject, etc. (Think: Mechanical Turk) (Web GUI)
4. Convert source images into ones ready for training. (i.e. Take all crop info - crop them and resized down to 28x28 or whatever for training)
5. Run training
6. Manually test inference on new or existing images (Web GUI)
7. Generate Confusion Matrix for veritication
8. Convert to TFLite
9. Quantize to 8-bit
10. Test Inference w/ 8-bit TFlite model (on Linux)

# Scripts

* train.py  - builds model - generates a tensorflow .h5 file, and a .json file of classes/categories
* quantize.py - Converts Tensorflow float model to TensorflowLite 8-bit model
* infer.py - Infernce server  - because infer.cgi takes a while to load, but infers fast
* infer.cgi - Runs inference from build bkgmodel.h5 - requires infer.py to be running (chown the socket unix-domain socket it creates so apache2 can read it!)
* liteinfer.py - Runs inference form the TFLite 8-bit model
* confusion_matrix.py - Generate a confusion matrix (on fed images) to judge model accuracy

# CGI Handlers
CGI script are as follows - recommend you place in a public_html directory w/ CGI and Python enabled

* espcam.cgi - "Main" CGI script - Mainly used to collect (and categorized) images for training, directly from ESP camera. Also allows you to run infernece on saved or "live" * images to test your model on your local computer.
* cam.cgi - This CGI is used internall by the espcam.cgi script to physically collect images from ESPcam. (You'll probably need to set an IP address of your camera in this script)
* buildmanifest.py - Finds all your "saved" images - and creates a JSON manifest (file) containing all (their metadata). Needed for bbox (next step)
* bbox.cgi - CGI to allow you to draw bounding boxes around collected images (to isolate features)
* clipimages.py - Once you have drawn bounding boxes around your images (above) this script will created isolated training images - i.e. 28x28 versions of just your bounded images.
* view.cgi - View previously saved images. (Allows you to review, and/or delete or recategorize as-needed)



![image (2)](https://user-images.githubusercontent.com/473399/138978538-9700c14f-e173-479c-bbf0-16b8e5256e71.png)
![image (1)](https://user-images.githubusercontent.com/473399/138978548-66715ba1-28a2-4132-9998-d739b498c154.png)
![image](https://user-images.githubusercontent.com/473399/138978551-44ce1672-5a9d-4353-a8c1-064d63166ea6.png)
