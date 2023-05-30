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
