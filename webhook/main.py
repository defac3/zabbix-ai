from __future__ import annotations

from aiohttp import ClientSession, ClientTimeout
from aiohttp.web import run_app, json_response, Application

from const import (
    IMPORTANT_SEVERITIES,
    ZABBIX_API_TOKEN,
    ZABBIX_PASSWORD,
    ZABBIX_SCRIPT_ID,
    ZABBIX_URL,
    ZABBIX_USER,
)
from models import ZabbixAPI
from utils import call_api

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from aiohttp.web import Request, Response


Zabbix = ZabbixAPI(
    url=ZABBIX_URL,
    user=ZABBIX_USER,
    password=ZABBIX_PASSWORD,
    script_id=ZABBIX_SCRIPT_ID
)

async def handle_webhook(request: "Request") -> "Response":
    try:
        body = await request.json()
    except Exception:
        return json_response({"status": "ok", "reason": "invalid json"}, status=200)
    severity = body.get("severity") or body.get("alert_severity") or ""
    message = body.get("message") or body.get("alert_message") or ""
    subject = body.get("subject") or body.get("alert_subject") or ""
    hostid = str(body.get("hostid") or body.get("host_id") or "")
    lines = [s for s in (message.strip(), subject.strip()) if s]
    if not lines:
        lines = [message or subject or "No message"]
    if severity not in IMPORTANT_SEVERITIES:
        return json_response({"status": "ok", "reason": "low severity"}, status=200)
    async with ClientSession(timeout=ClientTimeout(total=60)) as session:
        fix_resp = await call_api(session, "/api/fix", {"lines": lines})
        if not fix_resp:
            return json_response({"status": "ok", "reason": "api_error"}, status=200)
        if fix_resp.get("creds") is True:
            return json_response({"status": "ok", "reason": "creds_required"}, status=200)
        cmd = fix_resp.get("cmd")
        if not cmd:
            return json_response({"status": "ok", "reason": "no_cmd"}, status=200)
        if ZABBIX_API_TOKEN:
            zabbix_auth = None
            zabbix_headers = {"Authorization": f"Bearer {ZABBIX_API_TOKEN}"}
        else:
            zabbix_auth = await Zabbix.login(session)
            if not zabbix_auth:
                return json_response(
                    {"status": "ok", "reason": "zabbix_auth_failed"}, status=200
                )
            zabbix_headers = None
        ok = await Zabbix.execute(
            session, hostid, cmd, auth=zabbix_auth, headers=zabbix_headers
        )
    return json_response(
        {"status": "remediated" if ok else "ok", "reason": "script_run" if ok else "script_failed"},
        status=200,
    )


def main() -> None:
    app = Application()
    app.router.add_post("/", handle_webhook)
    app.router.add_post("/webhook", handle_webhook)
    run_app(app, host="0.0.0.0", port=9000)

if __name__ == "__main__":
    main()
