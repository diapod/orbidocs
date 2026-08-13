# Klauzula wieczności i procedura obrony Konstytucji DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-ENTRENCH-001` |
| `typ` | Ustawa wykonawcza sekcji "Rdzeń nienegocjowalny" i Art. XVI Konstytucji |
| `wersja` | 0.2.0-draft |
| `podstawa` | Art. I, II, III, XIV, XVI Konstytucji DIA |

---

## 1. Cel dokumentu

Konstytucja DIA sama definiuje skład rdzenia nienegocjowalnego oraz minimalne
własności jego ochrony. Niniejszy dokument NIE MOŻE zmieniać tego składu. Określa
procedurę obronną: sposób przeprowadzenia zmiany rdzenia, zgłoszenia zarzutu
niekonstytucyjności i rozstrzygnięcia sprawy bez tworzenia stałego organu centralnego.

---

## 2. Klauzula wieczności (ang. entrenchment clause)

### 2.1. Rdzeń nienegocjowalny

Kanonicznym źródłem składu rdzenia jest sekcja "Rdzeń nienegocjowalny" Konstytucji
oraz maszynowy `constitution-index.v1.json`. Ten akt odwołuje się do klauzul przez
stabilne identyfikatory i NIE MOŻE utrzymywać równoległych cytatów ich treści.

Rdzeń obejmuje ochronę:

- prymatu godności, bezpieczeństwa i przejścia mocy przez człowieka,
- dostępu do dóbr krytycznych bez przemocy systemowej i upokorzenia,
- osobistej sfery sprawczości, lokalności, eksportu, wyjścia i odgałęzienia,
- podłogi praw użytkowników wobec suwerenności operatora,
- redundantnego odpieczętowania tożsamości,
- nieodbieralnego minimum UBC,
- automatycznego wygaśnięcia okresu założycielskiego i ograniczenia władzy
  założycielskiej,
- konstytucyjnej hierarchii wartości.

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

W okresie założycielskim, o którym mowa w Konstytucji Art. XIII.7-12 oraz Art.
XVI.13, decyzje założycielskie zachowują pierwszeństwo wyłącznie poza rdzeniem
nienegocjowalnym. Założyciele NIE MOGĄ zawiesić, usunąć ani zawęzić ochrony rdzenia
z pominięciem procedury z pkt 2.2.

Każda decyzja założycielska MUSI pozostawiać uzasadnienie, analizę skutków, datę
i zakres obowiązywania. Automatyczne wygaśnięcie okresu założycielskiego NIE MOŻE
zależeć od wydania aktu kończącego ani od zgody organu, którego uprawnienia wygasają.

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

- **Konstytucja, sekcja "Rdzeń nienegocjowalny" i Art. XVI**: Konstytucja definiuje
  skład rdzenia i minimalne własności ochrony; niniejszy akt definiuje procedurę.
- **Konstytucja Art. XIII.7-12 oraz Art. XVI.13**: pierwszeństwo decyzji
  założycielskich NIE obejmuje zmiany rdzenia poza właściwą mu procedurą.
- **NORMATIVE-HIERARCHY.pl.md**: Poziom 0 wynika bezpośrednio z Konstytucji;
  niniejszy akt nie jest źródłem jego składu.
- **Konstytucja Art. XIV**: Środki tymczasowe są traktowane jako wyjątki podlegające
  minimalnym wymogom identyfikacji i wygaszenia.
- **Konstytucja Art. VII**: Panel ad-hoc jest spójny z zasadą proceduralnego ładu
  organizacyjnego (ang. governance), a nie ładu charyzmatycznego, oraz z rozdziałem ról.
