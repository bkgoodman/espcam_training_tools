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
function movesnapbutton(o,moveto){
	var s = document.getElementById("history_0");
	var path= s.getAttribute("bkg-data-path");
	var filename= s.getAttribute("bkg-data-filename");
	console.log("Move",j['path'],"to",moveto,"/",filename);
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "op.cgi?op=move&path="+path+"&moveto="+moveto, false);
  xhttp.send();
	console.log(xhttp.responseText);
	j = JSON.parse(xhttp.responseText);
	s.setAttribute("bkg-data-path",j['MoveTo']);

}
function move_history(src,dest) {
	var s = document.getElementById("history_"+src);
	var d = document.getElementById("history_"+dest);
	console.log(s);
	d.setAttribute("bkg-data-path",s.getAttribute("bkg-data-data"));
	d.setAttribute("bkg-data-filename",s.getAttribute("bkg-data-filename"));
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
	var sbtn = s.children[3];
	var dbtn = d.children[3];
	dbtn.setAttribute("filename",sbtn.getAttribute("filename"));
	var sbtn = s.children[4];
	var dbtn = d.children[4];
	dbtn.setAttribute("filename",sbtn.getAttribute("filename"));
}

function movebutton(xx) {
	var moveto =document.getElementById("savetype").value;
	console.log("Movebutton",xx);
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "op.cgi?op=move&path="+xx.parentElement.getAttribute("bkg-data-path")+"&moveto="+moveto, false);
  xhttp.send();
	console.log(xhttp.responseText);
}
function deletebutton(xx) {
	console.log("Deletebutton",xx);
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "op.cgi?op=delete&path="+xx.parentElement.getAttribute("bkg-data-path"), false);
  xhttp.send();
	console.log(xhttp.responseText);
}
function inferbutton(xx) {
  var xhttp = new XMLHttpRequest();
	document.getElementById('inference_results').innerHTML="";
	xhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
				 // Typical action to be performed when the document is ready:
				 //document.getElementById("demo").innerHTML = xhttp.responseText;
				document.getElementById('inference_results').innerHTML=xhttp.responseText;
				j = JSON.parse(xhttp.responseText);
				for (var x in j) {
					var z = document.getElementById("svgrect_"+x);
					var p = j[x]*1;
					console.log("GOT INFER PARMA",x,p);
					z.setAttribute("width",p);
					var z = document.getElementById("svgtspan2_"+x);
					console.log(z);
					z.innerHTML=p+"%";
				}
			} else if (this.readyState == 4) {
				document.getElementById('inference_results').innerHTML="Error communicating w/ Inference engine";
			}
	};
	if (xx == undefined)
		{ xx=document.getElementById("history_0"); }
	else
		{ xx=parentElement; }
  xhttp.open("GET", "infer.cgi?path="+xx.getAttribute("bkg-data-path"), false);
  xhttp.send();
}

function snap_and_infer(x) {
	dosnap(undefined);
	inferbutton(undefined);

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
  document.getElementById("history_0").setAttribute("bkg-data-path",j['path']);
  document.getElementById("history_0").setAttribute("bkg-data-filename",j['filename']);
	if ('filename' in j) {
		document.getElementById("history_0").children[1].innerHTML = j['short'];
		document.getElementById("history_0").children[2].setAttribute("filename",j['path']);
		document.getElementById("history_0").children[3].setAttribute("filename",j['path']);
		document.getElementById("history_0").children[4].setAttribute("filename",j['path']);
	}
	else {
		document.getElementById("history_0").children[1].innerHTML = "";
		document.getElementById("history_0").children[2].setAttribute("filename","");
		document.getElementById("history_0").children[3].setAttribute("filename","");
		document.getElementById("history_0").children[4].setAttribute("filename","");
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
<button id="snapinfer" class="activebutton" onclick="snap_and_infer(this);" style=":active {background: yellow}" name="snapinfer">Snap&Inf.</button>

<div id="history_0">
	<img />
	<p>--</p>
	<button filename="" onclick="deletebutton(this);">Delete</button>
	<button filename="" onclick="inferbutton(this);">Infer</button>
	<button filename="" onclick="movebutton(this);">Move</button>
</div>
<div>
""")
for x in directories:
	print (f"<button onclick=\"movesnapbutton(this,'{x}');\">{x}</button>")
print ("""
</div>

<div>

<svg
   width="200mm"
   height="{h}mm"
   viewBox="0 0 400 {vbh}"
   version="1.1"
   id="svg5"
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">
""".format(h=10*len(directories),vbh=(10*len(directories))))
for (i,x) in enumerate(directories):
	print ("""
    <rect
       style="opacity:0.613821;fill:#00FF00;fill-rule:evenodd;stroke-width:2.96492;stroke-linecap:round;stroke-linejoin:round"
       id="svgrect_{x}"
       width="100"
       height="11.640142"
       x="67.160336"
       y="{recty}" />
    <text
       xml:space="preserve" style="font-style:normal;font-weight:normal;font-size:10.5833px;line-height:1.25;font-family:sans-serif;text-align:end;text-anchor:end;white-space:pre;inline-size:69.2968;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.264583"
       x="60.020069" y="73.368156"
       id="svgtext_{x}"
       transform="translate(-4.814726,-60.846135)"><tspan
         x="80.020069"
         y="{texty}"
         id="svgtspan_{x}">{x}</tspan>
		</text>
    <text
       xml:space="preserve" style="font-style:normal;font-weight:normal;font-size:10.5833px;line-height:1.25;font-family:sans-serif;text-align:end;text-anchor:start;white-space:pre;inline-size:69.2968;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.264583"
       x="60.020069" y="73.368156"
       id="svgtext_{x}"
       transform="translate(-4.814726,-60.846135)"><tspan
         x="180.020069"
         y="{texty}"
         id="svgtspan2_{x}">100%</tspan>
		</text>
""".format(i=i,x=x,texty=69.368156+(i*15),recty=0+(i*15)))

print ("""
  </g>
</svg>

</object>
</div>
<div>
<p id="inference_results" />
</div>

<div>
	<div style="display:inline-grid;grid-column:1/6;grid-column-gap:10px;grid-template-columns:auto auto auto auto auto auto">
		<div id="history_1">
			<img  />
			<p>--</p>
			<button filename="" onclick="deletebutton(this);">Delete</button>
			<button filename="" onclick="inferbutton(this);">Infer</button>
			<button filename="" onclick="movebutton(this);">Move</button>
		</div>
		<div id="history_2">
			<img />
			<p>--</p>
			<button filename="" onclick="deletebutton(this);">Delete</button>
			<button filename="" onclick="inferbutton(this);">Infer</button>
			<button filename="" onclick="movebutton(this);">Move</button>
		</div>
		<div id="history_3">
			<img />
			<p>--</p>
			<button filename="" onclick="inferbutton(this);">Infer</button>
			<button filename="" onclick="deletebutton(this);">Delete</button>
			<button filename="" onclick="movebutton(this);">Move</button>
		</div>
		<div id="history_4">
			<img />
			<p>--</p>
			<button filename="" onclick="deletebutton(this);">Delete</button>
			<button filename="" onclick="inferbutton(this);">Infer</button>
			<button filename="" onclick="movebutton(this);">Move</button>
		</div>
		<div id="history_5">
			<img />
			<p>--</p>
			<button filename="" onclick="deletebutton(this);">Delete</button>
			<button filename="" onclick="inferbutton(this);">Infer</button>
			<button filename="" onclick="movebutton(this);">Move</button>
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
