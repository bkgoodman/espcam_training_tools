#!/usr/bin/python3


import os, sys, subprocess, glob
import fcntl
import json,cgi
import random, argparse
from math import floor,ceil

CLIP_WIDTH=28
CLIP_HEIGHT=28

CLIP_RATIO=CLIP_WIDTH/CLIP_HEIGHT

MANIFEST_FILENAME = "clipimage.json"
SAVED_DIR="saved_images"
CROPPED_DIR="cropped_images"

parser = argparse.ArgumentParser(description='Run training on images.')
parser.add_argument('--model', default="bkgmodel", help='Base name for model files')
parser.add_argument('--imagedir', default="saved_images", help='root directory of source categorized images')
parser.add_argument('--destdir', default="processed_images", help='root directory of desination categorized images')
parser.add_argument('--crop', action="store_true", help='crop images')
parser.add_argument('--resize', action="store_true", help='resize images')
args = parser.parse_args()

if not args.crop and not args.resize:
    print ("Must specified one of --crop or --resize")
    sys.exit(2)

fd = open(MANIFEST_FILENAME,"r")
fcntl.flock(fd.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
manifest = json.load(fd)
fd.close()

needpad=0
needcrop=0

for x in manifest:
	if 'crop' in manifest[x]:
		m = manifest[x]
		pc= (x.split(os.sep))
		xadjust=0
		yadjust=0
		if pc[0] == SAVED_DIR:
			cropped_fn = os.path.join(args.destdir,*pc[1:])
			if not os.path.isfile(cropped_fn):
				needcrop+=1
				orig_width = int(m['width'])
				orig_height = int(m['height'])
				src_clip_width = m['crop']['right']-m['crop']['left']
				src_clip_height = m['crop']['bottom']-m['crop']['top']
				dest_bottom = m['crop']['bottom']
				dest_top = m['crop']['top']
				dest_left = m['crop']['left']
				dest_right = m['crop']['right']
				if (src_clip_width == src_clip_height):
					clip_width=CLIP_WIDTH
					clip_height=CLIP_HEIGHT
				elif (src_clip_width < src_clip_height):
					clip_width = CLIP_WIDTH*(src_clip_width/src_clip_height)
					clip_height=CLIP_HEIGHT
					xadjust = (src_clip_height-src_clip_width)/2
					dest_left -= floor(xadjust)
					dest_right += ceil(xadjust)
				else:
					clip_height = CLIP_HEIGHT*(src_clip_height/src_clip_width)
					clip_width=CLIP_WIDTH
					yadjust = (src_clip_width-src_clip_height)/2
					dest_top -= floor(yadjust)
					dest_bottom += ceil(yadjust)
				if (dest_left < 0) or (dest_right >= orig_width) or (dest_top < 0) or (dest_bottom >= orig_height):
					needpad+=1
				print ("Process {}".format(cropped_fn),m)
				print ("  --- Orig Crop Size {}x{}".format(src_clip_width,src_clip_height))
				print ("   -- ORIG Clip Fix  {:0.0f}x{:0.0f}".format(xadjust,yadjust))
				print ("   -- Dest Crop Size {:0.0f}x{:0.0f}".format(clip_width,clip_height))
				print ("   -- Dest Crop To {}x{} -> {}x{}".format(dest_left,dest_top,dest_right,dest_bottom))
				print ("   -- Dest Crop Size {}x{}".format(dest_right-dest_left,dest_bottom-dest_top))
				if (args.resize):
					cmd = ['convert',x,'-crop']
					cmd += ['{}x{}+{}+{}'.format(m['crop']['left'],m['crop']['top'],src_clip_width,src_clip_height)]
					cmd += ['-resize','28x28',cropped_fn]
					print ("     "," ".join(cmd))
					if (os.path.isfile(x)):
						subprocess.check_output(cmd)
					else:
						print ("File",x,"does not exist")


print ("NeedCrop {} NeedPad {}".format(needcrop,needpad))
