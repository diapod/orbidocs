# Hierarchia normatywna dokumentów DIA

> **Projekt zmiany.** Zob. [tryb przyjęcia i przepisy przejściowe](../../40-constitution/pl/COMMUNITY-SELF-GOVERNMENT-AMENDMENT.pl.md).

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-NORM-HIER-001` |
| `typ` | Uzupełnienie sekcji "Moc normatywna i wykładnia" Konstytucji |
| `wersja` | 0.2.0-draft |
| `autor` | DIA / Orbiplex |
| `data` | 2026-03-10 |

---

## 1. Cel dokumentu

Niniejszy dokument precyzuje hierarchię normatywną dokumentów projektu DIA/Orbiplex,
rozstrzygając niejednoznaczność co do mocy wiążącej poszczególnych źródeł. Stanowi
propozycję rozszerzenia sekcji "Moc normatywna i wykładnia" Konstytucji (punkty 4-6).

---

## 2. Hierarchia normatywna

Dokumenty projektu tworzą następujące poziomy mocy normatywnej. Dokument niższego
poziomu nie może osłabiać, zawężać ani reinterpretować dokumentu wyższego poziomu
bez formalnej procedury zmiany odpowiedniego poziomu.

### Poziom 0 - Rdzeń nienegocjowalny

Klauzule wskazane bezpośrednio w sekcji "Rdzeń nienegocjowalny" Konstytucji.
Kanoniczny, maszynowo odczytywalny wykaz utrzymuje
`doc/normative/40-constitution/constitution-index.v1.json`. Ich zmiana,
zawieszenie lub reinterpretacja zawężająca wymaga procedury opisanej w
`ENTRENCHMENT-CLAUSE.pl.md`, w tym jednomyślności wszystkich federacji
uczestniczących w procesie zmiany oraz niezależnego kontradyktoryjnego przeglądu
(ang. adversarial review). Akt wykonawczy określa procedurę, lecz NIE MOŻE zmieniać
składu Poziomu 0.

### Poziom 1 - Konstytucja

Pozostałe artykuły dokumentu `doc/normative/40-constitution/pl/CONSTITUTION.pl.md`. Zmiana wymaga procedury
opisanej w Art. XVI: jawne uzasadnienie, analiza skutków, opis odwracalności, ślad
procesu decyzyjnego, okres próbny dla zmian o wysokiej stawce.

### Poziom 2 - Źródła wykładni

Dokumenty `doc/normative/30-core-values/pl/CORE-VALUES.pl.md` oraz
`doc/normative/20-vision/pl/VISION.pl.md`.

Służą interpretacji Konstytucji, ale **nie tworzą nowych obowiązków ani uprawnień**
wykraczających poza ramy Konstytucji. Sekcje tych dokumentów dzielą się na dwie
kategorie:

- **`[wartość]`** - wyrażenie zasady etycznej lub architektonicznej; ma moc
  wykładniczą przy interpretacji Konstytucji.
- **`[mechanizm - hipoteza]`** - opis proponowanego mechanizmu (np. Creator Credits,
  attribution graph, krzywe reputacji); nie ma mocy normatywnej do czasu walidacji
  empirycznej i formalnego przyjęcia przez federację.

Zmiana dokumentów Poziomu 2 wymaga jawnego uzasadnienia i przeglądu spójności
z Konstytucją, ale **nie wymaga pełnej procedury zmiany konstytucyjnej**.

`doc/normative/90-supplementary/pl/ONTOLOGICAL-BASIS.pl.md` oraz
`doc/normative/90-supplementary/pl/ECONOMY-OF-AGENTIC-MUTUALITY.pl.md` są materiałami
objaśniającymi genezę i spójność wartości oraz przyjętej syntezy
społeczno-ekonomicznej. Nie stanowią samodzielnych źródeł wykładni Poziomu 2 ani nie
tworzą praw, obowiązków lub klasyfikacji osób. Nie mogą służyć jako test
światopoglądowy, lojalnościowy, członkowski, tożsamościowy ani reputacyjny. W razie
rozbieżności pierwszeństwo mają Konstytucja i źródła Poziomu 2.

### Poziom 3 - Ustawy wykonawcze

Rejestr wskazuje akty projektu. Każdy stosuje się na zasadach jego przyjęcia i wejścia w
życie, wobec projektu w granicach jego mandatu lub wobec stron w zakresie jawnie podjętego
zobowiązania. Poza tym zakresem akt może służyć jako wzorzec.

- `AUTONOMY-LEVELS.pl.md` - gradient autonomii agentów
- `ABUSE-DISCLOSURE-PROTOCOL.pl.md` - próg, zakres i procedura warunkowej jawności
  odpowiedzialności za nadużycia
- `EXCEPTION-POLICY.pl.md` - procedura, model danych i monitoring wyjątków
- `FEDERATION-MEMBERSHIP-AND-QUORUM.pl.md` - operacyjne umocowanie korzenia zaufania,
  definicja federacji uprawnionej do głosu, statusów aktywności oraz reguł quorum i veta
- `ROOT-IDENTITY-AND-NYMS.pl.md` - model tożsamości pierwotnej, nymów,
  poziomów pewności i delegacji między urządzeniami
- `IDENTITY-ATTESTATION-AND-RECOVERY.pl.md` - pierwsze poświadczenie,
  pamięć wcześniejszego poświadczenia, fraza odzyskiwania i rekonstrukcja
  `anchor-identity`
- `ATTESTATION-PROVIDERS.pl.md` - mapowanie metod poświadczenia na klasy
  `weak` / `strong` i maksymalne poziomy `IAL`
- `IDENTITY-UPGRADE-ANOMALY-SIGNALS.pl.md` - minimalny katalog sygnałów
  anomalii, reakcji i review dla upgrade poświadczenia, zwłaszcza `phone -> strong`
- `IDENTITY-UNSEALING-BOARD.pl.md` - Federacja Izb Pieczęciowych, progi
  `nym -> node-id` i `node-id -> root-identity`, quorum oraz split-knowledge
- `UNSEAL-CASE-MODEL.pl.md` - wspólny model danych sprawy odpieczętowania
  dla progów `U1-U3`
- `ROLE-TO-IAL-MATRIX.pl.md` - minimalna mapa klas ról do poziomów `IAL`
  i reguł `fixed_power_bonus`
- `FIP-MEMBERSHIP-AND-QUORUM.pl.md` - członkostwo, aktywność i quorum
  Federacji Izb Pieczęciowych
- `MEMBERSHIP-AND-SPONSORSHIP-POLICY.pl.md` - polityka wejścia per powierzchnia,
  zakres sponsoringu, probation, odpowiedzialność sponsora, slow-start
  newcomerów i hamulce przeciw sponsor-ring
- `PARTICIPANT-COVENANT.pl.md` - krótkie przymierze operacyjne wejścia na
  wspólne powierzchnie wpływu
- `PROCEDURAL-REPUTATION-SPEC.pl.md` - specyfikacja domen, sygnałów i przeliczania
  reputacji proceduralnej
- `ADVOCACY-AND-SOLICITATION-POLICY.pl.md` - wymogi opt-in, ujawnienia i sankcje
  dla powierzchni perswazji oraz akwizycji
- `MARKETPLACE-ANTI-FRAUD-POLICY.pl.md` - limity wartości, oczekiwania escrow,
  reguły antyfraudowe i podstawa reputacji dla powierzchni marketplace
- `RAW-SIGNAL-POLICY.pl.md` - ochrona surowego sygnału, tryby transformacji stylu,
  metaznaczniki i ślad audytowy
- `UNIVERSAL-BASIC-COMPUTE.pl.md` - minimalny model Proof-of-Personhood,
  nieodbieralne minimum compute, ograniczona trans-federacyjność i rozliczenia UBC
- `UBC-LIMIT-PROFILES.pl.md` - kanoniczne profile limitów UBC, profile
  przenośności i minimalny most/rejestr FIP dla trans-federacyjnego PoP
- `SWARM-ECONOMY-SUFFICIENCY.pl.md` - próg dostatku, hamulce koncentracji,
  wspólny obieg nadwyżek i bariera między nagrodą a władzą proceduralną
- `PANEL-SELECTION-PROTOCOL.pl.md` - procedura kwalifikacji, losowania, veta i
  uzupełniania składu panelu ad-hoc
- `REPUTATION-VALIDATION-PROTOCOL.pl.md` - protokół walidacji mechanizmów reputacyjnych
- `ENTRENCHMENT-CLAUSE.pl.md` - procedura obrony konstytucyjnej i klauzula wieczności
- `ORBIPLEX-MAIN-ROOT-CHARTER.pl.md` - przyjęta karta 0.1.0 korzenia technicznego
  `orbiplex-main`. Zmiana karty i aktywacja produkcyjna to odrębne decyzje.

Kolejne akty wpisuje się z podstawą przyjęcia i zakresem. Sam projekt, wpis lub ścieżka
pliku nie wprowadzają aktu w życie.

Ustawy wykonawcze konkretyzują Konstytucję i Źródła wykładni. MOGĄ **zaostrzać**
wymogi, ale NIE MOGĄ osłabiać żadnego wyższego poziomu.

### Poziom 4 - Polityki federacyjne

Parametry, konfiguracje i reguły lokalne poszczególnych federacji. Obejmują:

- progi reputacyjne,
- parametry mechanizmów nagradzania,
- lokalne rozszerzenia ról,
- konfiguracje trybów (normalny / kryzysowy / pomocowy).

Poziom 4 obejmuje lokalne wykonanie zobowiązań w granicach ich wyraźnego przyjęcia.
Konstytucja społeczności ma własne źródło mocy i pozostaje poza tą hierarchią. O mocy i
pierwszeństwie postanowień włączonych z zewnątrz rozstrzyga lokalny akt przyjęcia.

### Poziom 5 - Materiały pochodne i wdrożeniowe (ang. onboarding)

Dokumenty pomocnicze, które **nie mają własnej mocy normatywnej**, lecz streszczają,
mapują albo ułatwiają korzystanie z dokumentów wyższych poziomów. Obejmują:

- `NODE-RIGHTS-CARD.pl.md` - wyciąg z praw i obowiązków węzła wraz z indeksem decyzyjnym,
- listy kontrolne wdrożeniowe (ang. onboarding),
- mapy procesów,
- skróty operacyjne i materiały szkoleniowe.

Dokument Poziomu 5:

- nie może tworzyć nowych obowiązków ani uprawnień,
- w razie rozbieżności przegrywa z dokumentem źródłowym,
- powinien wskazywać źródło każdego twierdzenia przez artykuł lub dokument bazowy.

---

## 3. Zasady rozstrzygania kolizji

1. Najpierw ustal zakres obowiązywania (Konstytucja, Moc normatywna 6 i 12-16). Jeżeli obie
   reguły dotyczą tej samej sprawy projektu, pierwszeństwo ma poziom wyższy.
2. W razie sprzeczności w ramach tego samego poziomu - stosuje się procedurę z Art.
    XIV Konstytucji (test odwracalności, proporcjonalności, jawności).
3. Teksty Konstytucji mają równą moc zgodnie z `const:norm.11`. Rozbieżności wymagają
   uzgodnienia wersji. W pozostałych aktach DIA objętych tą hierarchią pierwszeństwo ma
   wersja polska, chyba że rozbieżność wynika z błędu tłumaczenia lub akt stanowi inaczej.
4. Dokument niższego poziomu, który faktycznie narusza wyższy poziom, jest **nieważny
    w zakresie naruszenia** od momentu stwierdzenia naruszenia, nie od momentu
    publikacji.

---

## 4. Procedura oznaczania sekcji w Źródłach wykładni

Każda sekcja `doc/normative/30-core-values/pl/CORE-VALUES.pl.md` i
`doc/normative/20-vision/pl/VISION.pl.md` POWINNA zawierać w nagłówku tag:

```md
### Nazwa sekcji `[wartość]`
```

lub

```md
### Nazwa sekcji `[mechanizm - hipoteza]`
```

Sekcje nieoznaczone są domyślnie traktowane jako `[wartość]`, chyba że opisują
konkretny algorytm, parametr liczbowy lub schemat tokenowy - wówczas domyślnie
`[mechanizm - hipoteza]`.

---

## 5. Wejście w życie

Niniejszy dokument wchodzi w życie po formalnym przyjęciu zgodnie z procedurą zmiany
Konstytucji (Art. XVI), ponieważ modyfikuje sekcję "Moc normatywna i wykładnia".
