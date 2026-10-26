#!/usr/bin/env python3
"""Offline documentation privacy gate; no private reverse map is read by CI."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from html.parser import HTMLParser
import ipaddress
import json
from pathlib import Path
import re
import subprocess
import stat
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
EXCEPTIONS = "scripts/document-privacy-exceptions.json"
PRIVATE_MAP = "local/host-pseudonyms.json"
IP4 = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"
PATTERNS = {
    "IPv4": re.compile(r"(?<![\w.])" + IP4 + r"(?![\w]|\.[\w])"),
    "IPv6": re.compile(r"(?<![0-9A-Za-z_:])(?:[0-9A-Fa-f]{0,4}:){2,}(?:" + IP4 +
                       r"|[0-9A-Fa-f]{0,4})(?:%[A-Za-z0-9_.-]+)?(?![0-9A-Za-z_:])"),
    "local-host": re.compile(r"(?<![\w.-])(?:[A-Za-z0-9_-]+\.)+local(?![\w-]|\.[\w-])", re.I),
    "invalid-pseudonym": re.compile(r"(?<![\w.-])(?:host-[A-Z]+\.local|IPADDR-[A-Z]+)[.-][\w.-]+"),
    "absolute-path": re.compile(r"/(?:Users|home/users|mnt)/|/private/(?:tmp|var|Users|home)/[\w]"
                                r"|/Volumes/[^\s<>\"'`|\[\]{}()\\.,;:]+"),
}
HOST_PSEUDONYM = re.compile(r"host-[A-Z]+\.local\Z")
# Explicit project-wide exceptions approved for documentation examples. Keep
# these exact: neither subdomains nor adjacent addresses inherit the exception.
EXAMPLE_HOSTS = frozenset({"orbiplex.local"})
EXAMPLE_IPV4 = frozenset({"1.3.2.1"})  # Also appears as the upstream zlib version.
SCHEMA_URN = re.compile(r"urn:orbiplex:schema:[A-Za-z0-9._-]+:v[0-9]+")
# Keep the old source-like scope, including extensionless text and diagrams.
TEXT_SUFFIXES = {".md", ".markdown", ".toml", ".yml", ".yaml", ".json", ".py", ".sh",
                 ".txt", ".edn", ".clj", ".cljs", ".cljc", ".mmd", ".mermaid", ".html",
                 ".css", ".js", ".csv", ".tsv", ".rst", ".adoc", ".svg", ".xml"}


@dataclass(frozen=True)
class Finding:
    kind: str
    value: str
    start: int
    end: int


def candidates(text: str) -> list[Finding]:
    """Lexical candidates, followed by syntax and explicit semantic exclusions."""
    urns = [m.span() for m in SCHEMA_URN.finditer(text)]
    found = []
    for kind, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            value = match.group()
            if kind.startswith("IPv"):
                try:
                    address = ipaddress.ip_address(value)
                except ValueError:
                    continue
                if address.version != int(kind[-1]):
                    continue
                mapped = getattr(address, "ipv4_mapped", None)
                if address.is_loopback or (mapped and mapped.is_loopback):
                    continue
                if address.version == 4 and int(address) == 0:
                    continue
                if kind == "IPv4" and value in EXAMPLE_IPV4:
                    continue
                # Regex non-capturing group containing a literal colon, not an IP.
                if value == ":" * 2 and text[max(0, match.start()-2):match.start()] == "(?":
                    continue
            if kind == "local-host":
                if value.lower() in EXAMPLE_HOSTS:
                    continue
                if HOST_PSEUDONYM.fullmatch(value):
                    continue
                if any(a <= match.start() and match.end() <= b for a, b in urns):
                    continue
            found.append(Finding(kind, value, match.start(), match.end()))
    ipv6 = [(f.start, f.end) for f in found if f.kind == "IPv6"]
    return sorted((f for f in found if not (f.kind == "IPv4" and
                  any(a <= f.start and f.end <= b for a, b in ipv6))), key=lambda f: f.start)


def load_exceptions(root: Path) -> list[dict]:
    data = json.loads((root / EXCEPTIONS).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != {"schema", "exceptions"} or data["schema"] != "document-privacy-exceptions.v1":
        raise ValueError("invalid exception registry")
    if not isinstance(data["exceptions"], list):
        raise ValueError("exceptions must be a list")
    for item in data["exceptions"]:
        if not isinstance(item, dict) or set(item) != {"path", "value", "context", "reason"} or not all(
            isinstance(v, str) and v for v in item.values()
        ):
            raise ValueError("each exception needs an exact path, value, context and reason")
        if (item["value"] not in item["context"] or "*" in item["path"]
                or Path(item["path"]).is_absolute() or ".." in Path(item["path"]).parts):
            raise ValueError("exception must be literal and scoped")
    return data["exceptions"]


def inspect(text: str, path: str, exceptions: list[dict]) -> list[Finding]:
    permitted = []
    for item in exceptions:
        if item["path"] != path:
            continue
        for match in re.finditer(re.escape(item["context"]), text):
            permitted.append((item["value"], match.start(), match.end()))
    return [f for f in candidates(text) if not any(
        value == f.value and a <= f.start and f.end <= b for value, a, b in permitted
    )]


def git_paths(root: Path) -> list[str]:
    args = ["git", "-C", str(root), "ls-files", "-z", "--cached",
            "--others", "--exclude-standard"]
    return sorted(set(subprocess.check_output(args).decode().rstrip("\0").split("\0")) - {""})


def report(text: str, path: str, findings: list[Finding]) -> int:
    for finding in findings:
        line = text.count("\n", 0, finding.start) + 1
        print(f"{path}:{line}: {finding.kind}: {finding.value}")
    return len(findings)


def check_sources(root: Path, exceptions: list[dict]) -> int:
    errors = 0
    for name in git_paths(root):
        if name == PRIVATE_MAP or name.startswith("local/"):
            print(f"{name}: private local material must not be tracked")
            errors += 1
            continue
        path = root / name
        if path.is_symlink():
            print(f"{name}: symlink is not a checked documentation source")
            errors += 1
            continue
        if not path.exists():
            continue  # Working-tree deletion; CI sees the committed tree.
        if path.suffix and path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        raw = path.read_bytes()
        if b"\0" in raw:
            raise ValueError(f"{name}: NUL in source-like text")
        text = raw.decode("utf-8-sig")  # Decode failure is an error, not a clean scan.
        if name == EXCEPTIONS:
            # Registry literals are auditable test inputs; validate its other fields.
            text = "\n".join(i["path"] + " " + i["reason"] for i in exceptions)
        errors += report(text, name, inspect(text, name, exceptions))
    return errors


class VisibleHTML(HTMLParser):
    """Rejoin syntax-highlighted spans and scan attributes as well as visible text."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.attributes: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag not in {"span", "em", "strong"}:
            self.parts.append("\n")
        self.attributes.extend(value for _, value in attrs if value is not None)

    def handle_endtag(self, tag):
        if tag not in {"span", "em", "strong"}:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)


