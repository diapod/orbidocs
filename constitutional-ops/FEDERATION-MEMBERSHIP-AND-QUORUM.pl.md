# Członkostwo federacji i quorum DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-FED-001` |
| `typ` | Ustawa wykonawcza (Poziom 3 hierarchii normatywnej) |
| `wersja` | 0.1.0-draft |
| `podstawa` | Art. VI.6, VII.10, XIII.6, XV, XVI Konstytucji DIA; `ENTRENCHMENT-CLAUSE.pl.md`; `NORMATIVE-HIERARCHY.pl.md` |

---

## 1. Cel dokumentu

Konstytucja i klauzula wieczności operują na pojęciu "federacji", ale bez
operacyjnej definicji statusu federacji, prawa głosu i reguł quorum system pozostaje
podatny na dwie patologie:

- **deadlock przez martwe federacje** - brak odpowiedzi jest mylony z realnym vetem,
- **przejęcie sterowania (ang. capture) przez mnożenie fasadowych federacji** -
  jeden ośrodek kontroli próbuje sztucznie zwiększyć liczbę głosów.

Niniejszy dokument definiuje minimalny model członkostwa federacyjnego, statusy
federacji, kryteria aktywności, zasady liczenia quorum oraz reguły utraty prawa głosu
i veta.

---

## 2. Zasady ogólne

1. W ładzie międzyfederacyjnym (ang. governance) liczą się wyłącznie **federacje
   uprawnione do głosu**.
2. **Jedna aktywna federacja uprawniona do głosu = jeden głos**. Kapitał, liczba
   węzłów, ruch, przychód, moc obliczeniowa ani pozycja infrastrukturalna nie
   zwiększają wagi głosu.
3. Prawo głosu i veto wynika z **żywej odpowiedzialności proceduralnej**, a nie z
   historycznego faktu istnienia federacji.
4. Sposób wypracowania stanowiska **wewnątrz** federacji jest sprawą lokalnej
   polityki, ale głos zewnętrzny MUSI pozostawiać ślad, właściciela procesu i podpis
   właściwej roli lub ról.
5. Federacje pozostające pod **wspólną kontrolą** nie mogą mnożyć wpływu przez sam
   podział organizacyjny. W sprawach wysokiej stawki i konstytucyjnych są traktowane
   jako **jeden blok głosujący**, dopóki nie wykażą rzeczywistej niezależności
   proceduralnej.

---

## 3. Minimalny rekord federacji

Każda federacja uczestnicząca w ładzie międzyfederacyjnym (ang. governance) MUSI
publikować co najmniej następujący rekord:

```yaml
federation_record:
  federation_id: "FED-[slug]"
  status: "candidate" # candidate | active | dormant | suspended | retired
  governance_endpoint: "[URI lub kanał odbioru decyzji formalnych]"
  fallback_contact: "[kanał zapasowy]"
  governance_keys: []
  policy_refs: []
  heartbeat_at: "[timestamp]"
  last_notice_ack_at: "[timestamp]"
  last_governance_action_at: "[timestamp]"
  declared_common_control: []
  effective_from: "[timestamp]"
  owner_roles: []
  status_reason: "[powód bieżącego statusu]"
```

Minimalny rekord federacji jest obiektem audytu. Brak aktualnego rekordu oznacza brak
podstaw do utrzymania statusu `active`.

---

## 4. Statusy federacji

| Status | Znaczenie | Prawo głosu | Prawo veta |
| :--- | :--- | :--- | :--- |
| `candidate` | Federacja zarejestrowana, interoperacyjna, w okresie wejścia lub próbnego działania | nie | nie |
| `active` | Federacja żywa proceduralnie i uprawniona do udziału w ładzie międzyfederacyjnym (ang. governance) | tak | tak, jeśli dana procedura je przewiduje |
| `dormant` | Federacja czasowo nieaktywna, nieodpowiadająca albo niespełniająca kryteriów aktywności | nie | nie |
| `suspended` | Federacja czasowo wyłączona z głosowań z powodu incydentu, środka tymczasowego (`injunction`) albo innej decyzji proceduralnej | nie | nie |
| `retired` | Federacja wygaszona lub taka, która jawnie opuściła proces ładu międzyfederacyjnego (ang. governance) | nie | nie |

Status `candidate`, `dormant`, `suspended` i `retired` nie są karą ontologiczną:
federacja może nadal istnieć, routować ruch lub świadczyć usługi lokalne, ale nie
uczestniczy w międzyfederacyjnym liczeniu głosów, dopóki nie odzyska kwalifikacji.

