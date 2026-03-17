FROM alpine:latest
RUN apk add --no-cache python3 py3-pip
WORKDIR /app
COPY webhook/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY webhook/main.py webhook/const.py webhook/utils.py ./
COPY webhook/models/ models/
EXPOSE 9000
CMD ["python3", "-m", "main"]
