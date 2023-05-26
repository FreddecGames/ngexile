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
