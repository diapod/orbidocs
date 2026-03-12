# Federacja Izb Pieczęciowych i odpieczętowanie tożsamości w DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-SEAL-BOARD-001` |
| `typ` | Ustawa wykonawcza (Poziom 3 hierarchii normatywnej) |
| `wersja` | 0.1.0-draft |
| `podstawa` | Art. IV.6-9, Art. X.7-13, Art. XVI Konstytucji DIA; `ROOT-IDENTITY-AND-NYMS.pl.md`; `ABUSE-DISCLOSURE-PROTOCOL.pl.md`; `FIP-MEMBERSHIP-AND-QUORUM.pl.md`; `UNSEAL-CASE-MODEL.pl.md` |
| `status mechanizmów` | model governance i progów jest normatywny; technika split-knowledge pozostaje wdrożeniowa |

---

## 1. Cel dokumentu

Dokument definiuje:

- Federację Izb Pieczęciowych jako rozproszony organ konstytucyjny IRL,
- progi zejścia `nym -> node-id`,
- progi odpieczętowania `node-id -> root-identity`,
- zasady redundancji, quorum, dywersyfikacji jurysdykcyjnej i podziału wiedzy,
- minimalny ślad audytowy i tryb odwołania.

Celem jest umożliwienie egzekwowania odpowiedzialności bez tworzenia pojedynczego
punktu nacisku, odwetu lub przejęcia.

---

## 2. Zasada bazowa

1. Nie każde nadużycie wymaga poznania `root-identity`.

2. Domyślną ścieżką egzekwowania są:

   - środki lokalne na poziomie `nymu`,

   - sankcje infrastrukturalne na poziomie `node-id`.

3. `root-identity` wolno odkrywać tylko wtedy, gdy:

   - sama identyfikacja `node-id` nie wystarcza do ochrony ludzi, wspólnoty lub
     integralności procedury,

   - istnieje obowiązek prawny albo próg szkody najwyższej stawki,

   - decyzja przejdzie przez Federację Izb Pieczęciowych.

4. Żadna pojedyncza izba nie może być jedynym depozytariuszem pełnej zdolności
   odpieczętowania.

---

## 3. Model ustrojowy

### 3.1. Federacja Izb Pieczęciowych

Federacja Izb Pieczęciowych (`FIP`) jest federacją niezależnych izb IRL, które:

- działają według wspólnego minimalnego standardu konstytucyjnego,
- są rozproszone jurysdykcyjnie,
- podlegają audytowi i zasadom konfliktu interesów,
- współuczestniczą w odpieczętowaniu tożsamości pierwotnej wyłącznie przez
  quorum wieloizbowe.

### 3.2. Zakres kompetencji izb

Izba może:

- przyjmować i rejestrować wnioski o odpieczętowanie,
- sprawdzać kompletność formalną i progi wejścia,
- współdecydować o zejściu `node-id -> root-identity`,
- przechowywać udział w materiale split-knowledge,
- prowadzić ślad audytowy swoich decyzji.

Izba nie może:

- samodzielnie prowadzić zwykłych sporów reputacyjnych,
- zastępować paneli ad-hoc ani governance federacji,
- samodzielnie odpieczętować `root-identity`,
- używać materiałów tożsamościowych poza zakresem konkretnej procedury.

### 3.3. Redundancja

1. `FIP` POWINNA składać się z wielu izb globalnie.

2. Odpieczętowanie `root-identity` MUSI wymagać małego quorum ad-hoc złożonego z
   kilku izb, a nie działania całej federacji naraz.

3. Konkretne minima członkostwa, statusów i quorum określa
   `FIP-MEMBERSHIP-AND-QUORUM.pl.md`.

4. Federacja MOŻE zaostrzyć te minima, ale nie może ich poluzować.

---

## 4. Progi ujawniania

### 4.1. `U0` - brak zejścia

Sprawa pozostaje na poziomie `nymu`. Dopuszczalne są wyłącznie środki lokalne:

- rate limit,
- izolacja kontekstowa,
- lokalne wyciszenie,
- blokada pojedynczej akcji,
- monitoring.

