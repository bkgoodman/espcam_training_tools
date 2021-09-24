#!/usr/bin/python3

import requests,base64,os,uuid,json

r = requests.get('http://10.0.0.63/capture')

c = r.content
data = base64.b64encode(c).decode('utf-8')
if ('QUERY_STRING' in os.environ):
	qs = os.environ['QUERY_STRING']
	
#print (os.environ)
#print (qs)
jsondata={}
if qs:
	(k,v)=qs.split('=')
	if k=="save":
		u = uuid.uuid4().hex
		jsondata['filename']=u
		jsondata['type']=v
		try:
			with open("saved_images/{}/img-{}.jpg".format(v,u),"wb") as fd:
				fd.write(c)
		except BaseException as e:
			print (str(e))

jsondata['img'] = data
print ("""Content-type: application/json

""")
print (json.dumps(jsondata,indent=2))
