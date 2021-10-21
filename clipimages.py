#!/usr/bin/python3


import os, sys, subprocess, glob
import fcntl
import json,cgi
import random

CLIP_WIDTH=28
CLIP_HEIGHT=28

CLIP_RATIO=CLIP_WIDTH/CLIP_HEIGHT

MANIFEST_FILENAME = "clipimage.json"
SAVED_DIR="saved_images"
CROPPED_DIR="cropped_images"

fd = open(MANIFEST_FILENAME,"r")
fcntl.flock(fd.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
manifest = json.load(fd)
fd.close()

for x in manifest:
	if 'crop' in manifest[x]:
		m = manifest[x]
		pc= (x.split(os.sep))
		if pc[0] == SAVED_DIR:
			cropped_fn = os.path.join(CROPPED_DIR,*pc[1:])
			if not os.path.isfile(cropped_fn):
				print ("Process {}".format(cropped_fn),m)
				clip_width = m['crop']['right']-m['crop']['left']
				clip_height = m['crop']['bottom']-m['crop']['top']
				print ("  --- Orig Crop Size {}x{}".format(clip_width,clip_height))
				if (clip_width == clip_height):
					clip_width=CLIP_WIDTH
					clip_height=CLIP_HEIGHT
				elif (clip_width < clip_height):
					clip_width = CLIP_WIDTH*(clip_width/clip_height)
					clip_height=CLIP_HEIGHT
				else:
					clip_height = CLIP_HEIGHT*(clip_height/clip_width)
					clip_width=CLIP_WIDTH
				print ("   -- Dest Crop Size {:0.0f}x{:0.0f}".format(clip_width,clip_height))
