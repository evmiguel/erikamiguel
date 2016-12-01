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
	var table_rows = '<tr><th>Order</th><th>Name</th><th>Date</th><th>Company</th><th>Start</th><th>End</th><th>E-mail</th><th>Time Zone</th><th>Date</th></tr>';
	appointments = json_data
	for(var i = 0; i < json_data.length; i++) {
		object = json_data[i]
		start_tag = "<td>"
		end_tag = "</td>"
		column1 = start_tag + object['order'] + end_tag
		column2 = start_tag + object['name'] + end_tag
		column3 = start_tag + object['date'] + end_tag
		column4 = start_tag + object['company'] + end_tag
		column5 = start_tag + object['start_time'] + end_tag
		column6 = start_tag + object['end_time'] + end_tag
		column7 = start_tag + object['e-mail'] + end_tag
		column8 = start_tag + object['time_zone'] + end_tag
		column9 = start_tag + "<button id='message' class='btn btn-xs btn-default' data-toggle='modal' data-target='#modal"+i+"'>View</button>" + end_tag
		column10 = start_tag + "<button id='approved-" + i +"' class='btn btn-xs btn-primary' onClick='handleAppointment(this.id)'>Approve</button>" + end_tag
		column11 = start_tag + "<button id='rejected-" + i +"' class='btn btn-xs btn-danger' onClick='handleAppointment(this.id)'>Reject</button>" + end_tag
		row = "<tr>" + column1 + column2 + column3 + column4 + column5 + column6 + column7 + column8 + column9 + column10 + column11 + "</tr>"
		table_rows += row
		modal = "<div class='modal fade' id='modal"+i+"' tabindex='-1' role='dialog' aria-labelledby='modal"+i+"Label'>"
		modal += `<div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>`
        modal += "<h4 class='modal-title' id='modal"+i+"Label'>"+object['name']+"'s Message</h4></div><div class='modal-body'>"
      modal += object['message']
      modal +=`</div></div></div></div>`
		table_rows += modal
	}
	appointments_list.innerHTML = table_rows
}

function ordersLoad(){
	getUnapprovedAppointments("https://api.erikamiguel.com/consult/unapproved",processUnapprovedAppointments)
}

function handleAppointment(id){
	document.getElementById(id).disabled = true;
	var id_arr = id.split("-");
	var status = id_arr[0];
	var index = id_arr[1];
      if(status.includes("approved")){
    	document.getElementById("rejected-"+index).disabled = true;
    } else {
    	document.getElementById("approved-"+index).disabled = true;
    }
    appointment = appointments[parseInt(index)]
	appointment[status] = "yes"
	var xhr = new XMLHttpRequest();
	xhr = new XMLHttpRequest();
	xhr.open("POST", 'https://api.erikamiguel.com/consult/new-consultation', true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.onreadystatechange = function () { 
	    if (xhr.readyState == 4 && xhr.status == 200) {
	        var json = JSON.parse(xhr.responseText);
	        if(status.includes("approved")){
	        	document.getElementById(id).className = "btn btn-xs btn-success";
	        	document.getElementById(id).innerHTML = "Approved";
	        } else {
	        	document.getElementById(id).className = "btn btn-xs btn-warning";
	        	document.getElementById(id).innerHTML = "Rejected";
	        }
	        
	        
	    }
	}
	var data = JSON.stringify(appointment);
	xhr.send(data);
}

function noOrders(){
	document.getElementById("unapproved_appointments").innerHTML = "No orders to approve."
}