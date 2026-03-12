# Protokół selekcji panelu DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-PANEL-SEL-001` |
| `typ` | Ustawa wykonawcza (Poziom 3 hierarchii normatywnej) |
| `wersja` | 0.1.0-draft |
| `podstawa` | Art. VII.1-3, VII.6, XVI.3 Konstytucji DIA; `ENTRENCHMENT-CLAUSE.pl.md` sekcja 3.2; `PROCEDURAL-REPUTATION-SPEC.pl.md`; `ROOT-IDENTITY-AND-NYMS.pl.md` |
| `status mechanizmów` | `[mechanizm - hipoteza]` dla entropii VRF; reguły kwalifikowalności i procedury mają charakter normatywny |

---

## 1. Cel dokumentu

Konstytucja wymaga paneli ad-hoc dla zaskarżeń konstytucyjnych
(`ENTRENCHMENT-CLAUSE` 3.2), sporów o wysokiej stawce (Art. XVI.3) oraz
kontradyktoryjnego przeglądu (ang. adversarial review) (Art. VII.9). Brakuje jednak
specyfikacji, **w jaki sposób** paneliści są wybierani z puli kwalifikowalnych
węzłów.

Niniejszy dokument definiuje:

- kryteria kwalifikowalności do służby panelowej,
- minimalny poziom pewności tożsamości dla panelistów,
- źródło entropii i mechanizm losowania,
- procedurę veta,
- eskalację, gdy pula kwalifikowalnych węzłów jest zbyt mała,
- poziomy ujawniania tożsamości panelistów,
- reguły rozwiązania panelu i uzupełniania składu,
- oś czasu postępowania panelowego.

---

## 2. Zasady projektowe

1. **Losowanie równomierne, nie ważone reputacją**. Reputacja jest progiem
   kwalifikowalności, a nie wagą selekcji. W obrębie kwalifikowalnej puli każdy
   węzeł ma takie samo prawdopodobieństwo wyboru. Selekcja ważona reputacją
   tworzyłaby faktyczną kastę sędziowską, sprzeczną z Art. VII.1 (ład
   organizacyjny bez kapłanów).

2. **Konflikt interesów jako domyślny punkt wyjścia** (ang. COI-by-default)
   (Art. VII.6). Brak deklaracji konfliktu interesów oznacza brak danych, a nie
   brak konfliktu. Ciężar dowodu spoczywa na kandydacie, nie na stronie
   kwestionującej.

3. **Rozdział ról** (Art. VII.3). Węzeł nie może jednocześnie być stroną,
   arbitrem i wyrocznią w tej samej sprawie. Panelista, który odkryje konflikt
   ról w trakcie postępowania, MUSI niezwłocznie się wyłączyć.

4. **Entropia ponad autorytetem**. Ziarno losowania jest generowane kolektywnie;
   żaden pojedynczy węzeł nie kontroluje wyniku selekcji.

5. **Proporcjonalne ujawnianie**. Ekspozycja tożsamości rośnie wraz z potrzebą:
   pełna dla audytu, pseudonimowa dla stron, niejawna dla opinii publicznej.

---

## 3. Kryteria kwalifikowalności

Węzeł kwalifikuje się do selekcji panelowej, jeśli spełnia **wszystkie**
poniższe warunki:

| Kryterium | Wymóg | Źródło |
| :--- | :--- | :--- |
| Reputacja proceduralna | `procedural.score >= panel_procedural_threshold` (domyślnie: 0.6) | `PROCEDURAL-REPUTATION-SPEC` sekcja 13 |
| Poziom pewności tożsamości | `assurance_level >= panel_identity_assurance_threshold` (domyślnie: `IAL3`) | `ROOT-IDENTITY-AND-NYMS` sekcja 7 i 8 |
| Status aktywny | `status = active` (nie: `bootstrapping`, `inactive`, `suspended`) | `PROCEDURAL-REPUTATION-SPEC` sekcja 5 |
| Rozruch zakończony | `bootstrap_remaining_days = 0` | `PROCEDURAL-REPUTATION-SPEC` sekcja 7.3 |
| Brak COI | Pozytywnie przechodzi kontrolę COI dla konkretnej sprawy (sekcja 4) | Art. VII.6 |
| Brak konfliktu ról | Nie jest stroną, wnioskodawcą, celem ani wyrocznią w tej samej sprawie | Art. VII.3 |
| Brak wcześniejszej służby | Nie służył już w panelu tej samej sprawy (w tym apelacji) | Sekcja 11 |
| Członkostwo federacyjne | Jest członkiem federacji rozstrzygającej sprawę (lub puli międzyfederacyjnej, patrz sekcja 8) | `FEDERATION-MEMBERSHIP-AND-QUORUM` |

Reputacja proceduralna jest więc warunkiem koniecznym, ale niewystarczającym.
Węzeł o wysokiej reputacji, lecz zbyt niskim poziomie `IAL`, nie kwalifikuje się
do panelu wysokiej stawki.

### 3.1. Procedura kontroli COI

1. Przed losowaniem każdy węzeł z kwalifikowalnej puli otrzymuje **zaślepione
   streszczenie sprawy** (strony zanonimizowane, przedmiot opisany na poziomie
   kategorii).

2. Każdy węzeł MUSI zadeklarować w ciągu `coi_declaration_window` (domyślnie: 24
   godziny; 4 godziny dla spraw `critical`):

   - `brak konfliktu` (z poświadczeniem kryptograficznym), albo

   - `konflikt istnieje` (z kategorią, ale bez szczegółów), albo

   - brak odpowiedzi (traktowany jako niezadeklarowany COI -- węzeł jest
     wykluczony).

3. Węzły deklarujące konflikt albo nieodpowiadające są wykluczane z losowania dla
   tej sprawy. Brak odpowiedzi generuje negatywny sygnał `procedural`
   (`governance_inaction`) w `PROCEDURAL-REPUTATION-SPEC`.

4. Odkrycie COI po selekcji wyzwala wyłączenie danego członka panelu (sekcja 10).

### 3.2. Bramka pewności tożsamości

1. Każdy kandydat do panelu MUSI przed selekcją ujawnić systemowi swój bieżący
   `assurance_level` oraz referencję do poświadczenia zakotwiczenia.

2. Dla zwykłych paneli wysokiej stawki minimalny poziom domyślny to `IAL3`.

3. Dla paneli, które mogą:

   - decydować o ujawnieniu identyfikującym,

   - wchodzić w tor notyfikacji prawnej,

   - rozstrzygać sprawy publicznych ról zaufania o najwyższej stawce,

   federacja POWINNA wymagać `IAL4`.

4. Strony nie otrzymują automatycznie root-identity panelistów. Poziom `IAL`
   jest warunkiem kwalifikowalności, a nie trybem pełnej jawności.

---

## 4. Źródło entropii i mechanizm losowania `[hipoteza]`

Losowanie wykorzystuje weryfikowalną funkcję losową (ang. Verifiable Random
Function, VRF) wraz ze schematem commit-reveal, aby ograniczyć możliwość
manipulacji ziarnem losowania.

### 4.1. Faza commit

1. Po ustaleniu kwalifikowalnej puli wszystkie kwalifikowalne węzły są
   zapraszane do udziału w generowaniu ziarna.

2. Każdy uczestniczący węzeł generuje losowy nonce i wysyła zobowiązanie:
   `H(nonce || node_id)`.

3. Okno commit: `commit_window` (domyślnie: 24 godziny; 4 godziny dla spraw
   `critical`).

4. Minimalna liczba uczestników: co najmniej `min_commit_participants`
   (domyślnie: 5) węzłów MUSI przesłać commit, aby losowanie mogło się odbyć.
   Poniżej tego progu stosuje się sekcję 8 (eskalacja).

### 4.2. Faza reveal

1. Po zamknięciu okna commit wszystkie węzły, które złożyły commit, ujawniają
   swój nonce.

