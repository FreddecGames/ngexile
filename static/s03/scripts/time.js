var counters = [];

function Counter(name, seconds, display, endContent) {
    
	this.name = name;
	this.started = new Date().getTime();
	this.endTime = new Date().getTime() + seconds * 1000;
	this.display = display;
	this.endContent = endContent;

	this.remainingTime = function() { return Math.ceil((this.endTime - new Date().getTime()) / 1000); };

	this.update = function() {

		if (!this.obj) this.obj = document.getElementById(this.name);
		if (!this.obj && new Date().getTime() - this.started > 20000) return false;
		if (!this.obj) return true;

		try {
            
			var s = this.remainingTime();

			if (s <= 0) {
                
				if (this.endContent != '') this.obj.innerHTML = this.endContent;
				else this.obj.innerHTML = formatRemainingTime(0);

				return false;
			}
            else if (s > 0 && (this.display == null))
				this.obj.innerHTML = formatRemainingTime(s);

			return true;
		}
        catch(e) {
            
			return false;
		}
	}
}

function updateCounters() {
    
	for (var x in counters) {
		if (counters[x] != null)
			if(!counters[x].update()) counters[x] = null;
	}

	window.setTimeout("updateCounters()", 900);
}

updateCounters();

function formattime(s) {
    
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

function formatRemainingTime(s) {
    
	if (s < 0) s = 0;
	if (s < 600) return "<span class='text-success'>" + formattime(s) + "</span>";
	return formattime(s);
}

var countdownnbr = 0;

function startCountdown(name, seconds, displayCountdown, endContent) {
    
	var c = new Counter(name, seconds, displayCountdown, endContent);
	counters.push(c);
	return c;
}

function putcountdown1(seconds, endlabel, url)
{
	var c = startCountdown('cntdwn' + countdownnbr++, seconds, null, '<a href="' + url + '">' + endlabel + '</a>');
	document.write(c);
}

function putcountdown2(seconds, content1, content2)
{
	var c = startCountdown('cntdwn' + countdownnbr++, seconds, content1, content2);
	document.write(c);
}
