#!/usr/bin/python3


import os, sys, subprocess, glob
import fcntl
import json,cgi
import random

MANIFEST_FILENAME = "clipimage.json"


# fcntl.flock(fd.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
try:
	fd = open(MANIFEST_FILENAME,"r")
	fcntl.flock(fd.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
	manifest = json.load(fd)
	fd.close()
except:
	manifest = {}

crops=0
bad=0
nocrop=0
for x in list(manifest.keys()):
	if 'crop' in manifest[x]:
		crops+=1
	if 'crop' not in manifest[x]:
		nocrop+=1
	if 'bad' in manifest[x]:
		bad+=1

print ("Croped {} NotCropped {} Bad {}".format(crops,nocrop,bad))
