# Gradient autonomii agentów DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-AUTON-LEVELS-001` |
| `typ` | Ustawa wykonawcza (Poziom 3 hierarchii normatywnej) |
| `wersja` | 0.1.0-draft |
| `podstawa` | Art. II.3-4, II.8, V.10, V.13 Konstytucji DIA |

---

## 1. Cel dokumentu

Konstytucja (Art. II.3) wymaga, aby "największa moc systemu przechodziła przez
człowieka". Jednocześnie Art. V.10 wymaga od agenta wyłącznika awaryjnego (ang.
kill-switch), limitów i jawnego trybu zaufania. Niniejszy dokument definiuje
**cztery poziomy autonomii agenta**, które operacjonalizują te zasady bez tworzenia
wąskiego gardła wymagającego człowieka w pętli decyzyjnej (ang.
human-in-the-loop) na każdej operacji.

Gradient autonomii pozwala człowiekowi **ustawić ramy**, a nie klikać "OK" na każdym
kroku. Moc przechodzi przez człowieka, bo to człowiek definiuje gradient.

---

## 2. Poziomy autonomii

### A0 - Propozycja (Propose & Wait)

| Parametr | Wartość |
| :--- | :--- |
| **Opis** | Agent przygotowuje propozycję. Nie podejmuje żadnej akcji bez jawnego zatwierdzenia przez operatora. |
| **Kiedy domyślny** | Decyzje zmieniające polityki, kontrakty, uprawnienia, publikacje, dane wrażliwe. Każda akcja o nieodwracalnych lub trudno odwracalnych skutkach. |
| **Raportowanie** | Propozycja jest prezentowana operatorowi z uzasadnieniem, wariantami i oceną ryzyka. |
| **Cofanie** | Nie dotyczy - akcja nie została podjęta. |
| **Przykłady** | Redakcja dokumentu publicznego; zmiana polityki węzła; wysłanie komunikatu w imieniu użytkownika; eskalacja sprawy; modyfikacja kontraktu agenta. |

### A1 - Działaj i informuj (Act & Notify)

| Parametr | Wartość |
| :--- | :--- |
| **Opis** | Agent podejmuje akcję, ale natychmiast informuje operatora. Operator może cofnąć akcję w zdefiniowanym oknie czasowym. |
| **Kiedy domyślny** | Akcje o niskim ryzyku i wysokiej odwracalności, które wymagają szybkości, ale nie są rutynowe. |
| **Raportowanie** | Natychmiastowe powiadomienie z opisem akcji, uzasadnieniem i instrukcją cofnięcia. |
| **Cofanie** | Możliwe w zdefiniowanym oknie (domyślnie: parametr federacji, np. 15 minut). Po upływie okna akcja jest traktowana jako zatwierdzona. |
| **Przykłady** | Trasowanie (ang. routing) zadania do innego węzła; aktualizacja pamięci podręcznej (ang. cache) memarium; odpowiedź na zapytanie sieciowe o niskiej stawce; logowanie zdarzenia sensorium. |

### A2 - Działaj w ramach budżetu (Act Within Budget)

| Parametr | Wartość |
| :--- | :--- |
| **Opis** | Agent działa autonomicznie w ramach jawnie zdefiniowanego budżetu: limitów czasu, kosztu tokenowego, zakresu operacji i liczby akcji. Raportuje po fakcie. |
| **Kiedy domyślny** | Operacje rutynowe, powtarzalne, o przewidywalnym zakresie i niskim ryzyku jednostkowym. |
| **Raportowanie** | Raport zbiorczy (okresowy lub po wyczerpaniu budżetu) z metrykami: liczba akcji, koszt, odstępstwa od normy. |
| **Cofanie** | Poszczególne akcje mogą być trudne do cofnięcia, ale budżet ogranicza skalę szkody. |
| **Limity budżetu** | Definiowane w kontrakcie agenta: `max_cost`, `max_time`, `max_actions`, `scope_whitelist`, `scope_blacklist`. Przekroczenie dowolnego limitu -> automatyczny stop i powiadomienie operatora. |
| **Przykłady** | Odpowiadanie na rutynowe zapytania; agregacja danych sensorium; utrzymanie indeksu memarium; monitorowanie metryk zdrowia węzła. |

### A3 - Tryb kryzysowy (ang. Emergency Mode)

