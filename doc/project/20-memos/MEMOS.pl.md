---
render_macros: true
---

# Indeks memów

Ten katalog zawiera krótkie notatki ideowe, zalążki i prompty projektowe, które nie są jeszcze na tyle dojrzałe, by stać się propozycjami, wymaganiami albo stories.

## Bieżące mema

{{ list_matching_pages("*.md", page=page, exclude="*.pl.md,*.en.md", summaries=true) }}

## Reguła promocji

Każdy memo powinien pozostać krótki. Gdy idea uzyska stabilną semantykę, jawnych aktorów albo presję implementacyjną, należy awansować ją do jednej z poniższych kategorii:

- `doc/project/30-stories/` dla scenariuszy użytkownika,
- `doc/project/40-proposals/` dla kierunku architektonicznego,
- `doc/project/50-requirements/` dla konkretnych wymagań systemowych,
- `doc/normative/50-constitutional-ops/`, jeżeli staje się normatywna.
