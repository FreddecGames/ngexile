//---

function $(element) {

    if (arguments.length > 1) {
        for (var i = 0, elements = [], length = arguments.length; i < length; i++)
            elements.push($(arguments[i]))
        return elements
    }

    if (typeof element == 'string')
        return document.getElementById(element)

    return element
}

//---

var showIdx = 0

var lastObjRef = ''
var lastObjRefContent = ''

function hide() {
    
    if (lastObjRef != '') {
        
        $(lastObjRef).innerHTML = lastObjRefContent
        lastObjRef = ''
    }
}

function show(objRef, objBox) {
    
    hide()

    var objr = $(objRef)
    var objb = $(objBox)

    lastObjRef = objRef
    lastObjRefContent = objr.innerHTML

    objr.innerHTML = objb.innerHTML.replace(/XXX/g, showIdx)

    showIdx++

    return false
}

//---

function formatNumber(n) {

    let sign = ''
    if (n < 0) sign = '-'

    let absValue = Math.abs(n)

    let ret = '', symbol = null

    if (absValue >= 1e27) { ret = (Math.round(100 * absValue / 1e27) / 100); symbol = 'B'; }
    else if (absValue >= 1e24) { ret = (Math.round(100 * absValue / 1e24) / 100); symbol = 'Y'; }
    else if (absValue >= 1e21) { ret = (Math.round(100 * absValue / 1e21) / 100); symbol = 'Z'; }
    else if (absValue >= 1e18) { ret = (Math.round(100 * absValue / 1e18) / 100); symbol = 'E'; }
    else if (absValue >= 1e15) { ret = (Math.round(100 * absValue / 1e15) / 100); symbol = 'P'; }
    else if (absValue >= 1e12) { ret = (Math.round(100 * absValue / 1e12) / 100); symbol = 'T'; }
    else if (absValue >= 1e9) { ret = (Math.round(100 * absValue / 1e9) / 100); symbol = 'G'; }
    else if (absValue >= 1e6) { ret = (Math.round(100 * absValue / 1e6) / 100); symbol = 'M'; }
    else if (absValue >= 1e3) { ret = (Math.round(100 * absValue / 1e3) / 100); symbol = 'k'; }
    else ret = (Math.round(100 * absValue) / 100)

    return sign + ret + (symbol ? ' <small class="opacity-50">' + symbol + '</small>' : '')
}

function putNumber(n) { document.write(formatNumber(n)); }

//---

function formatTime(s) {
    
	d = Math.floor(s / (3600 * 24));

	h = Math.floor(s / 3600) % 24;
	if (h < 10) h = "0" + h;

	m = Math.floor(s / 60) % 60;
	if (m < 10) m = "0" + m;

	s = s % 60;
	if (s < 10) s = "0" + s

	if (d > 0) return d + "j" + " " + h + ":" + m + ":" + s;
	else return h + ":" + m + ":" + s;
}

function putTime(s) { document.write(formatTime(s)); }

//---

function Counter(name, seconds, display, endContent) {

	this.name = name;
	this.display = display;
	this.endContent = endContent;

	this.started = new Date().getTime();
	this.endTime = new Date().getTime() + seconds * 1000;

	this.remainingTime = function() {
        
        return Math.ceil((this.endTime - new Date().getTime()) / 1000);
    }
    
    this.formatRemainingTime = function(s) {
        
        if (s < 0) s = 0;
        if (s < 600) return "<span class='text-success'>" + formatTime(s) + "</span>";
        return formatTime(s);
    }
    
	this.update = function() {

		if (!this.obj) this.obj = document.getElementById(this.name);
		if (!this.obj && new Date().getTime() - this.started > 20000) return false;
		if (!this.obj) return true;

        var s = this.remainingTime();

        if (s <= 0) {
            
            if (this.endContent != '') this.obj.innerHTML = this.endContent;
            else this.obj.innerHTML = this.formatRemainingTime(0);

            return false;
        }
        else if (s > 0 && (this.display == null))
            this.obj.innerHTML = this.formatRemainingTime(s);

        return true;

	}

	this.toString = function() {
        
		var s = this.remainingTime();
		var toDisplay = this.display;
		if (!toDisplay) toDisplay = (s <= 0 && this.endContent != '') ? this.endContent : this.formatRemainingTime(s);
		return '<span id="' + this.name + '">' + toDisplay + '</span>';
	}
}

var counters = []

function updateCounters() {
    
	for (var x in counters) {
		if (counters[x] != null)
			if(!counters[x].update()) counters[x] = null
	}

	window.setTimeout('updateCounters()', 900)
}

updateCounters()

var countdownnbr = 0

function startCountdown(name, seconds, display, endContent) {
    
	var c = new Counter(name, seconds, display, endContent)
	counters.push(c)
	return c
}

function putCountdown(seconds, display, endContent)
{
	var c = startCountdown('cntdwn' + countdownnbr++, seconds, display, endContent)
	document.write(c)
}
