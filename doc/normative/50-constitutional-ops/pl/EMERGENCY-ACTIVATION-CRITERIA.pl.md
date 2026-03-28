# Kryteria aktywacji awaryjnej DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-EMRG-ACT-001` |
| `typ` | Ustawa wykonawcza (Poziom 3 hierarchii normatywnej) |
| `wersja` | `0.1.0-draft` |
| `podstawa` | Art. II.2, II.8, IX.3-5, V.10, V.13 Konstytucji DIA; `AUTONOMY-LEVELS.pl.md` (A3); `EXCEPTION-POLICY.pl.md` (sekcja 4.2) |
| `status mechanizmu` | `[mechanism - hypothesis]` dla progów oceny wiarygodności; taksonomia triggerów i pipeline są normatywne |

---

## 1. Cel dokumentu

Konstytucja dopuszcza działanie awaryjne, gdy istnieje bezpośrednie zagrożenie
życia albo nagła poważna szkoda (Art. II.8). `AUTONOMY-LEVELS.pl.md`
definiuje A3 (Tryb Awaryjny) jako najwyższy poziom autonomii agentów.
`EXCEPTION-POLICY.pl.md` definiuje typ wyjątku awaryjnego. Brakowało jednak
specyfikacji:

- co uruchamia aktywację awaryjną,
- jak oceniane są sygnały,
- jakie zabezpieczenia ograniczają nadużycia.

Dokument definiuje:

- klasy triggerów i ich zakres,
- poziomy wiarygodności sygnału i reguły oceny,
- pipeline `sensorium -> operator`,
- ścieżki aktywacji ręcznej i automatycznej,
- limity czasu i zasady przedłużania,
- obowiązkową rewizję pokryzysową,
- klasyfikację fałszywych alarmów i odpowiedzialność,
- reguły kryzysów kaskadowych,
- timeout operatora i eskalację.

---

## 2. Zasady projektowe

1. **A3 przyspiesza, ale nie tworzy nowych uprawnień**. Tryb awaryjny pozwala
   działać szybciej w ramach już istniejących uprawnień; nie daje uprawnień,
   których nie ma kontrakt agenta (Art. V.10, V.13).

2. **Domyślnie fail-closed**. Wygaśnięcie każdego limitu czasu przywraca system
   do A0. Przedłużenie trybu awaryjnego wymaga świeżych dowodów i jawnej decyzji.

3. **Pełny ślad, bez wyjątków**. Każde działanie podjęte w A3 generuje
   niezredagowany trace (`AUTONOMY-LEVELS`, sekcja 5.1). Ślad jest ceną za szybkość.

4. **Obowiązkowa rewizja**. Każda aktywacja A3 przechodzi rewizję pokryzysową
   (`AUTONOMY-LEVELS`, sekcja 5.3). Wyniki rewizji wracają jako sygnały reputacyjne.

5. **TC5 jest metaklasą, nie bezpośrednim aktywatorem**. Kryzys epistemiczny
   (`TC5`) nie może samodzielnie aktywować A3. Uruchamia wzmożony monitoring
   i alerty operatorskie. A3 wymaga manifestacji przez `TC1-TC4`.

6. **Proporcjonalność**. Reakcja MUSI być proporcjonalna do zagrożenia.
   Uprawnienia awaryjne nie są skrótem dla wygody ani przewagi politycznej.

---

## 3. Klasy triggerów

### 3.1. Taksonomia

| Klasa | Nazwa | Zakres | Przykłady | Podstawa konstytucyjna |
| :--- | :--- | :--- | :--- | :--- |
| `TC1` | Bezpośrednie zagrożenie życia | Bezpośrednie, osobiste zagrożenie | Przemoc, ryzyko samobójcze, ostry stan medyczny, sytuacja zakładnicza | Art. II.2, II.8 |
| `TC2` | Kryzys infrastrukturalny | Systemowa awaria infrastruktury krytycznej | Blackout, załamanie sieci, awaria krytycznego systemu, kompromitacja klucza, w tym `council:did:key` | Art. IX.3-5, IV.7 |
| `TC3` | Kryzys zdrowotny | Zagrożenie zdrowia w skali zbiorowej | Epidemia, zatrucie, skażenie środowiskowe, kontaminacja | Art. II.2, IX.7 |
| `TC4` | Prześladowanie lub przemoc ukierunkowana | Atak na osoby przez system albo przeciw systemowi | Atak ukierunkowany, doxxing, prześladowanie polityczne, odwet wobec sygnalisty, stalking | Art. X.1-3, II.11 |
| `TC5` | Kryzys epistemiczny (metaklasa) | Degradacja zdolności systemu do odróżniania sygnału od szumu | Kampania dezinformacyjna, zatrucie oracli, skażenie źródeł, skoordynowana manipulacja narracyjna | Art. XI.1, XI.7-8 |

