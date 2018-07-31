/*-----------------------------------------------------------------------------------------*/
/*EbAT Automation Test Tool                                                                */
/*@file js                                                                      */
/*Date          :   03.02.2016                                                             */
/*-----------------------------------------------------------------------------------------*/
var URLHttp = location.host;
function getHTTPObject() {
	if (typeof XMLHttpRequest != 'undefined') {
			return new XMLHttpRequest();
	}
	try { 
			return new ActiveXObject("Msxml2.XMLHTTP"); 
	} catch (e) { 
			try { 
				return new ActiveXObject("Microsoft.XMLHTTP"); 
			} catch (e) {} 
	}
	return false;
}
function httpGet(theUrl){
	try {
		var xmlHttp = null;
		var data = null;
		xmlHttp = getHTTPObject();
		xmlHttp.open( "GET", theUrl, false );
		xmlHttp.setRequestHeader("Pragma", "no-cache" );
		xmlHttp.send(null);
		data = xmlHttp.responseText;
		xmlHttp.abort()
		xmlHttp = null;
		return data;
		}
	catch(e){   
		return "http-408 the connection has timed out";
	}
}
self.onmessage = function(n) {
	self.postMessage(httpGet(n.data.Url));
	self.close();// Terminates the worker.
};

/*-----------------------------------------------------------------------------------------*/

function JAVAFunction(PAR){
	try {
		
		URLGet = httpGet('http://' + URLHttp + '/ExampleCall/' + '?param='+PAR);
		
		//alert(URLGet);
		document.getElementById("RESPONSE_1").innerHTML = URLGet;

		}
		
	catch(e){  
	
		return "http-408 the connection has timed out";
		
	}
}

function cyclicCall(InterVal) {
    setInterval(function() {ChangeStatusPicture();}, InterVal);
}

function ChangeStatusPicture(){
	try {

		URLGet = httpGet('http://' + URLHttp + '/Request');

		//alert(URLGet);
		document.getElementById("ServerConnectionStatus").src = URLGet;


		}

	catch(e){

		return "http-408 the connection has timed out";

	}
}