### 4.2. `U1` - proceduralne zejście `nym -> node-id`

`U1` jest progiem dla sankcji infrastrukturalnych i nie wymaga poznania
`root-identity`.

Minimalny próg:

- `stake-level >= S2`,
- `evidence-level >= E2`,
- współpodpis co najmniej dwóch ról sprawy.

Skutki dopuszczalne:

- identyfikacja `node-id`,
- identyfikacja aktywnych nymów i stacji powiązanych z `node-id`,
- nałożenie sankcji `I1-I4`,
- ujawnienie `node-id` w zakresie wewnętrznym lub federacyjnym.

`U1` nie daje prawa do poznania `root-identity`.

### 4.3. `U2` - zejście `node-id -> custodian_ref`

`U2` jest progiem pośrednim dla spraw, w których potrzebna jest identyfikacja
podmiotu odpowiedzialnego proceduralnie, ale nie jeszcze tożsamości pierwotnej.

`custodian_ref` oznacza tutaj trwały uchwyt proceduralny do dysponenta `node-id`,
na przykład `persistent_nym` albo federacyjny `procedural_ref`. Nie oznacza on
automatycznie `anchor-identity` ani `root-identity`.

Minimalny próg:

- `stake-level >= S3`,

- `evidence-level >= E3`,

- kontrola COI,

- współpodpis wielo-rolowy,

- uzasadnienie, że `node-id` nie wystarcza.

Skutki dopuszczalne:

- ujawnienie `custodian_ref` podmiotom uprawnionym,
- blokada ról lub uprawnień na poziomie dysponenta,
- wszczęcie przygotowania wniosku do `FIP`.

### 4.4. `U3` - pełne odpieczętowanie `node-id -> root-identity`

`U3` jest progiem najwyższym.

Minimalny próg:

- `stake-level >= S3` i `evidence-level >= E3`, gdy istnieje obowiązek prawny
  albo trwała krzywda, której nie da się zatrzymać sankcją infrastrukturalną,

lub

- `stake-level >= S4` i `evidence-level >= E3` w pozostałych sprawach.

Dodatkowo wymagane są:

- brak mniej inwazyjnej drogi osiągnięcia celu,

- decyzja quorum `FIP`,

- ścisły zakres ujawnienia,

- gotowość do ścieżki odwoławczej.

---

## 5. Quorum i dywersyfikacja

### 5.1. Quorum minimalne

Domyślne quorum dla `U2` i `U3`, a także statusy izb i tryb awaryjny, określa
`FIP-MEMBERSHIP-AND-QUORUM.pl.md`. Niniejszy dokument zachowuje wyłącznie zasadę,
że pełne odpieczętowanie nie może być wykonywane przez pojedynczą izbę ani przez
quorum pozbawione różnorodności jurysdykcyjnej i organizacyjnej.

### 5.2. Wyłączenia

Izba podlega wyłączeniu, gdy:

- ma konflikt interesów,
- pozostaje w relacji zależności z wnioskodawcą lub stroną sprawy,
- pochodzi z tej samej zwartej grupy kontrolnej co inna izba w quorum,
- jest objęta wiarygodnym sygnałem kompromitacji.

### 5.3. Tryb awaryjny

Jeżeli izba jest niedostępna, zastraszana albo objęta odwetem:

- sprawa przechodzi do quorum zastępczego,
- zdarzenie jest logowane jako `seal-body-disruption`,
- federacja uruchamia ochronę operacyjną i prawną.

---

## 6. Split knowledge

1. Mapowanie `node-id -> root-identity` NIE POWINNO być dostępne w całości jednej
   izbie.

2. System POWINIEN stosować model podzielonej wiedzy, np.:

   - threshold encryption,

   - secret sharing,

   - escrow wielostronny.

3. Kompromitacja pojedynczej izby nie może sama z siebie umożliwiać poznania
   `root-identity`.

