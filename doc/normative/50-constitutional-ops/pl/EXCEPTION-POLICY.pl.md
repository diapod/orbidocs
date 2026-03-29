# Polityka wyjątków DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-EXC-001` |
| `typ` | Ustawa wykonawcza (Poziom 3 hierarchii normatywnej) |
| `wersja` | 0.1.0-draft |
| `podstawa` | Art. II, IX, X, XIV, XVI Konstytucji DIA; `AUTONOMY-LEVELS.pl.md`; `ENTRENCHMENT-CLAUSE.pl.md` |

---

## 1. Cel dokumentu

Konstytucja wymaga, aby każdy wyjątek miał identyfikator, uzasadnienie, poziom
ryzyka, właściciela, czas wygaśnięcia i punkt powrotu do stanu bezpiecznego
domknięcia (ang. fail-closed). Niniejszy
dokument zamienia tę zasadę w procedurę operacyjną: definiuje model danych wyjątku,
typy wyjątków, minimalną ścieżkę zatwierdzania oraz monitoring skutków ubocznych.

Celem polityki wyjątków nie jest ułatwienie obchodzenia reguł, lecz uczynienie
wyjątku **obiektem pierwszej kategorii audytu**.

---

## 2. Zasada ogólna

1. Wyjątek jest dopuszczalny wyłącznie wtedy, gdy:
   - nie narusza rdzenia nienegocjowalnego,
   - jest ograniczony zakresem i czasem,
   - ma właściciela odpowiedzialnego za jego skutki,
   - ma jawny warunek wyłączenia,
   - prowadzi do zdefiniowanego stanu bezpiecznego domknięcia (ang. fail-closed).
2. Wyjątek nie może być trybem domyślnym ani stałą cechą architektury.
3. Wyjątek NIE MOŻE zawieszać zakazu wymuszania upokorzenia, uniżenia lub
   zależności emocjonalnej jako warunku dostępu do dóbr krytycznych, pomocy,
   procedur ochronnych lub podstawowych zasobów systemu.
4. Często powtarzający się wyjątek jest sygnałem, że brakuje reguły, kontraktu albo
   nowej ścieżki operacyjnej.

---

## 3. Minimalny model danych wyjątku

Każdy wyjątek MUSI posiadać co najmniej:

```yaml
exception:
  policy_id: "DIA-EXC-001"
  exception_id: "EXC-[federation]-[timestamp]-[nonce]"
  type: "ordinary" # ordinary | emergency | injunction
  owner: "[rola lub identyfikator węzła odpowiedzialnego]"
  requester: "[inicjator]"
  scope: "[jakie role, zasoby, dane lub procedury obejmuje wyjątek]"
  reason: "[uzasadnienie biznesowe / etyczne / bezpieczeństwa]"
  risk_level: "medium" # low | medium | high | critical
  constitutional_basis: ["XIV.3", "XIV.4"]
  created_at: "[timestamp]"
  expiry: "[timestamp]"
  fail_closed_target: "[stan powrotu]"
  approvals: []
  monitoring:
    metrics: []
    review_at: "[timestamp]"
  rollback_conditions: []
  status: "active" # proposed | active | suspended | expired | rolled_back
```

Pola `approvals`, `monitoring.metrics` i `rollback_conditions` nie mogą być puste
dla wyjątków o stawce `high` lub `critical`.

---

## 4. Typy wyjątków

### 4.1. Wyjątek zwykły (`ordinary`)

Wyjątek dla sytuacji, które nie są kryzysem czasu rzeczywistego, ale wymagają
czasowego odejścia od domyślnej reguły.

Przykłady:

- czasowe podniesienie limitu kosztowego agenta,
- czasowe rozszerzenie zakresu trasowania (ang. routingu),
- ręczne utrzymanie starszej wersji komponentu z przyczyn kompatybilności.

### 4.2. Wyjątek awaryjny (`emergency`)

Wyjątek uruchamiany pod presją czasu, gdy opóźnienie może zwiększyć krzywdę lub
uniemożliwić ochronę człowieka.

Przykłady:

- aktywacja trybu A3,
- czasowe ominięcie części przepływu działań (ang. workflow) w awarii zasilania
  lub łączności (ang. blackout),
- awaryjne zabezpieczenie kanału komunikacji sygnalisty.