2. Okno reveal: `reveal_window` (domyślnie: 12 godzin; 2 godziny dla spraw
   `critical`).

3. Commit bez ujawnienia: węzeł zostaje wykluczony z losowania, a dodatkowo
   generowany jest negatywny sygnał `procedural` (`protocol_violation`). Ujawnione
   nonce są przetwarzane bez brakujących wkładów.

4. Jeśli liczba ujawnionych nonce spadnie poniżej `min_commit_participants`,
   losowanie zaczyna się od nowej fazy commit.

### 4.3. Konstrukcja ziarna

Ziarno losowania wylicza się następująco:

```text
seed = VRF_prove(
  sk_draw_coordinator,
  H(challenge_hash || heartbeat_hash || sort(revealed_nonces))
)
```

Gdzie:

- `challenge_hash` = hash rekordu zaskarżenia konstytucyjnego,
- `heartbeat_hash` = hash ostatniego heartbeat federacji (zakotwiczenie w czasie),
- `sort(revealed_nonces)` = leksykograficznie posortowana konkatenacja wszystkich
  ujawnionych nonce,
- `sk_draw_coordinator` = klucz podpisujący wyznaczonego koordynatora losowania
  (rola rotacyjna, nie stały urząd).

Dowód VRF jest publikowany wraz z ziarnem, tak aby każdy węzeł mógł zweryfikować
poprawność jego wyprowadzenia.

### 4.4. Selekcja z puli

1. Kwalifikowalna pula (po wykluczeniach COI) jest sortowana według
   deterministycznego porządku kanonicznego (np. leksykograficzne `node_id`).

2. Ziarno jest używane do wygenerowania `panel_size` (domyślnie: 3) +
   `reserve_count` (domyślnie: 2) indeksów przez deterministyczny generator
   pseudolosowy zasilony wynikiem VRF.

3. Pierwsze `panel_size` indeksów wyznaczają skład podstawowy; pozostałe
   `reserve_count` to rezerwowi.

4. Całe losowanie jest reprodukowalne: każdy węzeł dysponujący dowodem VRF i
   listą kwalifikowalnej puli może zweryfikować wynik selekcji.

---

## 5. Skład panelu

### 5.1. Skład domyślny

| Parametr | Domyślnie | Uwagi |
| :--- | :--- | :--- |
| `panel_size` | 3 | Minimum. Federacje mogą zwiększać wyłącznie do liczb nieparzystych. |
| `reserve_count` | 2 | Rezerwowi na potrzeby podmian po vecie i ubytkach. |
| `max_panel_size` | 7 | Górna granica. Więcej nie znaczy lepiej; rośnie koszt koordynacji. |

### 5.2. Quorum

Panel ma quorum, gdy aktywna jest co najmniej liczba `ceil(panel_size / 2) + 1`
członków (obecnych i uczestniczących). Utrata quorum wyzwala podmianę z listy
rezerwowej albo, jeśli rezerwowi się wyczerpali, częściowe losowanie uzupełniające
(sekcja 10).

### 5.3. Reguła decyzji

Decyzje zapadają zwykłą większością głosów. W razie remisu (parzysty skład po
ubyciu członka) panel MUSI dobrać jeszcze jednego członka z rezerwowych albo
uruchomić częściowe losowanie uzupełniające. Remis nie jest rozstrzygany głosem
przewodniczącego.

---

## 6. Procedura veta

### 6.1. Prawo veta

Każda strona sporu może zgłosić **jedno veto** wobec wylosowanego panelisty.

### 6.2. Procedura veta

1. Po ogłoszeniu składu panelu każda strona ma `veto_window` (domyślnie: 48
   godzin; 12 godzin dla spraw `critical`) na użycie veta albo rezygnację z niego.

2. Veto MUSI zawierać pisemne uzasadnienie. Uzasadnienie jest rejestrowane, ale
   samo prawo ma charakter bezwarunkowy: strona nie musi udowadniać stronniczości.

