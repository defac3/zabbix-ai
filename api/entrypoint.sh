#!/bin/sh
set -e

export OLLAMA_HOST=127.0.0.1

ollama serve &
OLLAMA_PID=$!

for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
  if curl -s http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    echo "Ollama ready"
    break
  fi
  sleep 1
  echo "Waiting for ollama to be ready... $i"
done

export PORT=8443 UPSTREAM=api BACKEND_PORT=8000 LOCATION=/api
export LIMIT_REQ_ZONE='limit_req_zone $binary_remote_addr zone=api_limit:10m rate=50r/s;'
export LIMIT_REQ='limit_req zone=api_limit burst=20 nodelay;'
export EXTRA_LOCATION='location / { return 444; }'
envsubst '$PORT $UPSTREAM $BACKEND_PORT $LOCATION $LIMIT_REQ_ZONE $LIMIT_REQ $EXTRA_LOCATION' </app/nginx.conf >/app/nginx.gen.conf
exec sh -c "nginx -e /dev/null -c /app/nginx.gen.conf && exec /opt/venv/bin/python3 -m uvicorn main:app --host 127.0.0.1 --port 8000 --loop uvloop"
