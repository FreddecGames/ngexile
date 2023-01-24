/***********************************************
* Cool DHTML tooltip script- © Dynamic Drive DHTML code library (www.dynamicdrive.com)
* This notice MUST stay intact for legal use
* Visit Dynamic Drive at http://www.dynamicdrive.com/ for full source code
***********************************************/

var offsetxpoint=-60; //Customize x offset of tooltip
var offsetypoint=20; //Customize y offset of tooltip
var ie=document.all;
var ns6=document.getElementById && !document.all;

var tipname="dhtmltooltip";
var tipwidth=0;
var tiptext=null;
var tipobj=null;

function ietruebody(){
	return (document.compatMode && document.compatMode!="BackCompat")? document.documentElement : document.body;
}

function ddrivetip(thetext, thewidth) {
	tipobj = document.getElementById(tipname);

	if(!tipobj) return false;

	window.setTimeout(function() { if(tipobj) document.body.appendChild(tipobj); }, 10);

	if(tipwidth > 0) tipobj.style.width = tipwidth + 'px';
	if(thewidth != undefined) tipobj.style.width = thewidth + 'px';

	if(tiptext)
		tiptext.innerHTML = thetext;
	else
		tipobj.innerHTML = thetext;

	return false;
}

function positiontip(e) {
	if(tipobj) {
		var curX=(ns6)?e.pageX : event.clientX+ietruebody().scrollLeft;
		var curY=(ns6)?e.pageY : event.clientY+ietruebody().scrollTop;

		//Find out how close the mouse is to the corner of the window
		var rightedge=ie&&!window.opera? ietruebody().clientWidth-event.clientX-offsetxpoint : window.innerWidth-e.clientX-offsetxpoint-20
		var bottomedge=ie&&!window.opera? ietruebody().clientHeight-event.clientY-offsetypoint : window.innerHeight-e.clientY-offsetypoint-20

		var leftedge=(offsetxpoint<0)? offsetxpoint*(-1) : -1000

		//if the horizontal distance isn't enough to accomodate the width of the context menu
		if (rightedge<tipobj.offsetWidth)
			//move the horizontal position of the menu to the left by it's width
			tipobj.style.left=ie? ietruebody().scrollLeft+event.clientX-tipobj.offsetWidth+"px" : window.pageXOffset+e.clientX-tipobj.offsetWidth+"px"
		else if (curX<leftedge)
			tipobj.style.left="5px"
		else
			tipobj.style.left=curX+offsetxpoint+"px" //position the horizontal position of the menu where the mouse is positioned

		//same concept with the vertical position
		if (bottomedge<tipobj.offsetHeight)
			tipobj.style.top=ie? ietruebody().scrollTop+event.clientY-tipobj.offsetHeight-offsetypoint+"px" : window.pageYOffset+e.clientY-tipobj.offsetHeight-offsetypoint+"px"
		else
			tipobj.style.top=curY+offsetypoint+"px";

		tipobj.style.display="block";
		tipobj.style.visibility="visible";
	}
}

function hideddrivetip() {
	if(tipobj) {
		tipobj.style.display="none";
		tipobj.style.visibility="hidden";
		tipobj.style.left="-1000px";
		tipobj.style.backgroundColor='';
	//	tipobj.style.width='';

		tipobj = null;
	}
}

document.onmousemove=positiontip;