#!/usr/bin/env bash
echo
echo Starting local redis server...
redis-server &
echo Staring Remind Backend server. Endpoint: http://localhost:5000
source venv/bin/activate
python server.py
