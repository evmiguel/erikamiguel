function form_submit() {
	var form = document.getElementById("consultation_form");
	var name = form.elements[0].value;
	var email = form.elements[1].value;
	var date = formatDate(form.elements[2].value.split("-").join("/"))
	var start_time = getTime($("#hour_start :selected").text(), $("#minute_start :selected").text(),getMeridian("start"));
	var end_time = getTime($("#hour_end :selected").text(), $("#minute_end :selected").text(),getMeridian("end"));
	var timezone = getTimeZone()
	var appointment = {
		"name": name,
		"e-mail": email,
		"date": date,
		"start_time": start_time,
		"end_time": end_time,
		"time_zone": timezone
	}
	if(start_time.includes("PM") && end_time.includes("AM")){
		var end_date = new Date(date);
		end_date.setDate(end_date.getDate()+1);
		appointment.end_date = (end_date.getMonth()%12+1) + "/" + end_date.getDate() + "/" + end_date.getFullYear();
	}
	document.getElementById("success").innerHTML = "Appointment being made..."
	document.getElementById("consult-button").disabled = true;
	var xhr = new XMLHttpRequest();
	xhr = new XMLHttpRequest();
	var url = "url";
	xhr.open("POST", 'https://api.erikamiguel.com/consult/new-consultation', true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.onreadystatechange = function () { 
	    if (xhr.readyState == 4 && xhr.status == 200) {
	        var json = JSON.parse(xhr.responseText);
	        document.getElementById("success").innerHTML = "Success! You should get a confimation e-mail once your appointment is approved"
	        document.getElementById("consult-button").disabled = false;
	    }
	}
	var data = JSON.stringify(appointment);
	xhr.send(data);
}

function change_meridian(meridian) {
	addActive(meridian)
	start = "start";
	if (meridian.includes("end")) {
		start = "end";
	}
	element = document.getElementById(meridian);
	AM = element.innerHTML;
	if (AM.includes("AM") && AM.length == 2){
		opposite_meridian = start + "-pm"; 
		 if(isActive(opposite_meridian)){
		 	removeActive(opposite_meridian);
		 }
	} else {
		opposite_meridian = start + "-am"; 
		if(isActive(opposite_meridian)){
		 	removeActive(opposite_meridian);
		 }
	}
}

function isActive(element){
	if($("#"+element).hasClass("active")){
		return true
	}
	return false
}

function removeActive(element){
	$("#"+element).removeClass("active")
}

function addActive(element){
	$("#"+element).addClass("active")
}

function getTime(hour_start, minute_start, meridian){
	time = hour_start + ":" + minute_start + meridian
	return time
}

function getMeridian(start){
	if(start.includes("end")){
		start = "end"
	}
	meridian = start + "-pm"
	var AM = "AM"
	if (isActive(meridian)){
		AM = "PM"
	}
	return AM
}

function formatDate(date){
	month = date[5] + date[6]
	day = date[8] + date[9]
	year = date[0] + date[1] + date[2] + date[3]
	date = month + "/" + day + "/" + year
	return date
}

function getTimeZone(){
	var local = moment();
	var timezone = local.tz(moment.tz.guess()).format('z');
	var zone_name = local._z.name
	return zone_name
}

