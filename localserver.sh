#!/usr/bin/env bash
echo
echo Starting local redis server...
redis-server &
sleep 1
echo Staring Remind Backend server.
source venv/bin/activate
python server.py
