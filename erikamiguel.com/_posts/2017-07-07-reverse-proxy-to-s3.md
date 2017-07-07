---
layout: post
title: Reverse Proxy to S3
subtitle: Light Architecture
date: 2017-07-07
author: Erika Miguel
---

June has been jam packed with lots of adventures! In the first week of June, I visited parts of LA to catch up with friends who I haven't seen in two years. It was also an opportunity to experience what it felt like to work remotely from a location that is a few timezones from my homebase. My routine in LA would be to wake up at 6am and work through to 2pm to accommodate east coast hours, then, sightseeing and time with friends after. 

In the second and third week of June, Megan and I fully moved out of NYC. In three trips between her house in CT and our 85th street apartment, we managed to pack our Prius with our belongings on the first two trips and then rented a 9' U-Haul van for the furniture. I'm definitely going to miss living in New York City. As someone who grew up and went to school in the Bronx, it was a big step for me to have my own apartment on the Upper East Side right out of college. I am thankful to have had the opportunity to get to know NYC from different perspectives of the city from changing locations. Right now, we are in between NY, CT, and MA before we start our lease in Boston in September.

The last week of June, I was in the Philippines! I arrived at JFK yesterday morning. It was a bittersweet journey coming home because I felt so whole being around family I haven't seen in 9 years, but I really needed to get back so that I could fully be myself with my partner and my community. Suffice it to say that LGBTQIA+ communities in the Philippines exist, as my cousins have told me, but my experience there showed me that I couldn't be fully out because it still wasn't quite OK. However, I tried my best to respect my family's point of view and kept a low profile about my life in the States. I am grateful that despite our differences, we were able to connect as people through our familial bond.

Now that I am back, though, I (finally) have the chance to write a post on a reverse proxy to S3 architecture. This was a fun architecture for me to build because the proxy itself did not go to a server (although, S3 is hosted on a server somewhere, though it doesn't seem like it). So, it's kind of like a hybrid serverless setup.

To achieve this reverse proxy setup you need:
1. ElasticLoadBalancer hooked up to an Autoscaling group with only 1 instance
2. CNAME record pointing to the loadbalancer (e.g. foo.example.com)
3. S3 bucket also named foo.example.com with static web hosting enabled

On the EC2 instance, I installed NGINX as the web server. S3 is able to identify requests from the web server by using the HTTP Referer header. So, the configuration in NGINX looks like this:

    server {
      listen *:80;
      server_name           foo.example.com;
    
      index  index.html index.htm index.php;
    
      access_log            /var/log/nginx/foo.example.com.access.log combined;
      error_log             /var/log/nginx/foo.example.com.error.log;
    
      location / {
        proxy_set_header Referer 'http://foo.example.com/';
        proxy_set_header Authorization '';
        proxy_hide_header x-amz-id-2;
        proxy_hide_header x-amz-request-id;
        proxy_hide_header Set-Cookie;
        proxy_ignore_headers "Set-Cookie";
        proxy_intercept_errors on;
        proxy_pass http://foo.example.com.s3-website-us-east-1.amazonaws.com/;
      }
    }

On the S3 side, you need to create a bucket policy to allow GET on resources with the Referer name. Like this:

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::foo.example.com/*",
                "Condition": {
                    "StringLike": {
                        "aws:Referer": "http://foo.example.com/*"
                    }
                }
            }
        ]
    }

That's all you need for this reverse proxy to S3. From there you can implement htpasswd or serve other content from the webserver.

Hope you enjoyed this post!
