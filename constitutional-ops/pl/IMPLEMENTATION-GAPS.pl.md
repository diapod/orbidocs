# Luki implementacyjne warstwy konstytucyjnej DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-CONST-GAPS-001` |
| `typ` | Przegląd architektoniczny / backlog dokumentów wykonawczych |
| `wersja` | 0.1.0-draft |
| `data` | 2026-03-10 |

---

## Cel dokumentu

Niniejszy dokument zbiera luki, które pozostają po uzupełnieniu Konstytucji i
pierwszych dokumentów z katalogu `constitutional-ops/`. Nie ma mocy normatywnej;
służy porządkowaniu kolejnych kroków implementacyjnych.

---

## Ostatnio domknięte

### `FEDERATION-MEMBERSHIP-AND-QUORUM.pl.md`

Domknięto dnia `2026-03-10` przez dokument `DIA-FED-001`, który definiuje:

- status federacji aktywnej, uśpionej, zawieszonej i wygaszonej,
- minimalne kryteria aktywności,
- migawkę elektoratu, quorum i klasy decyzji,
- zasady utraty prawa veta przez martwą federację.

### `PROCEDURAL-REPUTATION-SPEC.pl.md`

Domknięto dnia `2026-03-12` przez dokument `DIA-PROC-REP-001`, który definiuje:

- domeny reputacji i typy sygnałów,
- definicję aktywnego węzła do celów reputacyjnych,
- rozruch i ograniczenia bootstrapu,
- przenośny pakiet dowodów zamiast nagiego przenoszenia wyniku,
- haki detekcji karteli i połączenie z metrykami zdrowia M1-M5.

### `PANEL-SELECTION-PROTOCOL.pl.md`

Domknięto dnia `2026-03-12` przez dokument `DIA-PANEL-SEL-001`, który definiuje:

- kwalifikowalność panelistów,
- źródło entropii i audytowalne losowanie składu,
- procedurę COI, veta i uzupełniania składu,
- eskalację do puli międzyfederacyjnej,
- poziomy ujawniania tożsamości panelistów i relację do apelacji.

### `ABUSE-DISCLOSURE-PROTOCOL.pl.md`

Domknięto dnia `2026-03-12` przez dokument `DIA-ABUSE-DISC-001`, który definiuje:

- zakaz ogólnej lustracji bez wiarygodnego sygnału teraźniejszego,
- warunki wejścia w pełną historię sprawy,
- progi `stake-level` i `evidence-level`,
- role multisig, zakres ujawnienia, retencję, odwołanie i notyfikacje jurysdykcyjne.

### `ROOT-IDENTITY-AND-NYMS.pl.md`

Domknięto dnia `2026-03-12` przez dokument `DIA-ROOT-ID-001`, który definiuje:

- rozdział `root-identity`, `anchor-identity`, `node-id`, `nym`, `station-id` i `agent-id`,
- poziomy pewności tożsamości (`IAL0`-`IAL4`),
- regułę "większy wpływ -> większe wymagania ujawnienia i potwierdzenia",
- model multisig poręczeń dla jurysdykcji bez silnego eID,
- ograniczenie mnożenia wpływu przez wiele nymów jednego źródła zakotwiczenia.

### `IDENTITY-ATTESTATION-AND-RECOVERY.pl.md`

Domknięto dnia `2026-03-12` przez dokument `DIA-ID-REC-001`, który definiuje:

- pierwsze poświadczenie `root-identity`,
- pamięć wcześniejszego poświadczenia dla `anchor-identity`,
- rolę frazy odzyskiwania, `salt` i parametrów KDF,
- odtwarzanie `anchor-identity` bez ponownego pełnego poświadczenia,
- procedurę aktualizacji danych tożsamościowych i odwołania.

### `ATTESTATION-PROVIDERS.pl.md`

Domknięto dnia `2026-03-12` przez dokument `DIA-ATTEST-PROVIDERS-001`, który definiuje:

- klasy siły poświadczenia `weak` / `strong`,
- domyślne mapowanie metod na maksymalne `IAL`,
- ograniczenia dla numeru telefonu i innych źródeł niskiej mocy dowodowej,
- zasady upgrade `weak -> strong` bez utraty kotwicy.

