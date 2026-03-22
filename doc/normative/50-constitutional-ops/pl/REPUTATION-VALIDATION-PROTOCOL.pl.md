# Protokół walidacji mechanizmów reputacyjnych DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-REP-VALID-001` |
| `typ` | Ustawa wykonawcza (Poziom 3 hierarchii normatywnej) |
| `wersja` | 0.1.0-draft |
| `podstawa` | Art. VII.4-5, Art. XIV Konstytucji; `doc/normative/30-core-values/pl/CORE-VALUES.pl.md` sekcja "Reputacja jako dźwignia, nie władza" |
| `status mechanizmów` | `[mechanizm - hipoteza]` zgodnie z `NORMATIVE-HIERARCHY.pl.md` |

---

## 1. Cel dokumentu

Mechanizmy reputacyjne opisane w `doc/normative/30-core-values/pl/CORE-VALUES.pl.md` - ważony głos,
spływające punkty uznania, krzywe podliniowe (ang. sublinear), detekcja karteli,
domniemanie konfliktu interesów przy braku danych (COI-by-default) - są
**hipotezami architektonicznymi**. Żaden z nich nie został zweryfikowany empirycznie
w środowisku zbliżonym do DIA.

Niniejszy protokół definiuje:

- klauzulę eksperymentalną dla mechanizmów reputacyjnych,
- metryki zdrowia, które muszą być mierzone,
- progi alarmowe i mechanizm bezpiecznika proceduralnego (ang. circuit breaker),
- minimalny przebieg walidacji.

Celem nie jest blokowanie wdrożenia, lecz **zaprojektowanie drogi od hipotezy do normy
z zachowaniem bezpieczeństwa**.

---

## 2. Klauzula eksperymentalna

Propozycja zapisu do umieszczenia w Art. VII Konstytucji lub w preambule sekcji
reputacyjnej `doc/normative/30-core-values/pl/CORE-VALUES.pl.md`:

> Mechanizmy reputacyjne opisane w niniejszym dokumencie, w szczególności: ważony głos
> w rozstrzygnięciach, spływające punkty uznania, krzywe podliniowe (ang.
> sublinear) przyrostów,
> detekcja karteli i asymetria ryzyka reputacyjnego, mają status **hipotez
> architektonicznych**. Przed nadaniem im mocy normatywnej wymagają walidacji
> empirycznej w co najmniej dwóch niezależnych federacjach przez okres nie krótszy niż
> 6 miesięcy, z pomiarem metryk zdrowia zdefiniowanych w niniejszym protokole. Do
> czasu pomyślnej walidacji federacja może wdrożyć mechanizmy w trybie
> eksperymentalnym z obowiązkowym bezpiecznikiem proceduralnym (ang. circuit
> breaker).

---

## 3. Metryki zdrowia reputacji

### 3.1. Metryki podstawowe (obowiązkowe)

Każda federacja wdrażająca mechanizmy reputacyjne MUSI mierzyć i raportować
następujące metryki w cyklach nie dłuższych niż 30 dni.

#### M1: Współczynnik koncentracji reputacji (Gini)

| Parametr | Wartość |
| :--- | :--- |
| **Co mierzy** | Czy rozkład reputacji tworzy oligarchię |
| **Definicja** | Współczynnik Gini'ego rozkładu zagregowanej reputacji wszystkich aktywnych węzłów w federacji |
| **Próg alarmowy** | Gini > 0.65 |
| **Próg bezpiecznika proceduralnego** | Gini > 0.80 |
| **Częstotliwość pomiaru** | Co 7 dni (okno kroczące 30 dni) |

#### M2: Czas do progu wpływu

| Parametr | Wartość |
| :--- | :--- |
| **Co mierzy** | Czy bariera wejścia rośnie w czasie (ossifikacja) |
| **Definicja** | Mediana czasu (w dniach) od pierwszego wkładu nowego węzła do osiągnięcia progu, przy którym węzeł uzyskuje ważony głos (A1 reputacji) |
| **Próg alarmowy** | Wzrost > 50% względem mediany z pierwszego kwartału walidacji |
| **Próg bezpiecznika proceduralnego** | Wzrost > 100% (podwojenie) |
| **Częstotliwość pomiaru** | Co 30 dni |

#### M3: Wskaźnik detekcji karteli

| Parametr | Wartość |
| :--- | :--- |
| **Co mierzy** | Skuteczność systemu antykartelowego |
| **Definicja** | Stosunek wykrytych wzorców kartelowych (wzajemne podbijanie, spływanie w zamkniętych grupach) do łącznej liczby transakcji reputacyjnych |
| **Próg alarmowy** | > 5% transakcji flagowanych jako kartelowe |
| **Próg bezpiecznika proceduralnego** | > 15% transakcji flagowanych LUB wzrost > 3x w jednym cyklu pomiarowym |
| **Częstotliwość pomiaru** | Co 7 dni |