### 3.2. TC5 — zasady szczególne

`TC5` jest **metaklasą kryzysu**. Opisuje sytuację, w której infrastruktura
epistemiczna systemu jest naruszona: oracla produkują niewiarygodne wyniki,
sygnały są zatrute lub skoordynowana manipulacja zniekształca środowisko
informacyjne.

**Samo `TC5` NIE MOŻE aktywować A3.** Uzasadnienie:

- A3 jest przeznaczone dla sytuacji **bezpośredniej, nagłej szkody** (Art. II.8).
  Kryzys epistemiczny jest zwykle stopniowy i rozlany.
- Przyznanie A3 na podstawie tezy „system nie odróżnia prawdy od szumu”
  tworzy paradoks: mechanizm oceniający zasadność A3 jest sam naruszony.
- Historia pokazuje, że framing „epistemicznego stanu wyjątkowego” jest
  wektorem autorytarnego nadużycia.

**TC5 aktywuje:**

1. **Wzmożony monitoring** — wszystkie sygnały z `sensorium` są tagowane
   zwiększoną niepewnością; automatyczna ocena wiarygodności przechodzi w tryb
   `degraded_trust`.
2. **Alert operatorski** — wszyscy operatorzy federacji otrzymują jawny alert
   z klasyfikacją `TC5` i materiałem wspierającym.
3. **Wstępną kwalifikację sygnału** — sygnały, które normalnie mogłyby
   autoaktywować się przy `C3+` (sekcja 4), wymagają ręcznego potwierdzenia
   operatora, gdy `TC5` jest aktywne.
4. **Kwarantannę oracli** — oracla oznaczone jako potencjalnie skompromitowane
   są odseparowywane: ich wyniki nadal się zbiera, ale wyłącza z automatycznych
   ścieżek decyzyjnych.

**Eskalacja `TC5` do A3** zachodzi wyłącznie wtedy, gdy kryzys epistemiczny
**manifestuje się przez** `TC1-TC4`. Przykład: zatrucie oracla (`TC5`)
prowadzi do awarii routingu izolującej węzeł pod aktywnym zagrożeniem (`TC4`) —
A3 aktywuje manifestacja `TC4`, nie samo `TC5`.

### 3.3. Kompromitacja klucza council (`TC2` subclass)

Kompromitacja `council:did:key` (zgodnie z protokołem nymów) jest podklasą
`TC2` i niesie szczególne konsekwencje:

1. **Zamrożenie trapdooru** — trapdoor mapujący `nym -> participant` zostaje
   natychmiast zamrożony. Nie wolno obsługiwać nowych wniosków
   deanonymizacyjnych do czasu wyjaśnienia kompromitacji.
2. **Awaryjna rotacja klucza** — generowany i dystrybuowany jest nowy
   `council:did:key`. Istniejące certyfikaty nymów zachowują ważność do końca
   swojego TTL, ale nie mogą być odnawiane kluczem skompromitowanym.
3. **Panel audytowy ad-hoc** — panel złożony zgodnie z
   `PANEL-SELECTION-PROTOCOL` bada zakres kompromitacji: które bindingi mogły
   zostać ujawnione, jakie operacje trapdoorowe wykonano oraz czy doszło do
   nieautoryzowanej deanonymizacji.
4. **Ciągłość linii nymów** — uczestnicy mogą wnosić o przyspieszone odnowienie
   nymów przy użyciu nowego klucza council. `Leniency window` istniejących
   certyfikatów zapewnia ciągłość przejścia.

Ta podklasa spina infrastrukturę tożsamości (`GENYM`) z konstytucyjną ramą kryzysową.

---

## 4. Poziomy wiarygodności sygnału `[hypothesis]`

Każdy sygnał wchodzący do pipeline’u awaryjnego jest oceniany pod względem
wiarygodności, zanim uruchomi jakąkolwiek ścieżkę aktywacji.

### 4.1. Skala wiarygodności

