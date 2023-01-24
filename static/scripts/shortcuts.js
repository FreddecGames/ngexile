var sclist = [];
var focuscount = 0;

function addShortcut(key, action) {

}

function keydown(e) {
	e = e || window.event;
	var x = e.keyCode;

	var obj = e.srcElement || e.fromElement;

	alert(obj + "-" + x);
}

function foc(e) {
//	alert("focus");
//	document.write("focus");
	$('impersonate').style.height='50px';
}
//if (document.captureEvents) document.captureEvents(Event.KEYDOWN);
document.onkeydown = keydown;
document.onfocus = foc;