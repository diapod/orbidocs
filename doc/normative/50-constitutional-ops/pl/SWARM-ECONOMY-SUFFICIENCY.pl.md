# Specyfikacja dostatku i wspólnego obiegu w ekonomii roju DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-SUFF-001` |
| `typ` | Ustawa wykonawcza (Poziom 3 hierarchii normatywnej) |
| `wersja` | `0.1.0-draft` |
| `podstawa` | Art. VIII.4-8, XII.5-13, XIV Konstytucji DIA; `doc/normative/30-core-values/pl/CORE-VALUES.pl.md` sekcja "Dostatek ponad akumulację" |
| `status mechanizmów` | model danych i testy zgodności są normatywne; funkcje naliczania mogą być federacyjnie parametryzowane w granicach tego dokumentu |

---

## 1. Cel dokumentu

Konstytucja zakazuje zamiany przewagi ekonomicznej na trwałą dominację ustrojową
oraz wymaga, aby nadwyżki ponad próg dostatku wracały do wspólnego obiegu. Brakuje
jednak specyfikacji minimalnej: jak federacja ma zdefiniować próg dostatku, jakie
hamulce koncentracji są obowiązkowe i jak audytować redystrybucję.

Niniejszy dokument definiuje:

- minimalne pojęcia i model danych polityki ekonomicznej,
- test zgodności progu dostatku,
- dopuszczalne klasy krzywych wynagradzania,
- obowiązkowy obieg nadwyżek,
- zakaz konwersji nagrody ekonomicznej na władzę proceduralną,
- minimalne metryki audytu federacyjnego,
- relację do wyjątków konstytucyjnych.

---

## 2. Zasada ogólna

1. Ekonomia roju służy utrzymaniu zdolności do działania ludzi, węzłów i wspólnoty,
   a nie nieskończonej akumulacji.
2. Dobrowolna wymiana kontraktowa między uczestnikami jest dopuszczalnym trybem
   wzajemności obok daru, ale jej ślady ekonomiczne nie mogą same przez się działać
   jako skrót do siły reputacyjnej, proceduralnej ani ustrojowej.
3. Federacja MUSI projektować nagrody tak, aby po osiągnięciu dostatku dalszy
   przyrost korzyści był malejący albo automatycznie kierowany do wspólnego obiegu.
4. Żaden mechanizm ekonomiczny nie może uzależniać wynagrodzenia przede wszystkim od
   napływu nowych uczestników zamiast od audytowalnego użycia, wpływu, utrzymania
   wartości lub realnego działania pomocowego.
5. Nagroda ekonomiczna nie jest ścieżką obejścia zasad reputacji proceduralnej,
   routingu, quorum, wyjątków ani kwalifikowalności ról wysokiej stawki; dotyczy to
   również salda, historii wymiany oraz samego faktu zawarcia lub wykonania
   kontraktu.
6. Zweryfikowana obecność człowieka w sieci może stanowić samodzielną podstawę do
   przyznania nieodbieralnego minimum zasobów obliczeniowych dla komunikacji,
   orientacji oraz trybów ratunkowych i opiekuńczych, niezależnie od chwilowego
   poziomu reputacji lub wkładu ekonomicznego.

---

## 3. Pojęcia podstawowe

| Pojęcie | Znaczenie |
| :--- | :--- |
| `sufficiency_threshold` | próg zasobów lub strumienia nagród wystarczający do bezpiecznego i stabilnego utrzymania węzła oraz jego operatora |
| `sufficiency_band` | pas tolerancji wokół progu dostatku, w którym system może wygładzać naliczanie zamiast stosować skok |
| `surplus` | część nagrody przekraczająca `sufficiency_threshold` po uwzględnieniu `sufficiency_band` |
| `common_circulation` | wspólny obieg nadwyżek według jawnych zasad federacyjnych |
| `infrastructural_function` | funkcja o wysokiej wartości wspólnotowej, która nie musi generować wysokiego zwrotu reputacyjnego ani rynkowego |
| `conversion_barrier` | reguła zabraniająca przekładania nagrody ekonomicznej na przewagę proceduralną lub ustrojową |
| `universal_basic_compute` | nieodbieralne minimum zasobów obliczeniowych gwarantowane zweryfikowanej osobie dla komunikacji, orientacji i trybów ochronnych |

Próg dostatku może być definiowany jako:

- kwota per okres,
- budżet kosztowy per węzeł,
- pasmo zasobów wieloskładnikowych,
- albo inny model funkcjonalnie równoważny.

Federacja NIE MOŻE definiować progu w sposób czysto narracyjny. Musi istnieć
operacyjny model, który da się audytować i aktualizować.