| Poziom | Nazwa | Definicja | Minimum dowodowe |
| :--- | :--- | :--- | :--- |
| `C0` | Szum | Sygnał nieweryfikowalny lub wewnętrznie niespójny | — |
| `C1` | Pojedyncze źródło | Jedno źródło, brak corroboration | Jeden sygnał z jednego sensora/zgłaszającego |
| `C2` | Uprawdopodobniony | Dwa niezależne źródła albo jedno źródło z kontekstem wspierającym | Dwa sygnały z różnych operatorów/źródeł albo jeden sygnał + zgodny kontekst |
| `C3` | Wysoka wiarygodność | Trzy niezależne źródła albo dwa + artefakt materialny | Trzy sygnały albo dwa + audytowalny artefakt |
| `C4` | Przeważająca wiarygodność | Wiele zbieżnych źródeł wraz z materiałem dowodowym | Wieloźródłowy materiał audytowalny spójny w czasie i autorstwie |

### 4.2. Reguły aktywacji według wiarygodności

| Wiarygodność | Ścieżka aktywacji | Ograniczenia |
| :--- | :--- | :--- |
| `C0` | Brak aktywacji | Sygnał jest tylko logowany |
| `C1` | Wyłącznie ręczna | Operator dostaje alert; brak reakcji automatycznej |
| `C2` | Ręczna z rekomendacją systemu | System pokazuje klasyfikację i sugerowaną reakcję; decyzję podejmuje operator |
| `C3` | Automatyczna dopuszczalna dla `TC1`, `TC2`, `TC4` | Autoaktywacja z natychmiastowym powiadomieniem operatora; operator może nadpisać w `operator_override_window` (domyślnie 5 min) |
| `C4` | Automatyczna dla `TC1-TC4` | Autoaktywacja z rozszerzonym trace; rewizja post-hoc obowiązkowa w 24h |

**Wyjątek `TC5`:** niezależnie od wiarygodności `TC5` nigdy nie aktywuje A3
automatycznie. Przy `C3+` uruchamia automatyczny alert i wzmożony monitoring,
ale A3 wymaga manifestacji przez `TC1-TC4`.

### 4.3. Wymogi niezależności źródeł

Aby sygnał liczył się jako „niezależny” dla oceny wiarygodności:

1. źródła MUSZĄ być obsługiwane przez **różnych operatorów**
   (odrębne `node:did:key` z odrębną tożsamością operatorską),
2. źródła MUSZĄ pochodzić z **różnych torów danych** (nie mogą być lustrami
   tego samego upstreamu),
3. bliskość czasowa (sygnały w obrębie `correlation_window`, domyślnie 15 min)
   jest traktowana jako corroboration, nie niezależność, chyba że źródła mogą
   wykazać niezależne ścieżki przyczynowe.

---

## 5. Pipeline awaryjny

### 5.1. Architektura

```
┌─ Etap 1: Ingest ─────────────────────────────────────────┐
│  Connectory sensorium -> surowe sygnały z metadanymi    │
│  (source, timestamp, type, confidence, evidence_ref)    │
├─ Etap 2: Ewaluacja ─────────────────────────────────────┤
│  Klasyfikacja (TC1-TC5)                                 │
│  Corroboration (między źródłami, czasowa, kontekstowa)  │
│  Scoring wiarygodności (C0-C4)                          │
│  Sprawdzenie TC5 degraded-trust                         │
├─ Etap 3: Decyzja ───────────────────────────────────────┤
│  IF C0: tylko log                                       │
│  IF C1: alert operatora                                 │
│  IF C2: alert + rekomendacja                            │
│  IF C3+ AND auto-eligible: aktywuj + powiadom operatora │
│  IF C3+ AND NOT auto-eligible: alert + wymagaj operatora│
│  Utwórz rekord wyjątku (model EXCEPTION-POLICY)         │
│  Uruchom odliczanie TTL                                 │
├─ Etap 4: Odpowiedź aktywna ─────────────────────────────┤
│  Agent działa w A3 w granicach kontraktu                │
│  Pełny trace dla każdej akcji                           │
│  TTL monitorowany; przedłużenie wymaga świeżych dowodów │
├─ Etap 5: Dezaktywacja ──────────────────────────────────┤
│  TTL wygasa ALBO operator wyłącza ALBO zagrożenie znika │
│  System wraca do A0 (fail-closed)                       │
│  Zaczyna biec zegar rewizji pokryzysowej (72h)          │
└─────────────────────────────────────────────────────────┘
```

