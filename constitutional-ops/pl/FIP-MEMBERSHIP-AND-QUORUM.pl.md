# Federacja Izb Pieczęciowych - członkostwo i quorum

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-FIP-QUORUM-001` |
| `typ` | Ustawa wykonawcza / członkostwo i quorum |
| `wersja` | 0.1.0-draft |
| `data` | 2026-03-12 |

---

## 1. Cel dokumentu

Niniejszy dokument definiuje minimalne zasady członkostwa, aktywności i quorum
w Federacji Izb Pieczęciowych (`FIP`), tak aby tor odpieczętowania nie opierał
się na pojedynczym organie ani przypadkowej grupie jurysdykcyjnie bliskich izb.

---

## 2. Relacja do ogólnej federacji

`FIP` jest federacją szczególnego celu. Nie zastępuje ogólnych reguł federacji z
`FEDERATION-MEMBERSHIP-AND-QUORUM.pl.md`, lecz nakłada dodatkowe wymogi na organy,
które chcą uczestniczyć w odpieczętowaniu `U2-U3`.

Jeżeli zachodzi kolizja, dla `FIP` pierwszeństwo mają wymogi ostrzejsze.

---

## 3. Statusy izb

Izba może mieć status:

- `candidate`,

- `active`,

- `restricted`,

- `suspended`,

- `retired`.

### 3.1. `candidate`

Izba przechodzi screening, nie bierze udziału w quorum `U3`, może brać udział
obserwacyjny albo testowy.

### 3.2. `active`

Izba spełnia wymogi aktywności, różnorodności jurysdykcyjnej i bezpieczeństwa.
Może brać udział w quorum `U2-U3`.

### 3.3. `restricted`

Izba działa, ale ma czasowo zawężone kompetencje, np. tylko do `U2` albo bez prawa
bycia izbą prowadzącą.

### 3.4. `suspended`

Izba jest czasowo wyłączona z quorum z powodu konfliktu interesów, odwetu,
podejrzenia przejęcia albo utraty zdolności operacyjnej.

### 3.5. `retired`

Izba została wycofana z federacji; nie bierze udziału w nowych sprawach, ale może
pozostawać stroną audytu spraw wcześniejszych.

---

## 4. Minimalne warunki statusu `active`

1. co najmniej `min_members = 3` kwalifikowanych członków izby,

2. każdy z nich ma `IAL4`,

3. izba ma jurysdykcyjne umocowanie IRL albo porównywalny kontrakt prawny,

4. izba utrzymuje bezpieczny kanał przyjmowania spraw i depozyt udziałów sekretu,

5. izba przechodzi okresowy audyt proceduralny,

6. izba nie jest pod dominującą kontrolą jednego podmiotu, który kontroluje też
   inne izby w danym quorum.

---

## 5. Quorum

### 5.1. Dla `U2`

Domyślne quorum wynosi `2 z 3` izb `active` albo `restricted`, z czego co najmniej:

- jedna izba nie pochodzi z federacji wnioskodawcy,

- jedna izba nie pochodzi z jurysdykcji strony objętej sprawą.

### 5.2. Dla `U3`

Domyślne quorum wynosi `3 z 5` izb `active`, z czego:

- co najmniej trzy różne jurysdykcje,

- co najmniej dwie różne federacje,

- żadna pojedyncza organizacja kontrolująca nie może dostarczyć więcej niż jednej
  izby do quorum.

### 5.3. Tryb awaryjny

Jeżeli nie da się zbudować quorum `3 z 5`, dopuszczalny jest tryb awaryjny `3 z 4`,
ale tylko gdy:

- jedna lub więcej izb ma status `suspended` z powodu odwetu, awarii albo siły
  wyższej,

- zachowana pozostaje różnorodność co najmniej trzech jurysdykcji,

- decyzja jest automatycznie oznaczona do rewizji ex post.

---

## 6. Migawka składu i konfliktów

1. Każda sprawa `U2-U3` MUSI mieć `fip_snapshot_id`.

2. Migawka składu MUSI zamrażać listę izb kwalifikowalnych na moment budowy quorum.

3. Izba objęta konfliktem interesów jest wyłączana ze sprawy, ale nie traci przez
   to automatycznie statusu `active` globalnie.

---

## 7. Minimalny model danych

```yaml
fip_chamber_record:
  chamber_id: "[identyfikator izby]"
  status: "[candidate | active | restricted | suspended | retired]"
  federation_ref: "[identyfikator federacji]"
  jurisdiction_ref: "[identyfikator jurysdykcji]"
  qualified_member_refs:
    - "[identyfikator członka IAL4]"
  capabilities:
    can_lead_u2: true
    can_lead_u3: true
    can_hold_secret_share: true
  last_audit_at: "[ISO 8601]"
  suspension_reason: null
```

```yaml
fip_snapshot:
  fip_snapshot_id: "[identyfikator migawki]"
  case_ref: "[case_id]"
  eligible_chambers:
    - "[chamber_id]"
  excluded_chambers:
    - chamber_id: "[identyfikator]"
      reason: "[COI | suspended | unreachable]"
  created_at: "[ISO 8601]"
```

---

## 8. Relacje do innych dokumentów

- `IDENTITY-UNSEALING-BOARD.pl.md` definiuje rolę `FIP` i progi `U2-U3`.

- `ROLE-TO-IAL-MATRIX.pl.md` definiuje minimalny `IAL4` dla członków izb.

- `FEDERATION-MEMBERSHIP-AND-QUORUM.pl.md` pozostaje aktem ogólnym dla federacji,
  ale `FIP` jest jego wyspecjalizowanym zaostrzeniem.
