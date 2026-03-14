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

exec sh -c "nginx -e /dev/null -c /app/nginx.conf && exec /opt/venv/bin/python3 -m uvicorn main:app --host 127.0.0.1 --port 8000 --loop uvloop"
