var appointments;

function getUnapprovedAppointments(url, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", url, true); 
    xmlHttp.send(null);
}

function processUnapprovedAppointments(data){
	json_data = JSON.parse(data)
	if(json_data.length <= 0) { 
		noOrders(); 
		return 
	}
	var appointments_list = document.getElementById("unapproved_appointments");
	appointments_list.innerHTML = "Loading.."
	var table_rows = '<tr><th>Order</th><th>Name</th><th>Date</th><th>Start</th><th>End</th><th>E-mail</th><th>Time Zone</th></tr>';
	appointments = json_data
	for(var i = 0; i < json_data.length; i++) {
		object = json_data[i]
		start_tag = "<td>"
		end_tag = "</td>"
		column1 = start_tag + object['order'] + end_tag
		column2 = start_tag + object['name'] + end_tag
		column3 = start_tag + object['date'] + end_tag
		column4 = start_tag + object['start_time'] + end_tag
		column5 = start_tag + object['end_time'] + end_tag
		column6 = start_tag + object['e-mail'] + end_tag
		column7 = start_tag + object['time_zone'] + end_tag
		column8 = start_tag + "<button id='" + i +"' class='btn btn-xs btn-primary' onClick='approveAppointment(this.id)'>Approve</button>" + end_tag
		row = "<tr>" + column1 + column2 + column3 + column4 + column5 + column6 + column7 + column8+ "</tr>"
		table_rows += row
	}
	appointments_list.innerHTML = table_rows
}

function ordersLoad(){
	getUnapprovedAppointments("https://api.erikamiguel.com/consult/unapproved",processUnapprovedAppointments)
}

function approveAppointment(id){
	document.getElementById(id).disabled = true;
	appointment = appointments[id];
	appointment["approved"] = "yes"
	var xhr = new XMLHttpRequest();
	xhr = new XMLHttpRequest();
	var url = "url";
	xhr.open("POST", 'https://api.erikamiguel.com/consult/new-consultation', true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.onreadystatechange = function () { 
	    if (xhr.readyState == 4 && xhr.status == 200) {
	        var json = JSON.parse(xhr.responseText);
	        document.getElementById(id).disabled = false;
	        document.getElementById(id).className = "btn btn-xs btn-success";
	        document.getElementById(id).innerHTML = "Approved";
	    }
	}
	var data = JSON.stringify(appointment);
	xhr.send(data);
}

function noOrders(){
	document.getElementById("unapproved_appointments").innerHTML = "No orders to approve."
}