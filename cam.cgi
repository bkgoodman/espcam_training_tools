#!/usr/bin/python3

import requests,base64,os,uuid,json,cgi

r = requests.get('http://10.0.0.63/capture')

c = r.content
data = base64.b64encode(c).decode('utf-8')
if ('QUERY_STRING' in os.environ):
	qs = os.environ['QUERY_STRING']
	
#print (os.environ)
#print (qs)
jsondata={}
folder = "unclassified_images"
form = cgi.FieldStorage()
if 'save' in form:
	folder = os.path.join("saved_images",form['save'].value)
	jsondata['type']=form['save'].value

u = uuid.uuid4().hex
jsondata['filename']=u
jsondata['path']=os.path.join(folder,"img-{}.jpg".format(u))
jsondata['short'] = jsondata['path'].replace("unclassified_images/img-","")[0:4]+"..."+jsondata['path'][-9:-4]
try:
	with open(jsondata['path'],"wb") as fd:
		fd.write(c)
except BaseException as e:
	print (str(e))

jsondata['img'] = data
print ("""Content-type: application/json

""")
print (json.dumps(jsondata,indent=2))
