---
layout: post
title: Serverless still means servers
subtitle: Thoughts on building serverless APIs in AWS
date: 2017-07-28
author: Erika Miguel
---

There is still a server behind a serverless API....... I just wanted to pay homage to that server out there that is running my Lambda function. I don't know who you are or what your IP is, but I appreciate you.

As I was writing an API Gateway endpoint for work today, I wondered how much of my brief stint as a developer at my first job helped me. Well, when I was an intern at the company that would later be my first job, I learned what a REST API is and how to use HTTP verbs to call one. I learned what HTTP status codes were. I learned how to write unit tests and validate data. I learned how to return a response with headers. This is knowledge is necessary in building an API endpoint with API gateway.

For example, say you want to create an endpoint with a URL called https://myendpoint.mydomain.com/myAPI. To make this serverless, you would need to do a couple of things:
1. Actually code a lambda handler in either Java, Python, or Node
2. Put that code (as a zip or inline) into Lambda
3. Create the API Gateway resource. This is the path.
4. Create the API Gateway Method. This is the HTTP verb used to invoke your API (POST, PUT, GET, etc.)
5. Integrate the API Gateway Method with your Lambda function:
6. Map any query parameters to your Lambda input (vague. Might elaborate on this later) 
7. Map HTTP response codes to any errors/messages from your Lambda function


From the DevOps persepctive, once you've tested and deployed your API, you still have to map your SSL certificate (You better be using HTTPS!) and domain name to the API Gateway stage. If your certificate is managed with ACM, then you can just choose that option from the dropdown. Otherwise, you can use LetsEncrypt (free!) or any other certificate provider to get a certificate and paste the contents into API Gateway. To map your domain name to the API, if you are using GoDaddy/other provider, simply create a CNAME record to the CloudFront resource generated for you, or create an A record to the CloudFront resource in Route53.


On that note, I would say that writing your own API with API Gateway is a great way to blend programming skills with ops work. It's why I do what I do. 