### 5.2. Model danych sygnału

```yaml
emergency_signal:
  signal_id: "[unikalny identyfikator]"
  source_node_id: "[node:did:key węzła zgłaszającego]"
  source_type: "sensorium"    # sensorium | operator | peer_report | oracle
  timestamp: "[ISO 8601]"
  trigger_class: "TC1"        # TC1 | TC2 | TC3 | TC4 | TC5
  description: "[czytelne podsumowanie]"
  evidence_ref: "[odnośnik do audytowalnych dowodów]"
  confidence: "C2"            # C0 | C1 | C2 | C3 | C4
  corroborating_signals: []   # lista signal_id
  tc5_active: false           # czy działa tryb degraded_trust
  metadata:
    geo_hint: "[opcjonalna lokalizacja zgrubna]"
    affected_scope: "[node | federation | inter-federation]"
    urgency: "immediate"      # immediate | hours | days
```

### 5.3. Rekord aktywacji

Każda aktywacja awaryjna tworzy rekord wyjątku zgodnie z
`EXCEPTION-POLICY.pl.md`, z dodatkowymi polami:

```yaml
emergency_activation:
  exception_id: "EXC-[federation]-[timestamp]-[nonce]"
  type: "emergency"
  trigger_class: "TC1"
  trigger_signals: ["sig_001", "sig_002"]
  credibility: "C3"
  activation_path: "automatic"    # automatic | manual
  activated_by: "[node:did:key operatora lub 'system']"
  activated_at: "[ISO 8601]"
  ttl_expires_at: "[ISO 8601]"
  max_extension_until: "[ISO 8601]"
  extensions: []
  agents_elevated: ["[agent_id:A3]"]
  scope: "[opis zakresu aktywacji]"
  fail_closed_target: "A0"
  deactivated_at: null
  deactivation_reason: null
  review_due_at: null           # ustawiane przy deaktywacji: deactivated_at + 72h
  review_status: "pending"      # pending | in_progress | completed
```

---

## 6. Limity czasu

### 6.1. Domyślne TTL według klasy triggera

| Klasa | TTL początkowe | Maksymalne przedłużenie | Wymóg przedłużenia |
| :--- | :--- | :--- | :--- |
| `TC1` | 4 godziny | 24 godziny | Operator + świeże dowody |
| `TC2` | 12 godzin | 48 godzin | Operator + raport statusu |
| `TC3` | 24 godziny | 72 godziny | Operator + świeże dowody |
| `TC4` | 8 godzin | 48 godzin | Operator + świeże dowody |
| `TC5` (tylko alert, bez A3) | 24 godziny | 72 godziny | Operator + niezależne corroboration |

### 6.2. Zasady przedłużania

1. Każde przedłużenie MUSI tworzyć nowy wpis w tablicy `extensions` rekordu
   aktywacji, zawierający:
   - `extended_by`: tożsamość operatora,
   - `extended_at`: timestamp,
   - `new_expires_at`: nowa data wygaśnięcia,
   - `justification`: uzasadnienie ze wskazaniem świeżych dowodów,
   - `evidence_refs`: odwołania do nowych dowodów.

2. Przedłużenia ponad `max_extension` są **zakazane**. Jeżeli zagrożenie trwa,
   rozpoczyna się nowy cykl aktywacji z nowym rekordem wyjątku i świeżą oceną
   dowodów. To ogranicza stan „wiecznego trybu awaryjnego”.

3. Wartości `max_extension` są **sufitem absolutnym**, nie kumulacją. Aktywacja
   `TC1` z TTL 4h może zostać przedłużona maksymalnie do 24h łącznego czasu,
   nie do `4h + 24h`.

### 6.3. Powrót fail-closed

Gdy TTL wygasa bez przedłużenia:

1. wszyscy agenci podniesieni do A3 wracają do **A0** (`Propose & Wait`),
2. rekord aktywacji dostaje `deactivated_at` z powodem `ttl_expired`,
3. zaczyna biec zegar rewizji pokryzysowej (72h),
4. jeżeli zagrożenie nadal istnieje, operator MUSI rozpocząć nowy cykl
   aktywacji na podstawie świeżych dowodów.

---

## 7. Timeout operatora i eskalacja

Gdy sygnał wymaga ręcznej reakcji operatora (`C1-C2` albo `C3+` dla klas
niedopuszczonych do autoaktywacji):

