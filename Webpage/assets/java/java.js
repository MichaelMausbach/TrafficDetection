var URLHttp = location.host;
var timearray = [];
var URLGet = "";

google.charts.load('current', {'packages':['corechart', 'table']});
google.charts.setOnLoadCallback(drawVisualization);

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
    //setInterval(function() {ChangeCarPicture();}, InterVal);
    //setInterval(function() {ChangeMeterValue();}, InterVal);
    //setInterval(function() {ChangeStatusText();}, InterVal);
    //setInterval(function() {ChangeSystemValue();}, InterVal);
    //setInterval(function() {Read_Dynamic_Data();}, InterVal);
    //setInterval(function() {drawVisualization2();}, InterVal);

    }

function cyclicCallslow(InterVal_Slow) {
    //setInterval(function() {drawVisualization();}, InterVal_Slow);
    //setInterval(function() {drawVisualization2();}, InterVal_Slow);
    //setInterval(function() {RequestErrorMessages();}, InterVal_Slow);
}

function ChangeStatusPicture(){
	try {

		URLGet = httpGet('http://' + URLHttp + '/Request');

		//alert(URLGet);
		//document.getElementById("TrafficCounter").innerHTML = URLGet[0].toString();
        //document.getElementById("State").innerHTML = URLGet[1];
        //document.getElementById("DirectionDetection").innerHTML = URLGet[2];
        var arri = eval(URLGet);
        console.log(arri)

        var test = arr[0];
        alert(test);


        var SystemDemand = arr[1][2]
        var SystemChargingLevel = round(arr[1][3],2)

        document.getElementById("TrafficCounter").innerHTML = test;

		}

	catch(e){

		return "http-408 the connection has timed out";

	}
}

function RequestErrorMessages(){
    try {

		URLGet = httpGet('http://' + URLHttp + '/RequestErrorMessages');
        var arr = eval(URLGet);

        var data = new google.visualization.arrayToDataTable(eval(URLGet), false)
        var table = new google.visualization.Table(document.getElementById('ErrorLogTable'));

        table.draw(data, {showRowNumber: false, width: '100%', height: '100%'});

    }

    catch(e){

        console.log(e);
        return "http-408 the connection has timed out";

    }
}

function ChangeStatusText(){
	try {

		URLGet = httpGet('http://' + URLHttp + '/RequestText');

		//alert(URLGet);

        document.getElementById("DatabaseConnectionStatusText").innerHTML = URLGet

		}

	catch(e){

		return "http-408 the connection has timed out";

	}
}

function Read_Dynamic_Data(){
	try {

		URLGet = httpGet('http://' + URLHttp + '/Read_Dynamic_Data');

		//alert(URLGet);

        //Behelfslösung, da auf die Schnelle kein besseres Replace gefunden wurde:
        URLGet =  URLGet.split("'").join(String.fromCharCode(34));
        single = JSON.parse(URLGet);

        console.log(typeof BatteryChargingLevel1);

        document.getElementById("DynamicDataArray").innerHTML = URLGet

		}

	catch(e){

		return "http-408 the connection has timed out";

	}
}

function ChangeSystemValue(){
	try {

		URLGet = httpGet('http://' + URLHttp + '/RequestSystem');

        var arr = eval(URLGet);

        var SystemState = arr[1][1]
        var SystemDemand = arr[1][2]
        var SystemChargingLevel = round(arr[1][3],2)

		document.getElementById("State").innerHTML = "State: " + SystemState;
		document.getElementById("Soc").innerHTML = SystemChargingLevel.toString() + " %";
		document.getElementById("Meter").value = SystemChargingLevel;

        }
	catch(e){
	    console.log(e);

		return "http-408 the connection has timed out";

	}

function round(value, number_of_decimals) {
        value = parseFloat(value);
        if (!value) return 0;
        number_of_decimals = parseInt(number_of_decimals);
        if (!number_of_decimals) number_of_decimals=0;
        var factor = Math.pow(10,number_of_decimals);
        return Math.round(value * factor) / factor;
    }
}

function ChangeMeterValue(){
	try {

		URLGet = httpGet('http://' + URLHttp + '/RequestBatt');

        var arr = eval(URLGet);

        var BatteryChargingLevel1 = round(arr[1][3],2)
        var BatteryChargingLevel2 = round(arr[2][3],2)
        var BatteryChargingLevel3 = round(arr[3][3],2)

        var BatterySystemActive1 = arr[1][1]
        var BatterySystemActive2 = arr[2][1]
        var BatterySystemActive3 = arr[3][1]

		document.getElementById("Met_1").value = BatteryChargingLevel1;
		document.getElementById("Met_2").value = BatteryChargingLevel2;
		document.getElementById("Met_3").value = BatteryChargingLevel3;
		document.getElementById("Val_1").innerHTML = BatteryChargingLevel1.toString() + " %";
		document.getElementById("Val_2").innerHTML = BatteryChargingLevel2.toString() + " %";
		document.getElementById("Val_3").innerHTML = BatteryChargingLevel3.toString() + " %";

        if (BatterySystemActive1 == "True") {
            document.getElementById("Dis_1").innerHTML = "Disconnect"
        } else {
            document.getElementById("Dis_1").innerHTML = "Connect"
		}

		if (BatterySystemActive2 == "True") {
            document.getElementById("Dis_2").innerHTML = "Disconnect"
        } else {
            document.getElementById("Dis_2").innerHTML = "Connect"
		}

		if (BatterySystemActive3 == "True") {
            document.getElementById("Dis_3").innerHTML = "Disconnect"
        } else {
            document.getElementById("Dis_3").innerHTML = "Connect"
		}

        }
	catch(e){
	    console.log(e);

		return "http-408 the connection has timed out";

	}

function round(value, number_of_decimals) {
        value = parseFloat(value);
        if (!value) return 0;
        number_of_decimals = parseInt(number_of_decimals);
        if (!number_of_decimals) number_of_decimals=0;
        var factor = Math.pow(10,number_of_decimals);
        return Math.round(value * factor) / factor;
    }
}