---

## 4. Minimalny model danych polityki ekonomicznej

Każda federacja, która uruchamia mechanizmy nagród lub tokenów, MUSI publikować
co najmniej:

```yaml
swarm_economy_policy:
  policy_id: "DIA-SUFF-001"
  federation_id: "[federacja]"
  version: "0.1.0"
  reward_unit: "[token / credit / punkt / inna jednostka]"
  measurement_period: "P30D"
  sufficiency_threshold:
    model_type: "fixed" # fixed | indexed | cost_profile | mixed
    value: "[wartość lub formuła]"
    review_period: "P90D"
    basis_ref: "[jawne uzasadnienie lub indeks]"
  sufficiency_band:
    lower: 0.9
    upper: 1.1
  reward_curve:
    type: "piecewise_sublinear"
    parameters: {}
  universal_basic_compute:
    enabled: true
    eligibility_basis: "proof_of_personhood"
    non_withdrawable: true
    guaranteed_modes:
      - "emergency"
      - "care"
    funding_sources:
      - "business_nodes"
      - "high_margin_instances"
      - "surplus_recirculation"
      - "voluntary_operator_surplus"
  surplus_policy:
    destination_classes:
      - "basic_survival_floor"
      - "bootstrap"
      - "weaker_links"
      - "temporary_harm"
      - "infrastructure"
    allocation_rule: "[jawna reguła lub formuła]"
    settlement_period: "P30D"
  conversion_barriers:
    governance_weight_from_rewards: false
    privileged_routing_from_rewards: false
    exception_access_from_rewards: false
    oracle_power_from_rewards: false
  audit_metrics:
    - "top_1_share"
    - "top_5_share"
    - "surplus_recirculation_rate"
    - "coverage_ratio"
    - "infrastructure_share"
```

Brak jawnego `swarm_economy_policy` oznacza, że federacja nie spełnia minimalnego
standardu dla mechanizmów wymienialnych lub quasi-wymienialnych.

---

## 5. Próg dostatku

### 5.1. Test zgodności

Próg dostatku MUSI przejść jednocześnie trzy testy:

1. **Test utrzymania**: próg wystarcza do bezpiecznego i stabilnego utrzymania
   węzła oraz jego operatora w trybie zwykłego działania.
2. **Test nie-dominacji**: próg nie może być ustawiony tak wysoko, by de facto
   wyłączał hamulce koncentracji dla małej liczby uprzywilejowanych podmiotów.
3. **Test jawności**: sposób wyznaczenia progu da się opisać, przeliczyć i
   zakwestionować proceduralnie.

### 5.2. Reguły minimalne

1. Próg dostatku MUSI być przeglądany okresowo.
2. Zmiana progu dostatku MUSI pozostawiać ślad decyzji, uzasadnienie i datę wejścia
   w życie.
3. Federacja może stosować różne profile kosztowe dla różnych klas węzłów, ale nie
   może używać ich do ukrytego premiowania własnych operatorów lub ról zaufania.

---

## 6. Krzywe wynagradzania i hamulce koncentracji

### 6.1. Dopuszczalne klasy mechanizmów

Po przekroczeniu `sufficiency_threshold` federacja MUSI stosować co najmniej jedną z
poniższych klas ograniczeń:

1. malejące przyrosty (`sublinear`),
2. pasmo wygaszania (`tapered plateau`),
3. twardy limit z przekierowaniem nadwyżki,
4. hybrydę powyższych.

### 6.2. Niedopuszczalne klasy mechanizmów

Niedopuszczalne są mechanizmy, które:

1. zachowują liniowy lub nadliniowy wzrost bez końca,
2. wynagradzają głównie za samą pozycję wejścia w czasie,
3. zwiększają siłę nagrody szybciej niż rośnie audytowalny wkład,
4. ukrywają koncentrację przez boczne kanały lub niejawne klasy benefitów.

### 6.3. Test anty-piramidowy

Mechanizm ekonomiczny NIE przechodzi testu konstytucyjnego, jeżeli spełnia
którykolwiek z warunków:

1. dominująca część wypłat dla wcześniejszych uczestników pochodzi z napływu nowych
   uczestników, a nie z audytowalnego użycia lub wartości,
2. starszeństwo samo przez się generuje trwały bonus bez wygasania,
3. utrata napływu nowych uczestników powoduje strukturalne załamanie wypłat
   podstawowych.

---

## 7. Wspólny obieg nadwyżek

### 7.1. Klasy przeznaczenia

Co najmniej następujące klasy MUSZĄ być obsługiwane przez `surplus_policy`:

