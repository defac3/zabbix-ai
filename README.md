# Automated incident response system based on Zabbix

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Alpine](https://img.shields.io/badge/Alpine-0D597F?logo=alpinelinux&logoColor=white)](https://alpinelinux.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Nginx](https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white)](https://nginx.org/)
[![Ollama](https://img.shields.io/badge/Ollama-000000?logo=ollama&logoColor=white)](https://ollama.com/)

## Running

```bash
docker compose up --build -d
```

## Net (zabbix_net 10.88.77.0/24)

| Сервис              | DNS (имя хоста)     | IPv4       | Порт  |
|---------------------|---------------------|------------|-------|
| Zabbix server       | zabbix-server       | 10.88.77.20| 10051 |
| Zabbix web          | zabbix-web          | (DHCP)     | 8080  |
| Agent (Debian)      | zabbix-agent-debian | 10.88.77.10| 10050 |
| Agent (Ubuntu)      | zabbix-agent-ubuntu | 10.88.77.11| 10050 |
| Agent (Rocky/Alma)  | zabbix-agent-rocky  | 10.88.77.12| 10050 |
| API                 | api                 |     DHCP     | 8443  |
| Webhook             | webhook             |     DHCP     | 9443  |
| PostgreSQL          | postgres            |     DHCP     | 5432  |

## TODO

- [ ] middleware request/response AI
- [ ] Webhook/custom plugin по UNIX socket для получения ошибок с агентов Zabbix