#### M4: Korelacja reputacja-jakość decyzji

| Parametr | Wartość |
| :--- | :--- |
| **Co mierzy** | Czy dźwignia reputacyjna jest uzasadniona jakością |
| **Definicja** | Korelacja Spearmana między rangą reputacyjną węzła a jakością jego decyzji mierzoną przez wyrocznie (trafność predykcji, dotrzymanie kontraktów, jakość aktualizacji) |
| **Próg alarmowy** | ρ < 0.3 (słaba korelacja: reputacja nie odzwierciedla jakości) |
| **Próg bezpiecznika proceduralnego** | ρ < 0.1 lub ρ < 0 (reputacja jest antysygnałem jakości) |
| **Częstotliwość pomiaru** | Co 30 dni (wymaga danych z wyroczni) |

#### M5: Wskaźnik rotacji w górnej warstwie reputacyjnej

| Parametr | Wartość |
| :--- | :--- |
| **Co mierzy** | Czy górna warstwa jest zamrożona (oligarchia) czy dynamiczna |
| **Definicja** | Odsetek węzłów w górnym decylu reputacji, które w ciągu ostatnich 90 dni weszły do tego decyla lub z niego wypadły |
| **Próg alarmowy** | Rotacja < 10% (zamrożenie) |
| **Próg bezpiecznika proceduralnego** | Rotacja < 5% przez dwa kolejne cykle |
| **Częstotliwość pomiaru** | Co 30 dni |

### 3.2. Metryki dodatkowe (zalecane)

- **M6: Odsetek decyzji z deklaracją COI** - mierzy, czy zasada domniemania
  konfliktu interesów przy braku danych (COI-by-default)
  jest faktycznie stosowana. Próg alarmowy: < 20% decyzji ważonych z jakąkolwiek
  deklaracją COI (sugeruje, że mechanizm jest martwy).

- **M7: Entropia rozkładu źródeł spływającej reputacji** - mierzy, czy punkty uznania
  pochodzą z wielu źródeł, czy z kilku dominujących. Niska entropia oznacza ryzyko
  kliki.

- **M8: Czas powrotu po utracie reputacji** - mierzy, czy system pozwala na naprawę
  i reintegrację (Art. XVI.4), czy kary są de facto permanentne.

---

## 4. Bezpiecznik proceduralny (ang. circuit breaker)

### 4.1. Definicja

Bezpiecznik proceduralny (ang. circuit breaker) to **automatyczny mechanizm
bezpieczeństwa**, który wyłącza dźwignię reputacyjną i przywraca równy głos, gdy
metryki zdrowia przekraczają zdefiniowane progi.

### 4.2. Zasada działania

```text
Stan normalny: dźwignia reputacyjna aktywna
       ->
Metryka przekracza próg alarmowy
       ->
[ALARM] -> raport do operatorów federacji + wpis w logu
       -> (jeśli brak korekty w ciągu 14 dni LUB próg bezpiecznika proceduralnego)
       ->
[CIRCUIT BREAK] -> automatyczne wyłączenie dźwigni reputacyjnej
       ->
Federacja wraca do RÓWNEGO GŁOSU dla wszystkich węzłów
       ->
Analiza przyczyn, korekta parametrów, ponowna walidacja
       ->
Reaktywacja dźwigni (wymaga jawnej decyzji dotyczącej ładu organizacyjnego (ang. governance) ze współpodpisem (ang. multisig))
```

### 4.3. Warunki bezpiecznika proceduralnego

Bezpiecznik proceduralny aktywuje się automatycznie, gdy **dowolna** z poniższych
sytuacji wystąpi:

1. Którakolwiek metryka podstawowa (M1-M5) przekracza próg bezpiecznika proceduralnego.
2. Dwie lub więcej metryk podstawowych jednocześnie przekraczają próg alarmowy.
3. Metryka M4 (korelacja reputacja-jakość) spada poniżej 0 (reputacja jest
   antysygnałem).

### 4.4. Skutki bezpiecznika proceduralnego

- Ważony głos w rozstrzygnięciach -> równy głos (1 węzeł = 1 głos).
- Spływające punkty uznania -> wyłączone (nagrody bez dopłaty systemowej).
- Reputacja jest nadal mierzona i wyświetlana, ale **nie ma mocy operacyjnej**.
- Stan zadziałania bezpiecznika proceduralnego (ang. circuit break) jest logowany i
  publicznie widoczny.

### 4.5. Reaktywacja

Reaktywacja dźwigni reputacyjnej po zadziałaniu bezpiecznika proceduralnego wymaga:

1. Identyfikacji przyczyny przekroczenia progu.
2. Korekty parametrów mechanizmu.
3. Ponownej walidacji przez co najmniej 30 dni z metrykami poniżej progów alarmowych.
4. Jawnej decyzji dotyczącej ładu organizacyjnego (ang. governance) ze
   współpodpisem (ang. multisig) (Art. VII.9).

