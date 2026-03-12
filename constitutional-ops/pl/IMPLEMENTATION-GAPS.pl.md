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
