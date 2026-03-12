# Specyfikacja reputacji proceduralnej DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-PROC-REP-001` |
| `typ` | Ustawa wykonawcza (Poziom 3 hierarchii normatywnej) |
| `wersja` | 0.1.0-draft |
| `podstawa` | Art. VII.4-5, VII.6, VII.8, XI Konstytucji DIA; `REPUTATION-VALIDATION-PROTOCOL.pl.md`; `../core-values/CORE-VALUES.pl.md` sekcja "Reputacja jako dźwignia, nie władza" |
| `status mechanizmów` | `[mechanizm - hipoteza]` dla funkcji scoringowych; model danych jest normatywny |

---

## 1. Cel dokumentu

Konstytucja wymaga reputacji proceduralnej jako zabezpieczenia trasowania zaufania
(Art. VII.4), kwalifikowalności panelowej (ENTRENCHMENT-CLAUSE 3.2) i asymetrycznej
odpowiedzialności (Art. VII.8). Brakuje jednak specyfikacji, **w jaki sposób**
reputacja proceduralna jest obliczana ze swoich źródeł.

Niniejszy dokument definiuje:

- domeny reputacji i źródła sygnałów,
- model scoringowy (oznaczony `[hipoteza]` tam, gdzie niewalidowany),
- definicję węzła aktywnego do celów reputacyjnych,
- procedurę rozruchu dla nowych węzłów (ang. cold start),
- asymetryczną odpowiedzialność dla ról zaufania publicznego,
- przenośny pakiet dowodów do mobilności międzyfederacyjnej,
- haki detekcji karteli,
- połączenie z metrykami zdrowia M1-M5 z `REPUTATION-VALIDATION-PROTOCOL.pl.md`.

---

## 2. Domeny reputacji

Reputacja **nie jest jedną globalną liczbą**. Jest rozłożona na cztery domeny,
z których każda mierzy inny wymiar wiarygodności.

| Domena | Co mierzy | Podstawa konstytucyjna |
| :--- | :--- | :--- |
| `contract` | Honorowanie kontraktów, jakość realizacji, zgodność z SLA | Art. V.2, XII.2 |
| `procedural` | Służba panelowa, udział w governance, deklaracje COI, zgodność protokołowa | Art. VII.4, VII.6 |
| `incident` | Reakcja na incydenty, korekty, ujawnianie podatności | Art. XVI.4, X.9 |
| `community` | Wkład, mentoring, dokumentacja, pomoc we wdrażaniu nowych węzłów | Art. XII.4, VI.4 |

Każda domena generuje wynik w przedziale `[0.0, 1.0]`, normalizowany w ramach
federacji.

**Tylko domena `procedural` kwalifikuje węzeł do selekcji panelu ad-hoc**
(ENTRENCHMENT-CLAUSE 3.2: "wysoka reputacja proceduralna, nie techniczna"). Inne
domeny informują trasowanie zaufania, ale nie dają dźwigni w governance.

---

## 3. Źródła sygnałów i ich typy

Sygnał reputacyjny to **opatrzone znacznikiem czasu, udokumentowane zdarzenie** --
fakt, nie opinia. Wynika to z konstytucyjnej preferencji faktów nad narracją
(Art. XI) i z wartości rdzeniowych kładących nacisk na dane ponad stan.

### 3.1. Model danych sygnału

```yaml
reputation_signal:
  signal_id: "[unikalny identyfikator]"
  node_id: "[identyfikator węzła]"
  federation_id: "[federacja]"
  domain: "contract"         # contract | procedural | incident | community
  signal_type: "[konkretny typ]"
  polarity: "positive"       # positive | negative
  weight: 1.0                # waga bazowa przed zastosowaniem krzywej
  evidence_ref: "[referencja do audytowalnego dowodu]"
  timestamp: "[ISO 8601]"
  source_node_id: "[kto wygenerował sygnał, jeśli dotyczy]"
  source_type: "oracle"      # oracle | protocol | peer | self_report
  ttl: "[ISO 8601 – wygaśnięcie]"
```

### 3.2. Typy sygnałów według domen

| Domena | Sygnały pozytywne | Sygnały negatywne |
| :--- | :--- | :--- |
| `contract` | `contract_fulfilled`, `quality_verified`, `sla_met` | `contract_violated`, `quality_below_threshold`, `sla_missed` |
| `procedural` | `panel_completed`, `governance_vote_cast`, `coi_declared`, `protocol_compliant` | `panel_no_show`, `coi_undeclared`, `protocol_violation`, `governance_inaction` |
| `incident` | `incident_reported`, `correction_applied`, `vulnerability_disclosed` | `incident_concealed`, `correction_refused`, `retaliation` |
| `community` | `contribution_accepted`, `mentoring_verified`, `documentation_added` | (brak aktywności nie jest negatywem -- tylko czynna szkoda generuje sygnały negatywne) |

