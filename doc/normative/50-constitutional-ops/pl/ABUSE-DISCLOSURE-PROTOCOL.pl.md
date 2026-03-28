# Protokół warunkowej jawności odpowiedzialności za nadużycia DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-ABUSE-DISC-001` |
| `typ` | Ustawa wykonawcza (Poziom 3 hierarchii normatywnej) |
| `wersja` | 0.1.0-draft |
| `podstawa` | Art. III.9, Art. X.4-10, Art. XVI.1-3 Konstytucji DIA |
| `data` | 2026-03-12 |

---

## 1. Cel dokumentu

Niniejszy dokument definiuje warunki, zakres i procedurę warunkowej jawności
odpowiedzialności za trwające lub ciężkie nadużycia w DIA. Celem nie jest lustracja
przeszłości jako takiej, lecz ochrona ludzi, wspólnoty i infrastruktury przed
kontynuowanym, ukrywanym lub ciężkim szkodzeniem.

Dokument konkretyzuje:

- próg wejścia do sprawy,
- standard dowodowy,
- role i wymóg współpodpisu,
- zakres dopuszczalnego ujawnienia,
- klasy sankcji infrastrukturalnych,
- relację między sankcjami infrastrukturalnymi a progami `nym -> node-id`,
- tryb odwołania,
- warunki notyfikacji prawnej.

---

## 2. Zasada bazowa

1. Bez wiarygodnego sygnału teraźniejszego NIE prowadzi się ogólnej retrospekcji
   przeszłości użytkownika ani operatora.

2. Wiarygodny sygnał teraźniejszy obejmuje co najmniej jedno z poniższych:
   - kontynuację nadużycia,
   - ukrywanie śladów lub dowodów,
   - odwet, zastraszanie lub próbę deanonimizacji,
   - wzorzec przemocy, korupcji albo sabotażu,
   - trwanie skutków ciężkiego nadużycia,
   - dalsze czerpanie korzyści z wcześniejszego nadużycia,
   - albo kompromitację zaufanego toru odpieczętowania lub emisji nymów, jeżeli
     zagraża ona ochronie ludzi, integralności dowodów lub prawu do wyjścia.

3. Po spełnieniu warunku z pkt 2 system MOŻE badać pełną genezę sprawy i cały łańcuch
   działań, także historycznych, o ile pozostaje to związane ze sprawą.

4. Im większa rola władcza, dostęp do danych wrażliwych albo wpływ na reputację,
   routing i bezpieczeństwo innych, tym surowszy standard odpowiedzialności oraz
   dłuższy dopuszczalny horyzont oceny.

---

## 3. Progi stawki i dowodów

### 3.1. Poziom stawki (`stake-level`)

| Poziom | Znaczenie | Skutek proceduralny |
| :--- | :--- | :--- |
| `S0` | brak istotnej szkody lub związku ze wspólnotą | brak sprawy |
| `S1` | niska szkoda, brak trwałych skutków | obserwacja lub korekta lokalna |
| `S2` | realna szkoda dla procedur, reputacji lub pojedynczych osób | przegląd i możliwe ograniczenia ochronne |
| `S3` | ciężka szkoda, wzorzec nadużyć albo istotne ryzyko dla ludzi lub infrastruktury | możliwe ujawnienie i sankcje infrastrukturalne |
| `S4` | bezpośrednie zagrożenie życia, zdrowia, wolności albo integralności systemu | natychmiastowa izolacja, możliwa notyfikacja prawna |

### 3.2. Poziom dowodów (`evidence-level`)

| Poziom | Znaczenie | Minimalny standard |
| :--- | :--- | :--- |
| `E0` | plotka | brak działania poza rejestracją sygnału |
| `E1` | poszlaka | pojedynczy sygnał bez niezależnego potwierdzenia |
| `E2` | uprawdopodobnienie | co najmniej dwa zgodne sygnały lub jeden artefakt wymagający weryfikacji |
| `E3` | twardy dowód | artefakt audytowalny lub dwa niezależne źródła, z których jedno ma postać materialnego śladu |
| `E4` | dowód wysoki | wieloźródłowy materiał audytowalny, spójny pod względem czasu, autorstwa i integralności |

### 3.3. Reguły decyzji

1. Wejście w pełną historię sprawy wymaga co najmniej `S2` i `E2`.

