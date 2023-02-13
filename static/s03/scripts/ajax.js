function newXMLHttpRequest() {

	try { return new ActiveXObject("Msxml2.XMLHTTP"); } catch (e) {}
	try { return new ActiveXObject("Microsoft.XMLHTTP"); } catch (e) {}
	try { return new XMLHttpRequest(); } catch(e) {}

	return false;
}

function getReadyStateHandler(req, responseXmlHandler) {

    return function() {
        if (req.readyState == 4) {            
            responseXmlHandler(req);
        }
    }
}

function openURL(url, callback) {

	var req = newXMLHttpRequest();
	if (!req) return false;

	var handlerFunction = getReadyStateHandler(req, callback);
	req.onreadystatechange = handlerFunction;

	req.open("GET", url, true);
	req.send("");

	return true;
}