| Parametr | Wartość |
| :--- | :--- |
| **Opis** | Agent działa z maksymalną szybkością w sytuacji bezpośredniego zagrożenia życia lub nagłej poważnej krzywdy. Zostawia pełny ślad. Rewizja post-hoc jest obligatoryjna. |
| **Kiedy aktywowany** | Wyłącznie gdy spełnione są warunki Art. II.8: bezpośrednie zagrożenie życia lub nagła, bezpośrednia i poważna krzywda zdrowotna. |
| **Raportowanie** | Pełny, neredagowany ślad wszystkich akcji (ang. trace), zapisywany lokalnie i (jeśli możliwe) replikowany. |
| **Cofanie** | Nie jest priorytetem w trakcie kryzysu. Po zakończeniu kryzysu -> obligatoryjna rewizja i ewentualna korekta. |
| **Limity czasowe** | Tryb A3 ma zdefiniowany maksymalny czas trwania (parametr federacji). Po jego upływie agent automatycznie wraca do poziomu A0 w trybie bezpiecznego domknięcia (ang. fail-closed). |
| **Aktywacja** | Automatyczna (na podstawie sygnałów sensorium lub detekcji wzorca kryzysowego) lub ręczna (operator). Aktywacja automatyczna wymaga oddzielnego potwierdzenia w logu. |
| **Przykłady** | Koordynacja pomocy w awarii zasilania lub łączności (ang. blackout); alert o zagrożeniu życia; wstępna kategoryzacja (ang. triage) medyczna pierwszego kontaktu; zabezpieczenie kanału komunikacji sygnalisty pod bezpośrednim zagrożeniem. |

---

## 3. Zasady przypisywania poziomów

### 3.1. Kontrakt agenta

Każdy agent w swoim kontrakcie (Art. V.10) deklaruje:

```yaml
autonomy:
  max_level: A2           # Maksymalny poziom, do jakiego agent jest zaprojektowany
  default_level: A1       # Poziom domyślny przy starcie
  emergency_capable: true # Czy agent ma zdolność A3
  budget:
    max_cost_tokens: 1000
    max_time_seconds: 3600
    max_actions_per_cycle: 50
    scope_whitelist:
      - "memarium.read"
      - "memarium.index"
      - "sensorium.aggregate"
    scope_blacklist:
      - "policy.modify"
      - "reputation.vote"
      - "publish.*"
```

### 3.2. Operator może obniżyć, nigdy podwyższyć

Operator węzła może ustawić agentowi **niższy** poziom niż `max_level` z kontraktu.
Nie może ustawić wyższego. Przykład: agent z `max_level: A2` może być ograniczony do
A0, ale agent z `max_level: A1` nie może otrzymać A2.

Uzasadnienie: poziom autonomii jest ograniczeniem architektonicznym, nie parametrem
wygody. Agent zaprojektowany na A1 nie ma mechanizmów budżetowych wymaganych przez A2.

### 3.3. Federacja może zaostrzać

Federacja może narzucić `max_level` niższy niż kontrakt agenta (np. w trybie
`CORP_COMPLIANT` wszystkie agenty na A0). Nie może osłabiać limitów z kontraktu.

### 3.4. Eskalacja poziomu w górę

Agent nie może sam eskalować swojego poziomu autonomii (**zakaz samonadawania
uprawnień**, ang. zero self-authorize, zgodnie z Art. V.13). Eskalacja wymaga:

- **A0 -> A1 lub A2**: decyzja operatora.
- **Dowolny -> A3**: operator lub automatyczna detekcja kryzysu z jawnym wpisem w logu
  i obowiązkową rewizją post-hoc.
- **A3 -> powrót**: automatyczny po upływie limitu czasowego (bezpieczne domknięcie,
  ang. fail-closed, do A0).

---

## 4. Matryca: typ operacji × poziom autonomii

Poniższa tabela jest domyślna. Federacje mogą ją zaostrzać (przesuwać w lewo),
nie mogą rozluźniać (przesuwać w prawo).

