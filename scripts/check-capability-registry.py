#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
NODE_ROOT = ROOT.parent / "node"
NODE_CAPABILITY = NODE_ROOT / "capability" / "src" / "lib.rs"
NODE_PROTOCOL = NODE_ROOT / "protocol" / "src" / "lib.rs"
MACHINE_REGISTRY = NODE_ROOT / "capability" / "capability-registry.v1.json"
AUTHORIZATION_POLICY = NODE_ROOT / "capability" / "capability-authorization-policy.v1.json"
NODE_AUTHORIZATION_POLICY_EXAMPLE = (
    NODE_ROOT
    / "protocol"
    / "contracts"
    / "examples"
    / "p071-workbench.capability-authorization-policy.json"
)
REGISTRY_EN = ROOT / "doc" / "project" / "60-solutions" / "CAPABILITY-REGISTRY.en.md"
REGISTRY_PL = ROOT / "doc" / "project" / "60-solutions" / "CAPABILITY-REGISTRY.pl.md"
EXAMPLES_ROOT = ROOT / "doc" / "schemas" / "examples"
AUTHORIZATION_POLICY_EXAMPLE = (
    EXAMPLES_ROOT / "p071-workbench.capability-authorization-policy.json"
)
DAEMON_HOST_CAPABILITY_ROUTE_FILES = (
    NODE_ROOT / "daemon" / "src" / "endpoint_routes" / "common.rs",
    NODE_ROOT / "daemon" / "src" / "endpoint_routes" / "module_capability.rs",
)


CONST_RE = re.compile(r'pub const ([A-Z0-9_]+): &str = "([^"]+)";')
MAP_RE = re.compile(
    r"pub static CAPABILITY_ADVERTISEMENT_MAP: &\[\(&str, &str\)\] = &\[(.*?)\];",
    re.S,
)
ENTRY_RE = re.compile(r'\(\s*([A-Z0-9_]+|"[^"]+")\s*,\s*"([^"]+)"\s*,?\s*\)')
BARE_ID_RE = re.compile(r"^[a-z][a-z0-9-]*(\.[a-z0-9-]+)*$")
CORE_ID_RE = re.compile(r"^core/[a-z][a-z0-9-]*$")
SOVEREIGN_ID_RE = re.compile(
    r"^~?[A-Za-z0-9_/-]+@(participant|node|org):did:key:z[1-9A-HJ-NP-Za-km-z]+$"
)
WIRE_NAME_RE = re.compile(r"^(app|core|host|plugin|proof|role|sensorium|sovereign)/\S+$")
HOST_CAPABILITY_POST_ROUTE_RE = re.compile(
    r'\("POST",\s*"/v1/host/capabilities/([A-Za-z0-9_.-]+)"'
)
KNOWN_SURFACES = {"federated", "host-local"}
KNOWN_STATUS = {"active", "deprecated", "reserved"}
FLAG_KEYS = {
    "dispatchable",
    "advertisable",
    "passport/eligible",
    "signing-domain",
    "host-route",
    "federated-discovery",
}
POLICY_CALLER_POSTURES = {
    "host-grant-required",
    "operator-confirmation-required",
    "host-broker-grant-required",
}
POLICY_APPROVAL_MODES = {
    "auto-with-grant",
    "operator-approved-by-default",
    "operator-only",
}
POLICY_AUTONOMY_FLOORS = {
    "read-only",
    "observation-only",
    "proposed-effect",
    "bounded-auto",
}
POLICY_COI_POLICIES = {
    "not-applicable",
    "declaration-required",
    "operator-review-required",
}
P071_AUTHZ_POLICY_CAPABILITIES = {
    "sensorium.workbench.terminal",
    "sensorium.workbench.file",
    "sensorium.workbench.patch",
    "sensorium.workbench.env",
    "interaction-broker.wait",
    "interaction-broker.watch",
    "interaction-broker.probe",
}


class RegistryError(Exception):
    pass


def is_sovereign(capability_id: str) -> bool:
    return "@participant:did:key:" in capability_id or "@org:did:key:" in capability_id


def is_formal(capability_id: str) -> bool:
    return not is_sovereign(capability_id)


def validate_capability_id_shape(capability_id: str) -> bool:
    return bool(
        BARE_ID_RE.fullmatch(capability_id)
        or CORE_ID_RE.fullmatch(capability_id)
        or SOVEREIGN_ID_RE.fullmatch(capability_id)
    )


def expected_surfaces(flags: dict[str, bool]) -> set[str]:
    surfaces: set[str] = set()
    if flags["advertisable"] or flags["passport/eligible"] or flags["federated-discovery"]:
        surfaces.add("federated")
    if flags["dispatchable"] or flags["host-route"]:
        surfaces.add("host-local")
    return surfaces


