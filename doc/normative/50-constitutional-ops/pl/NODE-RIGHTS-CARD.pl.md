# Karta Praw i Obowiązków Węzła DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-NODE-CARD-001` |
| `typ` | Wyciąg z Konstytucji - materiał wdrożeniowy (ang. onboarding) |
| `wersja` | 0.1.0-draft |
| `źródło` | Art. II, III, XV, XVI Konstytucji DIA |

---

## Twoje prawa jako węzła

| Prawo | Co oznacza | Konstytucja |
| :--- | :--- | :--- |
| **Prawo do wyjścia** | Możesz opuścić federację w dowolnym momencie, bez szantażu, bez utraty dostępu do własnych danych, bez ukrytych kar. | Art. III.4 |
| **Prawo do prywatności** | Telemetria jest domyślnie wyłączona. Twoje dane są lokalne. Ujawnianie jest selektywne i co do zasady wymaga Twojej zgody, z wyjątkiem proceduralnym dla trwających lub ciężkich nadużyć zgodnie z Art. III.9 i Art. X. | Art. III.7, III.8, III.9, Art. X |
| **Prawo do wglądu** | Możesz audytować interakcje swoich agentów, ślady decyzji i historię działań. | Art. XV.2 |
| **Prawo do odwołania** | Każdą decyzję reputacyjną lub sankcję możesz zakwestionować procedurą odwoławczą. | Art. XV.2, XVI.2 |
| **Prawo do bezpieczeństwa** | System chroni Cię przed nękaniem, ujawnianiem danych tożsamościowych (ang. doxxingiem), sabotażem i ekonomicznym wymuszaniem. | Art. XV.2 |
| **Prawo do lokalnej autonomii** | Możesz prowadzić węzeł "w ciszy": prywatnie, lokalnie, bez uczestnictwa w przestrzeniach publicznych. | Art. III.6 |
| **Prawo do odgałęzienia (ang. fork)** | Możesz skopiować specyfikacje, polityki i otwarte komponenty bez proszenia o zgodę centrum. | Art. III.5 |
| **Prawo do suwerenności danych** | Jesteś właścicielem swoich danych, polityk, agentów i lokalnych przestrzeni pamięci. Eksport w otwartych formatach jest gwarantowany. | Art. III.1, III.3 |

## Jeśli zaczynasz od poświadczenia `phone`

Poświadczenie numerem telefonu jest dopuszczalne jako wygodny próg wejścia, ale
traktowane jest jako źródło `weak`, a nie pełne zakotwiczenie wysokiej stawki.

Domyślne ograniczenia operacyjne:

- brak dostępu do ról governance,

- brak dostępu do paneli i izb pieczęciowych,

- brak dostępu do wyroczni wysokiej stawki,

- brak operacji wymagających toru `U2` albo `U3`,

- możliwe limity wpływu, tempa działań lub dojrzewania reputacyjnego do czasu
  przejścia na poświadczenie `strong`.

Przejście `phone -> strong` nie powinno niszczyć Twojej kotwicy ani trwałych
nymów, ale może wymagać okresu wyczekiwania i kontroli anomalii.

## Twoje obowiązki jako węzła

| Obowiązek | Co oznacza | Konstytucja |
| :--- | :--- | :--- |
| **Nie krzywdź** | Nie podejmuj działań celowo szkodzących ludziom, infrastrukturze ani integralności pamięci i dowodów. | Art. XV.4 |
| **Bądź uczciwy epistemicznie** | Oznaczaj spekulacje. Nie fałszuj dowodów. Nie manipuluj reputacją. | Art. XV.3 |
| **Współdziałaj protokołowo** | Respektuj kontrakty, wersje protokołu i limity. | Art. XV.3 |
| **Utrzymuj higienę operacyjną** | Dbaj o klucze, aktualizacje i podstawowe bezpieczeństwo węzła. | Art. XV.3 |
| **Bądź gotowy do pomocy** | W ramach swoich możliwości - bez obowiązku transakcyjnego rozrachunku. | Art. XV.3 |

## Hierarchia wartości (gdy wartości wchodzą w konflikt)