function ChangeCarPicture(){
	try {

		URLGet = httpGet('http://' + URLHttp + '/RequestBattPicture');
        var arr = eval(URLGet)

		document.getElementById("Pic_1").src = arr[1][1];
		document.getElementById("Pic_2").src = arr[2][1];
		document.getElementById("Pic_3").src = arr[3][1];

	}

	catch(e){

		return "http-408 the connection has timed out";

	}
}

function drawVisualization() {

    // draw voltage chart
    URLGet = httpGet('http://' + URLHttp + '/DrawChart4');

    var data = google.visualization.arrayToDataTable(eval(URLGet));

    var options = {
      //title : 'Current',
      vAxis: {title: 'Voltage in V'},
      curveType: 'function',
      legend: {position: 'bottom'}
    };

    var chart = new google.visualization.ComboChart(document.getElementById('VoltageChart'));
    chart.draw(data, options);

    // drar delta voltage chart
    URLGet = httpGet('http://' + URLHttp + '/DrawChart5');

    var data = google.visualization.arrayToDataTable(eval(URLGet));

    var options = {
        //title: 'Power',
        vAxis: {title: 'Delta Voltage in V'},
        //hAxis: {title: 'time [s]',ticks: [0, 60, 120, 180, 240]},
        curveType: 'function',
        legend: { position: 'bottom' }
    };

    var chart = new google.visualization.LineChart(document.getElementById('DeltaVoltageChart'));
    chart.draw(data, options);

    // draw soc chart
    URLGet = httpGet('http://' + URLHttp + '/DrawChart');
    var data = google.visualization.arrayToDataTable(eval(URLGet));

    var options = {
        //title: 'SoC Performance',
        vAxis: {title: 'SoC [%]','minValue': 0, 'maxValue':100},
        //hAxis: {title: 'time [s]',ticks: [0, 60, 120, 180, 240]},
        curveType: 'function',
        legend: { position: 'bottom' }

    };

    var chart = new google.visualization.LineChart(document.getElementById('PerformanceChart'));
    chart.draw(data, options);

}

function drawVisualization2() {

    URLGet = httpGet('http://' + URLHttp + '/DrawChart2');

    var data = google.visualization.arrayToDataTable(eval(URLGet));

    var options = {
      //title : 'Current',
      vAxis: {title: 'Current in A'},
      curveType: 'function',
      legend: {position: 'bottom'}
    };

    // draw first chart
    var chart = new google.visualization.ComboChart(document.getElementById('CurrentChart'));
    chart.draw(data, options);

    URLGet = httpGet('http://' + URLHttp + '/DrawChart3');

    var data = google.visualization.arrayToDataTable(eval(URLGet));

    var options = {
        //title: 'Power',
        vAxis: {title: 'Power in W'},
        //hAxis: {title: 'time [s]',ticks: [0, 60, 120, 180, 240]},
        curveType: 'function',
        legend: { position: 'bottom' }
    };

    // draw second chart
    var chart = new google.visualization.LineChart(document.getElementById('PowerChart'));
    chart.draw(data, options);

}

function set_system_active(system_number) {

    if (document.getElementById("Dis_" + system_number).innerHTML == "Disconnect") {

        if (confirm("Do you really want to disconnect battery system 'Sys_" + system_number + "'") == true) {

            if (httpGet('http://' + URLHttp + '/DisconnectBatterySystem/' + '?param='+system_number) == "True") {

                document.getElementById("Dis_" + system_number).innerHTML = "Connect"

            }
        }
    }
    else if (document.getElementById("Dis_" + system_number).innerHTML == "Connect") {

        if (confirm("Do you really want to connect battery system 'Sys_" + system_number + "'") == true) {

            if (httpGet('http://' + URLHttp + '/ConnectBatterySystem/' + '?param='+system_number) == "True") {

                document.getElementById("Dis_" + system_number).innerHTML = "Disconnect"

            }
        }
    }
}

function set_debug_level(system_number, debug_level) {

    httpGet('http://' + URLHttp + '/SetDebugLevel/' + '?param='+system_number+debug_level)

}

function add_battery_systems() {

    httpGet('http://' + URLHttp + '/AddBatterySystems/')

}

function start_scenario() {

    httpGet('http://' + URLHttp + '/StartScenario/')

}

function export_database_entries() {

    httpGet('http://' + URLHttp + '/ExportDatabaseEntries/')

}

function set_demand() {

    var data = parseInt(document.getElementById("Demand").value)

    if (data >= -100 && data <= 100) {

        if (confirm("Do you really want to set demand to '" + data + "'") == true) {
            httpGet('http://' + URLHttp + '/SetDemand/' + '?param='+data)
        }

    }

    else {

        confirm("Demand must be between '-100' and '100'!")

    }

}

function change_mode() {

    if (document.getElementById("b1").checked == true) {

        httpGet('http://' + URLHttp + '/ChangeMode/' + '?param=Auto')

        document.getElementById("Demand").setAttribute('disabled', 'disabled')
        document.getElementById("Set").setAttribute('disabled', 'disabled')

    }

    else if (document.getElementById("b2").checked == true) {

        httpGet('http://' + URLHttp + '/ChangeMode/' + '?param=Manual')

        document.getElementById("Demand").removeAttribute('disabled')
        document.getElementById("Set").removeAttribute('disabled')

    }

}

function shutdown() {

    if (confirm("Do you really want to shutdown?") == true) {

        httpGet('http://' + URLHttp + '/Shutdown/')

    }
}