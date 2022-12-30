var busy = false;

/*
 * Returns an new XMLHttpRequest object, or false if the browser
 * doesn't support it
 */
function newXMLHttpRequest() {

	try { return new ActiveXObject("Msxml2.XMLHTTP"); } catch (e) {} // Try to create XMLHttpRequest in later versions of Internet Explorer
	try { return new ActiveXObject("Microsoft.XMLHTTP"); } catch (e) {} // Try version supported by older versions of Internet Explorer
	try { return new XMLHttpRequest(); } catch(e) {} // Create XMLHttpRequest object in non-Microsoft browsers
	alert("XMLHttpRequest not supported");
	return false;
}

/*
 * Returns a function that waits for the specified XMLHttpRequest
 * to complete, then passes it XML response to the given handler function.
 * req - The XMLHttpRequest whose state is changing
 * responseXmlHandler - Function to pass the XML response to
 */
function getReadyStateHandler(req, responseXmlHandler) {

   // Return an anonymous function that listens to the XMLHttpRequest instance
   return function () {
     // If the request's status is "complete"
     if (req.readyState == 4) {
       busy = false;

		// Pass the XML payload of the response to the handler function.
		responseXmlHandler(req);
     }
   }
}

function openURL(url, callback)
{
	//if(busy) return;
	busy = true;
/*
	if(url.charat(0)=='/')
	{
		var slash = location.indexOf('/',8);
		if(slash==-1) slash = location.length;
		url = location.substring(1, slash) + url;
	}
	else
	{
		var slash = location.lastIndexOf('/');
		if(slash==-1) slash = location.length;
		url = location.substring(1, slash) + '/' + url;
	}*/

	// Obtain an XMLHttpRequest instance
	var req = newXMLHttpRequest();

	if(!req) return false;

	// Set the handler function to receive callback notifications from the request object
	var handlerFunction = getReadyStateHandler(req, callback);
	req.onreadystatechange = handlerFunction;

	// Open an HTTP GET connection
	req.open("GET", url, true);
	req.send("");

	return true;
}