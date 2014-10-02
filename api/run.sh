#!/bin/bash

PORT    = ${APP_PORT-5000}
WORKERS = ${NUMBER_OF_WORKERS-1}

gunicorn --access-logfile - --log-level debug --debug -b 0.0.0.0:$PORT -w $WORKERS app