### `IDENTITY-UPGRADE-ANOMALY-SIGNALS.pl.md`

Domknięto dnia `2026-03-12` przez dokument `DIA-ID-UPGRADE-ANOM-001`, który definiuje:

- klasy sygnałów `A1-A8` dla upgrade poświadczenia,
- minimalne poziomy reakcji `monitor`, `soft_hold`, `manual_review`, `hard_block`,
- profil domyślny dla `phone -> strong`,
- relację między upgradem poświadczenia a sporem proceduralnym.


### `IDENTITY-UNSEALING-BOARD.pl.md`

Domknięto dnia `2026-03-12` przez dokument `DIA-SEAL-BOARD-001`, który definiuje:

- Federację Izb Pieczęciowych jako redundantny organ IRL,
- progi `U1-U3` dla zejścia `nym -> node-id -> root-identity`,
- wieloizbowe i międzyjurysdykcyjne quorum,
- split-knowledge dla mapowania `node-id -> root-identity`,
- odwołanie od decyzji pełnego odpieczętowania.

### `UNSEAL-CASE-MODEL.pl.md`

Domknięto dnia `2026-03-12` przez dokument `DIA-UNSEAL-CASE-001`, który definiuje:

- wspólny model `unseal_case` dla progów `U1-U3`,
- osobny rekord decyzji z zakresem, skutkami i oknem odwoławczym,
- minimalne pola dla retencji, COI, panelu i notyfikacji,
- zasadę, że eskalacja zakresu nie nadpisuje historii sprawy.

### `ROLE-TO-IAL-MATRIX.pl.md`

Domknięto dnia `2026-03-12` przez dokument `DIA-ROLE-IAL-001`, który definiuje:

- minimalną mapę klas ról do `IAL0-IAL4`,
- zasadę, że `IAL` jest głównie bramką, a nie mnożnikiem wpływu,
- ograniczenie `fixed_power_bonus` do `<= 1%`,
- domyślne minima dla paneli, izb pieczęciowych i ról wysokiej stawki.

### `FIP-MEMBERSHIP-AND-QUORUM.pl.md`

Domknięto dnia `2026-03-12` przez dokument `DIA-FIP-QUORUM-001`, który definiuje:

- statusy izb `candidate`-`retired`,
- minimalne warunki statusu `active`,
- domyślne quorum `2 z 3` dla `U2` i `3 z 5` dla `U3`,
- tryb awaryjny, migawkę składu i reguły różnorodności jurysdykcyjnej.

### `SWARM-ECONOMY-SUFFICIENCY.pl.md`

Domknięto dnia `2026-03-21` przez dokument `DIA-SUFF-001`, który definiuje:

- operacyjny model progu dostatku i pasma wygaszania,
- dopuszczalne klasy hamulców koncentracji i test anty-piramidowy,
- minimalny model danych polityki ekonomicznej federacji,
- wspólny obieg nadwyżek i klasy ich przeznaczenia,
- barierę między nagrodą ekonomiczną a władzą proceduralną.

### `RAW-SIGNAL-POLICY.pl.md`

Domknięto dnia `2026-03-21` przez dokument `DIA-RAW-001`, który definiuje:

- tryby `raw` / `structured` / `transformed` / `redacted`,
- dopuszczalne podstawy transformacji sygnału,
- obowiązkowe metaznaczniki dla ingerencji AI,
- minimalny ślad audytowy transformacji wypowiedzi,
- testy zgodności przeciw niejawnej estetyzacji i profesjonalizacji.

### `UNIVERSAL-BASIC-COMPUTE.pl.md`

Domknięto dnia `2026-03-21` przez dokument `DIA-UBC-001`, który definiuje:

- minimalny model `Proof-of-Personhood` bez domyślnej deanonimizacji,
- nieodbieralne minimum compute dla komunikacji, orientacji i trybów ochronnych,
- ograniczoną trans-federacyjność: ratunek bez limitu oraz limitowaną komunikację i pomoc,
- modele danych `proof_of_personhood_attestation`, `ubc_allocation` i `ubc_settlement`,
- jawne źródła finansowania `UBC` i testy zgodności przeciw ukrytemu wykluczeniu.

