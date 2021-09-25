#!/usr/bin/python3
import os,sys,glob,cgi,html,pathlib,re,uuid
from globals import  directories,IMAGE_DIR 


def checkpath(x,directories):
	p = os.path.normpath(x)
	p = p.split("/")
	if len(p) != 3:
		raise(BaseException())
	if p[0] != IMAGE_DIR:
		raise(BaseException())
	if p[1] not in directories:
		raise(BaseException())
	if not os.path.isfile(x):
		raise(BaseException())
	return
	

form = cgi.FieldStorage()
debug=""
sourcedir = "none"
if "sourcedir" in form:
	sourcedir=form['sourcedir'].value
start=0
if "start" in form:
	start = int(form['start'].value)

PAGESIZE=12
moveto=None
if 'moveto' in form:
	moveto = form['moveto'].value
print ("""Content-type: text/html
Cache-Control: no-cache, no-store, must-revalidate

<head>
<title>ESPCam</title>

<style>
.activebutton:active
{
background-color:blue;
}
</style>
<script type="text/javascript">
function doload() {
}
function deletefile(x) {
alert("Delete "+x);
window.location.reload(false); 
}
function movefile(x) {
alert("Move "+x);
window.location.reload(false); 
}
</script>
</head>
<body onload=doload()>

<form method="POST">
<div>
""")

for x in form:
	if form[x].value =="Delete":
		checkpath(x,directories)
		debug += "Deleting {}\n".format(x)
		os.remove(x)
	if form[x].value =="Move":
		checkpath(x,directories)
		dest=os.path.join(IMAGE_DIR,moveto,os.path.split(x)[1])
		try:
			os.rename(x,dest)
		except BaseException as e:
			print (e)
		debug += "Moving {} to {}\n".format(x,dest)
if 'confirm' in form and form['confirm'].value == "Uncommit":
	files = glob.glob(IMAGE_DIR+"/"+sourcedir+"/*.jpg")
	committed = [x for x in files if os.path.split(x)[1].startswith("img-z")]
	for x in committed:
		u = uuid.uuid4().hex
		dest = os.path.join(IMAGE_DIR,sourcedir,"img-{}.jpg".format(u))
		debug += "REname {} to {}\n".format(x,dest)
		os.rename(x,dest)
if 'confirm' in form and form['confirm'].value == "Commit":
	debug += f"\nConfirm all {sourcedir}\n"
	files = glob.glob(IMAGE_DIR+"/"+sourcedir+"/*.jpg")
	committed = [x for x in files if os.path.split(x)[1].startswith("img-z")]
	uncommitted = [x for x in files if not os.path.split(x)[1].startswith("img-z")]
	"""
	for f in sorted(files):
		debug += f"{f}\n"
	for f in sorted(committed):
		debug += f"COMMITTED: {f}\n"
	for f in sorted(uncommitted):
		debug += f"UNCOMMITTED: {f}\n"
	"""
	lastcommit=0
	if (len(committed)>0):
		zz=sorted(committed)[-1]
		lastcommit=int(re.search("/img-z(\d+)\.jpg$",zz).group(1))
		debug += f"Lastcommit {zz} num={lastcommit}\n"
	lastcommit+=1
	for f in sorted(uncommitted):
		newname = os.path.join(IMAGE_DIR,sourcedir,"img-z{0:06d}.jpg".format(lastcommit))
		lastcommit+=1
		debug += f"RENAME {f} to {newname}\n"
		os.rename(f,newname)
	
	debug += f"Commited already {len(committed)}\n"

# Files have been handled - now render 
files = glob.glob(IMAGE_DIR+"/"+sourcedir+"/*.jpg")
for (i,x) in enumerate(sorted(files)[start:start+PAGESIZE]):
	short = os.path.split(x)[1]
	short = short[4:8]+".."+short[-8:]
	if ( i%5)==0:
		print ('<div style="display:inline-grid;grid-column:1/6;grid-column-gap:10px;grid-template-columns:auto auto auto auto auto auto">')
	print("""
		<div id="history_1" >
			<img src="{file}" width=100 height=100 />
			<p>{short}</p>
			<input type="submit" Value="Delete" name="{file}" />
			<input type="submit" Value="Move" name="{file}" />
		</div>
	""".format(file=x,short=short))
	if ( i%5)==4:
		print ('</div>')

for x in form:
	debug += "{}: {}\n".format(x,form[x].value)
debug += "\nDirectories: "+", ".join(directories)
debug += "\nMoveto is \"{}\"".format(moveto)
#debug = html.escape(str(form.keys()))
print ("""
</div>

<div>
Move to:
	<select name="moveto" id="moveto">
""")
for x in directories:
	if moveto == x:
		print ("<option selected>{}</option>".format(x))
	else:
		print ("<option>{}</option>".format(x))
print ("""
</select>
</div>
</form>
""")

for x in directories:
	print (f"<a href=\"?sourcedir={x}\">{x}</a>")


print ("<br />")
print (f"<a href=\"?start=0&sourcedir={sourcedir}\">First</a>")
prev = start - PAGESIZE
if prev<0: prev=0
print (f"<a href=\"?start={prev}&sourcedir={sourcedir}\">Prev</a>")
n = start+PAGESIZE
if n > (len(files)-PAGESIZE):
	n = len(files)-PAGESIZE
if n < 0: n=0
print (f"<a href=\"?start={n}&sourcedir={sourcedir}\">Next</a>")
start = len(files) - PAGESIZE
if start<0: start=0
print (f"<a href=\"?start={start}&sourcedir={sourcedir}\">Last</a>")
print ("<br />")
print (f"<a href=\"?confirm=Commit&sourcedir={sourcedir}\">Commit All</a>")
print (f"<a href=\"?confirm=Uncommit&sourcedir={sourcedir}\">Uncommit All</a>")
print (f"<a href=\"espcam.cgi\">Snap</a>")
print ("<br />")
print ("""
<div id="debug">
<h3>Debug</h3>
<pre>
{debug}
</pre>
</div>

</body>

<!--
{{"0xd3":8,"0x111":0,"0x132":137,"board":"AI-THINKER","xclk":20,"pixformat":3,"framesize":4,"quality":10,"brightness":0,"contrast":0,"saturation":0,"sharpness":0,"special_effect":0,"wb_mode":0,"awb":1,"awb_gain":1,"aec":1,"aec2":0,"ae_level":0,"aec_value":312,"agc":1,"agc_gain":0,"gainceiling":0,"bpc":0,"wpc":1,"raw_gma":1,"lenc":1,"hmirror":0,"dcw":1,"colorbar":0,"led_intensity":202,"hand_detect":0"hand_pose":0}}

http://10.0.0.63/control?var=colorbar&val=0
http://10.0.0.63/status

Set 240x240
http://10.0.0.63/control?var=framesize&val=4
http://10.0.0.63/control?var=led_intensity&val=224
2x CLock
http://10.0.0.63/reg?reg=273&mask=128&val=128
-->
""".format(debug=debug))