3. Panelista objęty vetem jest zastępowany przez kolejnego rezerwowego. Jeśli
   rezerwowi się wyczerpali, dla tego miejsca uruchamia się częściowe losowanie
   uzupełniające (sekcja 10.3).

4. Panelista objęty vetem nie otrzymuje negatywnego sygnału reputacyjnego. Sam
   fakt objęcia vetem nie jest proceduralnym uchybieniem.

### 6.3. Ograniczenia

- Maksymalnie jedno veto na stronę dla danego składu panelu.
- Veto nie może zostać użyte wobec rezerwowego, dopóki rezerwowy nie zastąpi
  członka podstawowego.
- Powtarzalne nadużywanie veta w celu opóźniania postępowania może zostać
  oznaczone jako sygnał proceduralny, ale wymaga to odrębnego rozstrzygnięcia
  przez sam panel.

---

## 7. Oś czasu

| Faza | Normalna | Krytyczna | Uwagi |
| :--- | :--- | :--- | :--- |
| Deklaracja COI | 24h | 4h | Sekcja 3.1 |
| Faza commit | 24h | 4h | Sekcja 4.1 |
| Faza reveal | 12h | 2h | Sekcja 4.2 |
| Okno veta | 48h | 12h | Sekcja 6.2 |
| **Cała selekcja** | **~5 dni** | **~1 dzień** | Od przyjęcia sprawy do osadzenia panelu |
| Deliberacja panelu | 30 dni | 7 dni | Od osadzenia do orzeczenia |
| Środek tymczasowy | -- | 48h | Od wniosku do decyzji (2/3 panelistów) |
| Wniesienie apelacji | 14 dni | 7 dni | Od publikacji orzeczenia |

Wszystkie harmonogramy są parametrami federacyjnymi. Obowiązuje reguła
"ostrożniej tak, luźniej nie": federacje mogą wydłużać terminy, ale nie mogą
ich skracać poniżej wartości domyślnych.

---

## 8. Eskalacja przy niewystarczającej puli

Gdy kwalifikowalna pula jest zbyt mała, by przeprowadzić uczciwe losowanie,
uruchamiane są kolejno następujące poziomy:

### Poziom 1: Złagodzenie progu

Obniż `panel_procedural_threshold` o jeden krok (np. 0.6 -> 0.5). Ponownie
sprawdź kwalifikowalność. Można to zrobić najwyżej raz.

### Poziom 2: Pula międzyfederacyjna

Poproś o kwalifikowalne węzły z federacji sojuszniczych. Paneliści
międzyfederacyjni:

- muszą spełnić te same kryteria COI i konfliktu ról,
- otrzymują oznaczenie `foreign_panelist` w rekordzie postępowania,
- podlegają tym samym zasadom ujawniania (sekcja 9),
- generują sygnały `procedural` w swojej federacji macierzystej.

### Poziom 3: Nadpisanie dla małej federacji

Dla federacji z mniej niż `min_federation_pool_size` (domyślnie: 10)
kwalifikowalnymi węzłami:

- panel jest domyślnie budowany z puli międzyfederacyjnej,
- dodawany jest lokalny obserwator (bez prawa głosu) dla kontekstu federacyjnego,
- obserwator nie ma prawa veta ani głosu, ale może złożyć pisemny kontekst.

### Poziom 4: Eskalacja do ładu międzyfederacyjnego

Jeśli po poziomach 1-3 nadal nie da się zbudować panelu:

- sprawa jest eskalowana do ładu międzyfederacyjnego,
- tymczasowy panel governance jest tworzony z co najmniej trzech federacji,
- eskalacja jest rejestrowana jako sygnał luki governance.

---

## 9. Poziomy ujawniania tożsamości

Tożsamość panelistów jest ujawniana na trzech poziomach, odpowiadających trzem
odbiorcom:

### 9.1. Poziom audytowy (pełne ujawnienie)

Dostępny dla: wyznaczonych audytorów, paneli apelacyjnych oraz - jeśli to
wymagane - postępowań prawnych.