### 3.3. Wiarygodność źródła sygnału

Sygnały z różnych źródeł mają różne bazowe wagi:

| Typ źródła | Opis | Mnożnik wagi |
| :--- | :--- | :--- |
| `oracle` | Zweryfikowane przez wyrocznię (pomiar wyniku) | 1.0 (referencja) |
| `protocol` | Wygenerowane automatycznie przez kontrolę zgodności protokołowej | 0.9 |
| `peer` | Zgłoszone przez inny węzeł | 0.7 |
| `self_report` | Zgłoszone przez sam węzeł (np. deklaracja COI) | 0.5 |

Mnożniki są parametrami federacyjnymi (`signal_source_weights`). Obowiązuje
zasada "ostrożniej tak, luźniej nie": federacja może obniżyć, ale nie podwyższyć
mnożników powyżej wartości domyślnych.

---

## 4. Model scoringowy

### 4.1. Obliczanie wyniku domeny `[hipoteza]`

Dla każdej domeny wynik oblicza się z sygnałów węzła w obrębie okna kroczącego:

```
domain_score = f(sum_positive, sum_negative, signal_count, diversity)
```

Gdzie:

- `sum_positive` = suma `g(weight * source_multiplier * decay_factor)` dla
  wszystkich sygnałów pozytywnych
- `sum_negative` = suma `g(weight * source_multiplier * decay_factor *
  asymmetry_factor)` dla wszystkich sygnałów negatywnych
- `g(x)` = podliniowa funkcja wzrostu (patrz 4.2)
- `domain_score` = `clamp(0.0, 1.0, normalize(sum_positive - sum_negative))`

Normalizacja jest relatywna wobec rozkładu sygnałów w federacji, przeliczana
co `measurement_cycle_days`.

### 4.2. Podliniowa krzywa wzrostu `[hipoteza]`

Funkcja wzrostu `g(x)` MUSI być wklęsła, aby zapobiec koncentracji:

```
g(x) = ln(1 + x) / ln(1 + cap)
```

Dokładna postać funkcji (`ln`, `sqrt`, `tanh` lub inna) jest parametrem
federacyjnym (`growth_function`). Ograniczenie to wklęsłość: `g''(x) < 0` dla
wszystkich `x > 0`.

Gwarantuje to malejące zwroty: setny spełniony kontrakt wnosi mniej niż
dziesiąty.

### 4.3. Zanik temporalny `[hipoteza]`

Sygnały zanikają eksponencjalnie w obrębie okna kroczącego:

```
decay_factor = exp(-lambda * age_days)
```

Gdzie `lambda = ln(2) / half_life_days`. Domyślny okres połowicznego zaniku
według domen:

| Domena | `half_life_days` | Uzasadnienie |
| :--- | :--- | :--- |
| `contract` | 90 | Niedawna niezawodność liczy się najbardziej |
| `procedural` | 120 | Ślad w governance wymaga dłuższej pamięci |
| `incident` | 60 | Szybka korekta ma znaczenie |
| `community` | 180 | Długoterminowe wkłady zanikają najwolniej |

Wyjątek: sygnały otagowane `continuing_benefit` (np. utrzymywana infrastruktura
wciąż w użyciu) zachowują minimalny próg zaniku 0.3, dopóki korzyść trwa.

### 4.4. Limity koncentracji

1. Żaden pojedynczy typ sygnału nie może wnieść więcej niż 40% pozytywnego wyniku
   domeny.
2. Żaden pojedynczy węzeł źródłowy nie może wnieść więcej niż 20% sygnałów innego
   węzła w żadnej domenie.
3. Naruszenie tych limitów wyzwala `concentration_warning` i obcina nadwyżkę.

---

## 5. Definicja węzła aktywnego

Węzeł jest `active` do celów reputacyjnych, jeśli spełnia wszystkie poniższe
warunki:

1. Wygenerował co najmniej `min_signals_per_period` (domyślnie: 3) audytowalnych
   sygnałów w `activity_window` (domyślnie: 90 dni).
2. Odpowiada na sygnały heartbeat federacji (spójnie z kryteriami aktywności
   z `FEDERATION-MEMBERSHIP-AND-QUORUM`).