4. Techniczna implementacja split-knowledge jest wymienna, ale MUSI zapewniać:

   - brak pojedynczego punktu odczytu,

   - możliwość rotacji udziałów,

   - ślad użycia udziałów,

   - możliwość wycofania izby z systemu.

---

## 7. Przebieg procedury

### 7.1. Wniosek

Wniosek o zejście `U2` albo `U3` MUSI zawierać:

- `case-id`,
- próg `U`,
- uzasadnienie konieczności,
- poziomy `stake-level` i `evidence-level`,
- wynik kontroli COI,
- proponowany zakres ujawnienia,
- wskazanie mniej inwazyjnych środków już użytych albo odrzuconych.

### 7.2. Kontrola formalna

Izba wejściowa sprawdza:

- kompletność,
- dopuszczalność progu,
- czy sprawa nie powinna zatrzymać się na `U1`,
- czy istnieje oczywisty konflikt interesów albo brak podstawy.

### 7.3. Rozstrzygnięcie

1. `U1` może być rozstrzygany wewnątrz federacji bez udziału `FIP`.

2. `U2` może wymagać udziału jednej izby jako nadzorcy proceduralnego, jeśli
   federacja tak stanowi.

3. `U3` wymaga quorum `FIP`.

### 7.4. Zakres ujawnienia

Nawet po pozytywnym rozstrzygnięciu `U3` ujawnienie MUSI być:

- adresowane do konkretnego odbiorcy albo klasy odbiorców,
- ograniczone do minimum koniecznego,
- opatrzone `expiry`,
- objęte śladem dalszego użycia.

---

## 8. Model danych

### 8.1. Rejestr izby

```yaml
seal_chamber_record:
  chamber_id: "[identyfikator]"
  jurisdiction: "[jurysdykcja]"
  federation_affiliation: "[federacja lub podmiot]"
  status: "active"              # active | suspended | compromised | retired
  public_key: "[klucz publiczny]"
  trust_class: "constitutional"
  valid_from: "[ISO 8601]"
  valid_until: null
```

### 8.2. Wniosek o zejście

```yaml
identity_unsealing_request:
  request_id: "[identyfikator]"
  case_id: "[sprawa]"
  threshold: "U3"              # U1 | U2 | U3
  target_nym: "[nym_id | null]"
  target_node_id: "[node_id | null]"
  requested_scope: "[custodian_ref | root_identity]"
  stake_level: "S3"
  evidence_level: "E3"
  less_invasive_means_checked: true
  coi_check: "pass"
  submitted_by: []
  submitted_at: "[ISO 8601]"
```

### 8.3. Decyzja quorum

```yaml
seal_quorum_decision:
  decision_id: "[identyfikator]"
  request_id: "[referencja]"
  chambers: []
  jurisdictions: []
  outcome: "approved"          # approved | denied | remand
  disclosure_scope: "root_identity"
  expiry: "[ISO 8601]"
  rationale_ref: "[referencja]"
  signatures: []
```

---

## 9. Odwołanie

1. Decyzja `U3` MUSI podlegać odwołaniu.

2. Odwołanie rozpoznaje nowe quorum, bez izb uczestniczących w decyzji
   pierwotnej.

3. Odwołanie może opierać się na:

   - kontr-dowodzie,

   - błędzie proceduralnym,

   - konflikcie interesów,

   - nieproporcjonalności zakresu ujawnienia,

   - naruszeniu reguł dywersyfikacji quorum.

---

## 10. Relacja do innych dokumentów

- **`ROOT-IDENTITY-AND-NYMS.pl.md`**: dokument definiuje warstwy `nym -> node-id -> root-identity`; ten akt definiuje, kto i przy jakim progu może schodzić między tymi warstwami.
- **`ABUSE-DISCLOSURE-PROTOCOL.pl.md`**: poziomy `stake-level`, `evidence-level`, sankcje infrastrukturalne i notyfikacje prawne są wspólną podstawą.
- **`IDENTITY-ATTESTATION-AND-RECOVERY.pl.md`**: split-knowledge i odpieczętowanie muszą być zgodne z pamięcią wcześniejszego poświadczenia i integralnością `anchor-identity`.
