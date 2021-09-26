#!/usr/bin/python3

import requests,base64,os,uuid,json

message=''
status='success'
try:
	# 240x240
	r = requests.get('http://10.0.0.63/control?var=framesize&val=4',timeout=5)
	# LED max dimness
	r = requests.get('http://10.0.0.63/control?var=led_intensity&val=255',timeout=5)
	# 2x CLock
	r = requests.get('http://10.0.0.63/reg?reg=273&mask=128&val=128',timeout=5)
except BaseException as e:
	status = 'error'
	message = str(e)

print ("""Content-type: application/json

""")
jsondata = {'status':status,'message':message}
print (json.dumps(jsondata,indent=2))
