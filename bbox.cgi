#!/usr/bin/python3


import os, sys, subprocess, glob
import fcntl
import json,cgi
import random

MANIFEST_FILENAME = "clipimage.json"

def swap(a,b):
	return (a,b) if (a<b) else (b,a)

# fcntl.flock(fd.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
try:
	fd = open(MANIFEST_FILENAME,"r")
	fcntl.flock(fd.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
	manifest = json.load(fd)
	fd.close()
except:
	manifest = {}

form = cgi.FieldStorage()
if 'save_good' in form:
	filename = form['filename'].value
	if filename in manifest:
		manifest[filename]['crop']={
			"left":round(float(form['startX'].value)),
			"right":round(float(form['endX'].value)),
			"top":round(float(form['startY'].value)),
			"bottom":round(float(form['endY'].value)),
		}

		(manifest[filename]['crop']['left'],manifest[filename]['crop']['right']) = swap(
			manifest[filename]['crop']['left'],
			manifest[filename]['crop']['right'])
		(manifest[filename]['crop']['top'],manifest[filename]['crop']['bottom']) = swap(
			manifest[filename]['crop']['top'],
			manifest[filename]['crop']['bottom'])
		fd = open(MANIFEST_FILENAME,"w")
		fcntl.flock(fd.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
		json.dump(manifest,fd,indent=2)
		fd.close()
if 'save_bad' in form:
	filename = form['filename'].value
	if filename in manifest:
		manifest[filename]['bad']=True
		fd = open(MANIFEST_FILENAME,"w")
		fcntl.flock(fd.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
		json.dump(manifest,fd,indent=2)
		fd.close()

nobbx=[]
crop_cnt=0
bad_cnt=0
total_cnt=0
for x in list(manifest.keys()):
	total_cnt += 1
	if 'crop' in manifest[x]:
		crop_cnt += 1
	elif 'bad' in manifest[x]:
		bad_cnt += 1
	else:
		nobbx.append(x)

debug = "Cropped {} Bad {} Remaining {} Total {}".format(
	crop_cnt,bad_cnt,total_cnt-(crop_cnt+bad_cnt),total_cnt)

if (len(nobbx)==0):
	print ("""
	<body>
	<h1>No moar left!</h2>
	<pre>{debug}</pre>
	</body>
	""".replace("{debug}",debug))
	sys.exit(0)


imgfile = random.choice(nobbx)

print ("""
<head>
<style>

@media (min-width: 513px) {
.kioskimg {
	height:36vw;
	width:48vw;
}
}
@media (max-width: 512px) {
.kioskimg {
	height:72vw;
	width:96vw;
}
}


.outsideWrapper{ 
    width:640px; height:640px; 
    xxmargin:20px 60px; 
    xxborder:1px solid blue;
    margin:0px 0px; 
    border:0px solid blue;
    }
.insideWrapper{ 
    width:100%; height:100%; 
    position:relative;}
.coveredImage{ 
    width:100%; height:100%; 
    position:absolute; top:0px; left:0px;
}
.coveringCanvas{ 
    width:100%; height:100%; 
    position:absolute; top:0px; left:0px;
    background-color: rgba(255,0,0,.1);
}
</style>

<script type="text/javascript">
function old_getMousePos(canvas, evt) {
        var rect = canvas.getBoundingClientRect();
        return {
          x: evt.clientX - rect.left,
          y: evt.clientY - rect.top
        };
      }
function  getMousePos(canvas, evt) {
  var rect = canvas.getBoundingClientRect(), // abs. size of element
      scaleX = canvas.width / rect.width,    // relationship bitmap vs. element for X
      scaleY = canvas.height / rect.height;  // relationship bitmap vs. element for Y

  console.log("Client RECT IS ",rect);
  console.log("CANVAS RECT IS ",canvas.width,canvas.height);
  console.log("SCALE IS ",scaleX,scaleY);
  return {
    x: (evt.clientX - rect.left) * scaleX,   // scale mouse coordinates after they have
    y: (evt.clientY - rect.top) * scaleY     // been adjusted to be relative to element
  }
}
function initDraw(canvas) {
    var mouse = {
        x: 0,
        y: 0,
        startX: 0,
        startY: 0,
        canvasStartPos: {
          X: 0,
          Y: 0
        }
    };
    canvas.style.cursor = "crosshair";
    function setMousePosition(e) {
        var ev = e || window.event; //Moz || IE
        if (ev.pageX) { //Moz
            mouse.x = ev.pageX + window.pageXOffset;
            mouse.y = ev.pageY + window.pageYOffset;
        } else if (ev.clientX) { //IE
            mouse.x = ev.clientX + document.body.scrollLeft;
            mouse.y = ev.clientY + document.body.scrollTop;
        }
    };

    var element = null;    
    var boxed = false;    
    canvas.onmousemove = function (e) {
        setMousePosition(e);
        if (element !== null) {
					/*
            element.style.width = Math.abs(mouse.x - mouse.startX) + 'px';
            element.style.height = Math.abs(mouse.y - mouse.startY) + 'px';
            element.style.left = (mouse.x - mouse.startX < 0) ? mouse.x + 'px' : mouse.startX + 'px';
            element.style.top = (mouse.y - mouse.startY < 0) ? mouse.y + 'px' : mouse.startY + 'px';
					*/
            canvas.style.cursor = "crosshair";
            ctx = canvas.getContext("2d");
            ctx.beginPath();
            ctx.clearRect(0,0,640,640);
            var now = getMousePos(canvas,e);
            //console.log("NOW",now);
            //console.log("STARTED",mouse.canvasStartPos);
            ctx.fillStyle="#ffffff80";
            //ctx.fillRect(10,10,100,100);
            //ctx.fillRect(mouse.x,mouse.y,mouse.startX,mouse.startY);
            ctx.fillRect(now.x,now.y,mouse.canvasStartPos.x-now.x,mouse.canvasStartPos.y-now.y);
            //console.log("WIDTH",mouse.canvasStartPos.x-now.x,"HEIGHT",mouse.canvasStartPos.y-now.y);
            //console.log(now.x,now.y,mouse.canvasStartPos.x-now.x,mouse.canvasStartPos.y-now.y);
						
						//console.log(xscale,yscale);
            document.getElementById("startX").value = Math.round(now.x );
            document.getElementById("startY").value = Math.round(now.y );
            document.getElementById("endX").value = Math.round(mouse.canvasStartPos.x );
            document.getElementById("endY").value = Math.round(mouse.canvasStartPos.y );

            ctx.fill(); // ????
        } else if (boxed == false) {
					/* Not clicked */
            ctx = canvas.getContext("2d");
            ctx.beginPath();
            ctx.fillStyle="#0000FF80";
            var now = getMousePos(canvas,e);
            ctx.clearRect(0,0,640,640);
            ctx.fillRect(now.x-1,0,2,640);
            ctx.fillRect(0,now.y-1,640,2);
				}
    }

    canvas.onclick = function (e) {
        if (element !== null) {
            element = null;
            canvas.style.cursor = "crosshair";
            console.log("finsihed.");
            ctx = canvas.getContext("2d");
            ctx.beginPath();
            ctx.clearRect(0,0,640,640);
            var now = getMousePos(canvas,e);
            console.log("NOW",now);
            console.log("STARTED",mouse.canvasStartPos);
            ctx.fillStyle="#ffffff80";
            //ctx.fillRect(10,10,100,100);
            //ctx.fillRect(mouse.x,mouse.y,mouse.startX,mouse.startY);
            ctx.fillRect(now.x,now.y,mouse.canvasStartPos.x-now.x,mouse.canvasStartPos.y-now.y);
            console.log("WIDTH",mouse.canvasStartPos.x-now.x,"HEIGHT",mouse.canvasStartPos.y-now.y);
            console.log(now.x,now.y,mouse.canvasStartPos.x-now.x,mouse.canvasStartPos.y-now.y);
            document.getElementById("startX").value = Math.round(now.x);
            document.getElementById("startY").value = Math.round(now.y);
            document.getElementById("endX").value = Math.round(mouse.canvasStartPos.x);
            document.getElementById("endY").value = Math.round(mouse.canvasStartPos.y);
            ctx.fill(); // ????
				
						// Convert Canvas coordinates to Image coordinates
						var img = document.getElementById("realImage");
						var canvasWidth = document.getElementById("canvas").width;
						var canvasHeight = document.getElementById("canvas").height;
						var imageWidth = img.naturalWidth;
						var imageHeight = img.naturalHeight;
						var xScale = imageWidth/canvasWidth;
						var yScale = imageHeight/canvasHeight;
						console.log("SAVESCALE ",xScale,yScale);

							
						document.getElementById("startX").value = Math.round(document.getElementById("startX").value * xScale);
						document.getElementById("startY").value = Math.round(document.getElementById("startY").value  * yScale);
						document.getElementById("endX").value = Math.round(document.getElementById("endX").value  * xScale);
						document.getElementById("endY").value = Math.round(document.getElementById("endY").value  * yScale);

						console.log("Start x/y ",
							document.getElementById("startX").value,
							document.getElementById("startY").value);
						console.log("End x/y ",
							document.getElementById("endX").value,
							document.getElementById("endY").value);
						var img = document.getElementById("realImage");
						document.getElementById("save_good").removeAttribute("disabled");
						
						console.log("Image actual size is ",img.naturalWidth,img.naturalHeight);
        } else if (boxed == false ){
            console.log("begun.");
            mouse.startX = mouse.x;
            mouse.startY = mouse.y;
            mouse.canvasStartPos = getMousePos(canvas,e);
            element = document.createElement('div');
            element.className = 'rectangle'
            element.style.left = mouse.x + 'px';
            element.style.top = mouse.y + 'px';
            canvas.appendChild(element)
            canvas.style.cursor = "crosshair";
						boxed=true;
						//document.getElementById("save_good").setAttributeNode(document.createAttribute("disabled"));
        } else if (boxed ==true ) {
						document.getElementById("save_good").setAttributeNode(document.createAttribute("disabled"));
					boxed=false;
            ctx = canvas.getContext("2d");
            ctx.clearRect(0,0,640,640);
				}
    }
}

function dorect(x1,y1,x2,y2,color) {
            canvas = document.getElementById("canvas");
            ctx = canvas.getContext("2d");
            ctx.beginPath();
            ctx.fillStyle=color;
            ctx.fillRect(x1,y1,x2-x1,y2-y1);
            ctx.fill();
}
</script>
</head>
<body>
   <h2>Feature Bounding Box</h2>
   
<div class="containter"> <!-- Base -->
	<div class="containter"> 
	<p><pre>{debug}</pre><br />Status: {{ res }}</p>
  <a class="btn btn-primary" href="{{ url_for("logs.kiosktrain",ke=p) }}">Prev</a>
  <a class="btn btn-primary" href="{{ url_for("logs.kiosktrain",ke=n) }}">Next</a>
  <form method="POST">
      <input type="hidden" name="filename" id="filename" value="{imgfile}" />
      <input type="hidden" name="startX" id="startX" value="" />
      <input type="hidden" name="endX" id="endX" value="" />
      <input type="hidden" name="startY" id="startY" value="" />
      <input type="hidden" name="endY" id="endY" value="" />
      <input type="submit" class="btn btn-primary" disabled id="save_good" name="save_good" value="Save Good" />
      <input type="submit" class="btn btn-primary" name="save_bad" value="Save Bad" />
      <!-- input type="submit" class="btn btn-primary" name="mark_invalid" value="Mark Invalid" /-->
  </form>

<div class="outsideWrapper">
    <div class="insideWrapper">
        <img id="realImage" src="{imgfile}" filename="FIXME.jpg") }}" class="coveredImage">
        <canvas width=640 height=640 id="canvas" class="coveringCanvas"></canvas>
    </div>
</div>
  </div> <! -- Member Add Collapse -->
</div> <!-- Base -->
<script type="text/javascript">
initDraw(document.getElementById('canvas'));
{{ drawcode|safe }}
</script>
</body>
""".replace("{imgfile}",imgfile).replace("{debug}",debug))