Zawartość:

- pełny `node_id` i tożsamość operatora,
- deklaracja COI i poświadczenie,
- dowód VRF i dane do weryfikacji losowania,
- podpis kryptograficzny pod orzeczeniem.

### 9.2. Poziom stron (pseudonimy proceduralne)

Dostępny dla: stron sporu.

Zawartość:

- proceduralny pseudonim (kryptograficzny, unikalny dla sprawy),
- rola w panelu (przewodniczący, członek, rezerwowy),
- podstawa wykluczenia COI (kategoria, bez szczegółu),
- przedział wyniku reputacji domenowej (np. `powyżej progu`), nie dokładny wynik.

### 9.3. Poziom publiczny (niejawny)

Dostępny dla: każdego obserwatora.

Zawartość:

- liczba panelistów i rezerwowych,
- potwierdzenie wykonania kontroli COI,
- proceduralne pseudonimy (nielinkowalne między sprawami),
- hash rekordu składu panelu,
- orzeczenie i uzasadnienie (przypisane panelowi jako ciału, nie jednostkom).

### 9.4. Nadpisanie poziomu ujawnienia

W sprawach dotyczących Art. X.4-X.8 (warunkowa jawność odpowiedzialności za
nadużycia) panel MOŻE podnieść poziom ujawnienia dla konkretnego panelisty,
jeżeli:

- stwierdzono, że panelista miał nieujawniony COI powiązany z nadużyciem,
- zwiększenie ujawnienia jest związane ze sprawą, proporcjonalne i ograniczone
  (Art. III.9),
- decyzja jest współpodpisana przez co najmniej dwóch panelistów.

Nadpisanie to nie daje blankietowej deanonimizacji; obowiązuje wyłącznie w
zakresie koniecznym dla integralności procedury.

---

## 10. Rozwiązanie panelu i uzupełnianie składu

### 10.1. Podstawy wymiany pojedynczego członka

Panelista jest wymieniany, gdy wystąpi:

| Podstawa | Wykrycie | Konsekwencja |
| :--- | :--- | :--- |
| Odkrycie COI po selekcji | Samoujawnienie, zaskarżenie przez stronę albo audyt | Natychmiastowe wyłączenie; zastępstwo z rezerwowych |
| Przekroczenie limitu bezczynności | Brak odpowiedzi w `inactivity_timeout` (domyślnie: 48h; 12h dla `critical`) | Zastępstwo z rezerwowych |
| Dowód zmowy | Sygnał z monitoringu albo zgłoszenie strony | Wymiana + negatywny sygnał `procedural` |
| Dobrowolne wyłączenie | Własna deklaracja panelisty | Zastępstwo z rezerwowych; bez negatywnego sygnału |

### 10.2. Procedura wymiany pojedynczego członka

1. Wolne miejsce zajmuje kolejny niewykorzystany rezerwowy.
2. Jeśli wszyscy rezerwowi się wyczerpali, uruchamiane jest częściowe losowanie
   uzupełniające (sekcja 10.3).
3. Zastępczy panelista dziedziczy materiały sprawy, ale dokonuje własnego,
   niezależnego przeglądu.
4. Harmonogram wydłuża się o `replacement_extension` (domyślnie: 7 dni; 2 dni
   dla `critical`), aby umożliwić nowemu członkowi zapoznanie się ze sprawą.

### 10.3. Częściowe losowanie uzupełniające

Częściowe losowanie wykorzystuje tę samą procedurę commit-reveal (sekcja 4), ale
dotyczy wyłącznie zwolnionego miejsca albo miejsc. Dotychczasowi paneliści są
wyłączeni z puli.

### 10.4. Pełne ponowne losowanie

Pełne ponowne losowanie (rozwiązanie i odtworzenie całego panelu) następuje
wyłącznie, gdy:

- ponad 50% składu panelu zostało skompromitowane (COI, zmowa albo bezczynność),
  albo
- systemowy problem integralności czyni postępowanie niewiarygodnym.