def source_path(location: str) -> str:
    path = unquote(urlsplit(location).path).lstrip("/")
    if path.startswith(("pl/", "en/", "cs/")):
        path = path.split("/", 1)[1]
    if path.endswith("index.html"):
        path = path[:-10]
    if path.endswith("/"):
        return path[:-1] + ".md"
    if path.endswith(".html"):
        return path[:-5] + ".md"
    return path


def rendered_exceptions(text: str, source: str, exceptions: list[dict]) -> list[Finding]:
    # HTML rendering changes punctuation and whitespace. Require the same source
    # document and exact reviewed token; source checking runs first with context.
    def family(path):
        return re.sub(r"\.(?:en|pl|cs)\.md$", ".md", path)
    allowed = {e["value"] for e in exceptions if family(e["path"]) == family(source)}
    return [f for f in candidates(text) if f.value not in allowed]


def check_site(site: Path, exceptions: list[dict]) -> int:
    if not site.is_dir() or next(site.rglob("*.html"), None) is None:
        raise ValueError("site must be an existing MkDocs output containing HTML pages")
    errors = 0
    for path in sorted(site.rglob("*")):
        if path.is_symlink():
            raise ValueError("symlink in published tree")
        if not path.is_file():
            continue
        name = path.relative_to(site).as_posix()
        if "host-pseudonyms.json" in path.name:
            print(f"{name}: private map must not be published")
            errors += 1
        if path.suffix == ".html":
            parser = VisibleHTML()
            parser.feed(path.read_text(encoding="utf-8"))
            text = "".join(parser.parts) + "\n" + "\n".join(parser.attributes)
            errors += report(text, name, rendered_exceptions(text, source_path(name), exceptions))
        elif path.name == "search_index.json":
            data = json.loads(path.read_text(encoding="utf-8"))
            for entry in data["docs"]:
                text = entry["title"] + "\n" + entry["text"]
                errors += report(text, name + ":" + entry["location"], rendered_exceptions(
                    text, source_path(entry["location"]), exceptions))
        elif path.suffix in {".json", ".md", ".txt", ".xml", ".mmd", ".mermaid"}:
            text = path.read_text(encoding="utf-8")
            errors += report(text, name, inspect(text, source_path(name), exceptions))
    return errors


