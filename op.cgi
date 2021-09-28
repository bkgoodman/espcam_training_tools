#!/usr/bin/python3

import requests,base64,os,uuid,json,cgi

jsondata={}
form = cgi.FieldStorage()
if 'op' in form:
	op = form['op'].value
	jsondata['op']=op
	path = form['path'].value
	jsondata['path']=path

try:
	if op =="delete":
		jsondata['removePath']=path
		os.remove(path)
	if op =="move":
		moveto=form['moveto'].value
		jsondata['moveto']=form['moveto'].value
		filename=os.path.split(path)[1]
		dest=os.path.join("saved_images",moveto,filename)
		jsondata["MoveTo"]=dest
		os.rename(path,dest)
except BaseException as e:
	jsondata['error']=str(e)

print ("""Content-type: application/json

""")
print (json.dumps(jsondata,indent=2))
