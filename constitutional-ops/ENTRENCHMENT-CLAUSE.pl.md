# Klauzula wieczności i procedura obrony Konstytucji DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-ENTRENCH-001` |
| `typ` | Propozycja uzupełnienia Art. XVI Konstytucji |
| `wersja` | 0.1.0-draft |
| `podstawa` | Art. I, II, III, XIV, XVI Konstytucji DIA |

---

## 1. Cel dokumentu

Konstytucja DIA deklaruje swoje pierwszeństwo nad wszystkimi innymi dokumentami,
politykami i decyzjami (sekcja "Moc normatywna i wykładnia", punkt 4). Jednak nie
definiuje:

- które artykuły są niezmienne (rdzeń nienegocjowalny),
- co się dzieje, gdy większość federacji chce złamać Konstytucję,
- kto i jak rozstrzyga zarzuty niekonstytucyjności.

Niniejszy dokument zamyka te luki, proponując klauzulę wieczności i minimalną
procedurę obronną - bez tworzenia stałego organu centralnego.

---

## 2. Klauzula wieczności (ang. entrenchment clause)

### 2.1. Rdzeń nienegocjowalny

Następujące artykuły Konstytucji stanowią **rdzeń nienegocjowalny**:

| Artykuł | Treść rdzeniowa |
| :--- | :--- |
| **I.5** | Żaden cel operacyjny ani finansowy nie może unieważnić prymatu godności, bezpieczeństwa człowieka i prawa do wyjścia. |
| **II.1** | Godność osoby ludzkiej jest wartością nadrzędną i nienegocjowalną. |
| **II.2** | Ochrona życia oraz obrona przed bezpośrednią, nagłą i poważną krzywdą zdrowotną mają najwyższy priorytet operacyjny. |
| **II.3** | Największa moc systemu MUSI przechodzić przez człowieka, nie obok człowieka. |
| **III.1** | Użytkownik pozostaje właścicielem swoich danych, polityk, agentów i lokalnych przestrzeni pamięci. |
| **III.2** | System MUSI działać sensownie w trybach lokalnych jako domyślnych (ang. local-first), bez połączenia z siecią (offline) i samodzielnie hostowanych (ang. self-hosted). |
| **III.3** | Eksport danych, polityk i historii MUSI być możliwy w otwartych formatach. |
| **III.4** | Prawo do wyjścia bez szantażu, bez utraty dostępu do danych, bez ukrytych kar. |
| **III.5** | Prawo do odgałęzienia (ang. fork). |
| **XIV.1** | Domyślna hierarchia wartości: godność > suwerenność > weryfikowalność > sprawczość > skuteczność > wygoda. |

### 2.2. Warunki zmiany rdzenia nienegocjowalnego

Zmiana, zawieszenie, usunięcie lub reinterpretacja zawężająca któregokolwiek artykułu
z rdzenia nienegocjowalnego wymaga **jednoczesnego** spełnienia wszystkich poniższych
warunków:

1. **Jednomyślność federacji** - zgoda wszystkich federacji uczestniczących w procesie
   zmiany. Jedna federacja = jedno veto. Brak głosu nie jest traktowany jako zgoda.

2. **Niezależny kontradyktoryjny przegląd (ang. adversarial review)** - panel
   zespołu kontrtestującego (ang. red-team) złożony z co najmniej trzech węzłów o
   wysokiej reputacji proceduralnej, niebędących inicjatorami zmiany i
   nieposiadających konfliktu interesów z przedmiotem zmiany. Panel publikuje jawne
   uzasadnienie poparcia lub sprzeciwu.

3. **Okres refleksji** - minimum 90 dni między formalnym zgłoszeniem propozycji a
   głosowaniem. W tym czasie propozycja jest publicznie dostępna, a każdy węzeł może
   zgłosić kontr-argumenty.

4. **Analiza skutków** - pisemna analiza obejmująca: przewidywane skutki dla godności,
   bezpieczeństwa, suwerenności i prawa do wyjścia; scenariusze nadużyć; warunki
   odwracalności.

