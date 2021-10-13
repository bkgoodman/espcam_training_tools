#!/usr/bin/python3

import requests,base64,os,uuid,json,cgi,glob,re

#print (os.environ)
#print (qs)
jsondata={}
folder = "unclassified_images"

filename = glob.glob(os.path.join(folder,"img-*.jpg"))[0]

#u = uuid.uuid4().hex
g = re.search("img-(.+).jpg$",filename)
u= g.groups()[0]
jsondata['filename']=filename
jsondata['path']=filename
jsondata['short'] = jsondata['path'].replace("unclassified_images/img-","")[0:4]+"..."+jsondata['path'][-9:-4]

data = base64.b64encode(open(filename,"rb").read()).decode('utf-8')
jsondata['img'] = data
print ("""Content-type: application/json

""")
print (json.dumps(jsondata,indent=2))
