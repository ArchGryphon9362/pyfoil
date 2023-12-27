#!/bin/sh

THREADS=${THREADS:-8}
PORT=${PORT:-9997}

gunicorn -k gevent -w $THREADS 'server:create_app()' -b 0.0.0.0:$PORT