def load_machine_registry() -> dict[str, dict[str, Any]]:
    raw = json.loads(MACHINE_REGISTRY.read_text(encoding="utf-8"))
    errors: list[str] = []
    if raw.get("schema/v") != "capability-registry.v1":
        errors.append("registry schema/v must be capability-registry.v1")
    entries = raw.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append("registry entries must be a non-empty array")
        entries = []

    by_id: dict[str, dict[str, Any]] = {}
    by_wire: dict[str, str] = {}
    for index, entry in enumerate(entries):
        prefix = f"entry[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix}: entry must be an object")
            continue
        capability_id = entry.get("capability/id")
        wire_name = entry.get("wire/name")
        flags = entry.get("flags")
        surfaces = entry.get("surfaces")
        status = entry.get("status")
        owner = entry.get("owner")

        if not isinstance(capability_id, str) or not capability_id:
            errors.append(f"{prefix}: capability/id must be a non-empty string")
            continue
        if capability_id in by_id:
            errors.append(f"{prefix}: duplicate capability/id {capability_id!r}")
        by_id[capability_id] = entry

        if not validate_capability_id_shape(capability_id):
            errors.append(f"{prefix}: invalid capability/id shape {capability_id!r}")
        if not isinstance(owner, str) or not owner:
            errors.append(f"{prefix}: owner must be a non-empty string")
        if not isinstance(wire_name, str) or not WIRE_NAME_RE.fullmatch(wire_name):
            errors.append(f"{prefix}: invalid wire/name {wire_name!r}")
        elif wire_name in by_wire:
            errors.append(
                f"{prefix}: duplicate wire/name {wire_name!r} used by {by_wire[wire_name]!r}"
            )
        else:
            by_wire[wire_name] = capability_id
        if status not in KNOWN_STATUS:
            errors.append(f"{prefix}: invalid status {status!r}")
        if not isinstance(flags, dict) or set(flags) != FLAG_KEYS:
            errors.append(f"{prefix}: flags must contain exactly {sorted(FLAG_KEYS)}")
            continue
        for name, value in flags.items():
            if not isinstance(value, bool):
                errors.append(f"{prefix}: flags.{name} must be boolean")
        if not isinstance(surfaces, list) or not surfaces:
            errors.append(f"{prefix}: surfaces must be a non-empty array")
        elif set(surfaces) - KNOWN_SURFACES:
            errors.append(f"{prefix}: unknown surfaces {sorted(set(surfaces) - KNOWN_SURFACES)}")
        elif set(surfaces) != expected_surfaces(flags):
            errors.append(
                f"{prefix}: surfaces {sorted(set(surfaces))} do not match flags-derived surfaces {sorted(expected_surfaces(flags))}"
            )

    if errors:
        raise RegistryError("\n".join(errors))
    return by_id