### 4.3. Wyjątek ochronny / konstytucyjny (`injunction`)

Wyjątek w postaci środka tymczasowego służącego zawieszeniu działania, które może być
niekonstytucyjne lub grozi nieodwracalną szkodą.

Przykłady:

- zawieszenie polityki federacyjnej,
- wstrzymanie publikacji do czasu rozstrzygnięcia,
- zamrożenie uprawnień roli zaufania publicznego.

---

## 5. Procedura zatwierdzania

### 5.1. Wyjątek zwykły

1. Inicjator tworzy rekord wyjątku z pełnym modelem danych.
2. Wyjątek musi być zatwierdzony przez co najmniej dwie role, z których jedna nie
   jest bezpośrednim beneficjentem wyjątku.
3. Dla wyjątków `high` i `critical` obowiązuje współpodpis (ang. multisig) oraz
   jawne wskazanie metryk monitorowania.
4. Po zatwierdzeniu wyjątek uzyskuje status `active`.

### 5.2. Wyjątek awaryjny

1. Może być aktywowany przez operatora albo automatycznie przez zdefiniowany
   wyzwalacz (ang. trigger).
2. Aktywacja tworzy rekord wyjątku natychmiast albo najpóźniej razem z pierwszym
   śladem działania.
3. Maksymalny czas życia wyjątku awaryjnego jest parametrem federacji, ale po
   wygaśnięciu system MUSI wrócić do stanu bezpiecznego domknięcia (ang.
   fail-closed).
4. Rewizja post-hoc jest obowiązkowa i musi się rozpocząć nie później niż 72 godziny
   po aktywacji, chyba że federacja jest nadal w trybie kryzysowym.

### 5.3. Wyjątek ochronny / konstytucyjny

1. Jest aktywowany przez panel ad-hoc albo inny uprawniony organ proceduralny
   określony przez Konstytucję.
2. Musi zawierać wskazanie grożącej szkody nieodwracalnej.
3. Wygasa automatycznie po pełnym rozstrzygnięciu albo po osiągnięciu `expiry`.
4. Nie może zostać przedłużony bez nowej decyzji i nowego śladu uzasadnienia.

---

## 6. Monitoring i automatyczne cofnięcie

Każdy wyjątek MUSI mieć:

- wskaźniki skutków ubocznych,
- termin przeglądu,
- warunki automatycznego zawieszenia,
- warunki automatycznego cofnięcia (ang. rollbacku).

Wyjątek MUSI zostać automatycznie zawieszony albo cofnięty, jeżeli:

1. pojawia się sygnał krzywdy lub nadużycia powiązany z wyjątkiem,
2. wyjątek przekracza `expiry`,
3. nie wykonano obowiązkowego przeglądu,
4. zniknął warunek, który uzasadniał jego uruchomienie,
5. wyjątek zaczyna działać jak trwała furtka architektoniczna,
6. wyjątek zaczyna uzależniać dostęp do pomocy, procedur ochronnych albo dóbr
   krytycznych od upokorzenia, uniżenia lub zależności emocjonalnej.

---

## 7. Metryki zdrowia wyjątków

Każda federacja powinna mierzyć co najmniej:

- liczbę aktywnych wyjątków per okres,
- średni czas życia wyjątku,
- odsetek wyjątków przedłużanych,
- odsetek wyjątków, które zakończyły się cofnięciem (ang. rollbackiem),
- udział wyjątków `emergency` i `injunction`,
- udział wyjątków powiązanych z krzywdą, incydentem lub odwołaniem.

Wysoki odsetek wyjątków albo ich stały wzrost jest sygnałem, że system dryfuje w
stronę zarządzania przez wyjątki zamiast przez kontrakty.

---

## 8. Relacja z innymi dokumentami

- **Konstytucja Art. XIV**: niniejszy dokument operacjonalizuje model danych i
  procedurę wyjątków.
- **`AUTONOMY-LEVELS.pl.md`**: aktywacja A3 jest wyjątkiem awaryjnym.
- **`ENTRENCHMENT-CLAUSE.pl.md`**: środek tymczasowy jest wyjątkiem ochronnym /
  konstytucyjnym.
- **`NORMATIVE-HIERARCHY.pl.md`**: polityka wyjątków jest dokumentem Poziomu 3.
