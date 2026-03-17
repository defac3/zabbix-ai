FROM alpine:latest

RUN apk add --no-cache python3 nginx gettext

RUN addgroup -g 1000 -S app && adduser -u 1000 -S -G app -h /app -D app

WORKDIR /app

COPY webhook/requirements.txt requirements.txt
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install -r requirements.txt

COPY webhook/ .
COPY nginx/nginx.conf /app/nginx.conf
RUN chmod +x /app/entrypoint.sh

RUN mkdir -p /app/.nginx/tmp/client_body /app/.nginx/tmp/proxy && \
    chown -R app:app /app /opt/venv /var/lib/nginx /var/log/nginx /app/.nginx/tmp
USER app

EXPOSE 9443
ENTRYPOINT ["/app/entrypoint.sh"]