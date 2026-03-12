# Hierarchia normatywna dokumentów DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-NORM-HIER-001` |
| `typ` | Uzupełnienie sekcji "Moc normatywna i wykładnia" Konstytucji |
| `wersja` | 0.1.0-draft |
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

Artykuły Konstytucji wymienione w klauzuli wieczności (patrz:
`ENTRENCHMENT-CLAUSE.pl.md`). Ich zmiana, zawieszenie lub reinterpretacja zawężająca
wymaga jednomyślności wszystkich federacji uczestniczących w procesie zmiany oraz
niezależnego kontradyktoryjnego przeglądu (ang. adversarial review).

Rdzeń nienegocjowalny obejmuje co najmniej:

- Art. I.5 - żaden cel operacyjny ani finansowy nie unieważnia godności,
  bezpieczeństwa i prawa do wyjścia.
- Art. II.1-3 - godność, ochrona życia, moc systemu przechodzi przez człowieka.
- Art. III.1-5 - suwerenność danych, lokalny tryb domyślny (ang. local-first),
  eksport, prawo do wyjścia, prawo do odgałęzienia (ang. fork).
- Art. XIV.1 - domyślna hierarchia wartości.

### Poziom 1 - Konstytucja

Pozostałe artykuły dokumentu `../CONSTITUTION.pl.md`. Zmiana wymaga procedury
opisanej w Art. XVI: jawne uzasadnienie, analiza skutków, opis odwracalności, ślad
procesu decyzyjnego, okres próbny dla zmian o wysokiej stawce.

### Poziom 2 - Źródła wykładni

Dokumenty `../core-values/CORE-VALUES.pl.md`, `../core-values/CORE-VALUES.en.md`
oraz `../VISION.pl.md`.

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

### Poziom 3 - Ustawy wykonawcze

Dokumenty operacyjne o mocy wiążącej w ramach federacji:

- `AUTONOMY-LEVELS.pl.md` - gradient autonomii agentów
- `ABUSE-DISCLOSURE-PROTOCOL.pl.md` - próg, zakres i procedura warunkowej jawności
  odpowiedzialności za nadużycia
- `EXCEPTION-POLICY.pl.md` - procedura, model danych i monitoring wyjątków
- `FEDERATION-MEMBERSHIP-AND-QUORUM.pl.md` - definicja federacji uprawnionej do głosu,
  statusów aktywności oraz reguł quorum i veta
- `ROOT-IDENTITY-AND-NYMS.pl.md` - model tożsamości pierwotnej, nymów,
  poziomów pewności i delegacji między urządzeniami
- `IDENTITY-ATTESTATION-AND-RECOVERY.pl.md` - pierwsze poświadczenie,
  pamięć wcześniejszego poświadczenia, fraza odzyskiwania i rekonstrukcja
  `anchor-identity`
- `PROCEDURAL-REPUTATION-SPEC.pl.md` - specyfikacja domen, sygnałów i przeliczania
  reputacji proceduralnej
- `PANEL-SELECTION-PROTOCOL.pl.md` - procedura kwalifikacji, losowania, veta i
  uzupełniania składu panelu ad-hoc
- `REPUTATION-VALIDATION-PROTOCOL.pl.md` - protokół walidacji mechanizmów reputacyjnych
- `ENTRENCHMENT-CLAUSE.pl.md` - procedura obrony konstytucyjnej i klauzula wieczności
- inne dokumenty polityk zapisanych w kodzie (ang. `policy-as-code`) lub dokumenty
  wykonawcze z katalogu `constitutional-ops/`, które jawnie wskazują swój typ i
  podstawę konstytucyjną

Ustawy wykonawcze konkretyzują Konstytucję i Źródła wykładni. Mogą **zaostrzać**
wymogi (np. w trybie `CORP_COMPLIANT`), ale **nie mogą osłabiać** żadnego wyższego
poziomu.

### Poziom 4 - Polityki federacyjne

Parametry, konfiguracje i reguły lokalne poszczególnych federacji. Obejmują:

- progi reputacyjne,
- parametry mechanizmów nagradzania,
- lokalne rozszerzenia ról,
- konfiguracje trybów (normalny / kryzysowy / pomocowy).

Polityki federacyjne są autonomiczne w zakresie niepokrywającym się z wyższymi
poziomami. Federacja może je swobodnie kształtować, o ile nie naruszają Poziomów 0-3.

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

1. W razie sprzeczności między poziomami - poziom wyższy ma pierwszeństwo.
2. W razie sprzeczności w ramach tego samego poziomu - stosuje się procedurę z Art.
   XIV Konstytucji (test odwracalności, proporcjonalności, jawności).
3. W razie sprzeczności między wersjami językowymi tego samego dokumentu -
   pierwszeństwo ma wersja polska, o ile nie wykazano, że rozbieżność wynika z błędu
   tłumaczenia.
4. Dokument niższego poziomu, który faktycznie narusza wyższy poziom, jest **nieważny
   w zakresie naruszenia** od momentu stwierdzenia naruszenia, nie od momentu
   publikacji.

---

## 4. Procedura oznaczania sekcji w Źródłach wykładni

Każda sekcja `../core-values/CORE-VALUES.pl.md`,
`../core-values/CORE-VALUES.en.md` i `../VISION.pl.md` POWINNA zawierać w nagłówku
tag:

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
