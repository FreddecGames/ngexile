var scriptPath = location.href;
var p = scriptPath.lastIndexOf('/');
if(p >= 0) scriptPath = scriptPath.substring(0, p);
scriptPath += '/';

var scriptFile = location.href;
p = scriptFile.indexOf('?');
if(p >= 0) scriptFile = scriptFile.substring(0, p);
p = scriptFile.indexOf('#');
if(p >= 0) scriptFile = scriptFile.substring(0, p);

function $(element) {
  if (arguments.length > 1) {
    for (var i = 0, elements = [], length = arguments.length; i < length; i++)
      elements.push($(arguments[i]));
    return elements;
  }
  if (typeof element == 'string')
    return document.getElementById(element);
  return element;
}

function donothide(event) { event.cancelBubble = true; return false; }


function mouseCoords(ev){
	ev = ev || window.event;

	if(ev.pageX || ev.pageY){
		return {x:ev.pageX, y:ev.pageY};
	}
	return {
		x:ev.clientX + document.body.scrollLeft - document.body.clientLeft,
		y:ev.clientY + document.body.scrollTop  - document.body.clientTop
	};
}


function getval(name){
	var obj = document.getElementsByName(name);
	if(obj != null) obj = obj[0];

	if(obj == null) obj = document.getElementById(name);
	if(obj == null) return 0;

	var s = parseInt(obj.value, 10);
	if(isNaN(s) || (s < 0)) return 0; else return s;
}

function setval(name, val){
	var obj = document.getElementsByName(name);
	if(obj != null) obj = obj[0];
	if(obj == null) obj = document.getElementById(name);
	obj.value = val;
}



function evalResponse(req){
	try{
		if(req.status=="200"){
			eval(req.responseText);
		}
		else
			window.location.reload(true);
	} catch (e)	{
		window.location.reload(true);
	}
}


/* Hide/Show div boxes */

var lastobjref='';
var lastobjrefcontent='';
var showidx=0;

function hide(){
	if(lastobjref != ''){
		$(lastobjref).innerHTML = lastobjrefcontent;
		lastobjref = '';
	}
}

function show(objref, objbox){
	hide();
	var objr = $(objref);
	var objb = $(objbox);

	lastobjref = objref;
	lastobjrefcontent = objr.innerHTML;

	objr.innerHTML = objb.innerHTML.replace(/XXX/g,showidx);

	showidx++;

	return false;
}

/* functions */

var wbr = "<wbr/>";
if(navigator.userAgent.indexOf("Opera") != -1) wbr = "&#8203;";	

function addWbr(str)
{
	if(str.length < 30) return str;

	var s = "";
	for(k=0;k<str.length;k+=2)
		s = s + str.substr(k,2) + wbr;
	return s;
}


function addThousands(nStr, outD, sep)
{
	nStr += '';
	var dpos = nStr.indexOf(".");
	var nStrEnd = '';
	if (dpos != -1) {
		nStrEnd = outD + nStr.substring(dpos + 1, nStr.length);
		nStr = nStr.substring(0, dpos);
	}
	var rgx = /(\d+)(\d{3})/;
	while (rgx.test(nStr)) {
		nStr = nStr.replace(rgx, '$1' + sep + '$2');
	}
	return nStr + nStrEnd;
}

function formatnumber(n){
	return addThousands(n,'.',' ');
}

Number.prototype.n = function() { return addThousands(this,'.',' '); }
Number.prototype.lz = function() { return (this < 10?"0":"") + this; }