### 7.1. Progi timeoutu

| Klasa triggera | Okno reakcji operatora | Cel eskalacji |
| :--- | :--- | :--- |
| `TC1` | 15 minut | Federacyjny operator awaryjny |
| `TC2` | 30 minut | Federacyjny operator awaryjny |
| `TC3` | 30 minut | Federacyjny operator awaryjny |
| `TC4` | 15 minut | Federacyjny operator awaryjny |
| `TC5` | 60 minut | Federacyjny kontakt governance |

### 7.2. Łańcuch eskalacji

1. **Operator główny** otrzymuje alert z pełnym kompletem danych sygnału.
2. Jeżeli nie odpowie w wymaganym czasie:
   - alert eskaluje do **federacyjnego operatora awaryjnego**
     (wyznaczonej roli zapasowej).
3. Jeżeli operator federacyjny również nie odpowie w kolejnym oknie timeoutu:
   - dla `TC1` i `TC4` (bezpośrednie bezpieczeństwo ludzi): następuje
     **autoaktywacja** z `activation_path: "escalation_auto"` i rozszerzonym
     trace; rewizja jest obowiązkowa w 24h, nie w zwykłych 72h,
   - dla `TC2`, `TC3`, `TC5`: sygnał jest rozgłaszany do
     **wszystkich operatorów federacji** z `urgency: critical`; brak
     autoaktywacji bez operatora.

### 7.3. Odpowiedzialność operatora

- Powtarzające się timeouty operatora
  (`> max_operator_timeouts_per_period`, domyślnie 3 w 30 dni) generują
  negatywny sygnał `procedural` (`governance_inaction`) w
  `PROCEDURAL-REPUTATION-SPEC`.
- Trwała niedostępność uruchamia rewizję adekwatności danej roli zaufania publicznego.

---

## 8. Obowiązkowa rewizja pokryzysowa

### 8.1. Harmonogram

Rewizja MUSI rozpocząć się nie później niż **72 godziny** po dezaktywacji trybu
awaryjnego. Dla aktywacji `escalation_auto` (sekcja 7.2) rewizja MUSI ruszyć
w ciągu **24 godzin**.

### 8.2. Zakres

Rewizja obejmuje:

1. **Adekwatność** — czy klasa triggera została poprawnie rozpoznana? Czy ocena
   wiarygodności była trafna?
2. **Proporcjonalność** — czy podjęte działania były proporcjonalne do zagrożenia?
   Czy istniały mniej inwazyjne alternatywy?
3. **Skutki uboczne** — jakie niezamierzone konsekwencje wystąpiły? Czy doszło
   do naruszenia praw?
4. **Kompletność śladu** — czy trace jest pełny i niezredagowany?
5. **Rekomendacje kalibracyjne** — czy należy skorygować progi aktywacji,
   scoring wiarygodności albo wartości timeoutów?

### 8.3. Ciało rewizyjne

- Dla **aktywacji ręcznych**: rewizję prowadzi ciało governance federacji operatora.
- Dla **aktywacji automatycznych**: rewizję prowadzi niezależny recenzent
  (nie operator, który dostał alert).
- Dla **aktywacji `escalation_auto`**: rewizję prowadzi panel ad-hoc złożony
  zgodnie z `PANEL-SELECTION-PROTOCOL`.

### 8.4. Sprzężenie z reputacją

Wyniki rewizji generują sygnały w `PROCEDURAL-REPUTATION-SPEC`:

| Wynik | Domena sygnału | Typ sygnału | Polaryzacja |
| :--- | :--- | :--- | :--- |
| Reakcja adekwatna i proporcjonalna | `procedural` | `crisis_response_adequate` | dodatnia |
| Reakcja nadmierna | `procedural` | `crisis_response_disproportionate` | ujemna |
| Reakcja niewystarczająca | `incident` | `crisis_response_inadequate` | ujemna |
| Fałszywy alarm — przedwczesny (uczciwy błąd) | `incident` | `false_alarm_premature` | neutralna (rejestrowana, bez wpływu na score) |
| Fałszywy alarm — błędny (błąd systemowy) | `incident` | `false_alarm_mistaken` | ujemna (lekka) |
| Fałszywy alarm — zmanipulowany (umyślny) | `procedural` | `false_alarm_manipulated` | ujemna (ciężka) |

---

## 9. Klasyfikacja fałszywych alarmów

