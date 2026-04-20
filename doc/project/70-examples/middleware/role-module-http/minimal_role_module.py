#!/usr/bin/env python3
"""Minimal Orbiplex role module example.

The process exposes one role capability behind Dator's `role-module` dispatch.
It deliberately contains no Sensorium connector logic. If a real role needs OS,
model, Git, filesystem, or network effects, it should call
`sensorium.directive.invoke` and let Sensorium-core mediate the connector.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

ROLE_CAPABILITY_ID = "role.example-summarizer.execute"
LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 47989


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def service_dispatch_response(
    task: dict[str, Any],
    status: str,
    *,
    answer_content: dict[str, Any] | None = None,
    message: str | None = None,
) -> dict[str, Any]:
    response: dict[str, Any] = {
        "schema_version": "v1",
        "capability_id": "service_dispatch_execute",
        "status": status,
        "dispatch/id": task.get("dispatch/id", "dispatch:unknown"),
        "provenance/origin-classes": ["role-module"],
        "message": message,
    }
    if status == "completed":
        response.update({
            "completed-at": iso_now(),
            "answer/content": answer_content or {},
            "answer/format": "application/json",
            "confidence/signal": 0.75,
            "human-linked-participation": False,
        })
    return response


def execute_role_task(task: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    if task.get("capability_id") != "role_task_execute":
        return 200, service_dispatch_response(
            task,
            "rejected-invalid-request",
            message="expected capability_id = role_task_execute",
        )
    if task.get("role/capability_id") != ROLE_CAPABILITY_ID:
        return 200, service_dispatch_response(
            task,
            "rejected-invalid-request",
            message="unsupported role/capability_id",
        )

    request_input = task.get("request/input")
    if not isinstance(request_input, dict):
        return 200, service_dispatch_response(
            task,
            "rejected-invalid-request",
            message="request/input must be an object",
        )

    text = str(request_input.get("text") or "")
    return 200, service_dispatch_response(
        task,
        "completed",
        answer_content={
            "summary": text[:120],
            "source_length": len(text),
            "workflow/run-id": task.get("workflow/run-id"),
            "workflow/phase-id": task.get("workflow/phase-id"),
            "correlation/id": task.get("correlation/id"),
        },
    )


def middleware_init_payload() -> dict[str, Any]:
    return {
        "schema_version": "v1",
        "module_name": "Example Role Module",
        "module_description": "Minimal role-module example for Dator authoring.",
        "module_role": "service-role",
        "capabilities": [
            {
                "capability_id": ROLE_CAPABILITY_ID,
                "class": "other",
                "description": "Executes the example summarizer role task.",
                "output_contract_ref": "middleware/schemas/service-dispatch-response.schema.json",
            }
        ],
        "handles_service_types": ["example/summarize"],
        "handles_workflow_kinds": [],
        "input_chains": [],
        "host_capability_handlers": [
            {
                "capability_id": ROLE_CAPABILITY_ID,
                "invoke_path": "/v1/role/execute",
            }
        ],
    }


class Handler(BaseHTTPRequestHandler):
    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length") or "0")
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def _write(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=True, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/healthz":
            self._write(200, {"status": "ok", "capability_id": ROLE_CAPABILITY_ID})
            return
        self._write(404, {"status": "not_found", "path": self.path})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/v1/middleware/init":
            self._write(200, middleware_init_payload())
            return
        if self.path == "/v1/role/execute":
            status, payload = execute_role_task(self._read_json())
            self._write(status, payload)
            return
        self._write(404, {"status": "not_found", "path": self.path})

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    server = ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), Handler)
    print(f"[role-module-example] listening on http://{LISTEN_HOST}:{LISTEN_PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