---

## 5. Kryteria uzyskania i utrzymania statusu `active`

Federacja uzyskuje albo utrzymuje status `active` wyłącznie wtedy, gdy łącznie:

1. publikuje aktualny rekord federacji,
2. posiada działający `governance_endpoint` oraz `fallback_contact`,
3. wysłała ważny heartbeat w oknie `heartbeat_ttl`,
4. potwierdziła odbiór co najmniej jednego formalnego zawiadomienia lub wykonała
   co najmniej jedną audytowalną czynność dotyczącą ładu organizacyjnego (ang.
   governance) w oknie `activity_ttl`,
5. nie jest objęta aktywnym zawieszeniem proceduralnym,
6. nie pozostaje w nierozstrzygniętym sporze o wspólną kontrolę, który wymaga
   agregacji głosu z inną federacją.

Status `candidate` może zostać podniesiony do `active` po spełnieniu wszystkich
powyższych warunków oraz po zakończeniu okresu próbnego `candidate_min_age`.

---

## 6. Przejścia statusów

### 6.1. `candidate` -> `active`

Przejście następuje po:

1. opublikowaniu minimalnego rekordu federacji,
2. co najmniej jednym poprawnym heartbeat,
3. co najmniej jednym potwierdzeniu odbioru formalnego zawiadomienia,
4. upływie okresu próbnego.

### 6.2. `active` -> `dormant`

Przejście następuje automatycznie lub proceduralnie, gdy wystąpi przynajmniej jeden z
warunków:

1. heartbeat wygasł,
2. federacja nie potwierdziła odbioru `missed_notice_limit` kolejnych formalnych
   zawiadomień,
3. `governance_endpoint` i `fallback_contact` są niedostępne przez pełne okno
   zawiadomienia,
4. rekord federacji jest nieaktualny albo niespójny i nie został naprawiony w oknie
   naprawczym.

### 6.3. `active` lub `dormant` -> `suspended`

Przejście następuje, gdy:

1. istnieje aktywny środek tymczasowy lub `injunction`,
2. zachodzi incydent bezpieczeństwa dotyczący kluczy `governance`,
3. występuje twardy sygnał przejęcia sterowania (ang. capture), fałszywego przedstawienia tożsamości lub
   manipulacji procesem głosowania.

### 6.4. `dormant` lub `suspended` -> `active`

Reaktywacja wymaga:

1. świeżego rekordu federacji,
2. świeżego heartbeat,
3. potwierdzenia zdolności odbioru zawiadomień,
4. usunięcia przyczyny zawieszenia albo dormancji,
5. pozostawienia śladu reaktywacji z `reason` i `effective_from`.

### 6.5. `dormant` -> `retired`

Przejście następuje po przekroczeniu `retired_after` albo przez jawne oświadczenie o
wyjściu z ładu międzyfederacyjnego (ang. governance).

---

## 7. Federacja uprawniona do głosu

Na potrzeby liczenia quorum i veta **federacją uprawnioną do głosu** jest wyłącznie
federacja, która:

- ma status `active`,
- znajduje się w migawce elektoratu utworzonej przy otwarciu danego procesu
  decyzyjnego (`electorate_snapshot`),
- nie została zgrupowana z inną federacją do jednego bloku głosującego z powodu
  wspólnej kontroli.

Migawka elektoratu MUSI zawierać:

```yaml
electorate_snapshot:
  decision_id: "[identyfikator procesu]"
  created_at: "[timestamp]"
  eligible_federations: []
  grouped_blocks: []
  quorum_base: 0
  decision_class: "ordinary" # ordinary | high_stake | entrenched_core
```

Po utworzeniu migawki baza quorum dla danego procesu nie zmienia się. Zmiany statusu
federacji wpływają na **kolejne** procesy, nie przeliczają wstecz procesu już
otwartego.

---

## 8. Klasy decyzji i quorum

### 8.1. Zasada podstawowa

Milczenie nie jest głosem. `abstain` liczy się do quorum, ale nie do większości
`yes/no`, chyba że dana procedura stanowi inaczej.

### 8.2. Klasy decyzji

| Klasa decyzji | Quorum | Warunek przyjęcia |
| :--- | :--- | :--- |
| `ordinary` | co najmniej `floor(N/2) + 1` bloków głosujących z migawki | więcej `yes` niż `no` |
| `high_stake` | co najmniej `ceil(2N/3)` bloków głosujących z migawki | co najmniej `ceil(2N/3)` jawnych głosów `yes` |
| `entrenched_core` | `N` z `N` bloków głosujących z migawki | każde uprawnione `active` musi oddać jawne `yes`; `no`, `abstain` albo milczenie oznacza brak zgody |

