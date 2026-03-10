# Karta Praw i Obowiązków Węzła DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-NODE-CARD-001` |
| `typ` | Wyciąg z Konstytucji - materiał onboardingowy |
| `wersja` | 0.1.0-draft |
| `źródło` | Art. II, III, XV, XVI Konstytucji DIA |

---

## Twoje prawa jako węzła

| Prawo | Co oznacza | Konstytucja |
| :--- | :--- | :--- |
| **Prawo do wyjścia** | Możesz opuścić federację w dowolnym momencie, bez szantażu, bez utraty dostępu do własnych danych, bez ukrytych kar. | Art. III.4 |
| **Prawo do prywatności** | Telemetria jest domyślnie wyłączona. Twoje dane są lokalne. Ujawnianie jest selektywne i wymaga Twojej zgody. | Art. III.7, III.8 |
| **Prawo do wglądu** | Możesz audytować interakcje swoich agentów, ślady decyzji i historię działań. | Art. XV.2 |
| **Prawo do odwołania** | Każdą decyzję reputacyjną lub sankcję możesz zakwestionować procedurą odwoławczą. | Art. XV.2, XVI.2 |
| **Prawo do bezpieczeństwa** | System chroni Cię przed nękaniem, doxxingiem, sabotażem i ekonomicznym wymuszaniem. | Art. XV.2 |
| **Prawo do lokalnej autonomii** | Możesz prowadzić węzeł "w ciszy": prywatnie, lokalnie, bez uczestnictwa w przestrzeniach publicznych. | Art. III.6 |
| **Prawo do forka** | Możesz skopiować specyfikacje, polityki i otwarte komponenty bez proszenia o zgodę centrum. | Art. III.5 |
| **Prawo do suwerenności danych** | Jesteś właścicielem swoich danych, polityk, agentów i lokalnych przestrzeni pamięci. Eksport w otwartych formatach jest gwarantowany. | Art. III.1, III.3 |

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
Ostrzeżenie -> Ograniczenie uprawnień -> Kwarantanna reputacyjna -> Odcięcie routingu
```

Każda sankcja zostawia ślad, daje możliwość odwołania i otwiera ścieżkę powrotu po
naprawie (Art. XVI.1-2).

---

**Pełna Konstytucja:** `../CONSTITUTION.pl.md`  
**Wartości i wykładnia:** `../core-values/CORE-VALUES.pl.md`  
**Wizja projektu:** `../VISION.pl.md`  
**Gradient autonomii agentów:** `AUTONOMY-LEVELS.pl.md`

---
---

# Indeks decyzyjny - od sytuacji do artykułu

Poniższa tabela mapuje najczęstsze sytuacje operacyjne na odpowiednie artykuły
Konstytucji i kluczowe zasady. Służy jako "router" - nie zastępuje lektury
Konstytucji, ale pozwala szybko znaleźć właściwą normę.

## Prawa i suwerenność użytkownika

| # | Sytuacja | Artykuły | Zasada / Działanie |
| :--- | :--- | :--- | :--- |
| 1 | Użytkownik chce zabrać swoje dane i odejść | III.3, III.4 | Eksport w otwartych formatach, bez szantażu i ukrytych kar |
| 2 | Użytkownik chce uruchomić węzeł offline | III.2, III.6 | System MUSI działać sensownie local-first i self-hosted |
| 3 | Użytkownik chce sforkować projekt | III.5 | Prawo do forka: specyfikacje, polityki, otwarte komponenty |
| 4 | Ktoś włączył telemetrię bez zgody użytkownika | III.7 | Telemetria domyślnie wyłączona; wymaga jasnej, odwoływalnej zgody |

## Agenty i autonomia

| # | Sytuacja | Artykuły | Zasada / Działanie |
| :--- | :--- | :--- | :--- |
| 5 | Agent podjął decyzję bez wiedzy użytkownika | II.3, II.4, V.10 | Moc przechodzi przez człowieka; domyślnie propozycje i warianty |
| 6 | Agent przekroczył budżet / czas / zakres | V.10, AUTONOMY-LEVELS.pl.md | Agent MUSI mieć kill-switch, limity uprawnień, czasu i kosztu |
| 7 | Agent eskalował sobie uprawnienia | V.13, AUTONOMY-LEVELS.pl.md | Zero self-authorize; błąd agenta nie może automatycznie eskalować uprawnień |
| 8 | Agent działa w sytuacji zagrożenia życia | II.8, IX.3, AUTONOMY-LEVELS.pl.md | MOŻE działać szybciej, ale zostawia ślad i podlega rewizji |

## Finansowanie i capture

| # | Sytuacja | Artykuły | Zasada / Działanie |
| :--- | :--- | :--- | :--- |
| 9 | Sponsor żąda uprzywilejowanego dostępu do danych | VIII.2 | Zakaz - finansowanie nie kupuje dostępu do danych, routingu, governance |
| 10 | Jedna zależność stała się krytyczna (model, infra, funding) | VIII.5 | Obowiązkowy plan dywersyfikacji |
| 11 | Napięcie między finansowaniem a integralnością konstytucyjną | VIII.7 | Integralność konstytucyjna ma pierwszeństwo |
| 12 | Model przychodowy oparty na uzależnianiu użytkownika | VIII.3, II.7 | Zakaz dopaminowego UX i ekonomii opartej na przytrzymywaniu |

## Reputacja i governance

| # | Sytuacja | Artykuły | Zasada / Działanie |
| :--- | :--- | :--- | :--- |
| 13 | Węzeł kwestionuje decyzję reputacyjną | XV.5, XVI.2 | Kontr-dowód lub wykazanie błędu proceduralnego; prawo do odwołania |
| 14 | Brak ujawnienia konfliktu interesów | VII.6 | COI-by-default: brak deklaracji = brak danych, nie brak konfliktu |
| 15 | Osoba pełni jednocześnie rolę strony i arbitra | VII.3 | Uprawnienia krytyczne MUSZĄ być rozdzielone między role |
| 16 | Decyzja o wysokiej stawce | VII.9 | Multisig + niezależny red-team |

## Bezpieczeństwo i kryzys

| # | Sytuacja | Artykuły | Zasada / Działanie |
| :--- | :--- | :--- | :--- |
| 17 | Podejrzenie Sybil / DoS / prompt injection | IX.1, IX.2 | Model zagrożeń jest częścią architektury, nie ozdobą |
| 18 | Sytuacja kryzysowa (blackout, konflikt) | IX.3, IX.4 | Tryb kryzysowy: wyższy rygor, redundancja, lokalność, jakość śladów |
| 19 | Węzeł częściowo odcięty od sieci | IX.5 | Węzeł POWINIEN zachowywać zdolność działania w częściowej izolacji |
| 20 | Potrzeba emergency cache (schronienie, żywność, triage) | IX.6, IX.7 | Memarium może utrzymywać przestrzenie kryzysowe |

## Sygnaliści i publikacja

| # | Sytuacja | Artykuły | Zasada / Działanie |
| :--- | :--- | :--- | :--- |
| 21 | Ktoś chce zgłosić nadużycie anonimowo | X.1, X.2 | Anonimowość domyślna, minimalizacja metadanych, triage sygnałów |
| 22 | Sygnalista narażony na odwet | X.3 | Opieka roju jest częścią infrastruktury, nie gestem moralnym |
| 23 | Rozważana publikacja materiału o wysokiej stawce | X.5 | Adversarial review, progi dowodowe, redakcja danych wrażliwych |
| 24 | Eskalacja działań naprawczych | X.4 | Schodkowo: weryfikacja -> korekta -> zgłoszenie -> audyt -> publikacja |

## Zmiany i wyjątki

| # | Sytuacja | Artykuły | Zasada / Działanie |
| :--- | :--- | :--- | :--- |
| 25 | Ktoś proponuje wyjątek od reguły | XIV.3, XIV.4 | Wyjątek wymaga: policy-id, reason, risk-level, expiry, owner, fail-closed |
| 26 | Wyjątek generuje sygnały krzywdy lub nadużycia | XIV.5 | Automatyczne zawieszenie wyjątku do wyjaśnienia |
| 27 | Propozycja zmiany Konstytucji | XIII.7-XIII.11, XVI.5, XVI.6, XVI.10 | Jawne uzasadnienie, analiza skutków, odwracalność; w okresie założycielskim decyzja założycieli ma moc rozstrzygającą |
| 28 | Polityka lokalna próbuje obejść Konstytucję | XVI.7 | Niedopuszczalne bez formalnej zmiany konstytucyjnej |
