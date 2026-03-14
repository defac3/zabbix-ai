from os import environ

OLLAMA_URL = environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = environ.get("OLLAMA_MODEL", "qwen2.5:3b")
