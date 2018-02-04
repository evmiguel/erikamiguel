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
		* INITIALIZE AWS RESOURCES
		***************************************************************/
		this.dynamodb = new AWS.DynamoDB(AWS.config.credentials);
		this.s3 = new AWS.S3(AWS.config.credentials)

		this.getBlogPosts();
		
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

	/***********************************************************************
	* GET HTML CONTENT FROM S3
	************************************************************************/
	this.getHTMLContent = function(s3Objects){
		for (var s3Obj of s3Objects){
			var params = {
				Bucket: s3Obj.s3_bucket.S,
				Key: s3Obj.s3_bucket_prefix.S + "/" + s3Obj.filename.S
			};

			// OBJECT TO BIND TO CALLBACK
			var obj = { "obj" : this,
						"title" : s3Obj.title.S,
						"author" : s3Obj.author.S,
						"date" : epochToDate(s3Obj.date.N)
					};

			this.s3.getObject(params, function(err, data){
				if (err) console.log(err, err.stack);
				else {
					var title = "<h1>"+this.title+"</h1>";
					var author = "<h2>Author: "+this.author+"</h2>";
					var date = "<h3>Date: "+this.date+"</h3>";
					var metaContent = title + author + date;
					var bodyContent = new TextDecoder("utf-8").decode(data.Body);
					var content = metaContent + bodyContent;
					this.obj.generateUI(content); 
				}
			}.bind(obj));
		};
	},

	/***********************************************************************
	* GET BLOG POSTS FROM DYNAMODB
	************************************************************************/
	this.getBlogPosts = function(){
		var params = { TableName: blogTable};
		this.dynamodb.scan(params, function(err, data){
			if (err) console.log(err, err.stack); // an error occurred
   			else {
   				postData = data.Items.sort(function(p1,p2){
   					var a = parseInt(p1.id.N);
   					var b = parseInt(p2.id.N);
   					if (a < b){ return -1; }
   					if (a > b){ return 1; }
   					return 0;
   				});
   				
   				filteredPostData = postData.filter(function(obj){
   					return "title" in obj; // check if object has title key
   				});
   				this.getHTMLContent(filteredPostData);
   			}
		}.bind(this));
	}

	this.init()
}

/**************************************************************
*
* UTILITY FUNCTIONS
*
**************************************************************/
function epochToDate(datetimeString){
	var d = new Date(0);
	d.setUTCSeconds(datetimeString);
	return d;
}


/**************************************************************
*
* CREATE UI
*
**************************************************************/
window.onload = function() {
  new GenerateUI();       			
}
