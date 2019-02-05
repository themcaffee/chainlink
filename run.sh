#!/bin/bash

redis-server &
supervisord -n -c supervisord.conf &
source venv/bin/activate
python run_server.py