---
layout: post
title: Trying Out Google Compute Platform
subtitle: Google Compute Vanilla Test
date: 2017-03-22
author: Erika Miguel
---

Hi team! It's been a crazy week with job changes and laser eye surgery. I managed to find time to play around with Google Compute Engine. Nothing fancy, just a manual provisioning of an instance. Here are my notes:

Adding SSH keys for your Google Compute Instance:


- Choose a project
- On sidebar, Google Compute Engine -> Metadata
- Add an ssh key
- If you need to generate an ssh key run: ssh-keygen -t rsa -f /path/to/file
- Paste public key into Value
- These keys will give you access to any machines in your fleet, with sudo capabilities

Provisioning One Google Compute Instance on GUI:


- On sidebar, Google Compute Engine -> VM Instances
- Create
- SSH per usual methods


Notes:


- GUI is a little slow


