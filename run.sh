#!/bin/sh

cd /home/web
nohup python3 -m http.server 5151 &
nohup python3 /home/backend/app.py &