Pełne ponowne losowanie resetuje oś czasu deliberacji. Produkt pracy
poprzedniego panelu jest dostępny jako materiał pomocniczy, ale nie wiąże
nowego składu.

---

## 11. Relacja do procedury apelacyjnej

Panel apelacyjny (`ENTRENCHMENT-CLAUSE` 3.4) jest powoływany zgodnie z tym samym
protokołem, z jednym dodatkowym ograniczeniem:

- **Brak wcześniejszej służby**: węzły, które służyły w panelu pierwotnym, są
  wyłączone z puli apelacyjnej.

Wszystkie pozostałe reguły (kwalifikowalność, COI, veto, eskalacja, ujawnianie)
stosuje się identycznie.

---

## 12. Tryby awarii i środki zaradcze

| Tryb awarii | Środek zaradczy |
| :--- | :--- |
| Manipulacja entropią | Commit-reveal z dowodem VRF; brak reveal jest karany; ziarno wymaga wkładu kolektywnego |
| Ukryty COI | Odkrycie COI po selekcji uruchamia wymianę + ciężki negatywny sygnał `procedural`; Art. III.9 gwarantuje, że prywatność nie osłania nadużycia |
| Nadużywanie veta dla opóźnień | Maksymalnie jedno veto na stronę; natychmiastowa podmiana z rezerwowych |
| Przejęcie małej federacji | Awaryjna pula międzyfederacyjna (poziom 2-3); lokalny obserwator dla kontekstu bez prawa głosu |
| Zamilknięcie panelisty | Limit bezczynności z automatyczną podmianą; wydłużenie harmonogramu dla zapoznania się zastępcy |
| Zmowa panelistów | Sygnały monitoringu; dowód zmowy wyzwala wymianę i sankcję `procedural` |
| Manipulacja koordynatorem losowania | Dowód VRF jest publicznie weryfikowalny; koordynator jest rolą rotacyjną |
| Globalnie zbyt mało kwalifikowalnych węzłów | Eskalacja do poziomu 4; rejestracja jako sygnał luki governance |

---

## 13. Parametry federacyjne

| Parametr | Domyślnie | Dopuszczalny zakres | Zasada |
| :--- | :--- | :--- | :--- |
| `panel_size` | 3 | 3-7, tylko nieparzyste | Ostrożniej tak, luźniej nie |
| `reserve_count` | 2 | >= 2 | " |
| `panel_procedural_threshold` | 0.6 | >= 0.5 | " (współdzielone z `PROCEDURAL-REPUTATION-SPEC`) |
| `panel_identity_assurance_threshold` | `IAL3` | `IAL2`-`IAL4` | " (współdzielone z `ROOT-IDENTITY-AND-NYMS`) |
| `coi_declaration_window` | 24h | >= 12h | " |
| `coi_declaration_window_critical` | 4h | >= 2h | " |
| `commit_window` | 24h | >= 12h | " |
| `commit_window_critical` | 4h | >= 2h | " |
| `reveal_window` | 12h | >= 6h | " |
| `reveal_window_critical` | 2h | >= 1h | " |
| `min_commit_participants` | 5 | >= 3 | " |
| `veto_window` | 48h | >= 24h | " |
| `veto_window_critical` | 12h | >= 6h | " |
| `deliberation_days` | 30 dni | >= 14 dni | " |
| `deliberation_days_critical` | 7 dni | >= 5 dni | " |
| `inactivity_timeout` | 48h | >= 24h | " |
| `inactivity_timeout_critical` | 12h | >= 6h | " |
| `replacement_extension` | 7 dni | >= 3 dni | " |
| `replacement_extension_critical` | 2 dni | >= 1 dzień | " |
| `min_federation_pool_size` | 10 | >= 7 | " |

---

## 14. Otwarte pytania

1. **Implementacja VRF**: Jaki schemat VRF wybrać? Kandydatem jest ECVRF
   (RFC 9381), ale wybór zależy od stosu kryptograficznego. Na razie to parametr
   projektowy, nieustalony w specyfikacji.