```text
Godność i bezpieczeństwo człowieka
  > Suwerenność i prywatność
    > Weryfikowalność i przejrzystość
      > Sprawczość i autonomia
        > Skuteczność i optymalizacja
          > Wygoda i estetyka
```

Źródło: Art. XIV.1. W razie konfliktu na tym samym poziomie stosuje się test
odwracalności, proporcjonalności i jawności (Art. XIV.2).

## Egzekwowanie jest stopniowalne

```text
Ostrzeżenie -> Ograniczenie uprawnień -> Kwarantanna reputacyjna -> Odcięcie trasowania (ang. routingu)
```

Każda sankcja zostawia ślad, daje możliwość odwołania i otwiera ścieżkę powrotu po
naprawie (Art. XVI.1-2).

---

**Pełna Konstytucja:** `doc/normative/40-constitution/pl/CONSTITUTION.pl.md`  
**Wartości i wykładnia:** `doc/normative/30-core-values/pl/CORE-VALUES.pl.md`  
**Wizja projektu:** `doc/normative/20-vision/pl/VISION.pl.md`  
**Gradient autonomii agentów:** `AUTONOMY-LEVELS.pl.md`

---
---

# Indeks decyzyjny - od sytuacji do artykułu

Poniższa tabela mapuje najczęstsze sytuacje operacyjne na odpowiednie artykuły
Konstytucji i kluczowe zasady. Służy jako mapa nawigacyjna - nie zastępuje lektury
Konstytucji, ale pozwala szybko znaleźć właściwą normę.

## Prawa i suwerenność użytkownika

| # | Sytuacja | Artykuły | Zasada / Działanie |
| :--- | :--- | :--- | :--- |
| 1 | Użytkownik chce zabrać swoje dane i odejść | III.3, III.4 | Eksport w otwartych formatach, bez szantażu i ukrytych kar |
| 2 | Użytkownik chce uruchomić węzeł offline | III.2, III.6 | System MUSI działać sensownie w trybie lokalnym jako domyślnym (ang. local-first) i samodzielnie hostowanym (ang. self-hosted) |
| 3 | Użytkownik chce utworzyć odgałęzienie projektu | III.5 | Prawo do odgałęzienia (ang. fork): specyfikacje, polityki, otwarte komponenty |
| 4 | Ktoś włączył telemetrię bez zgody użytkownika | III.7 | Telemetria domyślnie wyłączona; wymaga jasnej, odwoływalnej zgody |

## Agenty i autonomia

| # | Sytuacja | Artykuły | Zasada / Działanie |
| :--- | :--- | :--- | :--- |
| 5 | Agent podjął decyzję bez wiedzy użytkownika | II.3, II.4, V.10 | Moc przechodzi przez człowieka; domyślnie propozycje i warianty |
| 6 | Agent przekroczył budżet / czas / zakres | V.10, AUTONOMY-LEVELS.pl.md | Agent MUSI mieć wyłącznik awaryjny (ang. kill-switch), limity uprawnień, czasu i kosztu |
| 7 | Agent eskalował sobie uprawnienia | V.13, AUTONOMY-LEVELS.pl.md | Zakaz samonadawania uprawnień (ang. zero self-authorize); błąd agenta nie może automatycznie eskalować uprawnień |
| 8 | Agent działa w sytuacji zagrożenia życia | II.8, IX.3, AUTONOMY-LEVELS.pl.md | MOŻE działać szybciej, ale zostawia ślad i podlega rewizji |

## Finansowanie i przejęcie sterowania (ang. capture)

| # | Sytuacja | Artykuły | Zasada / Działanie |
| :--- | :--- | :--- | :--- |
| 9 | Sponsor żąda uprzywilejowanego dostępu do danych | VIII.2 | Zakaz - finansowanie nie kupuje dostępu do danych, trasowania ani ładu organizacyjnego (ang. governance) |
| 10 | Jedna zależność stała się krytyczna (model, infra, funding) | VIII.5 | Obowiązkowy plan dywersyfikacji |
| 11 | Napięcie między finansowaniem a integralnością konstytucyjną | VIII.7 | Integralność konstytucyjna ma pierwszeństwo |
| 12 | Model przychodowy oparty na uzależnianiu użytkownika | VIII.3, II.7 | Zakaz dopaminowego UX i ekonomii opartej na przytrzymywaniu |