---

## 5. Przebieg walidacji

### 5.1. Faza 0: Symulacja (przed wdrożeniem)

- Symulacja mechanizmów reputacyjnych na danych syntetycznych i/lub historycznych.
- Testowanie scenariuszy: Sybil, kartele, ossyfikacja, masowy napływ nowych węzłów.
- Kalibracja wstępna progów i parametrów.
- Czas trwania: zależny od dostępności danych, minimum 30 dni.

### 5.2. Faza 1: Tryb cienia (ang. shadow mode; wdrożenie bez mocy operacyjnej)

- Mechanizmy reputacyjne działają równolegle do systemu równego głosu.
- Reputacja jest mierzona, ale **nie wpływa na decyzje**.
- Metryki zdrowia są zbierane i raportowane.
- Czas trwania: minimum 3 miesiące w co najmniej jednej federacji.
- Kryterium przejścia: wszystkie metryki podstawowe poniżej progów alarmowych przez
  cały okres.

### 5.3. Faza 2: Pilot z bezpiecznikiem proceduralnym (ang. circuit breaker;
ograniczone wdrożenie)

- Dźwignia reputacyjna jest aktywowana w co najmniej dwóch niezależnych federacjach.
- Bezpiecznik proceduralny jest aktywny.
- Metryki zdrowia są monitorowane w cyklach 7-dniowych.
- Czas trwania: minimum 6 miesięcy.
- Kryterium przejścia: brak aktywacji bezpiecznika proceduralnego, wszystkie metryki poniżej
  progów alarmowych przez >=80% okresu.

### 5.4. Faza 3: Walidacja i formalizacja

Po pomyślnym przejściu Fazy 2:

1. Publikacja raportu walidacyjnego (dane, metryki, anomalie, wnioski).
2. Kontradyktoryjny przegląd (ang. adversarial review) raportu przez niezależny
   zespół kontrtestujący (ang. red-team).
3. Propozycja formalizacji: zmiana statusu mechanizmów z `[mechanizm - hipoteza]`
   na `[mechanizm - zwalidowany]` w `doc/normative/30-core-values/pl/CORE-VALUES.pl.md`.
4. Decyzja federacji o formalnym przyjęciu (procedura z Art. XVI dla zmian o
   średniej stawce).

---

## 6. Parametry konfigurowalne na poziomie federacji

Poniższe parametry są **domyślne** i mogą być zmieniane przez federację w ramach
polityk federacyjnych (Poziom 4 hierarchii normatywnej). Federacja **nie może**
wyłączyć bezpiecznika proceduralnego (ang. circuit breaker) ani podwyższyć progów
powyżej wartości domyślnych.

| Parametr | Wartość domyślna | Zakres dopuszczalny |
| :--- | :--- | :--- |
| `gini_alarm_threshold` | 0.65 | <= 0.65 |
| `gini_breaker_threshold` | 0.80 | <= 0.80 |
| `time_to_influence_alarm_pct` | 50% wzrost | <= 50% |
| `cartel_alarm_pct` | 5% | <= 5% |
| `correlation_alarm_rho` | 0.3 | >= 0.3 |
| `top_decile_rotation_alarm` | 10% | >= 10% |
| `shadow_mode_min_months` | 3 | >= 3 |
| `pilot_min_months` | 6 | >= 6 |
| `pilot_min_federations` | 2 | >= 2 |
| `measurement_cycle_days` | 7 | <= 7 |

Interpretacja: federacja może być **ostrożniejsza** (niższe progi, dłuższa walidacja),
ale nie **łagodniejsza** niż wartości domyślne.

---

## 7. Relacja z innymi dokumentami

- **Konstytucja Art. VII.4-5**: Niniejszy protokół operacjonalizuje zasadę, że
  reputacja jest zabezpieczeniem, nie statusem.
- **`doc/normative/30-core-values/pl/CORE-VALUES.pl.md` - "Reputacja jako dźwignia, nie władza"**:
  źródło mechanizmów poddawanych walidacji. Po pomyślnej walidacji sekcja zmienia
  status z `[mechanizm - hipoteza]` na `[mechanizm - zwalidowany]`.
- **`NORMATIVE-HIERARCHY.pl.md`**: Wyjaśnia, dlaczego mechanizmy z core values nie mają
  automatycznie mocy normatywnej.
- **`ENTRENCHMENT-CLAUSE.pl.md`**: Jeśli zwalidowany mechanizm reputacyjny zacznie
  naruszać rdzeń nienegocjowalny (np. godność, prawo do wyjścia), podlega zarzutowi
  niekonstytucyjności.
- **`AUTONOMY-LEVELS.pl.md`**: Głosowanie reputacyjne wymaga poziomu autonomii A0
  (propozycja i zatwierdzenie przez człowieka).