2. **Wybór koordynatora losowania**: Koordynator jest opisany jako rola rotacyjna.
   Mechanizm rotacji (round-robin, reputacyjny, losowy) nie został jeszcze
   zdefiniowany.

3. **Zaufanie międzyfederacyjne przy służbie panelowej**: Gdy węzeł służy w panelu
   innej federacji, jakie obowiązują założenia zaufania? Przenośny pakiet
   dowodów (`PROCEDURAL-REPUTATION-SPEC` sekcja 8) dostarcza materiału, ale model
   zaufania dla adjudykacji międzyfederacyjnej wymaga dalszej specyfikacji.

4. **Protokół deliberacji**: Ten dokument określa skład, ale nie format
   deliberacji (synchroniczny / asynchroniczny, debata ustrukturyzowana, zasady
   składania dowodów). Może być potrzebny osobny `PANEL-DELIBERATION-PROTOCOL`.

5. **Wynagrodzenie za służbę panelową**: Czy paneliści powinni otrzymywać
   wynagrodzenie (token, bonus reputacyjny albo inne)? Obecny projekt:
   zakończenie służby generuje pozytywny sygnał `procedural`
   (`panel_completed`), który jest jedyną zachętą.

---

## 15. Relacja do innych dokumentów

- **Konstytucja Art. VII.1-3**: Dokument operacjonalizuje proceduralny ład
  organizacyjny, definiując sposób budowania paneli rozstrzygających bez stałych
  organów i bez charyzmatycznego autorytetu.
- **Konstytucja Art. VII.6**: COI-by-default jest bazą kwalifikowalności.
- **Konstytucja Art. VII.3**: Rozdział ról jest egzekwowany przez wykluczenia
  kwalifikowalności.
- **Konstytucja Art. XVI.3**: Decyzje o wysokiej stawce wymagające niezależnej
  weryfikacji używają paneli złożonych zgodnie z tym protokołem.
- **Konstytucja Art. X.4-X.8, III.9**: Nadpisanie poziomu ujawnienia (sekcja 9.4)
  jest osadzone w reżimie warunkowej jawności; prywatność nie osłania nadużycia
  przed proceduralną odpowiedzialnością.
- **`ENTRENCHMENT-CLAUSE.pl.md` sekcja 3.2**: To jest mechanizm wskazywany tam dla
  budowy paneli ad-hoc.
- **`PROCEDURAL-REPUTATION-SPEC.pl.md`**: Dostarcza `procedural.score` i
  `panel_procedural_threshold` używane do kwalifikowalności. Służba panelowa
  generuje sygnały domeny `procedural`.
- **`ROOT-IDENTITY-AND-NYMS.pl.md`**: Dostarcza poziomy `IAL` i regułę, że
  wyższy wpływ wymaga silniejszego zakotwiczenia tożsamości; panel wysokiej stawki
  nie może opierać się wyłącznie na reputacji.
- **`EXCEPTION-POLICY.pl.md`**: Środki tymczasowe (sekcja 7, harmonogram
  `critical`) są wyjątkami konstytucyjnymi typu `injunction`.
- **`ABUSE-DISCLOSURE-PROTOCOL.pl.md`**: Sprawy rozstrzygane pod Art. X używają
  paneli złożonych według tego protokołu; poziomy ujawnienia (D0-D4) pozostają w
  interakcji z poziomami ujawniania tożsamości panelistów (sekcja 9).
- **`AUTONOMY-LEVELS.pl.md`**: Przegląd po kryzysie A3 może być prowadzony przez
  panel złożony zgodnie z tym protokołem.
- **`REPUTATION-VALIDATION-PROTOCOL.pl.md`**: Postępowania panelowe generują
  sygnały `procedural`, które zasilają metryki zdrowia M1-M5.
- **`NORMATIVE-HIERARCHY.pl.md`**: Niniejszy dokument jest ustawą wykonawczą
  Poziomu 3.