2. Ujawnienie tożsamości, faktów albo odpowiedzialności poza torem wewnętrznym wymaga
   co najmniej `S3` i `E3`.

3. Notyfikacja prawna wymaga co najmniej `S3` i `E3`, jeżeli sprawa dotyczy ciężkiego
   czynu naruszającego ludzi, wspólnotę, infrastrukturę, integralność dowodów albo
   procedur, w szczególności przemocy, poważnej korupcji, wyłudzenia, kradzieży,
   wymuszenia, odwetu wobec sygnalisty, deanonimizacji albo sabotażu. Dla pozostałych
   przypadków próg domyślny wynosi `S4` i `E3`, chyba że prawo właściwe wymaga
   niższego progu dla obowiązkowego zawiadomienia.

4. Dla ról zaufania publicznego oraz operatorów z dostępem do danych lub routingu próg
   wejścia w pełną historię sprawy może zostać obniżony do `S2` i `E2`, ale próg
   ujawnienia zewnętrznego pozostaje nie niższy niż `S3` i `E3`.

---

## 4. Role i wymóg współpodpisu

1. Każda sprawa MUSI mieć przypisane co najmniej role:
   - `Triage`,
   - `Evidence`,
   - `RedTeam`.

2. Dla ujawnienia zewnętrznego, sankcji `S3+` albo notyfikacji prawnej wymagany jest
   współpodpis co najmniej dwóch z trzech ról:
   - `Evidence`,
   - `RedTeam`,
   - `Governance` lub `Legal`, jeżeli rola istnieje w federacji.

3. Osoba z konfliktem interesów, relacją zależności, osobistym sporem lub interesem
   finansowym w sprawie MUSI zostać wyłączona.

4. Brak dostępnej roli `Legal` nie blokuje sprawy, ale blokuje notyfikację prawną,
   chyba że federacja ma ustawowy obowiązek zawiadomienia.

5. Zejście `nym -> node-id` dla sankcji infrastrukturalnych jest dopuszczalne przy
   progu `U1` określonym w `IDENTITY-UNSEALING-BOARD.pl.md` i nie stanowi jeszcze
   odpieczętowania `root-identity`.

6. Jeżeli sprawa dotyczy kompromitacji zaufanego anchoru council dla nymów,
   federacja POWINNA traktować ją jako incydent infrastrukturalny wysokiej stawki:

   - możliwe jest natychmiastowe zamrożenie trapdooru lub ścieżki odnowień,
   - rotacja klucza council staje się środkiem ochronnym, nie zwykłą operacją,
   - a audyt powinien zostać przekazany do panelu ad-hoc z zachowaniem zasady
     minimalnego ujawniania.

---

## 5. Model danych sprawy

Każda sprawa MUSI posiadać minimalny rekord:

| Pole | Opis |
| :--- | :--- |
| `case-id` | stabilny identyfikator sprawy |
| `opened-at` | czas otwarcia sprawy |
| `present-signal` | typ sygnału teraźniejszego |
| `stake-level` | ocena stawki `S0-S4` |
| `evidence-level` | ocena dowodów `E0-E4` |
| `role-risk` | związek sprawy z rolą i władzą nad innymi |
| `scope-justification` | uzasadnienie zakresu danych i retrospekcji |
| `coi-check` | wynik kontroli konfliktu interesów |
| `multisig-by` | role i osoby współpodpisujące decyzję |
| `disclosure-scope` | poziom ujawnienia `D0-D4` |
| `sanction-level` | poziom sankcji infrastrukturalnej |
| `appeal-window` | termin na odwołanie |
| `retention-class` | klasa retencji materiału |
| `jurisdiction` | jurysdykcja potencjalnie właściwa |
| `notification-mode` | tryb notyfikacji prawnej lub `none` |

---

## 6. Zakres ujawnienia (`disclosure-scope`)

| Poziom | Znaczenie |
| :--- | :--- |
| `D0` | brak ujawnienia poza zespołem sprawy |
| `D1` | ujawnienie wewnętrzne z redakcją tożsamości |
| `D2` | ujawnienie federacyjne z pseudonimową atrybucją i opisem ryzyka |
| `D3` | ujawnienie identyfikujące we wspólnocie, jeżeli jest konieczne dla ochrony ludzi lub infrastruktury |
| `D4` | ujawnienie identyfikujące + notyfikacja prawna zgodnie z pkt 10 |

