#!/bin/bash

source /app/venv/bin/activate

service cron start

tail -f /dev/null