1. `basic_survival_floor` - minimalny przydział dla zweryfikowanych osób bez
   wystarczającego bieżącego wkładu reputacyjnego lub ekonomicznego,
2. `bootstrap` - nowe węzły i wejście do ekosystemu,
3. `weaker_links` - węzły o niższej zdolności operacyjnej,
4. `temporary_harm` - węzły lub operatorzy czasowo poszkodowani,
5. `infrastructure` - funkcje o wysokiej wartości wspólnotowej.

Federacja może dodać inne klasy, ale nie może usunąć wszystkich klas ochronnych i
infrastrukturalnych jednocześnie.

### 7.2. Reguły minimalne redystrybucji

1. Nadwyżka MUSI być rozliczana okresowo, nie ad hoc według sympatii.
2. Reguła podziału MUSI być jawna albo wyrażona jako jawny algorytm.
3. Środki przeznaczone do wspólnego obiegu nie mogą wracać w tej samej rundzie do
   źródłowego beneficjenta przez ukryty kanał.
4. Redystrybucja MUSI pozostawiać ślad audytowy per okres.

### 7.3. Minimalny rekord rozliczenia

```yaml
surplus_settlement:
  settlement_id: "[unikalny identyfikator]"
  federation_id: "[federacja]"
  period_start: "[timestamp]"
  period_end: "[timestamp]"
  source_node_id: "[węzeł źródłowy]"
  gross_reward: 0
  retained_reward: 0
  surplus_amount: 0
  destination_class: "bootstrap"
  destination_ref: "[fundusz / pula / odbiorca]"
  policy_ref: "DIA-SUFF-001"
  created_at: "[timestamp]"
```

---

## 8. Bariera konwersji na władzę ustrojową

1. Saldo tokenów, kredytów lub innych nagród ekonomicznych nie może być bezpośrednim
   wejściem do obliczania wagi głosu, kwalifikowalności panelowej, siły wyroczni ani
   prawa do wyjątków.
2. Federacja nie może sprzedawać ani przyznawać za nagrodę ekonomiczną skrótów do
   ról zaufania publicznego.
3. Jeżeli system używa jednocześnie nagród ekonomicznych i reputacji, ścieżki
   naliczania MUSZĄ być rozdzielone i audytowalne.
4. Każda próba obejścia bariery konwersji przez benefit pośredni podlega ocenie jak
   naruszenie konstytucyjne, a nie jak zwykła optymalizacja ekonomiczna.

---

## 9. Metryki zdrowia federacyjnego

Federacja uruchamiająca ekonomię nagród MUSI mierzyć co najmniej:

- `top_1_share` - udział największego beneficjenta w całości wypłat,
- `top_5_share` - udział pięciu największych beneficjentów,
- `surplus_recirculation_rate` - odsetek nadwyżki, który faktycznie wrócił do
  wspólnego obiegu,
- `coverage_ratio` - odsetek aktywnych węzłów, które osiągają minimalny poziom
  utrzymania,
- `infrastructure_share` - udział redystrybucji przeznaczony na funkcje
  infrastrukturalne,
- `new_node_support_rate` - udział nowych węzłów objętych wsparciem bootstrapowym.

Trwały wzrost koncentracji przy niskim `surplus_recirculation_rate` jest sygnałem
patologii ustrojowej i powinien uruchamiać przegląd polityki ekonomicznej.

---

## 10. Wyjątki i relacja do innych dokumentów

1. Obejście hamulców koncentracji może nastąpić wyłącznie przez wyjątek zgodny z
   `EXCEPTION-POLICY.pl.md`.
2. Wyjątek nie może znosić bariery konwersji nagrody ekonomicznej na władzę
   proceduralną.
3. Każdy wyjątek dotyczący progu dostatku lub redystrybucji MUSI wskazywać:
   `reason`, `expiry`, `owner`, `risk-level` oraz metryki skutków ubocznych.

Relacje dokumentowe:

- **Konstytucja Art. VIII.4**: zakaz ekonomii typu piramidalnego i zakaz zamiany
  przewagi ekonomicznej na władzę.
- **Konstytucja Art. XII.6-13**: wymiana kontraktowa jako dopuszczalny tryb
  wzajemności, cel ekonomii, hamulce koncentracji, wspólny obieg nadwyżek i
  bariera konwersji.
- **`EXCEPTION-POLICY.pl.md`**: procedura wyjątków dla odstępstw czasowych.
- **`PROCEDURAL-REPUTATION-SPEC.pl.md`**: rozdział reputacji proceduralnej od nagrody
  ekonomicznej.
