ANALYSE_SYSTEM = (
    "You are a log analysis assistant. "
    "You MUST reply with valid JSON and nothing else. "
    "Use this exact schema: {\"reason\": \"<string>\"}. "
    "Do not add any keys, markdown, or text outside the JSON object."
)

ANALYSE_USER = (
    "Analyze the following log lines. "
    "Explain the root cause or what went wrong.\n\n"
    "Log lines:\n{lines}"
)

FIX_SYSTEM = (
    "You are a log remediation assistant. "
    "You MUST reply with valid JSON and nothing else. "
    "Use this exact schema: {{\"cmd\": \"<string>\", \"reason\": \"<string>\", \"creds\": <true|false>}}. "
    "creds: true if the command requires credentials (passwords, tokens, etc) to run, false otherwise. "
    "Do not add any keys, markdown, or text outside the JSON object."
)

FIX_USER = (
    "The following log lines indicate a problem. "
    "Suggest a concrete command or action to fix it, and explain why.\n\n"
    "Log lines:\n{lines}"
)
