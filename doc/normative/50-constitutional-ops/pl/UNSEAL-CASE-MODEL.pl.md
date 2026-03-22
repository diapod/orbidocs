# Model sprawy odpieczętowania DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-UNSEAL-CASE-001` |
| `typ` | Ustawa wykonawcza / model danych |
| `wersja` | 0.1.0-draft |
| `data` | 2026-03-12 |

---

## 1. Cel dokumentu

Niniejszy dokument definiuje minimalny wspólny model sprawy odpieczętowania
(`unseal_case`) dla procedur `U1-U3`, tak aby tor dowodowy, odwoławczy i audytowy
mówił jednym językiem danych.

Dokument nie zastępuje progów ani właściwości organów opisanych w
`IDENTITY-UNSEALING-BOARD.pl.md`, `ABUSE-DISCLOSURE-PROTOCOL.pl.md` i
`PANEL-SELECTION-PROTOCOL.pl.md`; dostarcza im wspólnej struktury sprawy.

---

## 2. Zakres

Model `unseal_case` obejmuje:

- wnioski o zejście `nym -> node-id`,

- wnioski o zejście `node-id -> custodian_ref`,

- wnioski o zejście `node-id -> root-identity`,

- odwołania, rewizje i wygasanie takich decyzji,

- minimalne pola wymagane do śladu działania, retencji i notyfikacji.

---

## 3. Definicje

1. `unseal_case`

   Sprawa proceduralna, w której uczestnik lub organ wnosi o zejście z warstwy
   bardziej osłonowej do mniej osłonowej tożsamości.

2. `requested_scope`

   Zakres żądanego zejścia: `node_id`, `custodian_ref` albo `root_identity`.

3. `requestor_ref`

   Proceduralny identyfikator podmiotu inicjującego sprawę.

4. `affected_ref`

   Identyfikator podmiotu, którego dotyczy sprawa na warstwie aktualnie znanej
   w systemie, np. `nym_id` albo `node_id`.

5. `case_state`

   Stan sprawy w cyklu życia: `draft`, `submitted`, `screened`, `active`,
   `decided`, `appealed`, `stayed`, `expired`, `closed`.

---

## 4. Zasady

1. Każda sprawa odpieczętowania MUSI mieć pojedynczy, stabilny `case_id`.

2. Każda sprawa MUSI deklarować `requested_scope` i `current_known_scope`.

3. Każda sprawa MUSI wskazywać podstawę konstytucyjną i wykonawczą.

4. Każda sprawa MUSI rozróżniać:

   - sygnały,

   - poszlaki,

   - dowody,

   - decyzje,

   - skutki wykonawcze.

5. Zmiana zakresu z `U1` do `U2` lub `U3` MUSI tworzyć nową decyzję w tej samej
   sprawie, a nie nadpisywać historii.

6. Sprawa MUSI mieć jawny `appeal_window` oraz `expiry`, jeśli decyzja ma charakter
   czasowy.

---

## 5. Minimalny model danych

```yaml
unseal_case:
  case_id: "[stabilny identyfikator sprawy]"
  policy_id: "DIA-UNSEAL-CASE-001"
  constitution_basis:
    - "Art. III"
    - "Art. X"
  source_documents:
    - "IDENTITY-UNSEALING-BOARD.pl.md"
    - "ABUSE-DISCLOSURE-PROTOCOL.pl.md"
  requested_scope: "[node_id | custodian_ref | root_identity]"
  current_known_scope: "[nym | node_id | custodian_ref]"
  case_state: "[draft | submitted | screened | active | decided | appealed | stayed | expired | closed]"
  requestor_ref: "[proceduralny identyfikator wnioskodawcy]"
  affected_ref:
    kind: "[nym | node_id]"
    value: "[identyfikator]"
  federation_ref: "[identyfikator federacji lub null]"
  jurisdiction_refs:
    - "[identyfikator jurysdykcji]"
  stake_level: "S2"
  evidence_level: "E2"
  current_signal:
    summary: "[krótki opis sygnału teraźniejszego]"
    observed_at: "[ISO 8601]"
    continuity_claim: false
  evidence_bundle_refs:
    - "[referencja do pakietu dowodów]"
  decision_refs:
    - "[referencja do decyzji]"
  sanction_refs:
    - "[referencja do sankcji]"
  legal_notice_refs:
    - "[referencja lub []]"
  coi_check_ref: "[referencja do kontroli COI]"
  panel_ref: "[referencja do panelu albo FIP quorum]"
  created_at: "[ISO 8601]"
  updated_at: "[ISO 8601]"
  appeal_window:
    opens_at: "[ISO 8601]"
    closes_at: "[ISO 8601]"
  expiry: "[ISO 8601 | null]"
  retention_profile: "[short | medium | long | legal_hold]"
```

---

## 6. Decyzje w sprawie

Każda decyzja w sprawie MUSI być osobnym rekordem:

```yaml
decision_record:
  decision_id: "[identyfikator decyzji]"
  case_ref: "[case_id]"
  threshold_applied: "[U1 | U2 | U3]"
  outcome: "[approved | denied | partial | stayed]"
  scope_granted: "[node_id | custodian_ref | root_identity | none]"
  rationale: "[krótki opis uzasadnienia]"
  signer_refs:
    - "[rola lub organ]"
  decided_at: "[ISO 8601]"
  appealable_until: "[ISO 8601]"
  side_effect_refs:
    - "[sankcja / notyfikacja / blokada]"
```

---

## 7. Reguły retencji

1. `unseal_case` MUSI mieć profil retencji adekwatny do stawki i skutków.

2. Sprawy zakończone odmową i bez dalszych skutków POWINNY mieć krótszą retencję
   niż sprawy zakończone `U2` albo `U3`.

3. Rekord decyzji `U3` MUSI być objęty retencją co najmniej `legal_hold` albo
   równoważnym trybem archiwum zabezpieczonego.

---

## 8. Relacje do innych dokumentów

- `IDENTITY-UNSEALING-BOARD.pl.md` definiuje progi `U1-U3` i organy właściwe.

- `ABUSE-DISCLOSURE-PROTOCOL.pl.md` definiuje warunki wejścia w sprawę i zakres
  dopuszczalnych ujawnień.

- `PANEL-SELECTION-PROTOCOL.pl.md` definiuje sposób tworzenia panelu, jeśli sprawa
  nie trafia od razu do `FIP`.

- `TRACE-MINIMUM.pl.md`, gdy powstanie, powinien ujednolicić minimalny ślad dla
  `unseal_case` i `decision_record`.
