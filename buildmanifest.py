#!/usr/bin/python3


import os, sys, subprocess, glob
import fcntl
import json

MANIFEST_FILENAME = "clipimage.json"

# fcntl.flock(fd.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
try:
	fd = open(MANIFEST_FILENAME,"r")
	fcntl.flock(fd.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
	manifest = json.load(fd)
	fd.close()
except:
	manifest = {}

directories = ['saved_images','unclassified_images']

for d in directories:
	for f in glob.glob(os.path.join(d,"**"),recursive=True):
		if os.path.isfile(f):
			ext = os.path.splitext(f)[1]
			basename = os.path.split(f)[1]
			if (ext == ".jpg") and (basename.startswith("img-z") and f not in manifest):
				print ("Adding Image",basename)
				#x = subprocess.check_output(["identify","-ping","-format","%w %h %z %r",f]).decode('utf-8')
				x = subprocess.check_output(["identify","-ping","-format","%w %h",f]).decode('utf-8')
				(width, height) = x.split()
				if f not in manifest:
					manifest[f]={}
				rec=manifest[f]
					
				rec['width'] = width
				rec['height'] = height

fd = open(MANIFEST_FILENAME,"w")
fcntl.flock(fd.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
json.dump(manifest,fd,indent=2)
fd.close()