5. **Jawność procesu** - pełny ślad procesu decyzyjnego (propozycja, argumenty,
   kontr-argumenty, głosy, uzasadnienia) jest trwale archiwizowany i publicznie
   dostępny.

### 2.3. Czego klauzula wieczności nie blokuje

Klauzula wieczności nie uniemożliwia:

- zmiany artykułów Konstytucji **spoza** rdzenia nienegocjowalnego (procedura z Art.
  XVI),
- zaostrzania rdzenia (dodawania nowych gwarancji),
- reinterpretacji **rozszerzającej** zakres ochrony,
- tworzenia nowych artykułów, o ile nie osłabiają rdzenia.

### 2.4. Okres założycielski

W okresie założycielskim, o którym mowa w Konstytucji Art. XIII.7-11 oraz Art.
XVI.10, mechanizm jednomyślności federacji i zwykłe ścieżki blokowania nie mogą
paraliżować decyzji założycielskich dotyczących kształtu systemu, jego architektury,
zasad rozruchowych i tekstu Konstytucji.

Nie oznacza to zawieszenia jawności ani śladu. Każda taka decyzja MUSI pozostawiać
uzasadnienie, analizę skutków, datę i zakres obowiązywania. Po zakończeniu okresu
założycielskiego pełna procedura z pkt 2.2 obowiązuje bez wyjątku.

---

## 3. Procedura obrony konstytucyjnej

### 3.1. Zarzut niekonstytucyjności

Każda federacja, każdy węzeł o statusie obywatela roju (Art. XV) oraz każda rola
zaufania publicznego może zgłosić **zarzut niekonstytucyjności** wobec:

- polityki federacyjnej,
- decyzji dotyczącej ładu organizacyjnego (ang. governance),
- ustawy wykonawczej,
- działania węzła, agenta lub roli,
- propozycji zmiany Konstytucji.

Zgłoszenie musi zawierać:

```yaml
constitutional_challenge:
  challenger_id: [identyfikator zgłaszającego]
  target: [identyfikator kwestionowanego dokumentu / decyzji / działania]
  articles_violated: [lista artykułów Konstytucji]
  reasoning: [uzasadnienie - dlaczego target narusza wskazane artykuły]
  evidence: [odniesienia do dowodów]
  urgency: [normal | elevated | critical]
  date: [timestamp]
```

### 3.2. Panel ad-hoc (zamiast stałego sądu konstytucyjnego)

DIA nie tworzy stałego organu rozstrzygającego - byłaby to centralizacja sprzeczna
z Art. VII. Zamiast tego:

**Powołanie panelu:**

1. Po przyjęciu zgłoszenia system losuje **3 lub więcej węzłów** z puli węzłów
   spełniających kryteria:
   - wysoka reputacja proceduralna (nie techniczna - Art. VII.4),
   - brak konfliktu interesów z przedmiotem sprawy (domniemanie konfliktu
     interesów przy braku danych, COI-by-default, Art. VII.6),
   - brak powiązań ze stronami sporu.

2. Strony sporu mogą zgłosić **po jednym veto** wobec wylosowanych węzłów
   (z uzasadnieniem), po czym losowanie jest powtarzane dla odrzuconych pozycji.

3. Panel działa kolegialnie; decyzje zapadają większością głosów.

**Praca panelu:**

1. Panel ma **30 dni** na wydanie rozstrzygnięcia (w trybie `critical` - 7 dni).
2. Panel bada zgodność target z Konstytucją, korzystając z Źródeł wykładni
   (Poziom 2 hierarchii normatywnej) i zasad interpretacji z sekcji "Moc normatywna
   i wykładnia".
3. Panel publikuje **uzasadnienie** zawierające: stan faktyczny, analizę prawną,
   rozstrzygnięcie i ewentualne zalecenia.

**Skutki rozstrzygnięcia:**

