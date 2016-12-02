function form_submit() {
	var form = $('#consultation_form');
	var name = form.find('input[name="full_name"]').val();
	var email = form.find('input[name="email"]').val();
	var phone_number = form.find('input[name="phone_number"]').val()
	var company = form.find('input[name="company"]').val()
	var date = formatDate(form.find('input[name="date"]').val().split("-").join("/"))
	var message = form.find('textarea[name="message"]').val();
	var hour_start = $("#hour_start :selected").text();
	var hour_end = $("#hour_end :selected").text();
	var minute_start = $("#minute_start :selected").text();
	var minute_end = $("#minute_end :selected").text();
	var start_meridian = getMeridian("start");
	var end_meridian = getMeridian("end");
	empty = getEmptyFields(name,email,phone_number,company,message,date);
	if(empty.length > 0){
		missing = "<b>Missing:</b> <br>"
		 for (var i = 0, j = empty.length; i < j; i++){
		 	item = "&nbsp;&nbsp;&nbsp;&nbsp;<b>" + empty[i] + "</b><br>"
			missing += item
		}
		document.getElementById("missing").innerHTML = missing;
		return
	} else {
		document.getElementById("missing").innerHTML = "";
	}

	incorrectFormat = isFormatCorrect(email,phone_number);
	if(incorrectFormat.length > 0 ){
		invalid = "<b>Incorrect Formatting:</b> <br>";
		for (var i = 0, j = incorrect.length; i < j; i++){
		 	item = incorrect[i];
			invalid += item;
		}
		document.getElementById("invalid").innerHTML = invalid;
		return
	} else {
		document.getElementById("invalid").innerHTML = "";
	}

	if (validateTimes(hour_start,hour_end,minute_start,minute_end,start_meridian, end_meridian)){
		var start_time = getTime(hour_start, minute_start,start_meridian);
		var end_time = getTime(hour_end, minute_end,end_meridian);
		var timezone = getTimeZone()
		createConsultation(name,email,phone_number,company,date,message,start_time,end_time,timezone);
	}
}

function isFormatCorrect(email,phone_number){
	incorrect = [];
	email_regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
	phone_number_regex = /^(?![a-zA-Z])([\+]?\d+[-]?[(]?\d+[)]?\d+[-.]?\d+[-.]?\d)$/;
	email_element = $('#consultation_form').find('input[name="email"]')[0];
	phone_number_element = $('#consultation_form').find('input[name="phone_number"]')[0];
	if(!email_regex.test(email)){
		incorrect.push("E-mail format should be <i>something@domain.com</i><br>");
		focusElement(email_element);
	} else {
		unFocusElement(email_element)
	}
	if(!phone_number_regex.test(phone_number)){
		incorrect.push("Phone number not valid.<br>");
		focusElement(phone_number_element);
	} else {
		unFocusElement(phone_number_element);
	}

	return incorrect;
}

function getEmptyFields(name,email,phone_number,company,message,date){
	var empty = []
	name_element = $('#consultation_form').find('input[name="full_name"]')[0];
	email_element = $('#consultation_form').find('input[name="email"]')[0];
	phone_number_element = $('#consultation_form').find('input[name="phone_number"]')[0];
	company_element = $('#consultation_form').find('input[name="company"]')[0];
	message_element = $('#consultation_form').find('textarea[name="message"]')[0];
	date_element = $('#consultation_form').find('input[name="date"]')[0];

	if(isEmpty(name)){
		empty.push("Name");
		focusElement(name_element);
	} else {
		unFocusElement(name_element);
	}
	if(isEmpty(email)){
		empty.push("E-mail");
		focusElement(email_element);
	} else {
		unFocusElement(email_element);
	}
	if(isEmpty(phone_number)){
		empty.push("Phone Number");
		focusElement(phone_number_element);
	} else {
		unFocusElement(phone_number_element);
	}
	if(isEmpty(company)){
		empty.push("Company");
		focusElement(company_element);
	} else {
		unFocusElement(company_element);
	}
	if(isEmpty(message)){
		empty.push("Message");
		focusElement(message_element);
	} else {
		unFocusElement(message_element);
	}
	if(date == "NaN/NaN/NaN"){
		empty.push("Date");
		focusElement(date_element);
	} else {
		unFocusElement(date_element);
	}
	return empty
}

function isEmpty(string){
	if(string == ""){
		return true
	}
	return false
}


function createConsultation(name,email,phone_number,company,date,message,start_time,end_time,timezone){
	var appointment = {
		"name": name,
		"e-mail": email,
		"date": date,
		"start_time": start_time,
		"end_time": end_time,
		"time_zone": timezone,
		"company": company,
		"message": message,
		"phone_number": phone_number
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

function validateTimes(hour_start,hour_end,minute_start,minute_end,start_meridian, end_meridian){
	var start_int = parseInt(hour_start)
	var end_int = parseInt(hour_end)
	var minute_start_int = parseInt(minute_start)
	var minute_end_int = parseInt(minute_end)
	var error_message = "Appointments should be 1 hour at most. Please modify times."
	if(start_meridian.includes("AM") && (start_int % 12) == 0){
		start_int = 0
	}
	if(end_meridian.includes("AM") && (end_int % 12) == 0){
		end_int += 12
	}
	if(start_meridian.includes("PM") && (start_int % 12) != 0){
		start_int += 12
	}
	if(end_meridian.includes("PM") && (end_int % 12) != 0){
		end_int += 12
	}
	if ((Math.abs(end_int-start_int) > 1) || ((Math.abs(end_int-start_int) >= 1) && (minute_end - minute_start > 0))) {
		document.getElementById("success").innerHTML = error_message
		return false
	} else if ((Math.abs(end_int-start_int) == 0)){
		document.getElementById("success").innerHTML = "Please select a time interval that is an hour at most."
		return false
	}
	return true
}

function focusElement(x) {
    x.style.background = "#FFC9C9";
}

function unFocusElement(x) {
    x.style.background = "";
}

Number.prototype.mod = function(n) {
	return ((this%n)+n)%n;
}