Interpretacja:

- `N` oznacza liczbę bloków głosujących w migawce elektoratu,
- blok głosujący może reprezentować jedną federację albo grupę federacji objętych
  zasadą wspólnej kontroli,
- jeżeli `N = 0`, proces międzyfederacyjny nie może zostać otwarty,
- dokument nie znosi dodatkowych wymogów z `ENTRENCHMENT-CLAUSE.pl.md`; jedynie
  definiuje, **kto** liczy się do jednomyślności.

---

## 9. Timeouty i parametry minimalne

Poniższe parametry są domyślne i mogą być zaostrzane przez federacje, ale nie mogą
być osłabiane poniżej wskazanego minimum:

| Parametr | Domyślnie | Minimum / maksimum |
| :--- | :--- | :--- |
| `heartbeat_ttl` | 30 dni | max 45 dni |
| `activity_ttl` | 90 dni | max 120 dni |
| `candidate_min_age` | 30 dni | min 14 dni |
| `missed_notice_limit` | 2 | min 2 |
| `notice_window` | 7 dni | min 72 godziny |
| `ordinary_vote_window` | 14 dni | min 7 dni |
| `high_stake_vote_window` | 30 dni | min 14 dni |
| `retired_after` | 180 dni | min 90 dni |

Federacja może być ostrożniejsza, ale nie może utrzymywać "aktywnych" federacji bez
heartbeat przez pół roku ani skracać okresu wejścia do zera.

---

## 10. Utrata prawa veta przez martwą federację

1. Federacja nieposiadająca statusu `active` w chwili tworzenia migawki elektoratu
   **nie ma prawa veta**.
2. Federacja, która utraciła status `active`, nie blokuje kolejnych procesów
   konstytucyjnych ani zwykłych tylko dlatego, że historycznie należała do federacji.
3. Federacja, która milczy w procesie wymagającym jednomyślności, może zablokować
   **ten konkretny proces**, jeśli była `active` w migawce, ale po przekroczeniu
   `missed_notice_limit` przechodzi do `dormant` i traci veto w procesach kolejnych.
4. Jawne wyjście z ładu międzyfederacyjnego (ang. governance) działa natychmiast na
   przyszłość: federacja przechodzi do `retired` i nie jest już liczona do quorum.

Zasada jest prosta: **veto przysługuje żywej odpowiedzialności, nie cieniowi po niej**.

---

## 11. Wspólna kontrola i mnożenie głosów

Za sygnały wspólnej kontroli uważa się co najmniej:

- wspólny klucz `governance`,
- tę samą dominującą rolę decyzyjną,
- to samo źródło finansowania lub ten sam podmiot zdolny jednostronnie wymuszać
  decyzje,
- brak realnej separacji śladu, odpowiedzialności i procedury odwoławczej.

Jeżeli istnieje wiarygodny spór o wspólną kontrolę:

1. federacje są tymczasowo grupowane do jednego bloku głosującego w sprawach
   `high_stake` i `entrenched_core`,
2. spór jest śledzony jako problem domniemania konfliktu interesów przy braku
   danych (COI-by-default),
3. przywrócenie osobnych głosów wymaga wykazania odrębności proceduralnej.

Ta reguła nie służy budowie centrum. Służy temu, by kapitał lub aparat organizacyjny
nie mógł kupić sobie dodatkowych głosów przez mnożenie fasad.

---

## 12. Relacja z innymi dokumentami

- **Konstytucja Art. VI.6 i VII.10**: dokument operacjonalizuje federacyjny wzrost
  bez utraty lokalnej autonomii oraz skalowanie przez lokalną odpowiedzialność.
- **Konstytucja Art. XIII.6**: statusy federacji implementują procedury wygaszenia,
  przekazania i archiwizacji.
- **Konstytucja Art. XVI**: dokument definiuje bazę quorum i uczestników procesów
  zmiany oraz egzekwowania.
- **`ENTRENCHMENT-CLAUSE.pl.md`**: dokument doprecyzowuje, które federacje liczą się
  do jednomyślności i veta.
- **`NORMATIVE-HIERARCHY.pl.md`**: polityka członkostwa federacji i quorum jest
  dokumentem Poziomu 3.
