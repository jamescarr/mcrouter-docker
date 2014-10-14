#!/bin/bash

readonly PORT=${APP_PORT-"5000"}
readonly WORKERS=${NUMBER_OF_WORKERS-"1"}

echo $PORT
echo $WORKERS

gunicorn --access-logfile - --log-level debug --debug -b 0.0.0.0:$PORT -w $WORKERS app:app