3. Nie jest aktualnie `suspended` ani `retired`.

Nieaktywne węzły zachowują historyczne wyniki, ale **nie mogą ich używać do
dźwigni w governance** (waga głosu, kwalifikowalność panelowa) do czasu
reaktywacji. Reaktywacja wymaga spełnienia progu aktywności przez pełne
`activity_window`.

---

## 6. Asymetryczna odpowiedzialność

Węzły pełniące role zaufania publicznego (Art. VII.8) podlegają surowszym
standardom:

1. Waga sygnałów **negatywnych** jest mnożona przez `asymmetry_factor`
   (domyślnie: 1.5).
2. Waga sygnałów **pozytywnych nie jest redukowana** -- asymetria działa tylko
   w dół.
3. Zbiór ról zaufania publicznego zostanie zdefiniowany w przyszłym dokumencie
   `ROLE-REGISTRY`. Do tego czasu kwalifikują się: członek panelu, operator
   federacji, głosujący z wagą, operator wyroczni.
4. Asymetria zaczyna działać natychmiast po objęciu roli i utrzymuje się przez
   `asymmetry_tail_days` (domyślnie: 90) po jej opuszczeniu.

---

## 7. Rozruch i inicjalizacja nowych węzłów

Nowy węzeł wchodzący do federacji napotyka problem zimnego startu: brak sygnałów,
brak wyniku, brak dostępu do governance.

### 7.1. Wynik rozruchowy

Nowy węzeł startuje z `bootstrap_score` w każdej domenie, równym **medianie
najniższego kwartyla** aktywnych węzłów w tej domenie. Zapobiega to:

- barierom wejścia z zerowym wynikiem (co narusza metrykę M2),
- zawyżonym wynikom wejściowym (co umożliwia eksploatację bootstrap).

### 7.2. Zanik rozruchowy

Wynik rozruchowy zanika liniowo ku rzeczywistemu wynikowi węzła w okresie
`bootstrap_decay_period` (domyślnie: 90 dni):

```
effective_score = actual_score + max(0, bootstrap_remaining) * (bootstrap_score - actual_score)
bootstrap_remaining = 1 - (days_since_join / bootstrap_decay_period)
```

### 7.3. Ograniczenia governance w okresie rozruchowym

Węzeł w okresie rozruchowym (`bootstrap_remaining > 0`) **nie może**:

- być wybrany do panelu ad-hoc,
- oddawać głosu ważonego (tylko głos równy),
- pełnić ról zaufania publicznego.

Ograniczenia te zapewniają, że dźwignia w governance wymaga faktycznej, zdobytej
reputacji proceduralnej.

---

## 8. Przenośny pakiet dowodów

Reputacja jest lokalna dla federacji, ale węzły mogą przenosić się między
federacjami. Przenośność jest realizowana przez **przenośny pakiet dowodów**,
nie przez nagi wynik.

### 8.1. Zawartość pakietu

```yaml
reputation_export_package:
  node_id: "[identyfikator węzła]"
  source_federation_id: "[federacja, która wygenerowała pakiet]"
  exported_at: "[ISO 8601]"
  package_signature: "[podpis kryptograficzny federacji źródłowej]"
  signal_history:
    - signal_id: "[...]"
      domain: "[...]"
      signal_type: "[...]"
      polarity: "[...]"
      weight: "[...]"
      evidence_ref: "[...]"
      timestamp: "[...]"
      source_type: "[...]"
  attestations:
    - type: "panel_service"
      description: "[...]"
      issued_by: "[identyfikator federacji lub panelu]"
      date: "[...]"
    - type: "sanction_served"
      description: "[...]"
      issued_by: "[...]"
      date: "[...]"
  appeals_history: []
  sanctions_history: []
  repairs_history: []
  roles_held: []
```

### 8.2. Zachowanie federacji przyjmującej

Federacja przyjmująca:

1. **Importuje** historię sygnałów jako dowody.
2. **Przelicza** wynik węzła według własnych parametrów (funkcja wzrostu, zanik,
   progi).
3. **Nie akceptuje** wyniku federacji źródłowej jako własnego.
4. **Może** zastosować `foreign_signal_discount` (domyślnie: 0.8) do
   importowanych sygnałów, odzwierciedlając ograniczoną weryfikowalność.
5. Traktuje importowany pakiet jako **przyspieszony rozruch**, nie transfer
   reputacji.

---

## 9. Haki detekcji karteli

### 9.1. Detekcja wzajemnego podbijania

System MUSI flagować pary lub grupy węzłów, w których:

- wzajemne sygnały pozytywne przekraczają `mutual_boost_threshold` (domyślnie:
  30% pozytywnych sygnałów każdego węzła pochodzi od drugiego),
- sygnały są zgrupowane czasowo (w `cluster_window`, domyślnie: 48 godzin).

Zaflagowane wzorce generują `cartel_flag` na dotkniętych węzłach i wyzwalają
przegląd.

### 9.2. Detekcja zamkniętego przepływu grupowego

System MUSI wykrywać zamknięte grupy, w których sygnały reputacyjne krążą
głównie wewnątrz grupy:

- udział sygnałów wewnątrzgrupowych > `closed_group_threshold` (domyślnie: 60%),
- rozmiar grupy < `max_cartel_group_size` (domyślnie: 10 węzłów).

### 9.3. Wymóg dywersyfikacji źródeł

Aby sygnał wniósł pełną wagę, węzeł musi mieć sygnały od co najmniej
`min_source_diversity` (domyślnie: 5) różnych węzłów źródłowych w tej samej
domenie w oknie kroczącym. Poniżej tego progu waga sygnału jest redukowana
proporcjonalnie.

---

## 10. Model danych rekordu reputacyjnego

```yaml
reputation_record:
  node_id: "[identyfikator węzła]"
  federation_id: "[federacja]"
  snapshot_at: "[ISO 8601]"
  status: "active"             # active | inactive | bootstrapping | suspended
  domains:
    contract:
      score: 0.0               # [0.0, 1.0]
      signal_count: 0
      positive_sum: 0.0
      negative_sum: 0.0
      last_signal_at: "[ISO 8601]"
    procedural:
      score: 0.0
      signal_count: 0
      positive_sum: 0.0
      negative_sum: 0.0
      last_signal_at: "[ISO 8601]"
    incident:
      score: 0.0
      signal_count: 0
      positive_sum: 0.0
      negative_sum: 0.0
      last_signal_at: "[ISO 8601]"
    community:
      score: 0.0
      signal_count: 0
      positive_sum: 0.0
      negative_sum: 0.0
      last_signal_at: "[ISO 8601]"
  roles: []                    # bieżące role do obliczania asymetrii
  bootstrap_remaining_days: 0
  cartel_flags: []
  concentration_warnings: []
```

---

## 11. Połączenie z metrykami zdrowia (M1-M5)

Niniejsza specyfikacja dostarcza dane, które konsumują metryki
z `REPUTATION-VALIDATION-PROTOCOL`:

| Metryka | Źródło danych z tej specyfikacji |
| :--- | :--- |
| M1 (Gini) | Rozkład `domain_score` wśród wszystkich aktywnych węzłów |
| M2 (Czas do progu wpływu) | Czas od pierwszego sygnału do osiągnięcia `panel_procedural_threshold` |
| M3 (Detekcja karteli) | Liczba `cartel_flag` względem łącznej liczby sygnałów |
| M4 (Korelacja reputacja-jakość) | Korelacja między `contract.score` a wynikami zweryfikowanymi przez wyrocznie |
| M5 (Rotacja górnej warstwy) | Wejścia/wyjścia węzłów w górnym decylu `procedural.score` |

---

## 12. Tryby awarii i środki zaradcze

| Tryb awarii | Środek zaradczy |
| :--- | :--- |
| Gaming wolumenu trywialnych sygnałów | Minimalne progi znaczności per typ sygnału; malejące zwroty przez krzywą podliniową; limity koncentracji (sekcja 4.4) |
| Atak Sybila wzajemnymi sygnałami | Haki detekcji karteli (sekcja 9); wymóg dywersyfikacji źródeł |
| Eksploatacja rozruchu | Ograniczenie `bootstrap_min_age`; domena proceduralna wymaga faktycznej służby panelowej |
| Zanik karzący długoterminowych kontrybutorów | Wyjątek `continuing_benefit`; domena `community` ma najwolniejszy zanik |
| Weaponizacja asymetrii przeciw rolom zaufania publicznego | Asymetria dotyczy tylko sygnałów negatywnych; procedura odwoławcza bez zmian |
| Nieprzejrzystość wyniku eroduje zaufanie | Każdy wynik jest dekompozowalny: węzeł może zażądać pełnej historii sygnałów i rozkładu wag |
| "Zakupy reputacyjne" między federacjami | Przenośny pakiet dowodów, nie przenośny wynik; federacja przyjmująca przelicza lokalnie |

---

## 13. Parametry federacyjne