### 9.1. Kategorie

| Kategoria | Definicja | Odpowiedzialność |
| :--- | :--- | :--- |
| `premature` | Warunki triggera wyglądały wiarygodnie, ale rozwiązały się zanim aktywacja zaczęła działać | Brak sygnału negatywnego. System zadziałał zgodnie z projektem. |
| `mistaken` | Błąd oceny: wiarygodność została zawyżona albo źle sklasyfikowano trigger | Lekki sygnał negatywny w domenie `incident`. Wymagana rewizja kalibracji. |
| `manipulated` | Celowe sfabrykowanie sygnałów w celu uruchomienia aktywacji awaryjnej | Ciężki sygnał negatywny w domenie `procedural`. Dochodzenie wg `ABUSE-DISCLOSURE-PROTOCOL`, jeżeli dowody spełniają próg `S2+`. |

### 9.2. Metryka zdrowia

Federacja MUSI śledzić:

- współczynnik fałszywych alarmów w danym okresie (rolling 6 miesięcy),
- rozbicie na kategorie (`premature` / `mistaken` / `manipulated`),
- rozbicie według klasy triggera.

**Próg:** jeżeli suma fałszywych alarmów `mistaken + manipulated` przekracza
**30%** wszystkich aktywacji w oknie 6 miesięcy, uruchamia się obowiązkowa
rewizja kalibracji. Rewizja bada jakość sensorów, parametry scoringu
wiarygodności i przygotowanie operatorów.

---

## 10. Kryzysy kaskadowe

Gdy aktywne są równocześnie różne klasy triggerów:

### 10.1. Reguły

1. Każda klasa triggera tworzy **oddzielny rekord wyjątku**. Kryzysów nie scala
   się w jedną aktywację.

2. Łączny TTL jest równy **najdłuższemu pojedynczemu TTL**, a nie sumie.
   Jednoczesne `TC1` (4h) + `TC3` (24h) daje sufit 24h, nie 28h.

3. Uprawnienia się nie sumują. A3 jest maksimum; dwie równoczesne aktywacje A3
   nie tworzą „A4”. Zakres całkowity jest sumą zakresów poszczególnych aktywacji.

4. Dezaktywacja jest **per trigger**. Gdy `TC1` wygasa, ale `TC3` trwa, rekord
   `TC1` jest zamykany i rewizowany niezależnie.

5. Jeżeli kryzys kaskadowy obejmuje `TC5`, tryb `degraded_trust` z `TC5`
   wpływa na ocenę wiarygodności wszystkich równoległych triggerów
   (sekcja 3.2, pkt 3: autoaktywacja wymaga wtedy ręcznego potwierdzenia).

### 10.2. Wykrywanie kaskady

System MUSI oznaczać równoczesne aktywacje jako `cascade_event` w rekordach
aktywacji. Kaskady podlegają wzmożonemu monitoringowi i priorytetowej rewizji.

---

## 11. Relacja z Art. X (sygnaliści i ujawnianie nadużyć)

Aktywacja awaryjna może wchodzić w relację z frameworkiem ujawniania nadużyć:

1. **Ochrona sygnalisty w warunkach kryzysu** (Art. X.1-3): jeżeli aktywacja
   `TC4` dotyczy sygnalisty pod aktywnym zagrożeniem, odpowiedź awaryjna obejmuje
   zabezpieczenie kanału komunikacyjnego sygnalisty
   (`ABUSE-DISCLOSURE-PROTOCOL`, sekcja 4).

2. **Nadużycie jako trigger** (Art. X.4-X.8): wykrycie trwającego ciężkiego
   nadużycia (spełniającego progi `S3+` i `E3+` z `ABUSE-DISCLOSURE-PROTOCOL`)
   może stanowić trigger `TC4`, jeśli występuje aktywne prześladowanie lub
   ukierunkowana przemoc wobec zgłaszającego albo osób dotkniętych.

3. **Tryb awaryjny nie omija procedury disclosure**. Aktywacja A3 nie daje prawa
   do disclosure (`D1-D4`) bez zachowania wielorolowego współpodpisu i wymogów
   dowodowych z `ABUSE-DISCLOSURE-PROTOCOL`. Tryb awaryjny przyspiesza czas,
   ale nie obniża standardu dowodowego.

