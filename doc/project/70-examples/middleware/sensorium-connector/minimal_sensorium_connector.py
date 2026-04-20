#!/usr/bin/env python3
"""Minimal Orbiplex Sensorium connector example.

The connector exposes `sensorium.connector.invoke`, but ordinary consumers and
role modules should not call it directly. They call `sensorium.directive.invoke`;
Sensorium-core mediates policy, allowlist lookup, audit, and admission.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

MODULE_ID = "example-sensorium-connector"
CONNECTOR_CLASS = "example"
ACTION_ID = "example.echo"
LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 47990


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def diagnostic(level: str, code: str, message: str, **extra: Any) -> dict[str, Any]:
    item: dict[str, Any] = {"level": level, "code": code, "message": message}
    item.update(extra)
    return item


def connector_result(
    status: str,
    *,
    result: dict[str, Any] | None = None,
    observations: list[dict[str, Any]] | None = None,
    diagnostics: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "schema": "sensorium-connector-result.v1",
        "status": status,
        "connector/id": MODULE_ID,
        "connector/kind": CONNECTOR_CLASS,
        "result": result or {},
        "artifacts": [],
        "observations": observations or [],
        "diagnostics": diagnostics or [],
    }


def connector_observation(
    *,
    directive: dict[str, Any],
    text: str,
    signal_kind: str,
    signal_family: str | None,
) -> dict[str, Any]:
    observed_at = iso_now()
    observation: dict[str, Any] = {
        "schema": "sensorium-observation.v1",
        "schema/v": 1,
        "connector/id": MODULE_ID,
        "connector/kind": CONNECTOR_CLASS,
        "observed/at": observed_at,
        "connector/submitted_at": observed_at,
        "signal/kind": signal_kind,
        "summary": {"lang": "en", "text": f"Echo connector observed {len(text)} characters."},
        "subject/kind": "example-message",
        "subject/id": str(directive.get("directive/id") or "directive:unknown"),
        "confidence": {"class": "high"},
        "freshness": {"ttl_sec": 3600},
        "sensitivity": {"class": "public"},
        "source/ref": {"kind": "connector", "value": MODULE_ID},
        "evidence/refs": [],
    }
    if signal_family:
        observation["signal/family"] = signal_family
    if directive.get("correlation/id"):
        observation["correlation/id"] = directive["correlation/id"]
    return observation


def connector_invoke(request: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    directive = request.get("directive")
    if not isinstance(directive, dict):
        return 400, connector_result(
            "failed",
            diagnostics=[diagnostic("error", "directive-missing", "directive must be an object")],
        )
    if directive.get("action_id") != ACTION_ID:
        return 422, connector_result(
            "failed",
            diagnostics=[diagnostic("error", "action-not-supported", "unsupported action_id")],
        )

    parameters = directive.get("parameters")
    if not isinstance(parameters, dict):
        return 422, connector_result(
            "failed",
            diagnostics=[diagnostic("error", "parameters-invalid", "parameters must be an object")],
        )

    text = str(parameters.get("text") or "")
    allowlist = request.get("allowlist_entry") if isinstance(request.get("allowlist_entry"), dict) else {}
    result_contract = allowlist.get("result_contract") if isinstance(allowlist.get("result_contract"), dict) else {}
    signal_kind = str(result_contract.get("signal_kind") or "ai.orbiplex.example/echo")
    signal_family_value = result_contract.get("signal_family")
    signal_family = str(signal_family_value) if isinstance(signal_family_value, str) else None
    result = {
        "action_id": ACTION_ID,
        "echo": text,
        "text_length": len(text),
    }
    observation = connector_observation(
        directive=directive,
        text=text,
        signal_kind=signal_kind,
        signal_family=signal_family,
    )
    return 200, connector_result(
        "completed",
        result=result,
        observations=[observation],
        diagnostics=[diagnostic("info", "action-completed", "example echo action completed")],
    )


def middleware_init_payload() -> dict[str, Any]:
    return {
        "schema_version": "v1",
        "module_name": "Example Sensorium Connector",
        "module_description": "Minimal Sensorium connector example.",
        "module_role": "sensorium-connector",
        "connector_class": CONNECTOR_CLASS,
        "connector_sensitivity_baseline": "public",
        "connector_incidental_effects": [],
        "connector_actions": [
            {
                "action_id": ACTION_ID,
                "parameters_schema": "schemas/example.echo.params.v1.json",
                "result_schema": "schemas/example.echo.result.v1.json",
            }
        ],
        "connector_observations": [
            {
                "signal_kind": "ai.orbiplex.example/echo",
                "signal_family": "example/echo",
            }
        ],
        "handles_service_types": [],
        "handles_workflow_kinds": [],
        "input_chains": [],
        "capabilities": [
            {
                "capability_id": "sensorium.connector.example.echo",
                "class": "other",
                "description": "Produces an example echo result and observation candidate.",
                "output_contract_ref": None,
            }
        ],
        "host_capability_handlers": [
            {
                "capability_id": "sensorium.connector.invoke",
                "invoke_path": "/v1/sensorium/connector/invoke",
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
            self._write(200, {"status": "ok", "module_role": "sensorium-connector"})
            return
        self._write(404, {"status": "not_found", "path": self.path})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/v1/middleware/init":
            self._write(200, middleware_init_payload())
            return
        if self.path == "/v1/sensorium/connector/invoke":
            status, payload = connector_invoke(self._read_json())
            self._write(status, payload)
            return
        self._write(404, {"status": "not_found", "path": self.path})

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    server = ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), Handler)
    print(f"[{MODULE_ID}] listening on http://{LISTEN_HOST}:{LISTEN_PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