## Reputacja i ład organizacyjny (ang. governance)

| # | Sytuacja | Artykuły | Zasada / Działanie |
| :--- | :--- | :--- | :--- |
| 13 | Węzeł kwestionuje decyzję reputacyjną | XV.5, XVI.2 | Kontr-dowód lub wykazanie błędu proceduralnego; prawo do odwołania |
| 14 | Brak ujawnienia konfliktu interesów | VII.6 | Domniemanie konfliktu interesów przy braku danych (COI-by-default): brak deklaracji = brak danych, nie brak konfliktu |
| 15 | Osoba pełni jednocześnie rolę strony i arbitra | VII.3 | Uprawnienia krytyczne MUSZĄ być rozdzielone między role |
| 16 | Decyzja o wysokiej stawce | VII.9 | Współpodpis (ang. multisig) + niezależny zespół kontrtestujący (ang. red-team) |

## Bezpieczeństwo i kryzys

| # | Sytuacja | Artykuły | Zasada / Działanie |
| :--- | :--- | :--- | :--- |
| 17 | Podejrzenie Sybil / DoS / wstrzyknięcia poleceń | IX.1, IX.2 | Model zagrożeń jest częścią architektury, nie ozdobą |
| 18 | Sytuacja kryzysowa (awaria zasilania lub łączności, konflikt) | IX.3, IX.4 | Tryb kryzysowy: wyższy rygor, redundancja, lokalność, jakość śladów |
| 19 | Węzeł częściowo odcięty od sieci | IX.5 | Węzeł POWINIEN zachowywać zdolność działania w częściowej izolacji |
| 20 | Potrzeba awaryjnej pamięci podręcznej (schronienie, żywność, wstępna kategoryzacja (ang. triage)) | IX.6, IX.7 | Memarium może utrzymywać przestrzenie kryzysowe |

## Sygnaliści i publikacja

| # | Sytuacja | Artykuły | Zasada / Działanie |
| :--- | :--- | :--- | :--- |
| 21 | Ktoś chce zgłosić nadużycie anonimowo | X.1, X.2 | Anonimowość domyślna, minimalizacja metadanych, wstępna kategoryzacja (ang. triage) sygnałów |
| 22 | Sygnalista narażony na odwet | X.3 | Opieka roju jest częścią infrastruktury, nie gestem moralnym |
| 23 | Pojawia się wiarygodny sygnał trwającego lub ukrywanego ciężkiego nadużycia | III.9, X.4-X.8 | Brak ogólnej lustracji bez sygnału teraźniejszego; po spełnieniu progu możliwe badanie pełnej historii sprawy, sankcje infrastrukturalne i procedura odwoławcza |
| 24 | Rozważana publikacja materiału o wysokiej stawce | X.10 | Kontradyktoryjny przegląd (ang. adversarial review), progi dowodowe, redakcja danych wrażliwych |
| 25 | Eskalacja działań naprawczych | X.9 | Schodkowo: weryfikacja -> korekta -> zgłoszenie -> audyt -> publikacja |

## Zmiany i wyjątki

| # | Sytuacja | Artykuły | Zasada / Działanie |
| :--- | :--- | :--- | :--- |
| 26 | Ktoś proponuje wyjątek od reguły | XIV.3, XIV.4 | Wyjątek wymaga: policy-id, reason, risk-level, expiry, owner, stanu bezpiecznego domknięcia (ang. fail-closed) |
| 27 | Wyjątek generuje sygnały krzywdy lub nadużycia | XIV.5 | Automatyczne zawieszenie wyjątku do wyjaśnienia |
| 28 | Propozycja zmiany Konstytucji | XIII.7-XIII.11, XVI.5, XVI.6, XVI.10 | Jawne uzasadnienie, analiza skutków, odwracalność; w okresie założycielskim decyzja założycieli ma moc rozstrzygającą |
| 29 | Polityka lokalna próbuje obejść Konstytucję | XVI.7 | Niedopuszczalne bez formalnej zmiany konstytucyjnej |