| Parametr | Domyślnie | Dopuszczalny zakres | Zasada |
| :--- | :--- | :--- | :--- |
| `growth_function` | `ln` | `ln`, `sqrt`, `tanh` | Musi być wklęsła |
| `decay_half_life_contract` | 90 dni | >= 60 dni | Ostrożniej tak, luźniej nie |
| `decay_half_life_procedural` | 120 dni | >= 90 dni | " |
| `decay_half_life_incident` | 60 dni | >= 45 dni | " |
| `decay_half_life_community` | 180 dni | >= 120 dni | " |
| `activity_window` | 90 dni | >= 60 dni | " |
| `min_signals_per_period` | 3 | >= 2 | " |
| `bootstrap_decay_period` | 90 dni | >= 60 dni | " |
| `asymmetry_factor` | 1.5 | >= 1.2 | " |
| `asymmetry_tail_days` | 90 dni | >= 60 dni | " |
| `panel_procedural_threshold` | 0.6 | >= 0.5 | " |
| `mutual_boost_threshold` | 30% | <= 30% | " |
| `closed_group_threshold` | 60% | <= 60% | " |
| `min_source_diversity` | 5 | >= 3 | " |
| `foreign_signal_discount` | 0.8 | [0.5, 1.0] | " |
| `concentration_cap_per_type` | 40% | <= 40% | " |
| `concentration_cap_per_source` | 20% | <= 20% | " |

---

## 14. Otwarte pytania

1. **Dokładna postać funkcji podliniowej**: `ln`, `sqrt` czy `tanh`? Wymaga
   symulacji (Faza 0 z REPUTATION-VALIDATION-PROTOCOL). Obecnie parametr
   federacyjny.

2. **Wyniki ujemne**: Czy domena `incident` powinna dopuszczać wyniki poniżej 0.0
   (tj. `[-1.0, 1.0]`), aby uchwycić "netto szkodliwy"? Obecny projekt: wyniki
   w `[0.0, 1.0]`.

3. **Waga sygnałów wyroczni**: Czy sygnały generowane przez wyrocznie powinny mieć
   mnożnik wyższy niż 1.0? Argument za: są zweryfikowane wynikiem. Argument
   przeciw: zaufanie do wyroczni jest zmienną.

4. **Rejestr ról**: Asymetryczna odpowiedzialność zależy od listy ról zaufania
   publicznego. Do czasu napisania `ROLE-REGISTRY` obowiązuje tymczasowa lista
   z sekcji 6.3.

5. **Interakcja międzydomenowa**: Czy ciężkie sygnały negatywne w `incident`
   powinny wpływać na domenę `procedural`? Obecny projekt: domeny są niezależne.
   Argument za kontaminacją: węzeł ukrywający incydenty nie powinien służyć
   w panelach.

---

## 15. Relacja do innych dokumentów

- **Konstytucja Art. VII.4-5**: Niniejszy dokument operacjonalizuje reputację jako
  domenowo specyficzną, zanikającą, ograniczoną koncentracyjnie i odporną na
  kartele.
- **`REPUTATION-VALIDATION-PROTOCOL.pl.md`**: Dostarcza metryki zdrowia (M1-M5),
  które mierzą, czy niniejsza specyfikacja działa zgodnie z intencją. Funkcje
  scoringowe oznaczone `[hipoteza]` podlegają przebiegowi walidacji tamże.
- **`ENTRENCHMENT-CLAUSE.pl.md`**: Wynik domeny `procedural` jest kryterium
  kwalifikowalności do selekcji panelu ad-hoc.
- **`PANEL-SELECTION-PROTOCOL.pl.md`**: Używa `panel_procedural_threshold`
  z niniejszej specyfikacji.
- **`EXCEPTION-POLICY.pl.md`**: Sygnały związane z wyjątkami (zarówno tworzenie,
  jak i prawidłowa obsługa wyjątków) zasilają domeny `procedural` i `incident`.
- **`FEDERATION-MEMBERSHIP-AND-QUORUM.pl.md`**: Definicja statusu `active` jest
  spójna z kryteriami aktywności federacyjnej.
- **`AUTONOMY-LEVELS.pl.md`**: Wyniki przeglądu post-kryzysu A3 zasilają domeny
  `procedural` i `incident`.
- **`ABUSE-DISCLOSURE-PROTOCOL.pl.md`**: Wyniki ujawnienia zasilają domenę
  `incident`.
- **`NORMATIVE-HIERARCHY.pl.md`**: Niniejszy dokument jest ustawą wykonawczą
  Poziomu 3.