4. **Granica z Art. III.9**: prywatność nie osłania nadużyć przed reakcją
   awaryjną. Pipeline awaryjny MUSI jednak przestrzegać zasady minimalnego
   ujawnienia: dostępne są tylko dane bezpośrednio istotne dla zagrożenia.

---

## 12. Tryby uszkodzeń i mitygacje

| Tryb uszkodzenia | Mitygacja |
| :--- | :--- |
| Fałszywy trigger (sfabrykowany sygnał) | `C3+` wymagane dla autoaktywacji; klasyfikacja `manipulated` niesie ciężką karę reputacyjną; dochodzenie wg `ABUSE-DISCLOSURE-PROTOCOL` |
| Kompromitacja sensora | Wymóg niezależności źródeł (sekcja 4.3); `TC5` obniża zaufanie do ewaluacji automatycznej |
| Niedostępny operator | Łańcuch eskalacji z timeoutem (sekcja 7); autoaktywacja tylko dla przypadków bezpośrednio zagrażających ludziom |
| Użycie A3 jako backdoora do działań nieuprawnionych | A3 nie tworzy nowych uprawnień; pełny trace; obowiązkowa rewizja; działania poza kontraktem agenta są naruszeniem |
| Niekończący się tryb awaryjny | Absolutny sufit `max_extension`; nowy cykl wymaga nowego rekordu wyjątku i świeżych dowodów |
| Kryzys kaskadowy jako droga do permanentnego A3 | Oddzielne rekordy per trigger; łączny TTL = najdłuższy, nie suma; deaktywacja i rewizja per trigger |
| Nadużycie `TC5` (ogłaszanie kryzysu epistemicznego, by blokować działanie) | `TC5` nie może aktywować A3; uruchamia tylko monitoring i alerty |
| Wykorzystanie kompromitacji klucza council w trakcie kryzysu | Podklasa `TC2` z zamrożeniem trapdooru, rotacją klucza i panelem audytowym (sekcja 3.3) |
| Zmęczenie rewizjami (zbyt wiele review) | Metryka zdrowia dla współczynnika fałszywych alarmów; rewizja kalibracyjna po przekroczeniu progu |

---

## 13. Parametry federacyjne

| Parametr | Domyślnie | Dopuszczalny zakres | Reguła |
| :--- | :--- | :--- | :--- |
| `ttl_tc1` | 4h | 2-8h | Bardziej ostrożnie tak, bardziej permisywnie nie |
| `ttl_tc2` | 12h | 6-24h | " |
| `ttl_tc3` | 24h | 12-48h | " |
| `ttl_tc4` | 8h | 4-16h | " |
| `ttl_tc5_alert` | 24h | 12-48h | " |
| `max_ext_tc1` | 24h | 12-48h | " |
| `max_ext_tc2` | 48h | 24-96h | " |
| `max_ext_tc3` | 72h | 36-144h | " |
| `max_ext_tc4` | 48h | 24-96h | " |
| `max_ext_tc5_alert` | 72h | 36-144h | " |
| `operator_timeout_tc1` | 15 min | 5-30 min | " |
| `operator_timeout_tc2` | 30 min | 15-60 min | " |
| `operator_timeout_tc3` | 30 min | 15-60 min | " |
| `operator_timeout_tc4` | 15 min | 5-30 min | " |
| `operator_timeout_tc5` | 60 min | 30-120 min | " |
| `operator_override_window` | 5 min | 2-15 min | " |
| `correlation_window` | 15 min | 5-30 min | " |
| `review_deadline_normal` | 72h | 48-168h | " |
| `review_deadline_escalation` | 24h | 12-48h | " |
| `false_alarm_review_threshold` | 30% | 20-40% | " |
| `max_operator_timeouts_per_period` | 3 w 30 dni | 2-5 w 30 dni | " |

---

## 14. Otwarte pytania

1. **Automatyzacja scoringu wiarygodności**: jak dokładnie obliczać poziom `C`
   z surowych sygnałów? Obecna spec opisuje progi jakościowo. Model ilościowy
   wymaga symulacji, podobnie jak scoring reputacyjny `[hypothesis]` w
   `PROCEDURAL-REPUTATION-SPEC`.

2. **Taksonomia connectorów sensorium**: jakie typy connectorów istnieją i jakie
   klasy sygnałów produkują? Dokument zakłada istnienie sygnałów `sensorium`,
   ale nie definiuje interfejsu connectora. Może być potrzebny oddzielny
   `SENSORIUM-CONNECTOR-SPEC`.
