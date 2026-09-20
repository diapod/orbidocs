"""Pure rendering of the exhaustive host-local catalogue, not semantic prose."""

from __future__ import annotations

import html
from collections import defaultdict
from typing import Any

BEGIN = "<!-- BEGIN GENERATED HOST CAPABILITIES -->"
END = "<!-- END GENERATED HOST CAPABILITIES -->"
OTHER_FLAGS = (
    "advertisable",
    "passport/eligible",
    "signing-domain",
    "federated-discovery",
)
LABELS = {
    "en": {
        "title": "Complete Host-local Catalogue",
        "intro": (
            "Generated from `node:capability/capability-registry.v1.json`; do not edit this block.\n"
            "Regenerate both languages with `make capability-registry-docs`.\n"
            "Includes every entry with the `host-local` surface, regardless of lifecycle status\n"
            "or `docs.human-registry` (which selects only the curated table above)."
        ),
        "summary": "Entries: **{count}** host-local / **{total}** total; **{owners}** owner groups.",
        "legend": (
            "Grouped by the exact registry `owner`, then sorted by `capability/id`.\n"
            "`dispatchable` and `host-route` are independent eligibility flags; the last column\n"
            "lists the other flags set to `true` (omitted flags are `false`). Entries may also\n"
            "have the `federated` surface, shown explicitly below.\n\n"
            "Neither an entry nor `active` status guarantees an installed handler, a running\n"
            "endpoint, or caller authorization. Runtime availability, grants, approvals and\n"
            "domain policy remain separate checks. Wire names are not endpoint URLs."
        ),
        "header": "| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |",
    },
    "pl": {
        "title": "Pełny katalog host-local",
        "intro": (
            "Wygenerowano z `node:capability/capability-registry.v1.json`; nie edytuj tego bloku ręcznie.\n"
            "Obie wersje językowe odświeża `make capability-registry-docs`.\n"
            "Katalog obejmuje każdy wpis z powierzchnią `host-local`, niezależnie od statusu\n"
            "i `docs.human-registry` (ta flaga wybiera tylko ręczną tabelę powyżej)."
        ),
        "summary": "Wpisy: **{count}** host-local / **{total}** ogółem; grupy właścicieli: **{owners}**.",
        "legend": (
            "Grupowanie zachowuje dokładne wartości `owner` z rejestru; wpisy są sortowane po `capability/id`.\n"
            "`dispatchable` i `host-route` to niezależne flagi kwalifikacji; ostatnia kolumna\n"
            "wymienia pozostałe flagi ustawione na `true` (pominięte mają wartość `false`).\n"
            "Wpis może mieć również powierzchnię `federated`, pokazaną jawnie w tabeli.\n\n"
            "Ani obecność wpisu, ani status `active` nie gwarantują zainstalowanego handlera,\n"
            "działającego endpointu lub uprawnienia wywołującego. Dostępność runtime, granty,\n"
            "zgody i polityka domenowa pozostają odrębnymi kontrolami. Nazwy wire nie są URL-ami endpointów."
        ),
        "header": "| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |",
    },
}


def literal(value: str) -> str:
    """Keep registry strings literal even inside Markdown tables and headings."""
    escaped = html.escape(value)
    for character in "|`*_[]\\\r\n":
        escaped = escaped.replace(character, f"&#{ord(character)};")
    return f"<code>{escaped}</code>"


def render_host_catalogue(registry: dict[str, dict[str, Any]], language: str) -> str:
    labels = LABELS[language]
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in registry.values():
        if "host-local" in entry["surfaces"]:
            groups[entry["owner"]].append(entry)
    count = sum(len(entries) for entries in groups.values())
    lines = [
        BEGIN,
        "",
        '<a id="host-local-capabilities"></a>',
        "",
        f"## {labels['title']}",
        "",
        labels["intro"],
        "",
        labels["summary"].format(count=count, total=len(registry), owners=len(groups)),
        "",
        labels["legend"],
    ]
    for owner, entries in sorted(groups.items()):
        lines.extend(
            [
                "",
                f"### {literal(owner)}",
                "",
                labels["header"],
                "|---|---|---|---|---|---|---|",
            ]
        )
        for entry in sorted(entries, key=lambda item: item["capability/id"]):
            flags = entry["flags"]
            cells = [
                literal(entry["capability/id"]),
                literal(entry["wire/name"]),
                literal(entry["status"]),
                ", ".join(literal(surface) for surface in sorted(entry["surfaces"])),
                str(flags["dispatchable"]).lower(),
                str(flags["host-route"]).lower(),
                ", ".join(literal(flag) for flag in OTHER_FLAGS if flags[flag]) or "—",
            ]
            lines.append("| " + " | ".join(cells) + " |")
    return "\n".join([*lines, "", END])


def update_document(
    text: str, registry: dict[str, dict[str, Any]], language: str
) -> str:
    """Replace exactly one marked block, preserving everything outside it."""
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ValueError(
            "expected exactly one BEGIN/END GENERATED HOST CAPABILITIES block"
        )
    start, end = text.index(BEGIN), text.index(END)
    if start >= end:
        raise ValueError("generated catalogue markers are reversed")
    for marker, offset in ((BEGIN, start), (END, end)):
        if (offset and text[offset - 1] != "\n") or (
            offset + len(marker) < len(text)
            and text[offset + len(marker)] not in "\r\n"
        ):
            raise ValueError("generated catalogue markers must occupy their own lines")
    return (
        text[:start]
        + render_host_catalogue(registry, language)
        + text[end + len(END) :]
    )
