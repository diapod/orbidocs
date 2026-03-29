# Profile limitów i przenośności UBC

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-UBC-LIMITS-001` |
| `typ` | Ustawa wykonawcza / profile limitów i przenośności |
| `wersja` | `0.1.0-draft` |
| `podstawa` | Art. XII.11-13 Konstytucji DIA; `UNIVERSAL-BASIC-COMPUTE.pl.md`; `FIP-MEMBERSHIP-AND-QUORUM.pl.md` |
| `status mechanizmów` | profile `bridge_minimum`, `trans_federation_limited` i katalog limitów są normatywne; federacje mogą je rozszerzać, ale nie osłabiać |

---

## 1. Cel dokumentu

`UNIVERSAL-BASIC-COMPUTE.pl.md` definiuje prawo do minimalnego przydziału
obliczeniowego, lecz pozostawia otwarte pytanie, jak dokładnie opisywać:

- profile limitów dla komunikacji i trybów pomocowych,
- profile przenośności między federacjami,
- minimalny tor uznawania trans-federacyjnego `Proof-of-Personhood` przez most
  lub rejestr `FIP`.

Niniejszy dokument wypełnia tę lukę.

---

## 2. Zasada ogólna

1. Profil limitów jest nazwanym kontraktem danych, a nie lokalnym zwyczajem
   implementacyjnym.
2. Profil przenośności określa, jaki minimalny zakres `UBC` jest honorowany
   lokalnie, między federacjami oraz przez minimalny most `FIP`.
3. Uznawanie trans-federacyjne może przebiegać:
   - przez bezpośrednie uznanie federacyjne,
   - przez minimalny rejestr/most `FIP`,
   - przez kombinację obu ścieżek.
4. Most `FIP` gwarantuje wyłącznie profil `bridge_minimum`, chyba że federacja
   jawnie zadeklaruje rozszerzenie.
5. Federacja może podnosić limity albo dodawać profile, lecz nie może zejść
   poniżej minimum określonego w tym dokumencie.

---

## 3. Pojęcia podstawowe

| Pojęcie | Znaczenie |
| :--- | :--- |
| `ubc_limit_profile` | nazwany profil limitów dla konkretnego trybu dostępu |
| `ubc_portability_profile` | nazwany profil określający zakres honorowania `UBC` lokalnie i trans-federacyjnie |
| `bridge_minimum` | minimalny profil dostępny przy uznaniu PoP przez most `FIP` |
| `federation_extension` | profil rozszerzający minimum przez decyzję federacji |
| `fip_pop_bridge_record` | rekord opisujący minimalny most/rejestr `FIP` dla uznawania PoP |

---

## 4. Kanoniczne profile limitów

### 4.1. `emergency_unlimited`

Profil obowiązkowy dla trybów ratunkowych.

- `access = true`
- `volume_limit = none`
- `rate_limit = none`
- `hard_stop = forbidden`

### 4.2. `communication_limited`

Profil minimalny dla komunikacji trans-federacyjnej.

- `access = true`
- `volume_limit = required`
- `rate_limit = allowed`
- `hard_stop = forbidden` dla ścieżek krytycznych do wezwania pomocy

### 4.3. `care_limited`

Profil minimalny dla trybów opiekuńczych i pomocowych.

- `access = true`
- `volume_limit = required`
- `rate_limit = allowed`
- `hard_stop = allowed` wyłącznie po wyczerpaniu jawnego limitu, nigdy dla ratunku

### 4.4. `bridge_minimum`

Profil przenośności gwarantowany przez most `FIP`.

- `emergency = emergency_unlimited`
- `communication = communication_limited`
- `care = care_limited`
- `expansion_authority = federation_only`

### 4.5. `trans_federation_extended`

Profil przenośności szerszy niż minimum, deklarowany federacyjnie.

- może podnosić limity komunikacyjne,
- może podnosić limity pomocowe,
- może dodawać lokalne tryby opieki,
- MUSI pozostawiać jawny ślad polityki i wersji profilu.

---

## 5. Minimalny model danych

### 5.1. `ubc_limit_profile`

```yaml
ubc_limit_profile:
  profile_id: "[identyfikator]"
  mode: "communication" # emergency | communication | care
  profile_class: "limited" # unlimited | limited | extended
  access: true
  volume_limit:
    amount: 100
    unit: "messages_per_day"
  rate_limit:
    amount: 10
    unit: "messages_per_hour"
  hard_stop: false
  emergency_override: true
  policy_ref: "DIA-UBC-LIMITS-001"
```

### 5.2. `ubc_portability_profile`

```yaml
ubc_portability_profile:
  portability_profile_id: "[identyfikator]"
  scope: "trans_federation_limited" # local_only | trans_federation_limited | trans_federation_extended
  recognition_paths:
    federation_direct: true
    fip_bridge: true
  emergency_profile_ref: "emergency_unlimited"
  communication_profile_ref: "communication_limited"
  care_profile_ref: "care_limited"
  federation_extension_allowed: true
  policy_ref: "DIA-UBC-LIMITS-001"
```

### 5.3. `fip_pop_bridge_record`

```yaml
fip_pop_bridge_record:
  bridge_id: "[identyfikator mostu/rejestru]"
  operator_ref: "[FIP lub wyspecjalizowany komponent FIP]"
  recognized_attestation_refs:
    - "[proof_of_personhood_attestation]"
  guaranteed_portability_profile_ref: "bridge_minimum"
  extension_profile_refs: []
  audit_ref: "[referencja do audytu albo migawki mostu]"
  created_at: "[timestamp]"
```

---

## 6. Reguły zgodności

System nie spełnia tej polityki, jeżeli:

1. most `FIP` deklaruje uznawanie PoP, ale nie dostarcza profilu `bridge_minimum`,
2. federacja opisuje profil jako `trans_federation_limited`, lecz nie zapewnia
   jawnych limitów dla komunikacji i pomocy,
3. profil ratunkowy posiada `hard_stop` albo praktyczny limit uniemożliwiający
   wezwanie pomocy,
4. rozszerzenie federacyjne usuwa jedną z trzech minimalnych klas dostępu,
5. implementacja używa lokalnych, niejawnych limitów zamiast nazwanych profili.

---

## 7. Relacja do innych dokumentów

- **`UNIVERSAL-BASIC-COMPUTE.pl.md`**: definiuje samo prawo do `UBC`, modele
  alokacji i finansowania.
- **`FIP-MEMBERSHIP-AND-QUORUM.pl.md`**: definiuje minimalną strukturę i
  odpowiedzialność `FIP`.
- **Konstytucja Art. XII.11-13**: wyznacza granice nieodbieralnego minimum i
  zakaz ukrytej przewagi.
