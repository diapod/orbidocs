#!/usr/bin/env python3
"""Minimal Python middleware with a server-html operator surface."""

from __future__ import annotations

import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def add_ui_helper_path() -> None:
    helper_dir = os.environ.get("ORBIPLEX_MIDDLEWARE_UI_PYTHON_LIB_DIR")
    if helper_dir:
        sys.path.insert(0, helper_dir)
        return

    vendored = Path(__file__).resolve().parent / "lib" / "ui" / "python"
    if vendored.exists():
        sys.path.insert(0, str(vendored))


add_ui_helper_path()

from orbiplex_middleware_ui import (  # noqa: E402
    HandlerMixin,
    MiddlewareEnv,
    nav_entry,
    panel,
    server_html_document,
    server_html_surface,
)

ENV = MiddlewareEnv.from_env(default_data_dir=Path.cwd() / "data")

SURFACE = server_html_surface(
    surface_id="example-python",
    label="Example Python",
    description="Example server-rendered Python middleware operator surface.",
    entry_path="ui",
    nav_entries=[
        nav_entry("Home", ""),
        nav_entry("Status", "status"),
    ],
    required_capabilities=["example.read"],
)


class Handler(HandlerMixin, BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        return

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0].rstrip("/")
        if path == "/healthz":
            self.write_json(200, {"ok": True})
            return
        if path in ("", "/ui"):
            self.write_html(
                200,
                server_html_document(
                    "Example Python",
                    panel("info", "Hello from a Python server-html surface."),
                    app_name="Example Python",
                ),
            )
            return
        if path == "/ui/status":
            self.write_html(
                200,
                server_html_document(
                    "Example Python Status",
                    panel("success", f"data_dir={ENV.data_dir}"),
                    app_name="Example Python",
                ),
            )
            return
        self.write_json(404, {"ok": False, "error": "not_found"})

    def do_POST(self) -> None:
        if self.path == "/v1/middleware/init":
            self.write_json(
                200,
                {
                    "module_id": "example-python",
                    "name": "Example Python",
                    "description": "Example supervised Python middleware.",
                    "middleware_contract_version": "0.1",
                    "host_api_version": "0.1",
                    "capabilities": ["example.read"],
                    "operator_surfaces": [SURFACE],
                },
            )
            return
        self.write_json(404, {"ok": False, "error": "not_found"})


def main() -> None:
    port = int(os.environ.get("PORT", "8080"))
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