| Kategoria operacji | Minimalny poziom | Uzasadnienie |
| :--- | :--- | :--- |
| Zmiana polityki / kontraktu | A0 | Nieodwracalne, wpływ na ład organizacyjny (ang. governance) |
| Publikacja / komunikat zewnętrzny | A0 | Wysoka stawka reputacyjna |
| Głosowanie reputacyjne | A0 | Wpływ na kierowanie zaufaniem (ang. trust routing) |
| Modyfikacja danych wrażliwych | A0 | Prywatność, godność |
| Zakresowa zmiana widoczności pamięci chroniąca prywatność | kontekstowo | Może być delegowana tylko wtedy, gdy operator wcześniej zatwierdził zakres, podmiot oraz model odwracalności/audytu |
| Trasowanie (ang. routing) zadania do innego węzła | A1 | Odwracalne, ale wymaga świadomości |
| Aktualizacja pamięci podręcznej (ang. cache) / indeksu | A2 | Rutynowe, budżetowalne |
| Odpowiedź na zapytanie rutynowe | A2 | Rutynowe, budżetowalne |
| Agregacja sensorium | A2 | Rutynowe, budżetowalne |
| Ochrona życia / kryzysowa wstępna kategoryzacja (ang. triage) | A3 | Art. II.8 |

### 4.1. Zapamiętane zgody operatora

A0 oznacza, że przed podjęciem akcji wymagana jest ludzka wola. Nie musi to
jednak zawsze oznaczać świeżego promptu dla każdego wystąpienia tej samej
ograniczonej akcji. Operator może wyrazić tę wolę jako zapamiętaną politykę
zgody, analogiczną do whitelisty agenta, jeżeli jawne są:

- kto może działać: participant, agent, moduł albo lokalna tożsamość operatora,
- jaka klasa danych lub akcji jest objęta zgodą,
- jaki poziom autonomii i budżet obowiązują po zatwierdzeniu,
- jak decyzja jest audytowana,
- jak zgodę można odwołać.

Przykład: `memarium.forget` nie jest jednym aktem społecznym. Natychmiastowe
zapomnienie w przestrzeni personal może być delegowane agentowi prywatności dla
ograniczonego podmiotu i klasy artefaktów. Publiczny tombstone, zapomnienie
wspólnotowe i zapomnienie w przestrzeni crisis pozostają operacjami governed
albo wymagającymi przeglądu operatora, ponieważ wpływają na pamięć wspólną,
publiczną rozliczalność albo konstytucyjne minimum materiałów.

---

## 5. Audyt i monitoring

### 5.1. Ślady decyzji (ang. trace)

Każda akcja agenta, niezależnie od poziomu, generuje wpis w logu z co najmniej:

- timestamp,
- `autonomy_level` w momencie akcji,
- `action_type`,
- `scope` (jakie zasoby były użyte),
- `cost` (jeśli mierzalne),
- `justification` (dla A1, A3 - jawne; dla A2 - dostępne na żądanie).

### 5.2. Przegląd budżetowy (dla A2)

Agent działający na A2 generuje raport budżetowy zawierający:

- wykorzystanie limitu kosztowego (%),
- wykorzystanie limitu czasowego (%),
- liczbę akcji vs. limit,
- odstępstwa od normy (anomalie).

Raport jest dostępny dla operatora na żądanie i generowany automatycznie przy
wyczerpaniu >=80% dowolnego limitu.

### 5.3. Rewizja post-hoc (dla A3)

Po zakończeniu trybu A3 obligatoryjna jest rewizja obejmująca:

- pełny ślad akcji,
- ocenę adekwatności aktywacji A3 (czy zagrożenie było realne),
- ocenę proporcjonalności podjętych akcji,
- identyfikację skutków ubocznych,
- rekomendacje dotyczące kalibracji progów aktywacji.

Rewizja jest dokumentowana i dostępna do audytu.

---

## 6. Relacja z innymi dokumentami

- **Konstytucja Art. II.3-4**: Gradient autonomii jest operacjonalizacją zasady
  "moc przechodzi przez człowieka".
- **Konstytucja Art. V.10**: Poziomy autonomii rozszerzają kontrakt agenta o jawny
  parametr `autonomy_level`.
- **Konstytucja Art. V.13**: Dokument konkretyzuje zakaz samodzielnej eskalacji
  uprawnień przez agentów.
- **Konstytucja Art. IX**: Tryb A3 jest formalizacją Art. II.8 i Art. IX.3.
- **Konstytucja Art. XIV**: Każde użycie A3 jest wyjątkiem konstytucyjnym, nawet jeśli
  ma uproszczoną ścieżkę aktywacji ze względu na presję czasową.
