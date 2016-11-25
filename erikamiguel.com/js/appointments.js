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
	var appointments_list = document.getElementById("unapproved_appointments");
	var table_rows = '<tr><th>Order</th><th>Name</th><th>Start</th><th>End</th><th>E-mail</th><th>Time Zone</th></tr>';
	json_data = JSON.parse(data)
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
	appointment = appointments[id];
	appointment["approved"] = "yes"
	console.log(appointment)
}

