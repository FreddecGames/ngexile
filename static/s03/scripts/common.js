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

function doNotHide(event) {
    
    event.cancelBubble = true
    return false
}

function getVal(name) {

    var obj = document.getElementsByName(name)
    if (obj != null) obj = obj[0]

    if (obj == null) obj = document.getElementById(name)
    if (obj == null) return 0

    var s = parseInt(obj.value, 10)
    if (isNaN(s) || (s < 0)) return 0
    else return s
}

function setVal(name, val) {

    var obj = document.getElementsByName(name)
    if (obj != null) obj = obj[0]
    if (obj == null) obj = document.getElementById(name)
    obj.value = val
}

function evalResponse(req) {

    try {
        
        if (req.status == '200') eval(req.responseText)
        else window.location.reload(true)
    
    } catch (e) {

        window.location.reload(true)
    }
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

function show(objref, objbox) {
    
    hide()

    var objr = $(objref)
    var objb = $(objbox)

    lastObjRef = objref
    lastObjRefContent = objr.innerHTML

    objr.innerHTML = objb.innerHTML.replace(/XXX/g, showIdx)

    showIdx++

    return false
}

//---

var wbr = '<wbr/>'
if (navigator.userAgent.indexOf('Opera') != -1) wbr = '&#8203'

function addWbr(str) {
    
    if (str.length < 30) return str

    var s = ''
    for (k = 0; k < str.length; k += 2)
        s = s + str.substr(k, 2) + wbr
    
    return s
}

//---

function addThousands(nStr, outD, sep) {

    nStr += ''
    var dpos = nStr.indexOf('.')
    var nStrEnd = ''

    if (dpos != -1) {
        
        nStrEnd = outD + nStr.substring(dpos + 1, nStr.length)
        nStr = nStr.substring(0, dpos)
    }

    var rgx = /(\d+)(\d{3})/
    while (rgx.test(nStr))
        nStr = nStr.replace(rgx, '$1' + sep + '$2')
    
    return nStr + nStrEnd
}

function formatnumber(n) { return addThousands(n, '.', ' ') }

//---

function newXMLHttpRequest() {

	try { return new ActiveXObject('Msxml2.XMLHTTP') } catch (e) {}
	try { return new ActiveXObject('Microsoft.XMLHTTP') } catch (e) {}
	try { return new XMLHttpRequest() } catch(e) {}

	return false
}

function getReadyStateHandler(req, responseXmlHandler) {

    return function() {
        if (req.readyState == 4) {            
            responseXmlHandler(req)
        }
    }
}

function openURL(url, callback) {

	var req = newXMLHttpRequest()
	if (!req) return false

	var handlerFunction = getReadyStateHandler(req, callback)
	req.onreadystatechange = handlerFunction

	req.open('GET', url, true)
	req.send('')

	return true
}
