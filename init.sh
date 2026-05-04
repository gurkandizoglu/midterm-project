#!/bin/bash

# Start SSH
mkdir -p /var/run/sshd
ssh-keygen -A
/usr/sbin/sshd

# Start web server
python -m gunicorn --bind 0.0.0.0:8000 app:app