### `UBC-LIMIT-PROFILES.pl.md`

Domknięto dnia `2026-03-21` przez dokument `DIA-UBC-LIMITS-001`, który definiuje:

- kanoniczne profile `emergency_unlimited`, `communication_limited` i `care_limited`,
- minimalny profil `bridge_minimum` dla uznawania PoP przez most/rejestr `FIP`,
- profile przenośności `local_only`, `trans_federation_limited` i `trans_federation_extended`,
- jawny model rekordu mostu `FIP` i regułę, że federacje mogą tylko rozszerzać limity,
- testy zgodności przeciw pozornemu uznawaniu trans-federacyjnego PoP bez realnego dostępu.

---

## Priorytet A - wymagane przed wejściem w realny ład organizacyjny (ang. governance)

Po domknięciu `PROCEDURAL-REPUTATION-SPEC.pl.md`,
`PANEL-SELECTION-PROTOCOL.pl.md` oraz `ABUSE-DISCLOSURE-PROTOCOL.pl.md`
nie ma obecnie otwartej luki klasy A. Warstwa minimalnego ładu organizacyjnego
ma już trzy brakujące wcześniej akty wykonawcze.

---

## Priorytet B - wymagane przed autonomią i sensorium o wyższej stawce

### 1. `EMERGENCY-ACTIVATION-CRITERIA.pl.md`

**Dlaczego brakuje:** gradient autonomii definiuje A3, ale nie określa katalogu
triggerów, minimalnych progów pewności ani zasad dopuszczania automatycznej aktywacji.

**Co musi zdefiniować:**

- klasy triggerów dla A3,
- minimalne progi wiarygodności sygnału,
- relację sensorium -> trigger -> operator,
- domyślne TTL i obowiązkową rewizję.

### 2. `SENSITIVE-DATA-REDUCTION.pl.md`

**Dlaczego brakuje:** publikacja, sygnaliści, wyjątki i materiały wdrożeniowe
(ang. onboarding) odwołują się do
redakcji danych wrażliwych, ale nie ma wspólnego standardu redakcji i ujawnień.

**Co musi zdefiniować:**

- klasy danych wrażliwych,
- poziomy redakcji,
- zasady ujawniania selektywnego,
- minimalne ślady audytowe bez deanonimizacji.

---

## Priorytet C - wymagane przed skalowaniem federacyjnym

### 3. `ROLE-REGISTRY.pl.md`

**Dlaczego brakuje:** konstytucja i suplementy używają pojęć "rola zaufania
publicznego", "operator", "zespół kontrtestujący (ang. red-team)", "panel", ale nie
mają wspólnego rejestru ról.

**Co musi zdefiniować:**

- katalog ról bazowych,
- minimalne uprawnienia i zakazy łączenia ról,
- wymagania dotyczące warstwowego sprawdzania ról (ang. screeningu),
- ścieżki rotacji i zastępowalności.

### 4. `TRACE-MINIMUM.pl.md`

**Dlaczego brakuje:** autonomia agentów, wyjątki, reputacja i obrona konstytucyjna
wymagają śladów działania, ale nie mają wspólnego minimalnego schematu.

**Co musi zdefiniować:**

- obowiązkowe pola śladu działania (ang. trace),
- relację ślad działania (trace) -> audyt -> odwołanie (ang. appeal),
- klasy retencji,
- wersjonowanie śladów i podpisy.

---

## Uwaga końcowa

Najbardziej krytyczne luki warstwy ładu organizacyjnego zostały domknięte przez
`EXCEPTION-POLICY.pl.md`, `FEDERATION-MEMBERSHIP-AND-QUORUM.pl.md`,
`PROCEDURAL-REPUTATION-SPEC.pl.md`, `PANEL-SELECTION-PROTOCOL.pl.md` oraz
`ABUSE-DISCLOSURE-PROTOCOL.pl.md`. Następny logiczny krok to doprecyzowanie
**kryteriów aktywacji kryzysowej**, **redakcji danych wrażliwych** oraz
**minimalnego schematu śladów działania**, aby warstwa wykonawcza była równie
spójna poza sporami i governance.
