#!/usr/bin/python3
import requests,base64,os,uuid,json,re,sys,glob

if ('QUERY_STRING' in os.environ):
	qs = os.environ['QUERY_STRING']
dirname = None
index=0
if qs:
	for qqs in qs.split("&"):
		(k,v)=qqs.split('=')
		if k=="dir":
			dirname = v
		if k=="index":
			index = int(v)
if dirname is None or re.match('^[0-9a-zA-Z\-_]+$',dirname) is None or not os.path.isdir(os.path.join("saved_images",dirname)):
	print ("""Content-type: text/plain

Invalid directory""")
	sys.exit(0)

dirpath = os.path.join("saved_images",dirname)

print ("""Content-type: text/html	

""")

print (f"""
<head>
<title>ESPCam {dirname} Directory<title>
</head>
<body>
	<div>
	</div>
</body>
""")

print (f"Index {index}")
files = glob.glob(os.path.join(dirpath,"img-*.jpg"))
for x in files[index:index+20]:
	print (x)