def validate_authorization_policy(registry: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    try:
        raw = json.loads(AUTHORIZATION_POLICY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{AUTHORIZATION_POLICY}: {exc}"]

    for mirror_path in (AUTHORIZATION_POLICY_EXAMPLE, NODE_AUTHORIZATION_POLICY_EXAMPLE):
        try:
            mirror = json.loads(mirror_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{mirror_path}: {exc}")
            continue
        if mirror != raw:
            errors.append(f"{mirror_path}: must mirror {AUTHORIZATION_POLICY}")

    if raw.get("schema/v") != "capability-authorization-policy.v1":
        errors.append("authorization policy schema/v must be capability-authorization-policy.v1")
    policy_id = raw.get("policy/id")
    if not isinstance(policy_id, str) or not policy_id.startswith(
        "policy:capability-authorization:"
    ):
        errors.append(
            "authorization policy policy/id must start with policy:capability-authorization:"
        )
    if raw.get("registry/ref") != "capability-registry.v1":
        errors.append("authorization policy registry/ref must be capability-registry.v1")

    entries = raw.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append("authorization policy entries must be a non-empty array")
        entries = []

    seen: set[str] = set()
    for index, entry in enumerate(entries):
        prefix = f"authorization policy entry[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix}: entry must be an object")
            continue
        capability_id = entry.get("capability/id")
        if not isinstance(capability_id, str) or not capability_id:
            errors.append(f"{prefix}: capability/id must be a non-empty string")
            continue
        if capability_id in seen:
            errors.append(f"{prefix}: duplicate capability/id {capability_id!r}")
        seen.add(capability_id)

        registry_entry = registry.get(capability_id)
        if registry_entry is None:
            errors.append(
                f"{AUTHORIZATION_POLICY}: unregistered policy capability {capability_id!r}"
            )
        elif registry_entry.get("status") == "reserved":
            errors.append(
                f"{AUTHORIZATION_POLICY}: reserved policy capability {capability_id!r}"
            )

        grants = entry.get("required/grants")
        if not isinstance(grants, list) or not grants:
            errors.append(f"{prefix}: required/grants must be a non-empty array")
        else:
            if len(set(grants)) != len(grants):
                errors.append(f"{prefix}: required/grants must be unique")
            for grant in grants:
                if not isinstance(grant, str) or not re.fullmatch(r"grant/\S+", grant):
                    errors.append(f"{prefix}: invalid required grant {grant!r}")

        if entry.get("caller/posture") not in POLICY_CALLER_POSTURES:
            errors.append(
                f"{prefix}: invalid caller/posture {entry.get('caller/posture')!r}"
            )
        if entry.get("approval/mode") not in POLICY_APPROVAL_MODES:
            errors.append(f"{prefix}: invalid approval/mode {entry.get('approval/mode')!r}")
        if entry.get("autonomy/floor") not in POLICY_AUTONOMY_FLOORS:
            errors.append(
                f"{prefix}: invalid autonomy/floor {entry.get('autonomy/floor')!r}"
            )
        if entry.get("coi/policy") not in POLICY_COI_POLICIES:
            errors.append(f"{prefix}: invalid coi/policy {entry.get('coi/policy')!r}")

    missing = sorted(P071_AUTHZ_POLICY_CAPABILITIES - seen)
    if missing:
        errors.append(
            "authorization policy is missing P071 seed capability ids: " + ", ".join(missing)
        )
    return errors


def load_runtime_capability_projection(path: Path, protocol_path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    consts = {name: value for name, value in CONST_RE.findall(text)}
    match = MAP_RE.search(text)
    if not match:
        raise RegistryError(f"Could not find CAPABILITY_ADVERTISEMENT_MAP in {path}")
    mapping: dict[str, str] = {}
    for raw_key, wire_name in ENTRY_RE.findall(match.group(1)):
        if raw_key.startswith('"'):
            capability_id = raw_key.strip('"')
        else:
            capability_id = consts.get(raw_key)
            if capability_id is None:
                raise RegistryError(
                    f"Map entry key {raw_key!r} is not a string literal and not a known const"
                )
        mapping[capability_id] = wire_name

    protocol_text = protocol_path.read_text(encoding="utf-8")
    protocol_consts = {name: value for name, value in CONST_RE.findall(protocol_text)}
    for const_name in (
        "CORE_CAP_MESSAGING",
        "CORE_CAP_DISCOVERY",
        "CORE_CAP_KEEPALIVE",
    ):
        capability_id = protocol_consts.get(const_name)
        if capability_id is None:
            raise RegistryError(f"Could not find {const_name} in {protocol_path}")
        mapping[capability_id] = capability_id

    node_operator = consts.get("NODE_PRIMARY_OPERATOR_CAPABILITY_ID")
    if node_operator is None:
        raise RegistryError(f"Could not find NODE_PRIMARY_OPERATOR_CAPABILITY_ID in {path}")
    mapping[node_operator] = "role/node-primary-operator"

    return mapping


def parse_human_registry_table(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    marker = "## Capability Registry"
    if marker not in text:
        raise RegistryError(f"Could not find {marker!r} in {path}")
    section = text.split(marker, 1)[1]
    rows: dict[str, str] = {}
    in_table = False
    for line in section.splitlines():
        if line.startswith("| capability_id |"):
            in_table = True
            continue
        if not in_table:
            continue
        if line.startswith("|---"):
            continue
        if not line.startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        capability = cells[0].strip("`")
        wire_name = cells[1].strip("`")
        rows[capability] = wire_name
    if not rows:
        raise RegistryError(f"No registry rows found in {path}")
    return rows


def docs_human_projection(registry: dict[str, dict[str, Any]]) -> dict[str, str]:
    projection: dict[str, str] = {}
    for capability_id, entry in registry.items():
        docs = entry.get("docs") or {}
        if docs.get("human-registry") is True:
            projection[capability_id] = entry["wire/name"]
    return projection


def advertisable_projection(registry: dict[str, dict[str, Any]]) -> dict[str, str]:
    projection: dict[str, str] = {}
    for capability_id, entry in registry.items():
        flags = entry.get("flags") or {}
        if flags.get("advertisable") is True:
            projection[capability_id] = entry["wire/name"]
    return projection


def compare_projection(expected: dict[str, str], actual: dict[str, str], label: str) -> list[str]:
    errors: list[str] = []
    expected_keys = set(expected)
    actual_keys = set(actual)
    missing = sorted(expected_keys - actual_keys)
    extra = sorted(actual_keys - expected_keys)
    if missing:
        errors.append(f"{label}: missing capability ids: {', '.join(missing)}")
    if extra:
        errors.append(f"{label}: extra capability ids: {', '.join(extra)}")
    for capability_id in sorted(expected_keys & actual_keys):
        if expected[capability_id] != actual[capability_id]:
            errors.append(
                f"{label}: wire name mismatch for {capability_id!r}: expected {expected[capability_id]!r}, got {actual[capability_id]!r}"
            )
    return errors


def compare_required_subset(required: dict[str, str], registry: dict[str, str], label: str) -> list[str]:
    errors: list[str] = []
    missing = sorted(set(required) - set(registry))
    if missing:
        errors.append(f"{label}: missing capability ids: {', '.join(missing)}")
    for capability_id in sorted(set(required) & set(registry)):
        if required[capability_id] != registry[capability_id]:
            errors.append(
                f"{label}: wire name mismatch for {capability_id!r}: expected {required[capability_id]!r}, got {registry[capability_id]!r}"
            )
    return errors


def require_registered(
    registry: dict[str, dict[str, Any]],
    capability_id: str,
    flag: str,
    source: Path,
    errors: list[str],
    wire_name: str | None = None,
) -> None:
    if not is_formal(capability_id):
        if not validate_capability_id_shape(capability_id):
            errors.append(f"{source}: invalid sovereign capability id {capability_id!r}")
        return
    entry = registry.get(capability_id)
    if entry is None:
        errors.append(f"{source}: unregistered formal capability id {capability_id!r}")
        return
    if entry.get("status") != "active":
        errors.append(f"{source}: capability id {capability_id!r} is not active")
    flags = entry.get("flags", {})
    if flags.get(flag) is not True:
        errors.append(f"{source}: capability id {capability_id!r} is not eligible for {flag}")
    if wire_name is not None and entry.get("wire/name") != wire_name:
        errors.append(
            f"{source}: wire/name mismatch for {capability_id!r}: expected {entry.get('wire/name')!r}, got {wire_name!r}"
        )



def validate_static_host_capability_routes(registry: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for path in DAEMON_HOST_CAPABILITY_ROUTE_FILES:
        text = path.read_text(encoding="utf-8")
        for capability_id in sorted(set(HOST_CAPABILITY_POST_ROUTE_RE.findall(text))):
            require_registered(registry, capability_id, "dispatchable", path, errors)
    return errors

def validate_capability_examples(registry: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for path in sorted(EXAMPLES_ROOT.glob("*.capability-advertisement.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for presented in data.get("capabilities/presented", []):
            capability_id = presented.get("capability/id")
            wire_name = presented.get("wire/name")
            if isinstance(capability_id, str):
                require_registered(registry, capability_id, "advertisable", path, errors, wire_name)
            passport = presented.get("passport")
            if isinstance(passport, dict) and isinstance(passport.get("capability_id"), str):
                require_registered(registry, passport["capability_id"], "passport/eligible", path, errors)

    for path in sorted(EXAMPLES_ROOT.glob("*.capability-passport-present.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        passport = data.get("passport")
        if isinstance(passport, dict) and isinstance(passport.get("capability_id"), str):
            require_registered(registry, passport["capability_id"], "passport/eligible", path, errors)

    for path in sorted(EXAMPLES_ROOT.glob("*.seed-capability-registration.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        capability_id = data.get("capability/id")
        if isinstance(capability_id, str):
            require_registered(registry, capability_id, "federated-discovery", path, errors)
        passport = data.get("passport")
        if isinstance(passport, dict) and isinstance(passport.get("capability_id"), str):
            require_registered(registry, passport["capability_id"], "passport/eligible", path, errors)
    return errors


def main() -> int:
    try:
        registry = load_machine_registry()
        runtime_projection = load_runtime_capability_projection(NODE_CAPABILITY, NODE_PROTOCOL)
    except (OSError, json.JSONDecodeError, RegistryError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    registry_by_wire = {capability_id: entry["wire/name"] for capability_id, entry in registry.items()}
    errors.extend(compare_required_subset(runtime_projection, registry_by_wire, "node runtime projection"))
    errors.extend(
        compare_required_subset(
            advertisable_projection(registry),
            runtime_projection,
            "advertisable registry projection",
        )
    )

    human_projection = docs_human_projection(registry)
    for registry_path in (REGISTRY_EN, REGISTRY_PL):
        try:
            human_registry = parse_human_registry_table(registry_path)
        except RegistryError as exc:
            errors.append(str(exc))
            continue
        errors.extend(compare_projection(human_projection, human_registry, registry_path.name))

    errors.extend(validate_static_host_capability_routes(registry))
    errors.extend(validate_capability_examples(registry))
    errors.extend(validate_authorization_policy(registry))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("ok capability registry, node projection, docs, and fixtures are in sync")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