1. Zakres ujawnienia MUSI być związany ze sprawą, proporcjonalny i minimalny.

2. Zakazane jest ujawnianie materiału obyczajowego, relacyjnego lub prywatnego bez
   bezpośredniego związku z ocenianym nadużyciem.

3. Sam fakt pełnienia roli zaufania nie znosi zasady minimalnego ujawniania; zwiększa
   wyłącznie zakres odpowiedzialności i wymóg transparentności proceduralnej.

---

## 7. Sankcje infrastrukturalne (`sanction-level`)

| Poziom | Znaczenie |
| :--- | :--- |
| `I0` | brak sankcji |
| `I1` | ostrzeżenie i monitoring |
| `I2` | ograniczenie uprawnień lub zawieszenie konkretnej funkcji |
| `I3` | kwarantanna reputacyjna lub zawieszenie roli |
| `I4` | odcięcie trasowania, blokada federacyjna lub izolacja węzła |

1. Sankcja MUSI odpowiadać poziomowi `stake-level`, odwracalności szkody i jakości
   dowodów.

2. Sankcja `I4` wymaga co najmniej `S3`, `E3` i współpodpisu zgodnie z pkt 4.

3. Sankcja może zostać nałożona przed publikacją zewnętrzną, jeśli wymaga tego ochrona
   ludzi albo integralności dowodów.

---

## 8. Retencja i dane

1. Dane sprawy wolno gromadzić wyłącznie w zakresie koniecznym do weryfikacji sygnału,
   ochrony ludzi, zachowania integralności dowodów i wykonania obowiązków prawnych.

2. Klasy retencji:
   - `R0` - sprawa odrzucona: 90 dni,
   - `R1` - sprawa zamknięta bez sankcji ciężkiej: 2 lata,
   - `R2` - sprawa z sankcją `I3-I4`: 7 lat,
   - `R3` - sprawa objęta legal hold lub torem prawnym: do zakończenia postępowania + 7 lat.

3. Materiał wykraczający poza zakres sprawy MUSI zostać zredagowany lub usunięty bez
   zbędnej zwłoki.

4. Korelaty danych wolno wykorzystywać wyłącznie wtedy, gdy ich związek ze sprawą został
   jawnie opisany w `scope-justification`.

---

## 9. Tryb odwołania

1. Osoba objęta ujawnieniem lub sankcją MUSI otrzymać:
   - opis zarzutu,
   - informację o materiale dowodowym w zakresie nieszkodzącym ofierze, sygnaliście
     lub integralności sprawy,
   - termin i ścieżkę odwoławczą.

2. Minimalne `appeal-window` wynosi 14 dni, chyba że bezpośrednie zagrożenie wymaga
   wcześniejszej izolacji.

3. Odwołanie rozpoznaje nowy skład, z wyłączeniem osób uczestniczących w decyzji
   pierwotnej.

4. Odwołanie może opierać się wyłącznie na:
   - kontr-dowodzie,
   - wykazaniu błędu proceduralnego,
   - wykazaniu konfliktu interesów w zespole sprawy,
   - wykazaniu nieproporcjonalności zakresu ujawnienia.

---

## 10. Notyfikacje jurysdykcyjne

1. `notification-mode = none` jest wartością domyślną.

2. Notyfikacja prawna jest dopuszczalna wyłącznie wtedy, gdy łącznie:
   - czyn spełnia próg z pkt 3.3,
   - istnieje dająca się wskazać jurysdykcja właściwa,
   - notyfikacja nie narusza silniejszego obowiązku ochrony ofiary, sygnalisty albo
     toczącego się postępowania,
   - decyzja została współpodpisana zgodnie z pkt 4.

3. Federacja POWINNA preferować tryb udokumentowanego przekazania materiału do
   właściwego organu nad publicznym ogłoszeniem, jeśli lepiej chroni to ludzi i
   integralność sprawy.

4. Każda notyfikacja MUSI zostawić ślad zawierający:
   - `jurisdiction`,
   - `legal-basis`,
   - `notified-at`,
   - `notified-by`,
   - `payload-hash`.

---

## 11. Zasada końcowa

Protokół nie służy karaniu za dawną biografię jako taką. Służy wykrywaniu i
ograniczaniu nadużyć, które trwają, są ukrywane, nadal przynoszą korzyść sprawcy albo
pozostają istotne dla bezpieczeństwa ludzi i integralności wspólnoty.
