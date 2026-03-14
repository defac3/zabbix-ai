#!/bin/sh

set -e
cd "$(dirname "$0")"
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout key.pem -out cert.pem \
  -subj "/CN=localhost/O=Local/C=XX"
chmod 644 cert.pem key.pem
