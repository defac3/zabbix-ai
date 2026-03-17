from os import environ

IMPORTANT_SEVERITIES = frozenset(("High", "Disaster", "high", "disaster"))
API_URL = environ.get("API_URL", "https://api:8443").rstrip("/")
ZABBIX_URL = environ.get("ZABBIX_URL", "http://zabbix-web:80").rstrip("/")
ZABBIX_USER = environ.get("ZABBIX_USER", "Admin")
ZABBIX_PASSWORD = environ.get("ZABBIX_PASSWORD", "zabbix")
ZABBIX_API_TOKEN = environ.get("ZABBIX_API_TOKEN", "")
ZABBIX_SCRIPT_ID = environ.get("ZABBIX_SCRIPT_ID", "")
CA_PATH = environ.get("CA_PATH", "")
