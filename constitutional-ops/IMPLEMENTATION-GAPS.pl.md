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

---

## Priorytet A - wymagane przed wejściem w realny governance

### 1. `PROCEDURAL-REPUTATION-SPEC.pl.md`

**Dlaczego brakuje:** panel ad-hoc i screening ról zakładają istnienie "wysokiej
reputacji proceduralnej", ale nie definiują jej składowych ani sposobu wyliczenia.

**Co musi zdefiniować:**

- źródła sygnałów reputacji proceduralnej,
- wagę kontraktów, incydentów, odwołań i korekt,
- warunki obniżania i odzyskiwania reputacji,
- definicję "aktywnego węzła" na potrzeby reputacji.

### 2. `PANEL-SELECTION-PROTOCOL.pl.md`

**Dlaczego brakuje:** procedura obrony konstytucyjnej zakłada losowanie panelu, ale
nie określa źródła losowości, anty-manipulacyjnego seedowania ani sposobu rozstrzygania
sporów o veto i eligibility.

**Co musi zdefiniować:**

- źródło entropii i jego audyt,
- eligibility panelistów,
- procedurę wyłączeń i vet,
- logikę retry przy konflikcie interesów.

---

## Priorytet B - wymagane przed autonomią i sensorium o wyższej stawce

### 4. `EMERGENCY-ACTIVATION-CRITERIA.pl.md`

**Dlaczego brakuje:** gradient autonomii definiuje A3, ale nie określa katalogu
triggerów, minimalnych progów pewności ani zasad dopuszczania automatycznej aktywacji.

**Co musi zdefiniować:**

- klasy triggerów dla A3,
- minimalne progi wiarygodności sygnału,
- relację sensorium -> trigger -> operator,
- domyślne TTL i obowiązkową rewizję.

### 5. `SENSITIVE-DATA-REDUCTION.pl.md`

**Dlaczego brakuje:** publikacja, sygnaliści, wyjątki i onboarding odwołują się do
redakcji danych wrażliwych, ale nie ma wspólnego standardu redakcji i ujawnień.

**Co musi zdefiniować:**

- klasy danych wrażliwych,
- poziomy redakcji,
- zasady ujawniania selektywnego,
- minimalne ślady audytowe bez deanonimizacji.

---

## Priorytet C - wymagane przed skalowaniem federacyjnym

### 6. `ROLE-REGISTRY.pl.md`

**Dlaczego brakuje:** konstytucja i suplementy używają pojęć "rola zaufania
publicznego", "operator", "red-team", "panel", ale nie mają wspólnego rejestru ról.

**Co musi zdefiniować:**

- katalog ról bazowych,
- minimalne uprawnienia i zakazy łączenia ról,
- wymagania screeningowe,
- ścieżki rotacji i zastępowalności.

### 7. `TRACE-MINIMUM.pl.md`

**Dlaczego brakuje:** autonomia agentów, wyjątki, reputacja i obrona konstytucyjna
wymagają śladów działania, ale nie mają wspólnego minimalnego schematu.

**Co musi zdefiniować:**

- obowiązkowe pola trace,
- relację trace -> audit -> appeal,
- klasy retencji,
- wersjonowanie śladów i podpisy.

---

## Uwaga końcowa

Najbardziej krytyczne luki zostały częściowo domknięte przez `EXCEPTION-POLICY.pl.md`
oraz `FEDERATION-MEMBERSHIP-AND-QUORUM.pl.md`. Następny logiczny krok to
doprecyzowanie **jak liczy się reputację proceduralną** i **jak losuje się panel
ad-hoc**, bo bez tego governance pozostaje poprawny filozoficznie, ale nadal zbyt
miękki operacyjnie w sprawach spornych.