- Rozstrzygnięcie jest **wiążące** do czasu formalnej zmiany Konstytucji.
- Rozstrzygnięcie **nie tworzy precedensu wiążącego** - każda sprawa jest
  rozpatrywana od nowa. To chroni przed "konstytucyjnym dryfem" przez akumulację
  interpretacji.
- Jeśli panel stwierdzi niekonstytucyjność, target jest **zawieszony** w zakresie
  naruszenia do czasu naprawy lub formalnej zmiany Konstytucji.

### 3.3. Środek tymczasowy (ang. injunction)

W sprawach oznaczonych jako `critical` - gdy opóźnienie może spowodować nieodwracalną
szkodę - zgłaszający może wnioskować o **środek tymczasowy**:

1. Wniosek wymaga wskazania, jaka szkoda jest nieodwracalna i dlaczego.
2. Decyzję o środku tymczasowym podejmują **2 z 3** wylosowanych członków panelu
   w ciągu **48 godzin**.
3. Środek tymczasowy **zawiesza** kwestionowane działanie do czasu pełnego
   rozstrzygnięcia.
4. Środek tymczasowy jest sam śledzony jako wyjątek konstytucyjny i musi zawierać
   `reason`, `risk-level`, `expiry` i `owner`, zgodnie z Art. XIV Konstytucji.

### 3.4. Odwołanie

Strona niezadowolona z rozstrzygnięcia może złożyć odwołanie w ciągu 14 dni.
Odwołanie rozpatruje **nowy panel** (losowany od nowa, z wykluczeniem poprzednich
członków). Rozstrzygnięcie drugiego panelu jest ostateczne.

---

## 4. Scenariusze zagrożeń i odpowiedzi

| Scenariusz | Odpowiedź systemu |
| :--- | :--- |
| Większość federacji głosuje za usunięciem prawa do wyjścia | Klauzula wieczności: wymaga jednomyślności + kontradyktoryjnego przeglądu (ang. adversarial review) + 90 dni refleksji. Jedna federacja blokuje. |
| Sponsor wymusza reinterpretację Art. VIII przez politykę federacyjną | Zarzut niekonstytucyjności -> panel ad-hoc -> zawieszenie polityki. |
| Grupa węzłów próbuje zdominować pulę losowania paneli | Kryteria domniemania konfliktu interesów przy braku danych (COI-by-default) + veto stron + reputacja proceduralna (nie techniczna) ograniczają przejęcie sterowania (ang. capture). |
| Panel wydaje rozstrzygnięcie stronnicze | Odwołanie do nowego panelu. Brak precedensu wiążącego -> stronnicze rozstrzygnięcie nie trwale kształtuje wykładni. |
| Tryb kryzysowy (Art. IX) wykorzystywany do obejścia Konstytucji | Tryb kryzysowy nie zawiesza rdzenia nienegocjowalnego. Obowiązkowa rewizja post-hoc. |

---

## 5. Relacja z innymi dokumentami

- **Konstytucja Art. XVI**: Niniejszy dokument jest propozycją uzupełnienia Art. XVI
  o punkty dotyczące rdzenia nienegocjowalnego i procedury obronnej.
- **Konstytucja Art. XIII.7-11 oraz Art. XVI.10**: okres założycielski ma
  pierwszeństwo proceduralne wobec pełnej ścieżki międzyfederacyjnej do czasu
  upływu swojej klauzuli czasowej.
- **NORMATIVE-HIERARCHY.pl.md**: Klauzula wieczności definiuje Poziom 0 hierarchii.
- **Konstytucja Art. XIV**: Środki tymczasowe są traktowane jako wyjątki podlegające
  minimalnym wymogom identyfikacji i wygaszenia.
- **Konstytucja Art. VII**: Panel ad-hoc jest spójny z zasadą proceduralnego ładu
  organizacyjnego (ang. governance), a nie ładu charyzmatycznego, oraz z rozdziałem ról.
