#!/usr/bin/env python3
"""Context-free maintenance relations after schema validation; never authority."""
import json
import re
import sys
from datetime import datetime


def instant(text):
    match = re.fullmatch(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.(\d{1,9}))?Z", text)
    if match is None:
        raise ValueError("invalid instant")
    delta = datetime.strptime(match[1], "%Y-%m-%dT%H:%M:%S") - datetime(1970, 1, 1)
    return (delta.days * 86400 + delta.seconds) * 10**9 + int((match[2] or "").ljust(9, "0"))


def validate(value):
    name = value["schema"]
    if name == "responsibility-maintenance-grant.local.v1":
        return value["grant/id"] == "grant/" + value["capability/id"] and instant(value["issued-at"]) < instant(value["expires-at"])
    if name == "responsibility-maintenance-plan.local.v1":
        generation, head = value["generation"], value["initial/head"]
        if (generation is None) != (head is None) or (head is not None and generation != head["generation"]):
            return False
        if generation is None and value["kind"] != "prepare":
            return False
        target = {"prepare":"verified", "abandon":"abandoned", "compact":"compacted", "reconcile":"reconciled"}.get(value["kind"])
        if value["kind"] == "verify":
            target = {"integrity":"verified", "archive-publication":"archive-verified", "shadow":"shadow-compared"}.get(value["verify/mode"])
        transition, compatibility = value["storage/transition"], value["compatibility"]
        return value["target"] == target and ((transition == "none" and compatibility is None) or (compatibility is not None and transition == str(compatibility["from/storage-version"]) + "-to-4"))
    if name == "responsibility-maintenance-retention-hold.local.v1":
        return value["action"] != "release" or value["predecessor/digest"] is not None
    if name == "responsibility-maintenance-report.local.v2":
        return len({case["id"] for case in value["cases"]}) == len(value["cases"]) and value["run/id"] == value["bindings"]["run/id"]
    return True


if __name__ == "__main__":
    try:
        with open(sys.argv[1], encoding="utf-8") as stream:
            valid = validate(json.load(stream))
    except (ValueError, KeyError, TypeError):
        valid = False
    sys.exit(0 if valid else 1)
