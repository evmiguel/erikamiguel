---
layout: post
title: Chef vs Puppet Architecture
subtitle: Which will prevail?
date: 2017-02-13
author: Erika Miguel
---

I have spent the last week setting up a simple Chef ecosystem. My first order of business was understanding the main components of a working Chef architecture. Chef requires:
1. Server - coordinate interaction with nodes and workstation; delegates environment and role specific files
2. Workstation - holds client list and repo
3. Node - client which receives configuration
I'd be interested to see how the Chef architecture would scale out.

This architecturee is different from the Puppet Master/Agent architecture, whereby the Puppet Master takes on the role of the Chef Server and Workstation. I'm curious to know why the people at opscode separated the two functions (Perhaps, I just need to read the documentation, heh). I haven't yet written any cookbooks, so I cannot adequately compare the configuration experience on the nodes. Saving that for another post!

I'm drawn to Chef's philosophy of Test Driven configuration. I do not write tests for my puppet configuration, and it doesn't seem intuitive that I should. The fact that Chef advertises testing is such a plus. Let's see how it works in practice. Until next time!