def check_private_map(root: Path) -> None:
    """Validate local editing metadata without returning aliases in diagnostics."""
    path = root / PRIVATE_MAP
    if path.is_symlink() or stat.S_IMODE(path.stat().st_mode) != 0o600:
        raise ValueError("private map must be a regular owner-only file (0600)")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != {"schema", "hosts", "addresses"} or data["schema"] != "documentation-pseudonyms.local.v1":
        raise ValueError("invalid private map shape")
    if not isinstance(data["hosts"], dict) or not isinstance(data["addresses"], dict):
        raise ValueError("private map groups must be objects")
    aliases = set()
    for label, entry in data["hosts"].items():
        if not HOST_PSEUDONYM.fullmatch(label) or not isinstance(entry, dict) or set(entry) != {"aliases"}:
            raise ValueError("invalid host entry")
        if not isinstance(entry["aliases"], list) or not entry["aliases"]:
            raise ValueError("a populated host entry requires aliases")
        for alias in entry["aliases"]:
            if not isinstance(alias, str) or not re.fullmatch(r"[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)+\.?", alias):
                raise ValueError("invalid host alias")
            normalized = alias.rstrip(".").lower()
            if normalized in aliases or normalized in {key.lower() for key in data["hosts"]}:
                raise ValueError("duplicate or conflicting host alias")
            aliases.add(normalized)
    addresses = set()
    for label, entry in data["addresses"].items():
        if not re.fullmatch(r"IPADDR-[A-Z]+", label) or not isinstance(entry, dict) or set(entry) != {"address"}:
            raise ValueError("invalid address entry")
        try:
            address = ipaddress.ip_address(entry["address"])
        except (ValueError, TypeError):
            raise ValueError("invalid mapped IP address") from None
        if address in addresses:
            raise ValueError("duplicate mapped address")
        addresses.add(address)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check-map", action="store_true", help="validate the ignored local reverse map without printing it")
    parser.add_argument("--site", type=Path, help="also inspect built pages, search index and text downloads")
    args = parser.parse_args()
    try:
        exceptions = load_exceptions(args.root)
        errors = check_sources(args.root, exceptions)
        if args.check_map:
            check_private_map(args.root)
        if args.site:
            errors += check_site(args.site, exceptions)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"Privacy check failed: {exc}", file=sys.stderr)
        return 2
    if errors:
        print(f"{errors} privacy finding(s). Use pseudonyms or a reviewed, scoped exception.")
        return 1
    print("Documentation privacy check passed (no private map required).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
