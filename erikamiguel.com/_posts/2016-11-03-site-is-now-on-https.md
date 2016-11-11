---
layout: post
title: Implementing your job skills in your personal life
subtitle: First post
date: 2016-11-03
author: Erika Miguel
---

At work, I set up web applications for developers. This entails setting up architecture on AWS, creating new build and deploy plans, and buying certs. I built this site in order to prove to myself that I could use my skills to create a personal brand. The site it hosted and s3 with HTTPS. Nothing major, but I'm excited about it.

These are the steps that I did to get the site up and running in two days:
1. Downloaded [jekyll](https://jekyllrb.com/)
2. Picked a [jekyll theme](http://jekyllthemes.org/)
3. Bought my domain, erikamiguel.com. I originally bought it through A Small Orange, and then I transferred it to AWS
4. Created an S3 bucket to host my static files
5. Downloaded [s3_website](https://github.com/laurilehmijoki/s3_website)
5. Ran a `jekyll build` and an `s3_website push` to get my files onto s3
6. Set up a CloudFront distribution with HTTPS, following this [tutorial](http://knightlab.northwestern.edu/2015/05/21/implementing-ssl-on-amazon-s3-static-websites/)

That's really all it takes!
