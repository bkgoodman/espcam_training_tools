import os,glob
IMAGE_DIR="saved_images"


directories = glob.glob(os.path.join(IMAGE_DIR,"*"))
directories = [x.replace(IMAGE_DIR+"/","") for x in directories if os.path.isdir(x)]
