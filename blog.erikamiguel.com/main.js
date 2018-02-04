/*******************************************************************************
*
* GENERATE UI OBJECT
*
* Requirements:
*   1. Create a file called config.js with values for
*			region			
*			identityPoolID
*			bucket
*			apiFile
*	2. Upload config.js in s3 bucket specified in config
*
********************************************************************************/
var GenerateUI = function()	{
	/************************************************************************
	* INIT FUNCTION
	*************************************************************************/
	this.init = function() {
		/**************************************************************
		* SET UP AWS COGNITO CONFIG
		***************************************************************/
		AWS.config.region = region;
		AWS.config.credentials = new AWS.CognitoIdentityCredentials({
		    IdentityPoolId: identityPoolID,
		});

		/**************************************************************
		* OBTAIN AWS CREDENTIALS USING COGNITO - LIMITED PERMISSIONS
		***************************************************************/
		AWS.config.credentials.get(function(){

		    // Credentials will be available when this function is called.
		    var accessKeyId = AWS.config.credentials.accessKeyId;
		    var secretAccessKey = AWS.config.credentials.secretAccessKey;
		    var sessionToken = AWS.config.credentials.sessionToken;

		});

		/**************************************************************
		* GET HTML CONTENT FROM S3 FILE
		***************************************************************/
		this.s3 = new AWS.S3(AWS.config.credentials)
		var params = {
				Bucket: bucket, 
		};
		this.s3.listObjects(params, function(err, data) {
			if (err) console.log(err, err.stack); // an error occurred
			else { this.processObjects(data.Contents) }
		}.bind(this));
	},

	/***********************************************************************
	* GENERATE UI FUNCTION
	************************************************************************/
	this.generateUI = function(html) {
		/**************************************************************
		* SET THE UI TO DISPLAY
		***************************************************************/
		el = document.getElementById("main");
		currentHTML = el.innerHTML;
		el.innerHTML = currentHTML + html;
	},

	this.processObjects = function(s3Objects){
		var params = {
			Bucket: bucket
		};
		for (var s3Obj of s3Objects){
			params.Key = s3Obj.Key
			this.s3.getObject(params, function(err, data){
				if (err) console.log(err, err.stack);
				else { 
					content = new TextDecoder("utf-8").decode(data.Body);
					this.generateUI(content); 
				}
			}.bind(this));
		}
	}

	this.init()
}


/**************************************************************
*
* CREATE UI
*
**************************************************************/
window.onload = function() {
  new GenerateUI();       			
}
