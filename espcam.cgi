#!/usr/bin/python
import os, sys,glob
from globals import  IMAGE_DIR,directories



print ("""Content-type: text/html


<head>
<title>ESPCam</title>

<style>
.activebutton:active
{
background-color:blue;
}
</style>
<script type="text/javascript">
var globalTimer;
var dirnames=["",
""")
for (i,x) in enumerate(directories):
	print ("\"{}\",\n".format(x))

print ("""
];
function move_history(src,dest) {
	var s = document.getElementById("history_"+src);
	var d = document.getElementById("history_"+dest);
	console.log(s);
	var s_img = s.children[0];
	var d_img = d.children[0];
	d_img.src = s_img.src;
	var sstr = s.children[1].innerHTML;
	d.children[1].innerHTML = sstr.substring(sstr.length-6);
	d_img.setAttribute("width",100);
	d_img.setAttribute("height",100);

	var sbtn = s.children[2];
	var dbtn = d.children[2];
	
	dbtn.setAttribute("filename",sbtn.getAttribute("filename"));
}

function deletebutton(xx) {
	console.log("Deletebutton",xx);
}
function inferbutton(xx) {
	console.log("InferButton",xx);
  var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
				 // Typical action to be performed when the document is ready:
				 //document.getElementById("demo").innerHTML = xhttp.responseText;
				alert(xhttp.responseText);
			}
	};
  xhttp.open("GET", "infer.py?filename="+xx, false);
  xhttp.send();
}
function doperp() {
	x = document.getElementById("perp").checked
	if (x) {
		dosnap(undefined);
		globalTimer=setTimeout(doload,250);
	} else {
		clearTimeout(globalTimer);
	}
}
function keyDownTextField(e) {
var keyCode = e.keyCode;
var key = e.key;
var i = key - '0';
		if ((i>=0) && (i<dirnames.length))
			dosnap(dirnames[i]);
		else if (keyCode == 32)
			dosnap(undefined);
	
return (true);
}
function doload() {
	var b = document.getElementById("initbutton");
	var x = b.innerText;
	b.innerText="Initializing...";
	var x = b.innerText;
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "cam_setup.cgi", false);
  xhttp.send();
	j = JSON.parse(xhttp.responseText);
	console.log("JSON",j);
	if (j['status'] != "success") {
		alert(j['message']);
	}
	b.innerText="Initialize";
document.addEventListener("keydown", keyDownTextField, false);

}
function dosnap(saveto) {
	var x =document.getElementById("cam");
	var save =document.getElementById("save_cb").checked;
	var name =document.getElementById("savetype").value;
  var xhttp = new XMLHttpRequest();
	var url = "cam.cgi"
	if (saveto !== undefined)
		url += "?save="+saveto;
	else if (save) {
		url += "?save="+name;
	}
  xhttp.open("GET", url, false);
  xhttp.send();
	j = JSON.parse(xhttp.responseText);
	console.log("JSON",j);

	/*
	move_history(5,1);
	document.getElementById("old5").src = document.getElementById("old4").src;
	document.getElementById("old4").src = document.getElementById("old3").src;
	document.getElementById("old3").src = document.getElementById("old2").src;
	document.getElementById("old2").src = document.getElementById("old1").src;
	document.getElementById("old1").src = document.getElementById("cam").src;
	*/

	move_history(4,5);
	move_history(3,4);
	move_history(2,3);
	move_history(1,2);
	move_history(0,1);
  document.getElementById("history_0").children[0].src = "data:image/jpeg;base64,"+j['img'];
	if ('filename' in j) {
		document.getElementById("history_0").children[1].innerHTML = j['filename'];
		document.getElementById("history_0").children[2].setAttribute("filename",j['filename']);
		document.getElementById("history_0").children[3].setAttribute("filename",j['filename']);
	}
	else {
		document.getElementById("history_0").children[1].innerHTML = "";
		document.getElementById("history_0").children[2].setAttribute("filename","");
		document.getElementById("history_0").children[3].setAttribute("filename","");
	}
	
	delete j['img'];
	document.getElementById("debug").innerHTML=JSON.stringify(j);

	var x = document.getElementById("perp").checked
	if (x) 
		globalTimer=setTimeout(dosnap,250);

}
</script>
</head>
<body onload=doload()>
<button onclick="dosnap(undefined);" class="activebutton" name="Snap">Snap</button>
<button id="initbutton" class="activebutton" onclick="doload();" style=":active {background: yellow}" name="Initialize">Initialize</button>

<div id="history_0">
	<img />
	<p>--</p>
	<button filename="" onclick="deletebutton(this);">Delete</button>
	<button filename="" onclick="inferbutton(this);">Infer</button>
</div>

<div>
	<div style="display:inline-grid;grid-column:1/6;grid-column-gap:10px;grid-template-columns:auto auto auto auto auto auto">
		<div id="history_1">
			<img  />
			<p>--</p>
			<button filename="" onclick="deletebutton(this);">Delete</button>
			<button filename="" onclick="inferbutton(this);">Infer</button>
		</div>
		<div id="history_2">
			<img />
			<p>--</p>
			<button filename="" onclick="deletebutton(this);">Delete</button>
			<button filename="" onclick="inferbutton(this);">Infer</button>
		</div>
		<div id="history_3">
			<img />
			<p>--</p>
			<button filename="" onclick="inferbutton(this);">Infer</button>
			<button filename="" onclick="deletebutton(this);">Delete</button>
		</div>
		<div id="history_4">
			<img />
			<p>--</p>
			<button filename="" onclick="deletebutton(this);">Delete</button>
			<button filename="" onclick="inferbutton(this);">Infer</button>
		</div>
		<div id="history_5">
			<img />
			<p>--</p>
			<button filename="" onclick="deletebutton(this);">Delete</button>
			<button filename="" onclick="inferbutton(this);">Infer</button>
		</div>
	</div>
</div>

</table>
<div><input type="checkbox" onchange="doperp()" id="perp" />Perpetual</div>
<div><input type="checkbox" id="save_cb" />Save</div>
<div><select id="savetype">
""")
for x in directories:
	print (f"<option>{x}</option>")
print ("""
</select></div>
<div id="debug">
</div>
<p>
<b>Snap Keys:</b><br />
""")
for (i,x) in enumerate(directories):
	print (f"{i+1}: {x}<br />")

print("""
Space: (Preview)<br />
<a href="view.cgi">View</a>
</p>
</body>

<!--
{"0xd3":8,"0x111":0,"0x132":137,"board":"AI-THINKER","xclk":20,"pixformat":3,"framesize":4,"quality":10,"brightness":0,"contrast":0,"saturation":0,"sharpness":0,"special_effect":0,"wb_mode":0,"awb":1,"awb_gain":1,"aec":1,"aec2":0,"ae_level":0,"aec_value":312,"agc":1,"agc_gain":0,"gainceiling":0,"bpc":0,"wpc":1,"raw_gma":1,"lenc":1,"hmirror":0,"dcw":1,"colorbar":0,"led_intensity":202,"hand_detect":0"hand_pose":0}

http://10.0.0.63/control?var=colorbar&val=0
http://10.0.0.63/status

Set 240x240
http://10.0.0.63/control?var=framesize&val=4
http://10.0.0.63/control?var=led_intensity&val=224
2x CLock
http://10.0.0.63/reg?reg=273&mask=128&val=128
-->
""")
