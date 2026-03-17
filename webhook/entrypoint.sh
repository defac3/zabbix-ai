#!/bin/sh

set -e
export PORT=9443 UPSTREAM=webhook BACKEND_PORT=9000 LOCATION=/
export LIMIT_REQ_ZONE= LIMIT_REQ= EXTRA_LOCATION=
envsubst '$PORT $UPSTREAM $BACKEND_PORT $LOCATION $LIMIT_REQ_ZONE $LIMIT_REQ $EXTRA_LOCATION' </app/nginx.conf >/app/nginx.gen.conf
exec sh -c "nginx -e /dev/null -c /app/nginx.gen.conf && exec /opt/venv/bin/python3 -m main"
