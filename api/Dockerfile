FROM alpine:latest
USER root

RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

RUN apk update && apk add --no-cache python3 curl nginx ollama

RUN addgroup -g 1000 -S app && adduser -u 1000 -S -G app -h /app -D app

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY api/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /app

COPY api/ .
COPY nginx/nginx.conf /app/nginx.conf

RUN chmod +x entrypoint.sh

RUN mkdir -p /app/.ollama /app/.nginx/tmp/client_body /app/.nginx/tmp/proxy && \
    chown -R app:app /app /opt/venv /var/lib/nginx /var/log/nginx

ENV HOME=/app

ENV OLLAMA_MODELS=/app/.ollama
RUN (ollama serve &) && sleep 15 && ollama pull qwen2.5:3b
RUN pkill ollama 2>/dev/null || true
RUN chown -R app:app /app/.ollama

USER app
EXPOSE 8443
ENTRYPOINT ["./entrypoint.sh"]
