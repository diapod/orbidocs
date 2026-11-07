# Propozycja 026: Opinie o zasobach i powierzchnie dyskusji

<a id="proposal-026-resource-opinions-and-discussion-surfaces"></a>

Based on:
- `doc/project/20-memos/resource-opinions-and-discussion.md`
- `doc/project/20-memos/reputation-signal-v1-invariants.md`
- `doc/project/20-memos/orbiplex-whisper.md`

## Status {#status}

Przyjęta. P026-001–003 są zaimplementowane i zakwalifikowane w runtime na dzień
2026-10-12: wspólne autorstwo otwartych referencji, odczyt opinii wyłącznie według
pary i odzyskiwalna odbudowa domenowa, z zachowanymi dowodami SQLite i Matrix.
Bogate powierzchnie dyskusji oraz nawigacja Agora P17 pozostają przyszłą pracą;
kwalifikacja nie ustanawia gotowości produkcyjnej ani federacji między homeserverami.

Kontynuacja ekspozycji ocen ma ograniczony pilotaż na lokalnym SQLite,
zakwalifikowany 2026-10-24 zgodnie z poniższym lokalnym checkpointem dowodowym.
Zamrożenie kontraktu, implementacja, ukierunkowane testy komponentów i rzeczywista
akceptacja hosta/przeglądarki to osobne twierdzenia. Szersza kontynuacja konsumencka
pozostaje częściowa; rundy zamknięte są planowane. Kwalifikacja P026-001–003
zachowuje pierwotny zakres.

Bieżący status lokalnej kontynuacji (2026-11-01): P026-012c-01 i wspólne 02/03
są zakwalifikowane wyłącznie w swoich przypiętych profilach. Poniższe domknięcie
wszystkich właścicieli dodaje trwałe S029, kapsuły/checkpointy i S020; proweniencja
kontekstu i późniejsze profile pozostają otwarte, a nadrzędne P026-012c/P073
pozostają częściowe. Wcześniejsze datowane checkpointy opisują pierwotne rewizje
historyczne.

## Data {#date}

2026-04-10

## Streszczenie {#executive-summary}

Orbiplex ma pojęcia zaufania i sygnałów zorientowanych na podmioty. Ta propozycja
definiuje przenośny sposób hard-MVP wyrażania przez uczestników opinii o dowolnych
zasobach, takich jak:

- URL,
- produkt identyfikowany przez EAN,
- węzeł,
- organizacja w roju,
- miejsce identyfikowane współrzędnymi GPS,
- przyszły artefakt publikacji,
- inny obiekt, do którego można odwołać się z zewnątrz.

Propozycja wprowadza mały artefakt MVP:

- `resource-opinion.v1`

Najważniejsze decyzje:

1. zasób docelowy jest identyfikowany parą `resource/kind` i `resource/id`,
2. kanoniczny klucz pochodny to `resource/kind + ":" + resource/id`,
3. tożsamość przedmiotu opinii, autorstwo i czas przenosi otaczająca koperta
   (`agora-record.v1` `record/about[0]`, `author/participant-id`, `authored/at`);
   samo `resource-opinion.v1` jest schematem treści i **nie** duplikuje tych pól,
4. opinia niesie opcjonalne `opinion/text` i może dodawać `opinion/lang`,
   `opinion/tags`, pięciopunktową `opinion/rating` w `1..5` (z `0` lub brakiem
   oznaczającym brak oceny) i pola relacyjne (`opinion/in-reply-to`,
   `opinion/related`, `opinion/see-also`); schemat pozostaje otwarty na rozszerzenia
   w przestrzeniach nazw właściwe dla rodzaju, takie jak `rumor/credibility`
   i `rumor/rejection-reason`,
5. artefakty opinii o zasobach pozostają odrębne od reputacji uczestnika lub węzła,
6. późniejsza powierzchnia dyskusji może wiązać się z tym samym kanonicznym kluczem
   zasobu, ale wątki dyskusji i semantyka forum nie należą do artefaktu opinii hard-MVP.

Dzięki temu rdzeń pozostaje mały:

- tożsamość zasobu pozostaje generyczna,
- wyrażanie opinii pozostaje tanie,
- bogatsza semantyka dyskusji może rozwijać się później, bez wymuszania dużego
  pierwszego schematu.

## Kontekst i problem {#context-and-problem-statement}

Orbiplex ma już pojęcia:

- tożsamości podmiotu,
- sygnałów o charakterze reputacyjnym,
- wymiany sygnałów społecznych,
- widocznych w protokole artefaktów publikacji.

Brakuje warstwy ocen skierowanej ku zasobom.

Bez takiej warstwy:

- opinie o zewnętrznych zasobach pozostają lokalne dla aplikacji,
- nie ma wspólnego kontraktu prostych śladów ocen lub rekomendacji,
- każda przyszła funkcja dyskusji o zasobach musiałaby od podstaw wymyślić własny
  model tożsamości przedmiotu dyskusji.

Zasoby docelowe mogą być niejednorodne. Na przykład:

- `url:https://example.org/article`
- `ean:5901234123457`
- `node:node:did:key:z6MkExampleNode`
- `org:org:did:key:z6MkExampleOrg`
- `gps:51.107883,17.038538`

Model tożsamości musi więc pozostać generyczny i nie zakładać jednej globalnej
ontologii zasobów.

## Cele {#goals}

- Zdefiniować jeden minimalny, przenośny artefakt opinii o zasobie autorstwa uczestnika.
- Zamrozić regułę tożsamości zasobu opartą na `resource/kind` i `resource/id`.
- Dopuścić wyrażanie słowne i skalarne.
- Zachować czystą ścieżkę rozszerzenia o powierzchnie dyskusji związane z zasobem.
- Oddzielić semantykę od reputacji i sankcji.

## Poza zakresem {#non-goals}

- Propozycja nie definiuje końcowego modelu moderacji.
- Nie definiuje schematów forum, kanałów ani komentarzy w wątkach.
- Nie definiuje algorytmów odkrywania, rankingu ani rekomendacji zasobów.
- Nie definiuje jednego globalnego rejestru poprawnych wartości `resource/kind`.
- Nie definiuje polityki delegowania agentów AI poza zachowaniem miejsca na jawne
  etykietowanie autorstwa w przyszłych artefaktach dyskusji.

## Decyzja {#decision}

### 1. Tożsamość zasobu {#1-resource-identity}

Każdy przedmiot opinii MUSI być identyfikowany przez:

- `resource/kind`
- `resource/id`

Kanoniczny klucz pochodny to:

- `resource/key = resource/kind + ":" + resource/id`

Reguły:

- `resource/id` MUSI być traktowane jako nieprzezroczyste w obrębie swojego rodzaju,
- konsumenci MUSZĄ dzielić `resource/key` tylko po pierwszym `:`,
- żaden konsument nie może zakładać semantyki URI dla `resource/id`, chyba że
  kontrakt rodzaju jawnie ją określa.

Jest to konieczne, ponieważ niektóre identyfikatory, np. URL-e, już zawierają `:`.

Typowe początkowe rodzaje zasobów MOGĄ obejmować:

- `url`
- `ean`
- `node`
- `org`
- `gps`

Dla `node` i `org` pole `resource/id` powinno używać kanonicznych identyfikatorów
widocznych w protokole. Dla `gps` pole `resource/id` pozostaje w tej propozycji nieprzezroczyste;
późniejszy kontrakt rodzaju powinien zamrozić kolejność współrzędnych, precyzję
i reguły prywatności.

#### 1.1. Przestrzenie nazw identyfikatorów o zakresie krajowym {#11-country-scoped-identifier-namespaces}

Rodzaj zasobu MOŻE wskazywać krajową przestrzeń nazw identyfikatorów przez
zapisany małymi literami kod kraju ISO 3166-1 alpha-2, po którym następuje
jednoznaczna nazwa systemu identyfikacji, rozdzielona łącznikami:
`<country>-<scheme>`. Gdy sama nazwa systemu jest niejednoznaczna, należy dodać
kwalifikator rejestru, np. `pl-nil-pwz` dla numerów PWZ w polskim Centralnym
Rejestrze Lekarzy i Lekarzy Dentystów. Jest to konwencja nazewnicza Orbipleksu,
a nie twierdzenie, że wynikowy slug jest oficjalnym zewnętrznym kodem systemu
identyfikacji.

Przykładowa referencja zasobu i jej klucz pochodny:

```json
{
  "resource/kind": "pl-nil-pwz",
  "resource/id": "<pwz-number>"
}
```

```text
pl-nil-pwz:<pwz-number>
```

`<pwz-number>` jest symbolem zastępczym w dokumentacji, nie wydanym numerem ani
numerem zwalidowanym domenowo. Przykład ustanawia konwencję przestrzeni nazw;
nie deklaruje zaimplementowanego wyszukiwania w rejestrze ani walidatora PWZ.

Następujące inwarianty zachowują generyczny kontrakt zasobu:

- Całe `resource/kind` jest kluczem przestrzeni nazw. Generyczni konsumenci NIE
  MOGĄ wywodzić autorytetu ani parsować części rozdzielonych łącznikami.
  Kwalifikatory krajowe opisują jurysdykcję systemu identyfikacji, nie narodowość,
  miejsce zamieszkania ani bieżące położenie posiadacza.
- Rodzaje pozostają otwartym katalogiem. Operatorzy i wspólnoty MOGĄ proponować
  nowe kontrakty rodzajów; konwencja nie wprowadza globalnej allowlisty ani nie
  wymaga prefiksów krajowych dla istniejących lub międzynarodowych rodzajów.
  Nieznane rodzaje pozostają nieprzezroczyste według kontraktu generycznego,
  podlegając zwykłej polityce admisji i ujawniania; NIE WOLNO ich po cichu
  mapować do znanej przestrzeni nazw.
- Kontrakt rodzaju MUSI wskazywać właściwy system/rejestr, to, co identyfikują
  wartości (np. osobę, licencję, organizację lub wpis rejestru), reguły
  kanonikalizacji i walidacji oraz znaną semantykę ponownego przydziału lub
  aliasów. Dla interoperacyjności MOŻNA dokumentować oficjalne URI/OID
  przestrzeni nazw; są to mapowania, nie dodatkowe pola wymagane w każdej
  referencji zasobu.
- Wartości pozostają stringami. Normalizacja specyficzna dla kraju i rejestru,
  cyfry kontrolne i wyszukiwanie należą do opcjonalnych walidatorów lub adapterów
  rodzaju, nie do generycznego schematu, indeksu Agory ani rdzenia. Samo dodanie
  pola `country` nie rozstrzygnie istniejącego klucza, który używa tylko rodzaju
  i identyfikatora.
- Równość identyfikatorów ustanawia wspólną referencję w tej przestrzeni nazw,
  nie zweryfikowaną tożsamość między przestrzeniami, aktualne uprawnienie
  zawodowe, reputację ani prawdziwość twierdzenia. Identyfikowanie osoby przez
  publiczny rejestr samo w sobie nie upoważnia do ujawnienia ani publicznej
  agregacji.

Projekt podąża za rozdzieleniem przestrzeni nazw i wartości z
[FHIR Identifier](https://hl7.org/fhir/R5/datatypes.html#Identifier) oraz
precedensem jurysdykcji/kodu listy z
[org-id.guide](https://docs.org-id.guide/en/latest/metadata.html#assigning-a-code),
bez importowania ich pełnych modeli danych i katalogów do rdzenia.

#### 1.2. Referencje w opiniach i plotce {#12-references-in-opinions-and-gossip}

Opinia o takim zasobie zachowuje kwalifikowaną parę w `record/about[0]` koperty;
do treści nie dodaje się pola kraju ani kopii tożsamości. Publiczna plotka
(`public-gossip.v1`) MOŻE używać tej samej pary w opcjonalnym `record/about`
koperty. Żadne z tych zastosowań nie zmienia statusu epistemicznego rekordu.

Gdy `opinion/see-also` lub `gossip/see-also` wskazuje bezpośrednio ten sam zasób,
zwarta reprezentacja ma postać `["pl-nil-pwz", "<pwz-number>"]`: pierwszy element
krotki niesie pełną przestrzeń nazw, a drugi wyłącznie identyfikator, nie
pochodny `resource/key`. Istniejące rodzaje referencji do rekordów/tematów
zachowują własne kontrakty. Każda powierzchnia zachowuje obecne limity rozmiaru;
oba pola `see-also` ograniczają id do 512 znaków, podczas gdy `resource-ref.v1`
dopuszcza 2048. Most NIE MOŻE obcinać identyfikatora, by zmieścić go w limicie.

Opinia oceniająca pogłoskę nadal odwołuje się do rekordu pogłoski zgodnie
z [P013](013-whisper-social-signal-exchange.md), zamiast zastępować ten przedmiot
osobą lub zasobem w niej wspomnianym. `opinion/subject-kind` pozostaje wskazówką
wyboru overlayu, nie zamiennikiem referencji w kopercie.

### 2. `resource-opinion.v1` jako artefakt MVP {#2-resource-opinionv1-as-the-mvp-artifact}

Artefaktem MVP opinii autorstwa uczestnika jest treść koperty `agora-record.v1`:

- `schema = "resource-opinion.v1"`

#### 2.1. Rozdzielenie koperty i treści {#21-envelope-vs-content-separation}

Gdy opinia o zasobie jest publikowana na podłożu Agory (transport MVP, zob.
propozycję 035 i requirements-014 FR-001/FR-002/FR-011), tożsamość, autorstwo,
czas, referencja przedmiotu i kanoniczny identyfikator rekordu znajdują się
w **kopercie** (`agora-record.v1`), nie w treści:

| Zagadnienie | Miejsce |
|---|---|
| przedmiot opinii | `record/about[0] = {resource/kind, resource/id}` koperty |
| uczestnik będący autorem | `author/participant-id` koperty |
| znacznik czasu autorstwa | `authored/at` koperty |
| kanoniczny identyfikator rekordu | `record/id` koperty (wyprowadzony z kanonicznych podpisanych bajtów) |
| podpis | `signature` koperty |
| routing tematu | `topic/key` koperty (konwencjonalnie `ai.orbiplex.opinions/<resource-kind>`) |

Obiekt `content` koperty, walidowany przez `resource-opinion.v1`, niesie **tylko
słowny i skalarny wyraz** opinii. Dzięki temu warstwa podłoża pozostaje otwarta
na `resource/kind` (koperta przyjmuje dowolną wartość zgodną z kształtem
`resource-ref.v1`), a treść opinii pozostaje małym, przenośnym kształtem
niezależnym od routingu tożsamości.

#### 2.2. Pola treści {#22-content-body-fields}

Zalecane minimalne pola `resource-opinion.v1`:

- `schema`
- opcjonalne `opinion/text`
- opcjonalne `opinion/lang`
- opcjonalne `opinion/rating`
- opcjonalne `opinion/tags`
- opcjonalne `opinion/subject-kind`
- opcjonalne `opinion/in-reply-to`
- opcjonalne `opinion/related`
- opcjonalne `opinion/see-also`

Inwarianty przyjęcia (stosowane tylko do treści):

1. `opinion/text`, jeśli występuje, MUSI być niepustym stringiem. Opinia MOŻE
   nie mieć tekstu, jeśli niesie co najmniej jedno z pól `opinion/rating`,
   `opinion/in-reply-to`, `opinion/related`, `opinion/see-also` lub klucz
   rozszerzenia specyficznego dla rodzaju (zob. §2.4).
2. `opinion/rating`, jeśli występuje, MUSI być liczbą całkowitą w zakresie
   `0..5`. Wartości `1..5` kodują skalę pięciopunktową, w której `1` oznacza
   najsłabszą, a `5` najsilniejszą pozytywną ocenę. Wartość `0` jest jawnym
   znacznikiem „brak oceny” i semantycznie odpowiada nieobecności pola.
   Konsumenci NIE MOGĄ po cichu przeskalowywać ocen do innego zakresu ani
   przekształcać ich w sygnał reputacyjny.
3. `opinion/lang`, jeśli występuje, opisuje język `opinion/text`.
4. `opinion/tags`, jeśli występuje, jest tablicą niepustych stringów.
5. `opinion/subject-kind`, jeśli występuje, jest krótkim stringiem nazywającym
   rodzaj przedmiotu opinii (np. `rumor`, `url`, `gps-location`, `public-person`,
   `ean`). To wskazówka na poziomie payloadu do wyboru schematu overlayu;
   nie zastępuje `record/about` koperty.
6. `opinion/in-reply-to`, jeśli występuje, jest `record/id` innej opinii,
   na którą autor odpowiada bezpośrednio. Konsumenci MUSZĄ tolerować referencje
   bez dostępnego celu.
7. `opinion/related`, jeśli występuje, jest tablicą wartości `record/id`
   innych opinii, do których odnosi się ta opinia (wcześniejsze stanowiska,
   potwierdzające spojrzenia, jawne kontrasty). Relacja jest celowo luźna.
8. `opinion/see-also`, jeśli występuje, jest tablicą dwuelementowych wektorów
   `[kind, id]` wskazujących inne obiekty podlegające opiniowaniu (URL-e,
   pogłoski, zasoby, tożsamości). W odróżnieniu od `opinion/related` wpisy NIE
   są ograniczone do opinii.

Inwarianty związane z polami koperty (egzekwowane przez kontrakt koperty,
nie przez `resource-opinion.v1`):

5. `record/about` koperty MUSI zawierać co najmniej jeden wpis
   `{resource/kind, resource/id}`; pierwszy jest głównym przedmiotem indeksowania
   i agregacji
6. `author/participant-id` koperty MUSI identyfikować bezpośredniego autora-uczestnika
7. konsumenci NIE MOGĄ dzielić `resource/key` wyprowadzonego z pól koperty
   po żadnym `:` poza pierwszym

#### 2.3. Użycie samodzielne (bez koperty) {#23-standalone-non-envelope-usage}

Przy eksportach archiwalnych, migawkach offline lub mostach do systemów bez
koperty Agory odbiorca MOŻE przedstawić opinię jako płaski obiekt z polami
natywnymi dla koperty (`resource/kind`, `resource/id`, opcjonalne `resource/key`,
`author/participant-id`, `authored/at`, `record/id`) obok treści. Ta płaska postać
jest **projekcją** koperty i treści, nie drugim autorytatywnym schematem;
nie uzyskuje pól, których koperta już nie niesie.

#### 2.4. Rozszerzenia specyficzne dla rodzaju {#24-kind-specific-extensions}

`resource-opinion.v1` zachowuje `additionalProperties: true`. Schemat rdzeniowy
jest celowo minimalny; pola domenowe należą do kluczy rozszerzeń w przestrzeniach
nazw postaci `<kind>/<field>`, gdzie `<kind>` odpowiada selektorowi
`opinion/subject-kind` (jeśli obecny) albo rodzajowi głównego wpisu
w `record/about` koperty.

Reguły:

1. Każde pole spoza przestrzeni nazw `opinion/*` MUSI mieć postać
   `<kind>/<field>`. Płaskie klucze rozszerzeń bez prefiksu są zastrzeżone dla
   rdzenia i NIE MOGĄ być wprowadzane przez rozszerzenia.
2. Przestrzenie nazw są płaskimi stringami (bez zagnieżdżonych postaci
   `<kind>/<sub>/<field>`). W jednej opinii MOŻE współistnieć kilka rodzajów,
   ale jest to odradzane; kanoniczny wzorzec to jedno `opinion/subject-kind`
   i jedna pasująca przestrzeń nazw.
3. Klucze rozszerzeń waliduje **schemat overlayu** rejestrowany osobno od
   rdzenia (np. `rumor-opinion.overlay.v1`). Overlay waliduje tylko własną
   przestrzeń nazw; nie redefiniuje pól `opinion/*`. Konsumenci bez
   zainstalowanego overlayu nadal MUSZĄ przyjąć kopertę – nieznane klucze
   z przestrzeniami nazw zapewniają zgodność w przód.
4. Overlaye NIE MOGĄ zmieniać znaczenia żadnego pola `opinion/*`.
   W szczególności `opinion/rating` zawsze ma pięciopunktowe znaczenie
   z §2.2, niezależnie od rodzaju. Wymiary oceny specyficzne dla rodzaju
   (np. `rumor/credibility`) należą do przestrzeni nazw overlayu.

Konkretny overlay zdefiniowany w tej rodzinie propozycji:

- `rumor-opinion.overlay.v1` – używany, gdy `opinion/subject-kind` równa się
  `rumor`. Pola:
  - `rumor/credibility` – liczba całkowita `1..5` (opcjonalna). Niezależna od
    `opinion/rating`; koduje ocenę operatora dotyczącą wiarygodności pogłoski.
    `0` lub brak oznacza brak oceny wiarygodności.
  - `rumor/rejection-reason` – zamknięty enum (opcjonalny). Rozpoznawane
    wartości: `spam`, `policy-violation`, `off-topic`, `abusive`, `duplicate`,
    `fabricated`. Obecność dowolnej wartości jest sygnałem tłumienia dla
    polityki propagacji wychodzącej węzła (propozycja 013 §Kuracja pogłosek
    za pośrednictwem operatora).

Dalsze overlaye (np. `url-opinion.overlay.v1`,
`public-person-opinion.overlay.v1`, `gps-location-opinion.overlay.v1`) można
dodać jako osobne artefakty bez zmieniania rdzenia.

### 3. Opinie słowne, skalarne i relacyjne są równoprawne {#3-verbal-scalar-and-relational-opinion-are-all-first-class}

Opinia MOŻE być:

- wyłącznie słowna (tekst i język),
- wyłącznie oceną (bez tekstu, tylko `opinion/rating`),
- wyłącznie relacyjna (bez tekstu, tylko `opinion/in-reply-to`,
  `opinion/related` lub `opinion/see-also`),
- wyłącznie specyficzna dla rodzaju (bez tekstu, tylko pola overlayu,
  np. `rumor/rejection-reason`),
- dowolną kombinacją powyższych.

Pozwala to uniknąć dzielenia pierwszego schematu na osobne artefakty recenzji
tekstowej, gwiazdek i samych linków, zachowując minimalne przypadki użycia:

- „Chcę tylko ocenić ten element na 4/5”,
- „Chcę tylko zostawić komentarz po polsku”,
- „Chcę oznaczyć tę pogłoskę jako spam, niczego nie pisząc”,
- „Chcę tekst i ocenę oraz odsyłacz do powiązanej wcześniejszej opinii”.

### 4. Opinia o zasobie nie jest reputacją {#4-resource-opinion-is-not-reputation}

`resource-opinion.v1` MUSI pozostać semantycznie odrębne od:

- `reputation-signal.v1`,
- poziomu pewności dotyczącego uczestnika,
- sankcji,
- rekordów incydentów zarządczych.

Rozróżnienie jest następujące:

- opinia o zasobie wiąże się z zasobem zewnętrznym lub wewnętrznym,
- reputacja wiąże się z podmiotem, takim jak uczestnik, węzeł, organizacja lub nym.

Gdy `resource/kind` wynosi `node` albo `org`, cel jest adresowalnym podmiotem,
ale artefakt nadal jest opinią o widoku zasobu, nie `reputation-signal.v1`.
Konsumenci NIE MOGĄ po cichu przekładać ocen zasobu na reputację podmiotu.

Jeżeli federacja chce, by opinie o węźle lub organizacji wpływały na reputację,
potrzebuje jawnej polityki i osobnego artefaktu reputacyjnego lub ścieżki walidacji.

### 5. Powierzchnia dyskusji jest późniejszą warstwą dołączaną {#5-discussion-surface-is-a-later-attached-layer}

Przyszłe powierzchnie dyskusji mogą wiązać się z tą samą tożsamością zasobu
przez osobną rodzinę artefaktów albo wpis rejestru, np.:

- `resource/channel-link.v1`
- `resource-forum-thread.v1`

To wyłącznie nazwy robocze. Propozycja zamraża tylko regułę warstwowania:

1. tożsamość zasobu jest stabilną bazą,
2. opinie są jedną warstwą ekspresji nad tą bazą, z zapisem tylko dopisywanym,
3. bogatsze media dyskusji można dołączyć później bez zastępowania artefaktu opinii.

#### Przyszły klient perspektyw dotyczących zasobu {#resource-perspectives-client}

Przyszły profil projektowy, 2026-11-04; P026-013 jest odroczone i nie dodaje
warunku wstępnego do bieżących prac MVP/alfa. Klient może składać dostępne relacje,
pogłoski, opinie, komentarze, odpowiedzi i korekty wokół zasobu: miejsca, firmy,
osoby publicznej w określonej roli albo konkretnego działania. Jego celem jest
wspólna orientacja społeczna i korygowalna pamięć, nie uniwersalna ocena reputacji.

**Jedna referencja, wiele perspektyw.** Ponownie użyć `record/about` koperty
z `ResourceRef`, indeksu przedmiotów, `gossip/see-also`, relacji opinii oraz
istniejących wątków komentarzy/odpowiedzi. Referencje nie są równoważne:
`record/about` wskazuje przedmioty, `see-also` dostarcza powiązanego kontekstu,
a opinia kuratorska dotyczy rekordu pogłoski, nie wspomnianej w niej osoby.
Luźny link nie ustanawia ani poparcia, ani sprzeczności. Nowe typowane relacje,
jeśli okażą się potrzebne, wymagają jawnego kontraktu domenowego; nie należy
wywodzić ich znaczenia ze współwystępowania w tablicy.

**Oddzielać osobę, rolę i działanie.** Zachować jako odrębne znaczenia osobę,
której dotyczy referencja, rolę i instytucję istotną dla relacji oraz konkretne
działanie/zdarzenie z jego czasem i kontekstem. Pełnienie roli jest twierdzeniem
kontekstowym, nie nieodłączną właściwością osoby ani nadaniem władzy. Na przykład
relacja o postępowaniu lekarza podczas jednej wizyty może wskazać zasób
`pl-nil-pwz`, rolę zawodową i zdarzenie; nie staje się osądem całej osoby,
wszystkich jej ról ani wszystkich wizyt. Firma lub miejsce wspomniane w tej
samej relacji nie stają się automatycznie kolejną stroną oskarżoną. Użyć
istniejących identyfikatorów i kontraktów domenowych, gdzie są adekwatne;
brak tożsamości roli lub zdarzenia pozostaje jawny, zamiast wymyślonej
równoważności. Zamrozić wymagany kształt relacji rola/działanie w P026-013
przed implementacją. Nie przyjmuje się tu nowej przestrzeni nazw, rejestru osób
publicznych ani usługi rozstrzygania tożsamości osób.

Model odczytu zachowuje atrybucję, pierwotną klasę epistemiczną, dostępną linię
pochodzenia źródła, czas zdarzenia odrębny od czasu publikacji, różnice zdań
i historię rewizji. Oddzielić twierdzenia źródła, wnioski modelu i to, co
zaakceptował recenzent; opcjonalna analiza podąża za
[P078](078-weak-signal-harvester.md#inquirium-epistemic-analysis).
Odpowiedzi i korekty pozostają odkrywalne obok twierdzeń, których dotyczą.
Wyniki zachowują nazwaną domenę i skalę; z liczby pogłosek, popularności ani
średniej z niepowiązanych kryteriów nie wyprowadza się zbiorczego werdyktu
na poziomie osoby. Kopie relacji nie stają się niezależnym potwierdzeniem,
a niepewne aliasy lub dopasowania między przestrzeniami nazw pozostają
propozycjami powiązań, zamiast cichych scaleń tożsamości.

**Pamięć obywatelska pomimo zmian roli.** Profil nadaje konkretny użytek
[Wartościom: Odpowiedzialność bez rozmywania w procedurze](../../normative/30-core-values/pl/CORE-VALUES.pl.md#odpowiedzialnosc-bez-rozmywania-w-procedurze):
zachowane relacje i opinie mogą pomagać uczestnikowi decydować, komu zaufać,
w jakiej roli i w jakim zakresie odpowiedzialności. Zmiana urzędu lub instytucji
nie musi zrywać dostępnej historii działań osoby. Odpowiedzialność nie przechodzi
automatycznie na następcę ani wszystkich członków instytucji.

Przykładowo przed powierzeniem radnemu kolejnej kadencji uczestnik może
przejrzeć wcześniejsze zobowiązanie, późniejsze głosowanie radnego, relacje
i opinie mieszkańców o jego skutkach, odpowiedź radnego oraz późniejsze
działania naprawcze. Zachować rzetelne postępowanie i spełnione zobowiązania
obok krytyki. Pogłoska pozostaje pogłoską, opinia – przypisaną autorowi oceną,
a dokument wspiera tylko to, co ustanawia jego treść. Umieszczenie ich na jednej
osi czasu nie ustanawia przyczynowości ani nie zmienia relacji w fakt.

**Wymagania osi czasu.** Ponownie użyć rekordów Agory, rewizji, indeksów
przedmiotów i odczytów bezpiecznych dla widza; oś czasu jest projekcją, nie
kolejnym autorytatywnym magazynem.

1. Rozróżniać czas lub przedział zdarzenia, czas publikacji oraz czas korekty/rewizji.
   Zachować jawnie daty nieznane, przybliżone i sporne; późna publikacja nie może
   przesuwać zdarzenia do teraźniejszości. Zadeklarować podstawę porządku
   i stabilny sposób rozstrzygania remisów, bez sugerowania porządku przyczynowego
   zdarzeń jednoczesnych lub niepewnych.
2. Wiązać każde działanie z deklarowanym aktorem, rolą i instytucją w danym
   czasie, ze źródłami powiązania i znanym okresem pełnienia roli. Późniejsza
   zmiana tytułu nie może przemianować wcześniejszych działań; nowy piastun
   urzędu nie dziedziczy ocen poprzednika. Niepewne dopasowania tożsamości lub
   roli pozostają nierozstrzygniętymi powiązaniami.
3. Wiązać odpowiedzi, spory, korekty i naprawę z twierdzeniami lub działaniami,
   których dotyczą. Utrzymywać widoczne rozróżnienie między tym, co twierdzono
   wtedy, a tym, co skorygowano później, zgodnie z retencją i polityką dostępu;
   nie nadpisywać po cichu wcześniejszej relacji ani nie wznawiać prezentacji
   samego zastąpionego oskarżenia.
4. Zachować klasę epistemiczną, atrybucję i linię pochodzenia źródła każdego
   elementu. Przedruki nie dodają niezależnego poparcia. Oceny pozostają
   przypisane do konkretnego działania, roli i kryterium; nie powstaje
   automatyczna ocena zaufania do całej osoby.
5. Podać wybrane okno czasu, zakres zapytania i znane ograniczenia pokrycia.
   Brakujące lub niedostępne okresy nie ustanawiają bezczynności ani czystej
   historii. Stosować istniejącą politykę admisji/ekspozycji do wpisów osi czasu,
   porządku, podsumowań i powiadomień; wskaźniki luk nie mogą ujawniać chronionych
   rekordów. Profil nie tworzy obowiązku bezterminowej retencji.

**Zakres i granice implementacji.** To projekcja dostępnych rekordów związana
z widzem, nie „cała wiedza sieci”. Podać zakres zapytania, świeżość i znaną
niekompletność bez ujawniania ukrytych rekordów. Brak wyników oznacza brak
wyników dostępnych w tym zakresie, nie brak zdarzeń ani czystą historię.
Użyć API odczytu i projekcji Agory przez admisję hosta, a następnie
[politykę ekspozycji ocen](#6-assessment-exposure-and-sealed-rounds); nie składać
indeksu po stronie klienta z surowych rekordów w celu obejścia ukrywania.
Wyszukiwanie, porządek, liczniki, podsumowania i powiadomienia zachowują tę samą
granicę widza. Każdy cache jest ograniczony i podlega kontraktom retencji/dostępu
właściciela. Same publiczne identyfikatory nie upoważniają ani do prywatnego
wiązania, ani do szerszego ujawnienia.

[P013](013-whisper-social-signal-exchange.md#resource-perspectives-client)
odpowiada za powiązanie specyficzne dla pogłosek. Użyć istniejących ścieżek
pobierania, publikacji i odpowiedzi; profil nie wprowadza crawlera, protokołu
agregacji całej sieci, uprawnienia do publikacji ani mechanizmu reputacji lub
egzekwowania. Korzyścią jest kontekstowa pamięć społeczna; ryzyka to m.in.
stronniczość selekcji, nieaktualny kontekst i wzmacnianie reputacyjne,
ograniczane jawnym zakresem, zachowaniem różnic zdań, linkami korekt i ekspozycją
egzekwowaną przez hosta zamiast pojedynczego werdyktu klienta.

Przed zamknięciem P026-013 zachować offline fixture’y projekcji: jedna osoba
w dwóch rolach, dwie osoby o podobnych nazwach, zmiana roli, działanie ograniczone
czasowo, sprzeczne relacje, przedruki, odpowiedź/korekta i częściowa/niedostępna
historia. Uwzględnić przykład radnego z późną publikacją, nieznaną datą zdarzenia,
następcą w urzędzie, spełnionym zobowiązaniem i naprawą; zweryfikować porządek
zdarzeń/publikacji/rewizji i zachowanie powiązania korekty z wcześniejszą relacją.
Dowieść, że oceny roli/działania nie przenoszą się na całą osobę, nieznane
przestrzenie nazw pozostają używalne, referencje zachowują znaczenie, a ukryte
dane nie wyciekają przez podsumowania, liczniki ani kolejność. Osobno
zakwalifikować prezentację w przeglądarce; sukces fixture’u ani UI nie dowodzi
kompletności sieci ani skuteczności społecznej.

### 6. Ekspozycja ocen i rundy zamknięte {#6-assessment-exposure-and-sealed-rounds}

**Decyzja projektowa, 2026-10-23.** Ograniczać zakotwiczenie społeczne bez
utożsamiania popularności z wartością, opóźniania pilnej ochrony ani twierdzenia
o dowiedzeniu psychologicznej niezależności jednostki. Ta sekcja jest
właścicielem wspólnego kontraktu;
[S008](../60-solutions/008-agora/008-agora.md#planned-assessment-exposure-and-round-projections)
odpowiada za granice usługi Agory.
[P013](013-whisper-social-signal-exchange.md#assessment-exposure-profile)
wiąże opinie o pogłoskach,
[P051](051-swarm-membership-and-reputation-bootstrap.md#11-first-review-must-be-anti-collusive-and-temporarily-blind)
wiąże oceny paneli, a [P069](069-corpus.md#shared-sealed-round-binding)
wiąże pierwsze oceny Corpus. Profile współdzielą mechanikę, nie władzę ani
semantykę payloadów.

Wymagane są dwa poziomy dostarczane niezależnie:

| Poziom | Gwarancja | Granica |
|---|---|---|
| Lokalna bramka ekspozycji | `local-display-only`: host kształtuje model odczytu ocen autoryzowanego widza | Nie powstrzymuje publikacji, replikacji, innego klienta/relaya ani ujawnienia poza protokołem; samo ukrywanie w UI nie wystarcza. |
| Runda zamknięta | Dopuszczone zobowiązanie należy do podpisanego zamkniętego zbioru, a jego późniejsze ujawnienie przechodzi weryfikację względem niego | Zapobiega zliczaniu odpowiedzi adaptacyjnej bez zobowiązania w tej rundzie, pod zadeklarowaną władzą bariery; nie zapewnia globalnej tajności, zaufanego datowania, odporności na Sybile ani psychologicznej niezależności. |

Ekspozycja dotyczy **(widz, przedmiot)** albo nazwanej rundy, nie wieku każdej
opinii. Późny odwiedzający nie powinien dziedziczyć wygasłego okna innych.
Lokalnej bramki nie wolno przedstawiać jako anonimowego głosowania ani moderacji.
Istniejące `hide-local`, ACL tematów i prawo do odwołania zachowują osobne znaczenia.

#### Polityka odczytu hosta i fakty lokalne {#host-read-policy-and-local-facts}

Potok usługi to `admit -> expose -> render`. Admisja zachowuje istniejącą
semantykę autoryzacji, w tym pomijanie niedostępnych tematów w zapytaniu
stronicowanym; odmowa na poziomie operacji nie jest zamieniana na `withheld`.
Dopiero po admisji czysta polityka ekspozycji kształtuje widok. Nie nadaje
dostępu ani nie ujawnia istnienia nieautoryzowanych rekordów.

Planowane `assessment-exposure-profile.v1` zawiera:

| Pole | Kontrakt |
|---|---|
| `profile/id`, kanoniczny digest | Dokładna tożsamość dopuszczonego profilu; konfiguracja operatora przez P091, z jawnie ograniczonymi wyborami użytkownika. |
| `applies-to` | Selektory rekordów i przedmiotów; przestrzenie nazw zasobów pozostają otwarte. |
| `mode` | Zamknięty enum: `open`, `blind-until-own-judgment`, `sealed-round`; ostatni deleguje do właściciela rundy. |
| `withheld` | Zamknięty enum elementów: `peer-ratings`, `peer-rationales`, `aggregates`, `counts`, `rating-order`, `popularity-badges`, `peer-discussion`. |
| `unlock` | Zamknięty enum elementów dla trybu lokalnego: `own-first-judgment`, `explicit-skip`, `subject-window-elapsed`. Runda wymaga zamiast tego zwalidowanej bariery, nie osobistego pominięcia. |
| `subject-window/seconds` | Ograniczony lokalny czas od trwale zapisanego pierwszego zetknięcia, nie od publikacji opinii ani dowolnego zegara UI. |
| `exempt/record-kinds` | Zamknięty, wersjonowany zbiór zarejestrowanych kontraktów rodzajów ochronnych dopuszczonych dla profilu; nie dowolne stringi nadawcy. |
| `guarantee` | `local-display-only` dla trybu lokalnego; nigdy poświadczenie niezależności. |

Obiekty polityki są zamknięte (`additionalProperties: false` na granicach
obiektów; `enum` na elementach tablic), w odróżnieniu od otwartej treści opinii.
Nieznane pola lub tryby polityki nie przechodzą walidacji, nigdy nie wracają
do `open`. Warunkowe gałęzie schematu niosą jawne listy `required`; inwarianty
między polami należą także do czystego rdzenia. Nie ma ogólnoświatowego
domyślnego czasu: `172800` sekund to przykład, nie zmierzone optimum. W pierwszym
pilotażu preferować ukrywanie ocen, agregatów i odznak popularności. Uzasadnienia
mogące ujawniać oceny obejmuje ten sam profil pilotażowy. `peer-discussion` jest
jawnym wyborem profilu, nie cichym globalnym tłumieniem rozmowy.

Planowane `assessment-exposure-fact.v1` wiąże `viewer/ref`, `subject/key`
(istniejące `ResourceRef::to_key()`), opcjonalne `round/ref`, `event`, opcjonalne
`cause/record-id`, `profile/digest`, `recorded/at` i klucz idempotencji. Oprócz
`own-first-judgment`, `explicit-skip`, `subject-window-elapsed` i `barrier-released`
zamknięty słownik zdarzeń potrzebuje `subject-first-seen` oraz `view-released`:
timer wymaga trwałego początku, a ujawnienia w trybie otwartym nie wolno później
pomylić z niewidzianym przedmiotem. Są to fakty lokalne przyjęte przez hosta,
nie deklaracje klienta o tym, co człowiek rzeczywiście zobaczył. Ewaluator
odczytu dostaje jawne `now`; uwierzytelniona komenda zetknięcia/odblokowania
zapisuje przejścia. Bez ukrytej mutacji bazy w nominalnie czystym zapytaniu.
Utrwalić odsłonięcie przed zwróceniem treści innych uczestników; ponowienie jest
idempotentne, a nieudany zapis faktu nie może nadać nowego odsłonięcia.
Anulowanie żądania po zapisaniu odsłonięcia może konserwatywnie zawyżyć ekspozycję,
nigdy poświadczyć ocenę bez wcześniejszej ekspozycji.

Przechowywać te prywatne fakty u temporalnego właściciela S028 usługi, **nie**
w `ProjectionStore` Agory odbudowywalnym z relaya. Wykorzystać mechanikę
zdarzeń/logów/profili temporalnych i kontroli prywatnego magazynu, z manifestem,
ograniczoną liczbą przedmiotów, retencją i replayem. Pełne zdarzenia można
kompaktować do wystarczającego podsumowania ekspozycji. Jeśli i ono zostanie
usunięte, zwracać nieznaną historię: dozwolone jest konserwatywne ponowne
ukrycie, ale nie przywraca ono twierdzenia o niezależności. Zaostrzenie profilu
nie cofa zapisanego odsłonięcia w tym zakresie; odwołanie autoryzacji nadal
odmawia dostępu. Nowe rundy mają odrębne zakresy. Nie scalać po cichu aliasów
zasobów ani widzów; przełączanie kont i delegowane odczyty zachowują powiązanie.

Odblokowanie `own-first-judgment` wymaga przyjętej opinii autora-widza o tym
przedmiocie, nie szkicu ani próby publikacji. Istniejące linki zastąpienia
klasyfikują znane rewizje, ale brak `record/supersedes` w częściowej replice
nie dowodzi globalnie pierwszej opinii. Wiele korzeni, nieznane pochodzenie
i wkład autorstwa agentów wymagają jawnej obsługi; żadne nie uzyskuje
niezależności na podstawie lokalnej historii ekspozycji. V1 nie dodaje
samodeklarowanego overlayu `assessment/exposure` do publicznej opinii.

#### Projekcja API związana z widzem {#viewer-bound-api-projection}

Proponowane `resource-assessment-view.v1` ma następujący przykładowy kształt
ukrytego widoku (referencje zastępcze nie są wykonywalnymi fixture’ami schematu):

```json
{
  "schema": "resource-assessment-view.v1",
  "viewer/ref": "participant:viewer-placeholder",
  "subject/key": "url:https://example.org/article",
  "exposure": {
    "state": "withheld",
    "profile/digest": "sha256:…",
    "withheld": ["peer-ratings", "peer-rationales", "aggregates", "counts", "rating-order", "popularity-badges"],
    "unlock/options": ["own-first-judgment", "explicit-skip"],
    "guarantee": "local-display-only"
  },
  "own": [],
  "exempt": [],
  "peers": null
}
```

Ukryte nie oznacza zera: pominąć sumy innych uczestników, kompletność, kursory,
wersje projekcji, `as-of`, ETagi i znaczniki świeżości zależne od ukrytych danych.
Strumienie własny i ochronny mają w razie potrzeby niezależną ograniczoną
paginację; nie mogą nieść metadanych stron innych uczestników. Przy stałych
wejściach własnych/wyjątków/publicznej polityki zmiana ukrytych danych innych
uczestników nie może zmieniać kształtu ani długości serializowanej odpowiedzi,
rankingu, granic stron ani emisji zdarzeń. Przed rankingiem lub ograniczaniem
wyniku obejmującego wiele przedmiotów użyć neutralnego porządku; filtrowanie po
sortowaniu według popularności powoduje wyciek. Unikać skanowania ukrytych opinii
tylko po to, by utworzyć ukrytą odpowiedź. Ograniczyć zakres cache albo go wyłączyć;
nigdy nie współdzielić projekcji widza między wywołującymi lub profilami. Jest to
testowalna granica kanału aplikacyjnego, nie deklaracja wyeliminowania wszystkich
kanałów bocznych czasu sieciowego lub korelacji zewnętrznej.

HTTP, UI (w tym strony bez JS), CLI,
[obserwacje Agenta](073-agent-orchestration-organ.md#assessment-observations)
i [powiadomienia S039](../60-solutions/039-notifications/039-notifications.md#planned-assessment-exposure-rendering)
muszą używać tej samej projekcji. Bezpośrednie zapytania szczegółów/by-id,
wyszukiwanie, eksporty, liczniki i strumienie na powierzchni widza nie mogą jej
omijać. Surowa replikacja relaya i jawnie uprzywilejowana inspekcja pozostają
poza gwarancją lokalnej prezentacji i muszą być tak oznaczone, zamiast być
potajemnie używane przez Agenta widza. Agent dziedziczy zakres reprezentowanego
widza; nie może syntetyzować pominięcia na podstawie dostępności narzędzia.
Pominięcie wymaga autoryzowanego, jawnego wyboru tego widza.

#### Zamrożenie kontraktu lokalnego pilotażu (2026-10-24) {#local-pilot-contract-freeze-2026-10-24}

Pierwszy lokalny slice zamraża `assessment-exposure-profile.v1`,
`assessment-exposure-fact.v1`, `assessment-exposure-command.v1`
i `resource-assessment-view.v1`. Kwalifikacja runtime jest zapisywana osobno
w lokalnym checkpoincie dowodowym; zamrożenie nie ustanawia ukończenia runtime.
Każdy własny/odsłonięty cudzy wpis zachowuje dopuszczoną otwartą treść `opinion`,
w tym overlaye wiarygodności i odrzucenia pogłoski; starsza projekcja
`opinions.v2` pozostaje bez zmian. Zachowuje to typowaną treść P013 zamiast
redukować każdą opinię do opcjonalnej ogólnej wartości skalarnej. Widok wiąże
ponadto `viewer/ref`; uwierzytelniony host wyprowadza tę wartość z bieżącego
powiązania wywołującego. Publiczne komendy zawierają tylko przedmiot, opcjonalne
dopuszczone przejście, klucz idempotencji i przyczynę w postaci przyjętego rekordu.
Samo zadeklarowanie widza, tożsamości modułu lub `participant_ref` Agenta nie
nadaje władzy widza. Istniejący uwierzytelniony kanał host/middleware przenosi
rozstrzygnięte powiązanie do usługi; wspólny token produktu nie może go
reprezentować. Pierwsze powiązanie przeglądarki wymaga jawnego uwierzytelnienia
operatora; UI na loopbacku bez uwierzytelnienia ani zwykła sesja użytkownika nie
mogą pożyczyć operatorskiej tożsamości kontrolnej backendu.

Pilotaż ukrywa wszystkie sześć elementów: oceny/uzasadnienia/agregaty/liczniki/
porządek/odznaki; `peer-discussion` pozostaje jawnym opcjonalnym wyborem.
Selektory rodzajów zasobów lokalnego profilu pozostają otwarte. Tryb rundy
zamkniętej jest rozpoznawany i odrzucany, dopóki nie istnieją jego osobne
kontrakty właściciela i akceptacja. Do opinii nie dodaje się publicznej
deklaracji ekspozycji ani poświadczenia niezależności.

Zetknięcie i odblokowanie są jawnymi uwierzytelnionymi komendami. Odczyt widoku
jest czysty; upłynięcie okna lub otwarta polityka wymaga trwałego przejścia
odsłonięcia przed zwróceniem cudzej treści. Jawne zetknięcie może zapisać takie
przejście, także przy powtórzonej komendzie ocenianej z nowym jawnym czasem
(przejrzana semantyka monotoniczna poniżej). Lokalne zetknięcie wskazuje
nieprzezroczysty przedmiot i ani nie sonduje istnienia rekordu, ani nie nadaje
dostępu. Każdy renderowany rekord nadal przechodzi zwykłą admisję tematu.
Prywatny magazyn S028 należący do usługi jest niezależny od odbudowy projekcji
relaya. Zachowuje wystarczające podsumowania przy kompakcji i zapisuje nieznaną
historię po utracie, przy ograniczonej populacji przedmiotów i zdarzeń.

Pierwszy profil implementacji wymaga jawnego backendu lokalnego SQLite;
start Matrix odmawia przy skonfigurowanej ekspozycji, dopóki metadane receiptów
publikacji nie zostaną niezależnie zakwalifikowane. Podpisywanie z referencjami
parent/supersedes również odmawia, dopóki nie może użyć admisji związanej
z widzem. Przyjęcie podpisanego rekordu i operatorska odbudowa projekcji są
jawnymi operacjami transportu/utrzymania poza gwarancją prezentacji widza
i nie mogą być fallbackiem obserwacji Agenta.

Początkowa projekcja widza jest ograniczona do 100 wpisów na strumień.
Mieszane strony surowego relaya i inspekcja surowych rekordów przy użyciu tylko
wspólnego tokena produktu odmawiają przy skonfigurowanym profilu; ich kursorów
relaya, liczników i SSE nie można bezpiecznie użyć jako metadanych widza.
Konsumenci używają zamiast tego projekcji hosta. Bogata paginacja bezpieczna
dla widza i osobny uprzywilejowany interfejs surowej inspekcji wymagają przed
wprowadzeniem własnej implementacji i dowodów. Istniejący właściciele typowanej
propagacji pogłosek, ochrony i odwołań zachowują dopuszczone ścieżki. Lista
wyjątków opinii ochronnych jest pusta, dopóki nie zostaną dopuszczone konkretne
zamknięte kontrakty rodzajów; pilność deklarowana przez nadawcę ani ogólny
znacznik moderacji nie mogą jej wypełnić.

#### Korekta lokalnego pilotażu po przeglądzie (2026-10-24) {#local-pilot-review-amendment-2026-10-24}

Operator zaakceptował dwie korekty przed implementacją. Idempotencja lokalnych
komend jest monotoniczna dla widza/przedmiotu/rodzaju komendy, oparta na
zachowanych faktach; ponowne zetknięcia oceniają nowe jawne `now`. Klucze żądań
klienta są referencjami korelacyjnymi, nie trwałymi receiptami żądanie–wynik.
Retencja balanced/minimal S028 kompaktuje wystarczające podsumowania przy limicie
zdarzeń. Żadna kompakcja nie usuwa faktów odsłonięcia/historii ani nie tworzy
poświadczenia niezależności. Full-audit zachowuje zakaz przycinania i jawną
odmowę pojemnościową.

Opinia z diagnostyką trafia do kwarantanny zamiast blokować cały przedmiot.
Odsłonięty strumień używa deterministycznych ograniczonych wkładów autorów;
jego konserwatywny znacznik `degraded: true` zawsze oznacza ograniczone/niepełne
pokrycie, nie wyrocznię liczebności ani kondycji niedopuszczonych tematów.
Znacznik jest nieobecny, gdy cudze opinie są ukryte. Pierwsza polityka kandydatów
bierze do 64 tematów na autora (4096 kandydatów łącznie) i do 16 dopuszczonych
opinii na autora, rotacyjnie przed limitem 100 wpisów. Nie deklaruje globalnej
kompletności, odporności na Sybile ani stałego kosztu bazy. Można pominąć całe
wpisy opinii, by spełnić limit bajtów odpowiedzi hosta; pola zachowanej opinii
nigdy nie są po cichu obcinane.

Odczyt open/spoza selektora bez faktu odsłonięcia zwraca
`disclosure-not-recorded`, puste listy ukrywania/odblokowania i `peers: null`,
dopóki jawne zetknięcie nie zapisze ujawnienia. Ukryte widoki mogą pokazywać
początek/termin/stan własnego okna widza. Odczyt wyłącznie sondujący odróżnia
konkretną odmowę `exposure-not-configured` od stanu zamkniętego/aktywnego bez
rozstrzygania widza ani czytania jego ocen. Uwierzytelnienie UI poprzedza
rzeczywiste zapytanie widza. Trasy produktu używają audytowanej allowlisty
z domyślną odmową; znaczniki moderacji skierowane na rekord i POST-y sondujące
stan nie mogą omijać ekspozycji. Renderowane komendy UI/CLI mogą przypinać
wyświetlony `profile/digest`; niezgodność odmawia przed skutkami. Klucze klienta
nie nadają autoryzacji. Prywatny magazyn używa SQLite FULL jako minimum
trwałości „ujawnienie przed treścią”; nie jest to kwalifikacja fizycznej utraty
zasilania. Narzędzie lokalnej inspekcji/kompakcji przy zatrzymanym właścicielu
ujawnia prywatne liczniki pojemności, nigdy eksport historii dla widza.
Pojemność, zabronione odblokowanie i przejściowa awaria magazynu mają odrębne
kontrakty statusu i możliwości ponowienia; zakres oraz limity full-audit są
widoczne dla operatora. Te korekty kontraktu nie odnawiają wcześniejszego
checkpointu runtime; implementację i nowe dowody akceptacji zapisuje się osobno.

#### Checkpoint dowodowy lokalnego pilotażu (2026-10-24) {#local-pilot-evidence-checkpoint-2026-10-24}

Przyjęte lokalne zamrożenie obejmuje cztery zamknięte kontrakty profilu/faktu/
komendy/widoku. Node implementuje czystą politykę, osobny prywatny magazyn
faktów S028 i uwierzytelnioną projekcję hosta, z ograniczonymi adapterami UI, CLI,
zarejestrowanego Agenta i powiadomień. Ukierunkowane testy komponentów obejmują
niepewność zegara, nieudane zapisy, luki retencji, idempotencję, zmiany profilu,
izolację widzów i replay. Regresja wspólnego widoku odsłania widok, odwołuje jego
admisję tematu, weryfikuje pominięcie cudzej treści i zachowuje to samo trwałe
podsumowanie odsłonięcia po ponownym otwarciu/replayu. Fixture’y kontrolera
Agenta i właściciela powiadomień używają skryptowanych odpowiedzi właścicieli
i zachowują ten zakres.

Pierwotny raport `2026-10-24-local-04` przypina czyste Node `63ece2a4`
i Orbidocs `7cf59bf4`. Przeszło dziewięć rzeczywistych lokalnych przypadków
SQLite host/API/UI/CLI, obejmujących odmowy dla uwierzytelnionego wywołującego,
stabilne bajtowo ukryte widoki po zmianie ukrytych ocen, ukrycie/odsłonięcie
treści pogłoski, przyjętą własną ocenę, restart procesu i odbudowę projekcji
Agory. Rzeczywiste przebiegi Chrome obejmują JS włączony i wyłączony. Niezależna
kwalifikacja weryfikuje zachowane pierwotne bajty i hashe świadków; negatywne
regresje weryfikatora używają kopii zaliczonego raportu. Dowody i dwie wcześniejsze
odrzucone próby są zachowane pod `node:docs/evidence/agent-runtime/2026-10-24-rate-exposure/README.md`.

Checkpoint kwalifikuje ograniczony pilotaż lokalnej prezentacji. P026-005
pozostaje partial, ponieważ kontrakty rund/rodzajów ochronnych mają osobne
bramki. P026-007/008 zachowują szersze prace akceptacji konsumentów, w tym pełne
macierze P013, powiadomień i Agenta. Fixture pogłoski zachowuje pola rozszerzeń
opinii przez wspólny widok; nie wprowadza samodzielnego schematu admisji overlayu
pogłoski ani nie kwalifikuje pełnego workflowu kuracji/propagacji Whisper.
Zarejestrowane powiadomienia pozostają informacyjne i wyłącznie odpytywane,
bez automatycznego producenta powiadomień o ocenach. Matrix/federacja, rundy
zamknięte, P051/P069, rzeczywiste modele, pełne kampanie, psychologiczna
niezależność, skuteczność społeczna i gotowość wydania pozostają poza dowodami.

#### Checkpoint dowodowy przeglądu lokalnego pilotażu (2026-10-24) {#local-pilot-review-evidence-checkpoint-2026-10-24}

Przebieg przeglądu `2026-10-24-review-01` przypina czyste Node `91babeb0`
i Orbidocs `414acd72`. Przechodzi dziewięć ograniczonych przypadków na
rzeczywistych procesach, w tym identyczne bajtowo ukryte widoki z biegnącym
własnym oknem widza, zamknięte sondowanie bez widza, domyślna odmowa nowej trasy,
zapytania o znaczniki rekordów, identyczne odmowy POST dla znanych/brakujących
rekordów, nieaktualna zgoda na profil bez skutków, zgodność CLI, restart/odbudowa
i renderowanie okna/terminu w Chrome z JS i bez JS. Sprzątanie potwierdzono.
Niezależna kwalifikacja v2 zgadza się przy zwykłym uruchomieniu, z Python `-O`
i po rozpakowaniu archiwum; wszystkie 38 mutacji dowodów spotyka się z odmową.
Historyczne raporty i kwalifikator v1 pozostają bez zmian. Zob.
`node:docs/evidence/agent-runtime/2026-10-24-rate-exposure-review/README.md` oraz
`node:docs/audits/REVIEW-RATE-EXPOSURE-2026-10-24.md`.

Migracja pełnych starych receiptów, dokładna granica pojemności zdarzeń,
odmowa full-audit, utrzymanie offline, izolacja autora przy 4097 tematach, stan
otwarty/niewybrany i wygaśnięcie z jawnym czasem pozostają dowodami komponentów.
Bieżący rzeczywisty widz UI/CLI to operator węzła. Inni reprezentowani uczestnicy
i powiązania Agenta/powiadomień zachowują zakres syntetycznego hosta, w tym
odmowę tożsamości/klasyfikacji przed odczytem i wykluczenia centralnej uwagi.
Nie zakwalifikowano rzeczywistego producenta powiadomień o ocenach, pełnej
macierzy wcześniejszego kontekstu Agenta, wieloużytkownikowego runtime, fizycznej
utraty zasilania, kompletnego/odpornego na Sybile pokrycia, Matrix/federacji ani
gotowości wydania. Statusy kontynuacji P026-005/007/008 i P013/P057/P073
pozostają partial; P026-006 pozostaje done tylko dla lokalnej polityki/prywatnych
faktów.

#### Kontrakt ograniczonej kwalifikacji Q-02 (2026-10-24) {#q-02-bounded-qualification-contract-2026-10-24}

Przyjęty zakres: przypadek modułu jako widza używa dopuszczonego przez harness
`CallerBinding`, wstawianego do istniejącego resolvera daemona przez zwykłe API
właściciela. Nie dopuszcza się zastąpienia resolvera, deklaracji widza przez
moduł ani powierzchni provisioningu produkcyjnego. Hook wstawiania/usuwania
istnieje tylko pod jawną funkcją buildu akceptacyjnego; dowody wiążą zestaw
funkcji, źródło i plik wykonywalny. Przypadki mają klasę `fixture-bound-input`,
odrębną od przypadków `runtime` ścieżki produkcyjnej. Zwykłe powiązanie
`module:*` musi zwracać `viewer-unbound`, bez fallbacku operatora, surowej
obserwacji ani automatycznego pominięcia.

Wygaśnięcie i odwołanie muszą odmawiać następnego odczytu, zachowując trwałe
fakty odsłonięcia. Restart nie może przywrócić dzierżawy harnessu; ponowna
admisja może wykazać przetrwanie pierwotnych faktów odsłonięcia. Kwalifikacja
Agenta używa istniejącej lokalnej kontroli, niezależnie od powiązania harnessu.
Deterministyczny adapter testowy może ćwiczyć rzeczywistą ścieżkę kontrolera/
obserwacji/śladu bez prawdziwego modelu; nie jest to kwalifikacja inferencji,
kompletności wcześniejszego kontekstu ani niezależności poznawczej.

Ścieżka modułu jest zakwalifikowana tylko z powiązaniem dopuszczonym przez
harness. Moduły produkcyjne nie mogą być widzami ocen, dopóki nie istnieje
osobny slice provisioningu identity-host. P026-005/007 pozostają partial.
Ten kontrakt nie jest dowodem runtime.

#### Checkpoint ograniczonych dowodów Q-02 (2026-10-24) {#q-02-bounded-evidence-checkpoint-2026-10-24}

Przebieg `2026-10-24-q02-07` przypina czyste Node `4e29d5d3` i Orbidocs `48282704`.
Przechodzi siedem przypadków z potwierdzonym sprzątaniem. Cztery mają klasę
`runtime`: rzeczywiste tworzenie tożsamości, odmowa zwykłemu modułowi,
produkcyjne przejścia Agenta przez local-control i zawieszenie/wznowienie Agenta
z odmową niewłaściwemu uczestnikowi. Trzy mają klasę `fixture-bound-input`:
izolacja widza modułowego, odsłonięcie z wygaśnięciem/odwołaniem oraz restart/
reset/replay. Ich `origin: synthetic-input` nie może stać się twierdzeniem
o produkcyjnym provisioningu. Rzeczywiste receipty funkcji Cargo i hashe plików
wykonywalnych wiążą zwykły daemon (bez funkcji), wariant wyłącznie akceptacyjny
i rzeczywistego właściciela Agory.

Nadzorowany moduł na B reprezentuje rzeczywistego uczestnika A dopiero po
wstawieniu przez harness skończonego CallerBinding przez to samo API właściciela
co przy starcie. Żaden resolver nie jest zastępowany. Zwykłe odczyty `module:*`
zwracają `viewer-unbound`; deklarowani widzowie, pominięcia modułu
z powiązaniem/bez oraz surowy fallback odmawiają bez uruchamiania historii
operatora. Po odsłonięciu wygaśnięcie/usunięcie odmawia następnego odczytu.
Restart traci dzierżawę fixture’u; jawna ponowna admisja i reset/replay Agory
zachowują trwałe fakty odsłonięcia. Dwusekundowe okno jest ograniczonym
ustawieniem fixture’u, nie kwalifikacją schedulera.

Agent działa niezależnie na zwykłym pliku wykonywalnym i istniejącej lokalnej
kontroli. Trzy rzeczywiste przejścia kontrolera używają widoków: ukrytego, jawnie
odsłoniętego, a następnie odsłoniętego po wznowieniu; digesty source-version
metadanych odpowiadają rzeczywistym widokom Agory. Pierwsze przejście nie wykonuje
zetknięcia ani pominięcia. Istniejący deterministyczny adapter Story-011 nie ładuje
modelu. Test runtime ujawnił brak kwalifikatora kontekstu operacyjnego w adapterze:
naprawa używa wspólnego zwalidowanego kontraktu kontekstu, zachowuje klasę
badawczego źródła tylko do odczytu i monotoniczne lokalne minimum ostrożności
kontrolera. Odpowiedzi modułu zyskały też brakujące nagłówki prywatnego cache.
Nie osłabiono żadnej wspólnej bramki admisji ani ostrożności.

Niezależna kwalifikacja zgadza się normalnie, z `-O` i po rozpakowaniu. Wszystkie
21 mutacji dowodów spotyka się z odmową w obu trybach (44 wywołania), także na
rozpakowanych dowodach. Zachowano sześć niekompletnych pierwotnych prób
z odrębnymi przyczynami; szósta zapisuje defekt adaptera kontrolera. Zob.
`node:docs/evidence/agent-runtime/2026-10-24-rate-exposure-q02/README.md` i `node:docs/audits/Q02-RATE-EXPOSURE-2026-10-24.md`.

Moduły produkcyjne nadal nie mogą stawać się widzami uczestników: provisioning
P026-012 należy do identity host/P073/P066 i pozostaje todo. P026-005/007/008
i pełna macierz P073 historii/forku/alternatywnego narzędzia pozostają partial.
Nie zakwalifikowano wieloużytkownikowego UI, rzeczywistej produkcji powiadomień
o ocenach, szerszych transportów, rund zamkniętych, modeli, niezależności
społecznej/poznawczej ani gotowości wydania. Wcześniejsze dowody przeglądarki/
pilotażu pozostają bez zmian; checkpoint nie dodaje przebiegu przeglądarkowego.

#### Checkpoint dowodowy krytycznego przeglądu Q-02 (2026-10-24) {#q-02-critical-review-evidence-checkpoint-2026-10-24}

Przebieg przeglądu `2026-10-24-q02-review-02` przypina czyste Node `6abf71df`
i Orbidocs `d09d1035`, zalicza siedem przypadków i potwierdza sprzątanie oraz
zgodność źródła/obrazu po zatrzymaniu procesu. Cztery przypadki pozostają
`runtime`; trzy pozytywne przypadki modułów pozostają `fixture-bound-input`.
Zwykły plik wykonywalny nie ma funkcji akceptacyjnej; tylko plik B włącza hook.
Produkcyjny provisioning nadal nie istnieje.

Przegląd wykazał, że jednostkowy wariant revoke serde przyjmował dodatkowe pola.
Zamknięty wariant pustej struktury teraz ich odmawia bez usunięcia powiązania;
niepoprawny stan resolvera także odmawia zamiast cicho wykonywać bootstrap.
Tylko nieznany usunięty selektor pozwala na ponowną admisję. Rzeczywiste świadki
HTTP invalid-revoke/lease i natywne regresje przechodzą. Nie rozszerzono władzy
wywołującego ani polityki ekspozycji.

Sześć zmanipulowanych kopii nadal przechodziło historyczny weryfikator:
pominięte odczyty admisji/mutacji/restartu, inna przyczyna odmowy Agenta,
odwrócony lifecycle i zetknięcie zastąpione pominięciem. Diagnozują luki
weryfikacji, nie zaobserwowane obejścia runtime. V2 zachowuje niezmienione
kontrole strukturalne v1 i dodaje uporządkowane tworzenie tożsamości, podpisaną
admisję i zmiany opinii innych, utratę powiązania tego samego widza, ukończony
reset/replay oraz świadki tożsamości/kroku/lifecycle Agenta. Rozbieżność
końcowego źródła i wybranego obrazu nie może dać zaliczonego raportu runtime.
Nieudany build usuwa stare receipty; zmiany czystej rewizji Orbidocs podczas
buildu także powodują odmowę.

Wyniki v2 normalnie/z -O oraz z luźnych/rozpakowanych plików zgadzają się.
Wszystkie 42 manipulacje dowodów odmawiają w obu trybach (86 wywołań), również
po końcowym rozpakowaniu archiwum. Przechodzi 12 testów ocen daemona, dziewięć
testów zabezpieczeń źródła/obrazu/receiptów i Clippy. Pierwszy runtime przeglądu
przeszedł, ale pozostaje odrzucony w kwalifikacji, ponieważ weryfikator błędnie
oczekiwał HTTP 201 od istniejącego tworzenia tożsamości zwracającego HTTP 200.
Ta próba, początkowa regresja natywna oraz historyczne archiwum/narzędzia Q-02
zachowują odrębne przyczyny i znaczenie. Zob.
`node:docs/evidence/agent-runtime/2026-10-24-rate-exposure-q02-review/README.md` i `node:docs/audits/REVIEW-Q02-RATE-EXPOSURE-2026-10-24.md`.

Klient HTTP modułu to zaufany harness używający poświadczeń nadzorowanego
fixture’u. Zakwalifikowana jest rzeczywista ścieżka uwierzytelniania/resolvera
HTTP; własne zachowanie aplikacji modułu przy generowaniu żądań, zgoda
i podpisana delegacja – nie. Wygaśnięcie powiązania korzysta z istniejącego
UTC hosta; cofnięcie zegara i kwalifikacja długotrwała pozostają poza krótkim
przypadkiem. Weryfikacja samych danych nie jest poświadczeniem wykonania przez
stronę trzecią ani samodzielną weryfikacją podpisów offline. P026-012 pozostaje
todo, a P026-005/007/008 i pełna macierz P073 – partial. Nie ma nowego twierdzenia
o przeglądarce, producencie powiadomień, modelu, federacji, rundzie zamkniętej,
niezależności ani wydaniu.

#### Produkcyjny checkpoint ChannelJson P026-012a (2026-10-25) {#p026-012a-production-channeljson-checkpoint-2026-10-25}

[Przyjęty kontrakt grantu](026-assessment-viewer-grants.md) jest zaimplementowany i zakwalifikowany w ograniczonym profilu lokalnym. Przebieg 06 przy czystym Node `e726624c` / Orbidocs `2e73ed3a` zalicza osiem przypadków zwykłego daemona/aplikacji/przeglądarki z pustymi zestawami funkcji Cargo i potwierdzonym sprzątaniem/zgodnością źródła i obrazu. Sama aplikacja wywołuje uwierzytelnione SDK; harness nigdy nie czyta jej poświadczeń. Zgoda operatora i konsumpcja P066 poprzedzają użycie. Odczyty HTTP modułu i samodzielna odpowiedź odmawiają. Rzeczywiste wygaśnięcie, odwołanie, restart modułu/daemona i reset/replay zachowują prywatne fakty ekspozycji bez zachowywania aktywacji. Obce rekordy są `signed-fixture-input` przechodzącym rzeczywistą admisję.

Osobne kontrole komponentów przy Node `5d6200a1` obejmują awarie pary czasów i trwałości, współbieżność, wycofanie sesji oraz uwierzytelnioną starą ramkę oczekującą przed admisją właściciela, gdy nowe uruchomienie otrzymuje grant produkcyjnego właściciela/P066. Nie jest to obserwacja wymuszonej kolejki ani globalnego miernika zapytań w zwykłym daemonie. Bieżący kwalifikator wiąże pełny łańcuch przyczynowy i odrzuca 59 mutacji z ponownie obliczonymi hashami normalnie/z `-O`, na luźnych plikach i po rozpakowaniu. Pierwotne Q-02 i odrzucone próby pozostają bez zmian; migawki źródeł nigdy nie są wykonywane. Zob. `node:docs/evidence/agent-runtime/2026-10-24-p026-012a/README.md` i `node:docs/audits/P026-012A-2026-10-25.md`.

P026-012a jest done tylko dla jednego lokalnego operatora, jednego węzła i aplikacji akceptacyjnej. Nadrzędne P026-012/P073 oraz P026-005/007/008 pozostają partial; 012b osobno odpowiada za pozytywną politykę konsumenta Agent, proweniencję obserwacji i końcową kwalifikację inferencji/kontekstu/forku/wznowienia/alternatywnego narzędzia. Nie ma twierdzenia o module produktowym, replikacji, fizycznym zegarze, utracie zasilania, wrogim OS, modelu, rundzie ani wydaniu. Wcześniejsze stwierdzenia o braku produkcyjnego provisioningu opisują datowane historyczne checkpointy.

#### Wspólny kontrakt zobowiązania i bariery {#shared-commitment-and-barrier-contract}

Wspólnym prymitywem jest `salted-sha256-jcs-v1`: SHA-256 dokładnego preimage
JCS z wyróżnikiem domeny i świeżą, kryptograficznie losową solą długości 32 bajtów;
kodowanie digestów używa istniejącej konwencji `sha256:` i base64url bez paddingu.
Ponownie użyć canonical-json i narzędzi kryptograficznych. Wydzielić mały czysty
`commitment-core` tylko dla wspólnej mechaniki, z ograniczonymi wejściami i bez
I/O, zegarów, pozyskiwania losowości ani admisji domenowej wewnątrz. Host
bezpiecznie dostarcza sól.

Dla Agory preimage wiąże `domain = orbiplex.agora.assessment-commitment.v1`,
`round/ref`, `author/participant-id`, `subject/key`, `opinion` (zwalidowaną
wartość `resource-opinion.v1`) i `salt`. Corpus zachowuje
`orbiplex.corpus.first-judgment-commitment.v1` i powiązanie Room/runda/uczestnik/ocena.
Responsibility zamraża własną domenę i payload przeglądu. Re-use nigdy nie
wtłacza werdyktu panelu ani swobodnej deliberacji w ocenę zasobu.

Kanonikalizacja nie może zmieniać wartości zobowiązania podczas transportu.
Normalizacja koperty Agory i JCS nie są zamienne. Przed kodowaniem zamrozić
powiązanie bezpieczne dla transportu: w razie potrzeby przenosić ograniczone
kanoniczne bajty JCS jako nieprzezroczyste albo walidować i deklarować
normalizację przed zobowiązaniem, nigdy po nim. Uwzględnić golden fixtures
non-NFC, Unicode, liczb i zgodności między językami oraz budżet/kodowanie
nośnika Matrix z P035. Sparsowane ujawnienie musi przejść walidację schematu
domenowego oraz zgadzać się z digestem.

Planowane kontrakty rodzajów Agory są odrębne od `opinion`:

Przed zamknięciem ścieżka publikacji rundy emituje tylko zobowiązania; treści
i sole pozostają w chronionym lokalnym magazynie oczekujących wpisów uczestnika.
To bariera publikacji, odmienna od lokalnego ukrywania już opublikowanych opinii.
Nie utajnia wstecz danych publicznych ani nie zabrania zwykłej opinii poza rundą.
Taka publikacja zewnętrzna nie dowodzi zakwalifikowanego ujawnienia i pozostaje
jawnie wyłączonym kanałem wycieku.

| `record/kind` | Wymagane powiązanie | Podpisujący |
|---|---|---|
| `assessment-round` | Przedmiot; rewizja/digest profilu; kwalifikowalność (`open` albo `enumerated`, dokładna referencja/digest zbioru); reguła bariery; referencja autorytetu; czasy zamknięcia commit/reveal/max; limity; schemat zobowiązania | Upoważniony otwierający |
| `assessment-commitment` | Runda, uwierzytelniony autor, digest zobowiązania stałego rozmiaru i schemat; bez treści, soli ani wskazówek zależnych od treści | Uczestnik |
| `assessment-barrier` | Runda, czas/przyczyna odsłonięcia, dokładna ograniczona posortowana lista różnych identyfikatorów zobowiązań, liczba i digest JCS zbioru z separacją domen | Autorytet wskazany przez dopuszczoną rundę |
| `assessment-reveal` | Runda, **referencja bariery**, referencja zobowiązania, sól i dokładna typowana treść objęta zobowiązaniem w zamrożonym kodowaniu transportowym | Ten sam uczestnik |

Starsi konsumenci nie mogą indeksować nieznanych rodzajów jako zwykłych opinii.
Tylko projekcja świadoma rund emituje kwalifikujące się widoki ujawnionych opinii,
z zachowaniem proweniencji rundy i wyniku. `OpinionView` nie musi stawać się
właścicielem stanu rundy. Corpus/Responsibility używają równoważnych podpisanych
faktów domenowych przez istniejącego właściciela, nie obowiązkowej publicznej
publikacji prywatnych głosów w Agorze.

Autorytet szereguje admisję zobowiązań i zamknięcie bariery przez istniejące
wzorce trwałego właściciela/CAS i outboxu. Zamraża jeden przyjęty zbiór,
utrwala zamknięcie przed opublikowaniem podpisanej bariery i odmawia późniejszym
zobowiązaniom tej fazy. Uczestnik potrzebuje uwierzytelnionego receiptu admisji,
jeśli polega na włączeniu przed terminem; zamrożenie musi określić uzgadnianie
receiptów/zbioru i dowód czasu admisji. `authored/at` i niepodpisane,
usuwalne `relay/received-at` nie są takim dowodem. Ocena terminu należy do
dopuszczonego autorytetu z zadeklarowaną polityką zegara/niepewności; niepewny
moment graniczny nie może po cichu dopuścić oceny do zliczenia.

**Referencja bariery dowodzi powiązania, nie czasu publikacji.** Digest można
obliczyć wcześniej, autorytet może antydatować, pomijać lub tworzyć forki,
a współpracownicy mogą ujawnić treści. Weryfikacja zależy więc od zadeklarowanego
autorytetu i zachowanych dowodów zamknięcia/admisji, nie od twierdzenia o globalnej
chronologii. Sprzeczne podpisane bariery albo zobowiązanie z receiptem nieobecne
w zamkniętym zbiorze unieważniają zliczanie do wyjaśnienia; nie wybierać wersji
pierwszego relaya. Repliki muszą pobrać i zwalidować wskazany zbiór przed
kwalifikacją. Częściowa historia lub niedostępny autorytet oznaczają
nierozstrzygnięte dowody, nie wymyślony pusty zbiór.

| Stan | Zdarzenie | Wynik |
|---|---|---|
| `committing` | Kwalifikujące się zobowiązanie dopuszczone przed terminem | Pozostaje `committing`; dokładny replay jest idempotentny. |
| `committing` | Poprawna podpisana bariera zamykająca przyjęty zbiór | `revealing`; późniejsze ujawnienia muszą wiązać tę barierę. |
| `committing` | Brak zamknięcia do obowiązkowego `round/max-closes-at` u właściciela | `void`; brak wyniku niezależnej oceny. Replika bez dowodów nie może wywieść globalnego void wyłącznie z lokalnej nieobecności. |
| `revealing` | Poprawne ograniczone ujawnienie autora zobowiązania przed terminem ujawnienia | Pozostaje `revealing`; zweryfikować treść, przynależność, autorytet i domenę. |
| `revealing` | `reveal/closes-at` | `closed`; jawnie raportować brakujące i niepoprawne ujawnienia. |
| `closed` | Późniejsza opinia/rewizja/odpowiedź polemiczna | Osobny strumień po barierze; nie może wejść do zbioru pierwszych ocen. |

Zamrozić poprawny porządek terminów (`commit < reveal <= max`) i zachowanie
fail-closed spóźnionej bariery; bez adaptacyjnego przedłużenia po zobaczeniu ocen.
Otwarta kwalifikowalność dopuszcza tylko barierę terminu. Odsłonięcie po kworum
lub wszystkich uprawnionych wymaga przypiętego skończonego zbioru
kwalifikowalności i zadeklarowanej polityki COI/wyłączeń. Wszystkie polityki
ograniczają uczestników, rekordy, bajty, pracę weryfikacyjną, ponowienia i czas
życia rundy. Scheduler S020 może budzić pracę; nie jest właścicielem prawdy
terminów ani władzy bariery.

Wyniki na zobowiązanie są zamknięte: `counted`, `missing-reveal`, `invalid-reveal`,
`outside-barrier`, `equivocation`, `round-void`. Różne zobowiązania jednego autora
w jednej rundzie powodują equivocation; dokładna retransmisja – nie. Projekcja
musi diagnozować sprzeczne zobowiązania nawet wtedy, gdy tylko jedno umieszczono
w barierze; niekompletny zbiór wejściowy nie może poświadczyć ich braku.
Ograniczać wyniki do migawki dowodów, zachowując proweniencję korekty, gdy
późniejsze dopuszczalne dowody zmieniają wynik. Brak ujawnienia nie jest zerem
ani niezgodą. Krótkie okna ujawniania ograniczają, ale nie usuwają stronniczości
selektywnego przerwania.

Tylko zweryfikowany wynik `counted` może nieść `independent-first-judgment = true`,
co jawnie oznacza **zobowiązanie zakwalifikowane protokołem**, nie niezależność
psychologiczną lub społeczną. Lokalne ukrywanie, deklaracja klienta, ukryte
nazwiska panelistów ani równoległe wywołania modeli nigdy nie wystarczą.
P051 może używać tylko takich wyników jako pochodzącego z rundy wejścia
niezależnej oceny; nie zabrania to osobno uzasadnionej reputacji proceduralnej
ani natychmiastowego działania ochronnego opartego na dowodach.

#### Ochrona, wartości domyślne i pozostałe wybory {#protection-defaults-and-remaining-choices}

Pilna ochrona, dowody krzywdy i dostęp do odwołania nie mogą czekać na żadną
z bramek. Zamrozić zamknięte mapowanie dopuszczonych ochronnych **kontraktów
rodzajów**, władzy i minimalnych niezbędnych pól; nazwy `safety-warning`,
`harm-evidence` i `appeal-notice` to proponowane role, nie twierdzenie, że
schematy już istnieją. Ich kontrakty odrzucają `opinion/rating` i równoważne
pola agregatów/odznak; etykiety nadawcy ani tekst deklarujący pilność nie mogą
nadawać wyjątku. Wykorzystać istniejące ścieżki ochronne bez wtłaczania wrażliwych
dowodów w publiczny strumień opinii. Narracje o bezpieczeństwie nadal mogą
wpływać na recenzenta: nie deklarować poznawczej ślepoty po koniecznym
ujawnieniu i nigdy nie ukrywać dowodów ani składu panelu potrzebnych do obrony,
wyłączenia lub odwołania. Budżety/progi propagacji Whisper pozostają niezależne
od prezentacji. Ochrona nie jest głosowaniem popularności.

Wybory v1 i pytania przed zamrożeniem:

1. **Q-01 rozstrzygnięte:** bez overlayu ekspozycji klienta ani wagi reputacyjnej
   dla niego.
2. **Q-02 proponowana bezpieczna wartość domyślna:** tworzenie rund wymaga
   dopuszczonej polityki otwierających, kwot i wyboru konsumenta według jawnie
   zaufanego autorytetu i referencji rundy. Wiele rund pozostaje odrębnych;
   nie wybierać automatycznie największej, najnowszej ani najkorzystniejszej.
   Dokładna polityka otwierających dla otwartego zasobu pozostaje do zamrożenia
   w P026-005 przed włączeniem rund.
3. **Q-03 proponowana wartość domyślna:** `peer-discussion` wymaga opt-in profilu;
   oceny i agregaty pozostają osobno kontrolowane. Sam podgląd dyskusji może
   ujawniać oceny, więc węższe profile muszą podawać to ograniczenie.
4. Zamrozić władzę bariery/odzyskiwanie receiptów, retencję prywatnej soli,
   niepewność zegara i powiązania rodzajów wyjątków przed slice’em rund zamkniętych.

Kompromisy obejmują wolniejszą informację zwrotną, ukrywanie użytecznych
uzasadnień, koszt prywatności stanu lokalnego, zaufanego właściciela zamknięcia
i selektywne nieujawnianie. Nie ma gwarancji globalnej tajności już publicznych
opinii. Hipoteza skuteczności społecznej wymaga własnej ewaluacji, odrębnej od
akceptacji implementacji; ani udany fixture UI, ani wybrane okno nie dowodzą
ograniczenia efektu stadnego.

## Zalecany przykład {#recommended-example}

Opinia o zasobie w transmisji przez podłoże Agory – jedna koperta
`agora-record.v1` niosąca treść `resource-opinion.v1`. Koperta zawiera tożsamość
i routing; treść zawiera samą opinię.

```json
{
  "schema": "agora-record.v1",
  "record/id": "sha256:4b7c9fzkMyAL8GBfQExampleRecordId00000000000000",
  "record/kind": "opinion",
  "topic/key": "ai.orbiplex.opinions/url",
  "record/about": [
    {
      "resource/kind": "url",
      "resource/id": "https://example.org/article"
    }
  ],
  "author/participant-id": "participant:did:key:z6MkExample",
  "authored/at": "2026-04-10T08:15:00Z",
  "content/schema": "resource-opinion.v1",
  "content": {
    "schema": "resource-opinion.v1",
    "opinion/text": "Useful overview, but the sourcing is thin in the final section.",
    "opinion/lang": "en",
    "opinion/rating": 3
  },
  "signature": {
    "alg": "ed25519",
    "value": "sig_example_opinion_url_article_0001"
  }
}
```

Ta sama opinia o przedmiocie innym niż URL ponownie używa kształtu treści
i zmienia tylko `record/about[0]` oraz `topic/key` koperty:

```json
{
  "schema": "agora-record.v1",
  "record/kind": "opinion",
  "topic/key": "ai.orbiplex.opinions/ean",
  "record/about": [
    { "resource/kind": "ean", "resource/id": "5901234123457" }
  ],
  "content/schema": "resource-opinion.v1",
  "content": {
    "schema": "resource-opinion.v1",
    "opinion/text": "Solid packaging, product matched the description.",
    "opinion/rating": 4
  }
}
```

Ilustruje to, dlaczego warstwy podłoża (przyjmowanie, zapytania, indeks
przedmiotów, ACL tematów) pozostają otwarte na `resource/kind`: nowy rodzaj nie
dodaje nowego schematu treści ani nowej powierzchni relaya.

## Konsekwencje dla modeli odczytu MVP {#mvp-read-model-consequences}

Minimalne modele odczytu wynikające z propozycji:

- lista opinii według dokładnego `resource/key`, rozstrzygniętego
  z `record/about[0]` koperty,
- lista opinii według `author/participant-id` koperty,
- obliczanie prostych agregatów, takich jak liczba opinii i średnia ocena,
  tam, gdzie oceny występują.

Wszystkie trzy modele odczytu są budowane na polach koperty i treści
`resource-opinion.v1`; żaden nie czyta tożsamości z treści.

Konsumenci hard-MVP POWINNI tolerować:

- zasoby bez ocen, z samym tekstem,
- zasoby z ocenami i bez tekstu,
- wiele opinii tego samego autora w czasie, gdy polityka nie egzekwuje jeszcze
  `supersedes`.

## Zalecenia implementacyjne {#implementation-recommendations}

Stosować `node:DEV-GUIDELINES.md`: ponownie użyć istniejącej pary zasobu, granic
podpisywania i admisji oraz projekcji zasilanych replayem. Ta kontynuacja zamyka
luki konsumentów; nie wprowadza kolejnego protokołu identyfikatorów, rejestru
krajowego w rdzeniu ani obowiązkowego wyszukiwania NIL.

### Re-use i granice konsumentów {#reuse-and-consumer-boundaries}

Przegląd konsumentów z 2026-10-10 wykazał następujące pozostałe miejsca integracji:

- `node:agora-core/src/envelope.rs` już jest właścicielem `ResourceRef`;
  `node:agora-relay-trait/src/subject_index.rs` indeksuje pełną nieprzezroczystą
  parę. Użyć ich zamiast dodawać typ tożsamości świadomy krajów.
- `node:agora-ui/src/agora.rs` ma już wyszukiwanie przedmiotów i builder opinii
  z osobnymi wartościami rodzaju/id, ale formularz opinii wymusza `url`;
  generyczny builder compose nie wypełnia `record/about` koperty.
- `node:agora-projections/src/lib.rs` obecnie wyprowadza `resource_key` opinii
  jako digest pary, a `node:agora-service/src/main.rs` odpytuje bezpośrednio
  ten zapisany klucz. To niezgodność konsumenta z §1, nie zamiennik przyjętego
  kontraktu `kind:id`.
- Publiczna plotka zachowuje `gossip/see-also` w treści, ale nie projektuje
  tych linków tak jak opinie. Osobnym właścicielem jest
  [backlog Agory P17](../60-solutions/008-agora/008-agora-backlog.md#p17-public-gossip-resource-links);
  nie jest to zależność podstawowej publikacji zasobu ani wyszukiwania przedmiotu.

Są to ustalenia z kodu, nie twierdzenie o zachowanej akceptacji runtime.
Dowody implementacji i szczegółowe noty migracyjne należą do Node.

### Małe kształty danych, wspólne konwersje {#small-data-shapes-shared-conversions}

Zachować odrębność poniższych kształtów; są powiązaniami istniejących kontraktów,
nie nowymi schematami transmisji:

| Powierzchnia | Kształt | Reguła |
|---|---|---|
| Wartość zasobu | `{"resource/kind": "pl-nil-pwz", "resource/id": "<pwz-number>"}` | Użyć `ResourceRef`; rodzaj pozostaje otwarty, id pozostaje stringiem. |
| Główny przedmiot opinii | `record/about[0] = ResourceRef` | Wymagany dla opinii; późniejsze wpisy nie mogą zmieniać kolejności ani zastępować głównego przedmiotu. |
| Przedmioty generycznego compose | `record/about = [ResourceRef, ...]` | Opcjonalne dla rodzin rekordów niewymagających przedmiotu, w tym publicznej plotki. |
| Powiązana referencja | `[kind, id]` w `opinion/see-also` lub `gossip/see-also` | Zachować pełną przestrzeń nazw i id; nie zastępować drugiego elementu kluczem pochodnym. |
| Publiczny klucz pochodny | `kind + ":" + id` | Dzielić tylko po pierwszym dwukropku; jeśli podano obok pary, odrzucać niezgodność. |

Użyć wspólnego edytora zasobów UI z osobnymi wejściami rodzaju/id i wygodnym
trybem URL. Tryb URL wybiera `kind = url`; tryb generyczny nie może uruchamiać
parsera URL ani wymagać zarejestrowanego walidatora. Podpowiedzi przestrzeni nazw
są opcjonalne, nie są allowlistą. Zachować początkowe zera, wielkość liter,
interpunkcję i wewnętrzne dwukropki nieprzezroczystych id; bez wymuszania typu
liczbowego ani cichego przycinania/normalizacji. Normalizacja właściwa dla rodzaju
należy do jawnie wybranego kontraktu rodzaju, nie generycznego edytora ani relaya.
Escapować wyświetlane wartości i kodować procentowo każdy segment lokalnej trasy;
nieznane id nie jest automatycznie nawigowalnym zewnętrznym URL-em.

Oba formularze powinny mapować lokalne pola szkicu do istniejącego buildera
koperty przed podpisaniem. Nie umieszczać `record/about` w `content`, nie
wywodzić go z `see-also` ani nie zastępować celu opinii wskazującego rekord
pogłoski osobą w niej wspomnianą. Użyć istniejącego przepływu signer/unlock
i polityki admisji; walidacja klienta nie zastępuje Schema Gate na granicach
protokołu. Jawnie stosować limity każdego pola odbiorczego (w tym limit 512
znaków id w `see-also` wobec 2048 w `resource-ref.v1`); odrzucać nadmiarowe
wejście z diagnostyką pola, zamiast je obcinać lub częściowo publikować.

Zaimplementować konwersje pary na klucz, klucza na parę i pary na krotkę raz,
jako czyste operacje u najniższego istniejącego wspólnego właściciela. Nie
tworzyć nowej usługi ani crate’a tylko dla helperów. Testować
`decode(encode(pair)) = pair`, również dla id zawierających dwukropki,
i zachować walidację każdego nośnika na jego granicy.

### Zgodność klucza projekcji i odzyskiwanie {#projection-key-compatibility-and-recovery}

Autorytatywne wyszukiwanie używa dokładnej pary, z porównaniem uwzględniającym
wielkość liter (`BINARY`). Publiczny DTO `agora-projections.opinions.v2`
udostępnia `subject/kind`, `subject/id` i pochodny `subject/key`. `subject/key`
przedstawia pojęciowy `resource/key` z §1; unika mylenia tej tożsamości
z `effects[].resource/key` middleware, które ma niezależny kontrakt. Żaden
digest ani klucz pochodny nie jest autorytatywny ani zapisywany dla nowych
wierszy opinii.

**Decyzja (2026-10-12):** zapytania o opinie przyjmują tylko `resource_kind`
i `resource_id`, każde dokładnie raz. Stare nazwy parametrów `resource_key`
i `resource-key` zawsze zwracają HTTP 400 `legacy-digest-parameter-removed`,
dla każdej wartości, również obok poprawnej pary. Starsze `sha256:<digest>`
samo jest poprawną otwartą referencją; heurystyczne wykrywanie wartości lub
zastrzeżenie `sha256` naruszałoby otwarte przestrzenie nazw. Zinwentaryzowanym
konsumentem w repo jest usługa Agora; zmienia się wraz z API projekcji.
HATEOAS używa pełnej pary.

Migracja tworzy indeks `(resource_kind, resource_id, authored_at, record_id)`.
Przestarzała kolumna `resource_key NOT NULL` pozostaje czytelna tylko dla
starego oprogramowania: istniejące wartości pozostają nienaruszone, a nowe
wiersze zapisują pustą wartość. Bieżący czytelnicy nigdy jej nie używają.
Podpisane rekordy źródłowe, ich id i podpisy pozostają bez zmian.

Stosować [S028 Temporal Storage Convention](../60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md)
dla osobnego operatorskiego trybu replayu `rebuild` (domyślny `incremental`,
początkowo tylko domena opinii). Wspólnie przygotować opinie, tagi, linki
i indeksowane bieżące blokady przedmiotów, utrwalać kursory źródłowe, nadgonić
współbieżne przyjmowanie i atomowo podmienić domenę. Odczyty sieciowe
i weryfikacja działają poza transakcjami zapisu. Brak/przycięcie źródła lub
przerwana praca zachowują aktywną projekcję i raportują niekompletną
rekonstrukcję. Awarie przypisywalne parze degradują tylko tę parę;
nieprzypisywalne jawnie raportują nieznaną kompletność. Przyrostowy replay
i odbudowa używają tej samej decyzji projekcji: niepoprawne zachowane rekordy
są diagnozowane jako odrzucone i przesuwają kursor źródła. Brak źródła jest
inną awarią i nadal zachowuje aktywną projekcję. Bieżące blokady przedmiotów
są indeksowanym stanem; dziennik diagnostyczny nie jest skanowany przy każdym
odczycie.

Admisja odczytu tematu poprzedza limit widocznych wyników. Ograniczony skan
zwraca `complete` i związany z parą `next_cursor`, w tym częściową pustą stronę
po wyczerpaniu budżetu skanu. Kontynuacja UI używa pełnej pary. Błędy referencji
ujawniają typowane wartości `field` i `reason` w kebab-case.

### Autorstwo i historyczne referencje {#authoring-and-historical-references}

Czyste konwersje ResourceRef zachowują parę i dzielą klucz po pierwszym
dwukropku. Walidacja jest osobną operacją: nowe buildery, endpointy podpisywania
i zapytania egzekwują rodzaj w postaci sluga, 1–2048 punktów kodowych Unicode
(najwyżej 8192 bajty UTF-8), granice białych znaków ECMA-262, brak znaków
kontrolnych i NFC. NFC używa tej samej definicji co kanonikalizacja podpisów.
Nie normalizować nieprzezroczystych id ani nie odrzucać wszystkich znaków
formatowania/bidi. Wyświetlać przyjęte znaki formatowania z widocznymi
znacznikami punktów kodowych i izolacją kierunku tekstu.

[Profil autorstwa Agory](../../schemas/agora-record-authoring.v1.schema.json),
stosowany tylko przy tworzeniu, ogranicza nowe tablice `record/about` do ośmiu
unikatowych referencji. Istniejące podpisane koperty v1 nie dziedziczą tego
ostrzejszego profilu. Ingress, indeksowanie i replay zachowują dopuszczoną
historię i zapisują ostrzeżenia w diagnostyce projekcji. Historyczne id non-NFC
zachowuje pierwotną parę i odczyt przez record-id; ścisłe zapytanie o tę
niepoprawną parę zwraca 400. Ograniczenia nośników pozostają lokalne, w tym
limit 512 znaków id w `see-also`.

Nowa publikacja ma wspólny budżet koperty JSON 48 KiB, włącznie z podpisem
i metadanymi relaya. Sprawdzać oszacowanie przed podpisaniem i rzeczywistą
podpisaną kopertę przed publikacją, z diagnostyką pola/koperty i bez obcinania.
Zostawia to konserwatywny zapas w limicie pełnego PDU Matrix wynoszącym 64 KiB;
musi go potwierdzić rzeczywista akceptacja Matrix. `+` w query dekoduje się do
spacji, `%2B` do plusa; `+` w ścieżce jest literalny. Jeden encoder URI emituje
literalnie tylko znaki niezastrzeżone. Dopuszczalna linia żądania 32 KiB jest
lokalna dla odczytów przedmiotów i opinii; pozostałe trasy zachowują 8 KiB.

Wspólny edytor bez JavaScript trzyma szkice w polach formularza. Chronione
CSRF intencje POST podglądu dodają, usuwają i przestawiają wiersze bez
podpisywania. Wiersz zerowy opinii jest jawnie głównym przedmiotem. Podgląd
zamraża autora, znacznik czasu, dokładny dokument i digest; edycja wymaga
nowego podglądu, a ponowienia 423/unlock zachowują dokument. UI przedmiotu
łączy odczyty projekcji opinii z publiczną plotką z indeksu przedmiotów relaya,
deduplikując id rekordów i pokazując diagnostykę źródeł. Nie implementuje to
nawigacji powiązanych linków P17.

### Granica akceptacji {#acceptance-boundary}

Transport publikacji jest osobną wymaganą integracją hard-MVP Node, należącą do
[P035-001–003](035-agora-topic-addressed-record-relay.md#delivery-integration-tracker):
producenci compose/opinion/comment podpisują przez istniejącego hosta
i przekazują dokładne rekordy adapterowi Agora w AD. Zachować `record/about`,
otwarte przestrzenie nazw zasobów, władzę tematu i id rekordów; pokazywać
publikację oczekującą w kolejce odrębnie od przyjętej przez relay. Nie
wprowadzać nadawcy ani kolejki ponowień specyficznych dla opinii. P026-001–003
pozostają niezależnie zamykalne na istniejącej ścieżce publikacji; po migracji
ponowić ich asercje konsumentów przez AD, zamiast twierdzić, że stare dowody
potwierdzają nową ścieżkę. Operator promował P035-001–003 2026-11-04: wszystkie
trzy muszą być zamknięte przed gotowością hard MVP lub `alpha-node`.
Historyczne ukończenie P026 nie spełnia tej osobnej bramki integracji.

Użyć syntetycznych fixture’ów dla `pl-nil-pwz` i niezarejestrowanej przestrzeni
nazw, dwóch rodzajów ze wspólnym identycznym id, id z początkowymi zerami oraz
id zawierającego dwukropki i znaki wrażliwe dla URL. Nie potrzeba żywego
rejestru zawodowego ani opinii o rzeczywistej osobie. Nowy rodzaj musi działać
bez zmiany kodu ani allowlisty.

Zachować dowody dla obu builderów UI i zwykłej ścieżki podpis → publikacja →
zapytanie o przedmiot → zapytanie projekcji → odczyt UI, następnie powtórzyć
odczyty po restarcie/replayu. Uwzględnić publiczną plotkę na przyjętym temacie
public-signals, zachowując status epistemiczny. Osobno przećwiczyć zachowanie
kształtu `see-also`; nawigację linków plotki kwalifikuje tylko Agora P17,
nie ten podstawowy slice. Przypadki negatywne obejmują brak przedmiotu opinii,
usunięte nazwy parametrów digestu, brakujące lub powtórzone elementy pary,
niepoprawne/nadmiarowe referencje, odmowę publikacji i escapowany złośliwy tekst
wyświetlany. Sama nieznana przestrzeń nazw nie jest powodem odmowy według
generycznej walidacji kształtu; zwykła polityka admisji i ujawniania nadal obowiązuje.

Same fixture’y schematów i testy jednostkowe nie zamykają bramki UI/runtime.
Zapisać testowane rewizje, komendy, zakres runtime/backendu i zachowany raport
w Node; uzgodnić ledger implementacji oraz dotknięte twierdzenia MVP po wejściu
implementacji, zamiast oznaczać je jako ukończone na podstawie planu.

### Ekspozycja ocen: re-use i akceptacja {#assessment-exposure-reuse-and-acceptance}

Przed dodaniem endpointów zbadać i ponownie użyć tych miejsc integracji
(inspekcja: 2026-10-23):

| Warstwa | Istniejące miejsce integracji / planowany dodatek | Granica |
|---|---|---|
| Prymityw | Istniejące helpery canonical-json i kryptografii; mały wspólny moduł/crate zobowiązań, jeśli uzasadniają go oba powiązania | Tylko hashowanie/weryfikacja JCS; domena, typowany payload, generowanie soli i admisja pozostają jawnymi wejściami/właścicielami. Zobowiązania entropii panel-draw nie są głosowaniem ocen. |
| Polityka | Planowany czysty `assessment-exposure-core` | Zwalidowany profil + fakty w zakresie + jawny czas -> typowane `ExposureDecision`; zamknięte enumy, bez zależności od hosta. |
| Kontrakty | Istniejące Schema Gate i dispatch kontraktów rodzajów Agory | Dodać/wersjonować kontrakty profilu, faktu, widoku i czterech rodzajów rundy z `x-dia-basis`; zachować otwartą przestrzeń nazw zasobów i podpisane historyczne bajty. |
| Projekcja | `node:agora-projections/src/lib.rs` | Użyć reguł parsowania/rewizji opinii; osobna projekcja rundy i proweniencja wyniku. `OpinionView` nie jest polityką ani prywatnym magazynem ekspozycji. |
| Usługa | `node:agora-service/src/opinion_query.rs` | Istniejący callback `admit` pozostaje autoryzacją. Dodać `expose` po admisji, przed skanowaniem/rankingiem/paginacją cudzych opinii; surowe `OpinionPage` nie jest DTO klienta. |
| Lokalna trwałość | Temporalny log zdarzeń/profil/manifest [S028](../60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md) | Prywatne fakty ekspozycji są osobną domeną odzyskiwania; odbudowa projekcji relaya nie może ich usunąć. Utrwalać tylko ograniczone niezbędne fakty, nigdy niepowiązaną historię przeglądania. |
| Skutki i powierzchnie | Istniejący signer/relay Agory, outboxy domenowe, rejestr P072, obserwacje P073, renderowanie P057/S039 | Bez drugiego systemu podpisywania, schedulera, powiadomień ani capabilities. UI/CLI renderują te same dane projektowane przez hosta. |

Pierwszą dostawą jest lokalna bramka opinii i kuracji pogłosek, obejmująca każdą
dopuszczoną powierzchnię widza. Może się zamknąć bez rund zamkniętych. Druga
dostawa dodaje zobowiązania/bariery i jawne powiązania profili; nie może wstecz
etykietować pierwszej jako protokołowo niezależnej. Samo dodanie kontynuacji
nie powinno blokować ścieżki do alfy ani ponownie otwierać zakwalifikowanej bazy.

Akceptacja zaczyna się od odmów, restartu i replayu, używając syntetycznych
uczestników i fixture’ów zamiast ocen rzeczywistych osób:

- Przy identycznych wejściach własnych/wyjątków/publicznej polityki zmieniać
  ukryte cudze wartości, liczbę, porządek i napływ: bajty API, kursory, ETagi,
  rankingi, skład stron, wynik renderowania i aktywność powiadomień/SSE nie
  mogą ujawniać zmian. Sprawdzić listę, szczegóły, wyszukiwanie, by-id, eksport,
  CLI i ścieżki Agenta, nie tylko CSS przeglądarki.
- Klienci przeglądarkowi bez JS i z JS pokazują `withheld`, nie zero,
  udostępniają jawne pominięcie i zachowują je po restarcie. Zweryfikować
  osobnych widzów, zaostrzenie profilu, odmowy odczytu, przyjętą własną ocenę,
  wygaśnięcie lokalnego okna i współbieżne odblokowanie.
- Odbudować opinie z relaya bez utraty prywatnych faktów ekspozycji. Testować
  kompakcję, brak historii, awarię magazynu, cofnięcie zegara i brak syntetycznej
  niezależności po retencji. Awaria schedulera nie może wydłużać rzeczywistego terminu.
- Różne sole dla równych treści o małej entropii dają różne zobowiązania;
  zła treść/sól/domena/autor/runda i niekanoniczne kodowania nie przechodzą.
  Odtworzone rekordy są idempotentne, różne powtórzone zobowiązania powodują
  equivocation, brak ujawnienia jest raportowany, zobowiązanie spoza zbioru
  otrzymuje `outside-barrier`, a brakujące/niepoprawne referencje bariery nie
  mogą być zliczone. Zweryfikować ograniczoną pracę weryfikatora i odzyskiwanie po restarcie.
- Testować wyścig zamknięcia z admisją, brak zobowiązania mającego receipt,
  forki bariery, nieudostępnioną barierę, częściową historię relaya, termin
  ujawnienia i round-trip transportu. Spóźnione przedłożenie nie może wejść
  do pierwszego zbioru; korekty zachowują wcześniejszą proweniencję.
- Sfałszowana etykieta bezpieczeństwa lub ocena przemycona w rodzaju ochronnym
  jest odrzucana. Rzeczywista pilna ochrona, obrona/wyłączenie i odwołanie
  pozostają dostępne, gdy zwykłe cudze oceny są ukryte; żaden wynik ekspozycji
  nie nadaje uprawnień egzekwowania.

Zachować w Node jeden raport z przypiętym źródłem, osobnymi kwalifikacjami
lokalnymi/rund/profili, negatywnymi fixture’ami, zadeklarowanymi wyłączeniami
i dowodami odzyskiwania. Użyć harnessu open-reference/Agora oraz fixture’ów
local-accountability/Corpus dla odpowiednich powiązań. Aktualizować ledger/MVP
Node tylko zgodnie z dowodami; skuteczność społeczna i federacja wymagają
osobnej kwalifikacji.

Motywacja badawcza, nie reguła ustawiania okna:
[randomizowany eksperyment](https://pubmed.ncbi.nlm.nih.gov/23929980/)
Muchnika, Arala i Taylora wykazał asymetryczne skutki wcześniejszych ocen,
w tym narastający pozytywny efekt stadny. Wspiera to testowanie najpierw
ukrywania agregatów/wskazówek popularności; nie ustanawia czasu właściwego
Orbipleksowi ani gwarancji, że opóźnione ujawnianie poprawi oceny każdej wspólnoty.

## Tracker implementacji {#implementation-tracker}

Ten tracker obejmuje kontynuację konsumentów, nie retrospektywny inwentarz
już zaimplementowanego podłoża. Statusy to `todo`, `in-progress`, `partial`,
`done`, `blocked` i `deferred`; `done` wymaga wskazanej bramki i powiązanych
dowodów Node.

| ID | Zadanie | Status | Zależności | Bramka ukończenia |
|---|---|---|---|---|
| P026-001 | Generyczne autorstwo zasobów w UI opinii i compose | done | Istniejąca baza signera i indeksu przedmiotów Agory | Oba formularze używają edytora rodzaju/id i wypełniają `record/about` koperty; pozostaje wygodny tryb URL; nieznany rodzaj działa bez rejestracji; przechodzą testy nieprzezroczystych id, limitów pól, escapowania i odmowy publikacji. |
| P026-002 | Kanoniczne publiczne klucze opinii i migracja starszej projekcji | done | Kontrakt tożsamości §1; S028 | Wspólne konwersje zachowują `kind:id`; zapytania używają dokładnej pary; usunięte nazwy parametrów digestu są odrzucane; przestarzała kolumna nigdy nie jest czytana; odbudowa domeny i zmiany konsumentów są udokumentowane; przerwana odbudowa, równoważność replayu i diagnostyka niekompletnego źródła są testowane bez przepisywania podpisanych rekordów. |
| P026-003 | Akceptacja konsumentów otwartych przestrzeni nazw | done | P026-001, P026-002 | Zachowane dowody UI i runtime obejmują macierz granicy akceptacji dla opinii i publicznej plotki, w tym dwie przestrzenie nazw z tym samym id, restart/replay i ścieżki odmów; zakres raportu odróżnia podstawowe referencje od nawigacji linków Agora P17; uzgodnione są odpowiednie dowody ledgera/MVP Node. |

Zakwalifikowany checkpoint (2026-10-12): `node:docs/evidence/open-references/README.md`
zachowuje istniejący profil `story-008.smoke-result.v1`, jego kwalifikator
i artefakty procesów/HTTP na przypadek: 20 przypadków runtime SQLite i 18 Matrix
oraz osobne procesy zgodności. Matrix B buduje indeks przedmiotów z przychodzącego
`/sync` przed projekcją opinii, a następnie powtarza odczyty UI/API po restarcie
i replayu. Podpisana historia non-NFC jest zachowana dokładnie i diagnozowana.
Oba backendy publikują kopertę 49 134 bajtów w budżecie 48 KiB i odmawiają
nadmiarowemu tworzeniu. Ledger Node i wpisy MVP Story-008 zapisują ten zakres
konsumentów.

Matrix używa odrębnych klientów na jednym homeserverze; dowodzi to dystrybucji,
nie federacji. **Plotka Matrix jest zakwalifikowana tylko dla całkowitych liczb
JSON**; zachowany fixture ma `confidence=1`. Zwykła ułamkowa pewność, np. `0.5`,
pozostaje niezakwalifikowana. To niezgodność kontraktu transportu: kanoniczny
JSON Matrix dopuszcza tylko liczby całkowite w `[-(2^53)+1, (2^53)-1]`.
Conduit v0.7.0 ujawnił ją jako HTTP 500 (`IntConvert`); odpowiedź jest
obserwacją, nie przyczyną ograniczenia.
[Kanoniczny JSON Matrix](https://spec.matrix.org/latest/appendices/#canonical-json)

[P035-004](035-agora-topic-addressed-record-relay.md#matrix-carrier-tracker)
odpowiada za zastąpienie nieprzezroczystym nośnikiem i budżet zakodowanego PDU.
Zamknięcie tych trzech wierszy nie kwalifikuje ogólnej plotki z liczbami
dziesiętnymi, innych powierzchni P026 ani gotowości produkcyjnej. Pierwotne
artefakty procesów i rewizje pozostają zamrożone; raport kwalifikacji i indeks
dowodów niosą korektę zakresu.

Korekty przeglądu (2026-10-12): bieżąca projekcja, przyrostowy replay i odbudowa
domeny współdzielą decyzje odrzucenia opinii i diagnostykę. Odrzucenie treści
przesuwa przygotowywany kursor źródła; utrata źródła nadal oznacza niekompletną
odbudowę. Bieżące blokady par należą do indeksowanego modelu odczytu
`opinion_subject_blocks`, osobnego od dziennika tylko dopisywanego, i są
zastępowane wraz z przygotowaną domeną. Admisja odczytu poprzedza limit
widocznych wyników przez ograniczone skanowanie stron; `complete` i związany
z parą `next_cursor` odróżniają wyczerpanie od niedokończonej pracy. Pola
przedmiotu DTO używają `subject/kind`, `subject/id`, `subject/key`. Hashe
przeglądu używają JCS bez normalizacji stringów. Niedawna diagnostyka
historyczna odsyła do pobierania przez record-id bez rozluźniania ścisłych
zapytań o parę.

Zachowane `node:docs/evidence/open-references/2026-10-12-review/qualification.json`
kwalifikuje korekty przez 20 przypadków runtime SQLite, 18 Matrix i 453 testy
zgodności na backend. Rewizje źródeł runtime to Node `9f114aae` i Orbidocs
`308e936`; indeks dowodów wyjaśnia obserwacje odrzuconej historii, widoczności
i materializowanych blokad. Ogólna plotka z liczbami dziesiętnymi nadal nie
jest zakwalifikowana.

### Kontynuacja dla przyciętych źródeł {#pruned-source-continuation}

| ID | Zadanie | Status | Zależności | Bramka ukończenia |
|---|---|---|---|---|
| P026-004 | Jawne przenoszenie poprzedniego stanu dla przyciętych źródeł opinii | todo | P026-002; S028 | Zachować ścisłą odbudowę jako domyślną. Jawny tryb carry-forward zachowuje wcześniejsze wiersze opinii/tagów/linków/blokad tylko tam, gdzie dowiedziono utraty źródła; zapisywać wcześniejszą rewizję projekcji, granice źródła i dziedziczoną proweniencję każdego rekordu. Raporty odróżniają wiersze przeliczone od odziedziczonych, zachowują wcześniejsze blokady i nieznaną kompletność oraz nigdy nie deklarują równoważności replayu z pełnego źródła. Fixture’y restartu, współbieżnego przyjmowania, utraty źródła i przyszłego formatu kwalifikują tryb przed promocją statusu. |

P026-001 i P026-002 mogą postępować niezależnie względem istniejącego kontraktu
pary; P026-003 zamyka wspólny slice. Indeksowanie i nawigacja powiązanych linków
publicznej plotki pozostają zadaniem z jednym źródłem
[Agora P17](../60-solutions/008-agora/008-agora-backlog.md#p17-public-gossip-resource-links),
które może postępować niezależnie i nie może blokować podstawowego wsparcia
otwartych przestrzeni nazw.

<a id="assessment-exposure-continuation-planned"></a>

### Kontynuacja ekspozycji ocen {#assessment-exposure-continuation}

| ID | Zadanie | Status | Zależności | Bramka ukończenia |
|---|---|---|---|---|
| P026-005 | Zamrożenie wspólnych kontraktów ekspozycji i rund | partial | Istniejące kontrakty tożsamości i admisji P026; P091; S028 | Zbadać wszystkie ścieżki odczytu/powiadomień/rankingu/surowego dostępu; zamrozić zamknięte kształty polityki/faktu/widoku, uwierzytelnionego widza i semantykę zetknięcia/odsłonięcia, limity, powiązania rodzajów ochronnych oraz Q-02/Q-03. Osobno zamrozić typowane powiązania domenowe, dokładne bajty zobowiązania, reguły autorytetu/receiptów/zegara/forków i retencję sekretów rund. Dodać pozytywne/negatywne fixture’y Schema Gate; sama obecność schematu nie deklaruje nowej capability runtime. Lokalny checkpoint 2026-10-24: zamrożono cztery lokalne kontrakty i ich fixture’y Schema Gate. Autorytet/receipty/bajty zobowiązań rund i konkretne powiązania rodzajów ochronnych pozostają odroczone; lokalna lista wyjątków jest pusta. Korekta przeglądu: przyjęto monotoniczne fakty komend, nowy jawny czas zetknięcia, ograniczone zdegradowane pokrycie, kształty oczekiwania na ujawnienie/okna i sondy; nie zamyka to kontraktów rund. Q-02 zamraża admisję właściciela związaną z funkcją buildu jako wejście fixture’u, odrębne od produkcyjnego provisioningu (P026-012); dowody runtime nie zamykają odroczonych kontraktów. Krytyczny przegląd Q-02 egzekwuje istniejący zamknięty kontrakt hooka bez zmiany semantyki domeny; bramki provisioningu i rund pozostają osobne. |
| P026-006 | Lokalna polityka ekspozycji i prywatne fakty temporalne | done | Lokalne kontrakty 005 | Czysta polityka z jawnym czasem, trwałe fakty zetknięcia/odblokowania/odsłonięcia i odtwarzalne ograniczone podsumowania; użyć mechaniki S028 poza ProjectionStore. Dowieść restartu, idempotencji, odwołania autoryzacji, zmiany profilu, luk retencji, niepewności zegara i zachowania po nieudanym zapisie. Lokalny checkpoint 2026-10-24: testy czystego rdzenia i prywatnego magazynu obejmują wskazane lokalne bramki; regresja odwołania wspólnego widoku zachowuje trwałe odsłonięcie, pomijając niedopuszczoną treść. Pierwotny przebieg 04 dodaje dowody rzeczywistego restartu procesu i odbudowy projekcji. Zamyka to tylko lokalną politykę/prywatne fakty. Testy granic/migracji przeglądu obejmują pełne stare receipty, atomową kompakcję balanced/minimal, odmowę full-audit i utrzymanie przy zatrzymanym właścicielu, zachowując ujawnienie/historię. |
| P026-007 | Projekcja widza u konsumentów Agory | partial | 006 | Złożyć admit/expose w usłudze; objąć bramką każdą zbadaną powierzchnię listy/szczegółów/wyszukiwania/eksportu/rankingu/strumienia/CLI/Agenta bez zmiany autoryzacji. Przy ukryciu brak kursorów, ETagów, liczników i zerowych placeholderów wyprowadzonych z cudzych opinii; strumienie własny/ochronny pozostają ograniczone. Rejestrować tylko rzeczywiście nowe operacje przez P072, jeśli istniejące nie mogą przenieść kontraktu. Lokalny checkpoint 2026-10-24: zaimplementowano ograniczony widok (do 100 wpisów na strumień własny/cudzy) i zarejestrowane adaptery; mieszane surowe odczyty/strumienie/sondy podpisywania referencji odmawiają niepowiązanego dostępu. Bogata paginacja, szersza kwalifikacja konsumentów i osobna uprzywilejowana inspekcja bezpieczna dla widza pozostają przyszłą pracą. Implementacja przeglądu używa allowlisty tras z domyślną odmową, odmowy znaczników rekordów/POST, admisji UI/Agenta przed odczytem i jednej polityki wykluczeń uwagi; ograniczone pokrycie pozostaje jawne. Przebieg Q-02 07 kwalifikuje rzeczywistą izolację/utratę/restart modułu z powiązaniem harnessu i zwykłe przejścia Agenta przez local-control; produkcyjni widzowie modułowi są niedostępni do P026-012. Krytyczny przegląd zamyka revoke z dodatkowymi polami i fallback niepoprawnego właściciela w hooku wyłącznie akceptacyjnym; HTTP modułu nadal prowadzi harness z poświadczeniami. |
| P026-008 | Akceptacja lokalnej ekspozycji | partial | 007; P013-AE-001; P057-014; P073 assessment-exposure-observations | Dowody host/API/przeglądarki bez JS i z JS z przypiętymi źródłami zaliczają powyższe lokalne przypadki, w tym powiadomienia, tożsamość Agenta, macierz wycieków, odbudowę i retencję. Zakres local-display-only pozostaje jawny; bez twierdzenia o rundach zamkniętych ani skuteczności społecznej. Pierwotny przebieg 04 kwalifikuje dziewięć lokalnych przypadków host/API/UI/CLI i rzeczywiste przeglądarki JS/no-JS. Fixture’y komponentów/syntetycznego hosta Agenta i powiadomień są zapisane osobno. Pełna wspólna macierz P013/P057/P073 i szersza kwalifikacja transportów/profili pozostają otwarte. Przebieg przeglądu 01 dodaje nowe świadki odmów/okna przy czystym Node 91babeb0 / Orbidocs 414acd72; niezależne v2 i 38 negatywnych przypadków weryfikatora zgadzają się przed i po rozpakowaniu. Przebieg Q-02 07 dodaje siedem ograniczonych przypadków rzeczywistych procesów przy Node 4e29d5d3 / Orbidocs 48282704: cztery runtime i trzy fixture-bound-input, w tym rzeczywiste zawieszenie/wznowienie Agenta. Kwalifikacja normalnie/-O/po rozpakowaniu i 21 negatywnych przypadków weryfikatora zgadzają się; sześć niekompletnych prób zachowano. Pełne macierze i provisioning pozostają otwarte. Przebieg przeglądu Q-02 02 przy Node 6abf71df / Orbidocs d09d1035 dodaje końcową zgodność źródła/obrazu i uporządkowane świadki władzy/Agenta v2; wszystkie 42 negatywy odmawiają normalnie/-O i po rozpakowaniu. Początkowa odmowa kwalifikacji pozostaje zachowana. |
| P026-009 | Wspólna mechanika zobowiązania i bariery | todo | Kontrakty rund 005 | Użyć kanonicznego JSON/kryptografii, signera i prymitywów trwałego właściciela. Dowieść izolacji soli/domen, dokładnych bajtów transportu, ograniczonego zamknięcia przyjętego zbioru, receiptów admisji, forków/equivocation, jawnych terminów i replayu. Mechanika biblioteczna nie liczy się jako zaimplementowana domenowa bariera publikacji. |
| P026-010 | Właściciel rund zamkniętych Agory i projekcje | todo | 009; 007 | Wdrożyć cztery dopuszczone rodzaje rekordów, właściciela/CAS/outbox, chronioną lokalną retencję treści/soli i projekcję świadomą rund z wynikami na zobowiązanie. Nieznane rodzaje pozostają nieindeksowane przez starszych konsumentów opinii; żaden prywatny payload zarządzania/Room nie jest wtłaczany w publiczną Agorę. |
| P026-011 | Adwersarialna akceptacja rund zamkniętych | todo | 010 | Zachować powyższe przypadki rund przez rzeczywiste API signera, relaya, właściciela i widza; testować wyścigi terminów, pominięte wpisy z receiptami, forki autorytetu, przerwanie, brak historii, restart i limity. Kwalifikacja publicznego transportu zachowuje zakres; powiązania P051/P069 wymagają własnych dowodów i nie są warunkiem dostarczenia lokalnej bramki. |
| P026-012 | Provisioning reprezentowanych lokalnych wywołujących | partial | Identity host; P073; P066; P026-005 | Podział v2 przyjęty 2026-10-24: 012a to produkcyjny provisioning modułów ChannelJson; 012b odpowiada za osobnego konsumenta P073. Zob. [zamrożony kontrakt 012a](026-assessment-viewer-grants.md). Historyczne Q-02 pozostaje dowodem związanym z fixture’em. |
| P026-012a | Provisioning widza ocen operatora przez ChannelJson | done | P066; identity host; P080 | Ograniczony checkpoint 2026-10-25: przebieg 06 przy czystym Node e726624c / Orbidocs 2e73ed3a kwalifikuje osiem przypadków zwykłego daemona/aplikacji/przeglądarki bez funkcji akceptacyjnej, z rzeczywistymi wywołaniami SDK, konsumpcją P066, prywatnością, budżetem i lifecycle. Osobne dowody komponentów obejmują uchwycone pochodzenie z kolejki, zegary, trwałość i współbieżność. Bieżąca kwalifikacja normalnie/-O/po rozpakowaniu i 59 kontroli negatywnych na lokalizację zgadzają się. Krytyczny przebieg przeglądu 01 przy Node 9b2e3b47 / Orbidocs 298671c5 dodatkowo kwalifikuje naprawy lifecycle/źródła przez osiem przypadków runtime, 16 testów właściciela/dziewięć przypięć i 67 kontroli normalnie/-O/po rozpakowaniu. Zob. checkpointy i zamrożony kontrakt; bez twierdzenia o module produktowym, pozytywnym konsumencie P073 ani wydaniu. |
| P026-012b | Powiązanie zamkniętego konsumenta P073 z produkcyjną władzą widza | done | 012a; P073; P066 | Ograniczony checkpoint 2026-10-25: [zamknięty konsument](026-assessment-agent-consumer.md#measured-closed-profile-checkpoint-2026-10-25), dziewięć zwykłych przypadków przy Node ea9138ba / Orbidocs 6097c43b; osobne awarie komponentów i 77 kontroli normalnie/-O na luźnych/rozpakowanych plikach. Świeży kontekst hosta, dokładny posiadacz, niezależna zgoda i wynik tylko w RAM. Bez twierdzenia o modelu/module produktowym/012c/wydaniu. |
| P026-012c | Rozszerzenie zależnego kontekstu Agenta i odbiorców | in-progress | 012b; S028; P036; P073; P066 | [Przyjęty projekt etapowy](026-assessment-dependent-context.md): strumienie z właścicielem poprzedzają retencję/dispatch jednostki, proweniencję, kontynuację i dostarczenie operatorskie dla tego samego widza. Etap 01 jest done dla zamrożonego lokalnego profilu magazynu/przełączenia. Etapy 02/03 są done dla [zakwalifikowanego wspólnego profilu lokalnego](026-assessment-dependent-context.md#p026-012c-0203-review-qualification-2026-11-01): retencja całego właściciela, trwałe S029, kapsuły/checkpointy i S020, z sześcioma zwykłymi przypadkami i osobnymi dowodami komponentów z jawnym czasem po przeglądzie R-01–R-17. Proweniencja kontekstu i późniejsze etapy pozostają otwarte. Pamięć/forki kwalifikuje się osobno; przyjęcie planu nie implikuje dowodów implementacji. |
| P026-013 | Przyszły klient perspektyw dotyczących zasobu | deferred | P026-001–003; admisja/ekspozycja widza dla wybranej powierzchni; P013-AE-003 dla integracji pogłosek | Zamrozić [profil](#resource-perspectives-client), w tym brakujący kontrakt relacji rola/działanie; użyć indeksów przedmiotów, relacji zasób/opinia/komentarz i API bezpiecznych dla widza. Fixture’y offline i ograniczone dowody przeglądarkowe zachowują granice osoby/roli/działania, konkurujące perspektywy, chronologię zdarzeń/publikacji/rewizji, sukcesję ról, korekty i naprawę, pochodzenie i jawną niekompletność bez uniwersalnego werdyktu ani wycieków ukrytych danych. Bez nowego warunku wstępnego MVP/alfa. |

### Tracker widza będącego uczestnikiem – 2026-11-06 {#participant-viewer-tracker-2026-11-06}

[P098 §8](098-alpha-ui.md#8-participant-access-contract-memarium-and-whisper)
potrzebuje projekcji rzeczywistego uczestnika, nie widza operatora/modułu
z P026-012a. Zadania ponownie używają przyjętych lokalnych kontraktów P026-005
i właściciela P026-006. Dostarczają nazwany slice uczestnika w P026-007/008,
bez czekania na rundy zamknięte ani sugerowania ukończenia szerszej macierzy
konsumentów. Ich dowody zasilają szersze zadania; ta relacja raportowania nie
jest odwrotną zależnością od ukończenia P026-007/008 ani P098.

| ID | Pozycja | Status | Zależności | Rezultat i bramka | Konsumenci (nie warunki wstępne) |
|---|---|---|---|---|---|
| P026-014 | Zamrożenie kontraktu widza-uczestnika i kontynuacji | todo | P024-009 | Związać dopuszczonego uczestnika z widzem, audytorium, projekcją właściciela i ograniczoną kontynuacją. Zachować rozdzielenie admit/expose, strumienie własny/ochronny, embargo/private-correlation i brak liczników/porządku/kursorów/ETagów pochodzących od innych przy ukryciu. Zamrozić kanoniczne kształty odczytu/kontynuacji i odmów, dokładne mapowanie tras/rejestru i brak surowego fallbacku; bez nowego kontraktu rundy. Samo powiązanie widza nie zapisuje zetknięcia ani publikacji; zachować przejścia zetknięcia określone przez właściciela. | P026-015; P098-010c |
| P026-015 | Dostarczenie projekcji odczytu Agory bezpiecznych dla uczestnika | todo | P026-014; P024-010; P026-006 | Wdrożyć ograniczone listy/szczegóły/kontynuację uczestnika i projekcje ocen. Dowieść izolacji widzów P/Q, zmiany kontekstu/polityki między stronami, niedostępnej ekspozycji, perturbacji ukrytych danych w porządku/licznikach/linkach i regresji widza operatorskiego. Zachować dowody właściciela/API niezależnie od renderowania P098. Rzeczywisty konsument Whisper i integracja kuracji/uwagi są ćwiczone przez P013-PA-003 i P098; przekazać wyniki do P013-AE-001/P026-008 bez uzależniania tego zadania właściciela od konsumentów. | P013-PA-003; P098-006 |

## Otwarte pytania {#open-questions}

Nie pozostały nierozstrzygnięte pytania dla pierwotnego slice’a opinii. Poniższe
decyzje zapisują zatwierdzone wartości domyślne; planowana kontynuacja ekspozycji
ma własne pytania do zamrożenia w sekcji 6, bez ponownego otwierania decyzji bazy.

Rozstrzygnięte 2026-07-05:

1. `resource/kind` pozostaje otwarte. Poszczególne kontrakty rodzajów mogą
   uzyskać dedykowaną walidację, gdy wymaga tego interoperacyjność lub
   bezpieczeństwo; nie zamyka to generycznego katalogu przestrzeni nazw (zob. §1.1).
2. Opinie o zasobach `node` i `org` wymagają jawnych reguł przeciwdziałania
   nękaniu, odwołań lub moderacji, zanim pojawią się w publicznych agregatach.
3. Zasoby `gps` używają klucza lokalizacji o ograniczonej precyzji. Surowe
   `lat,lon` nie jest domyślnym publicznym identyfikatorem zasobu.
4. Jeden autor ma najwyżej jedną aktywną opinię na zasób. Rewizje są tylko
   dopisywane i powiązane przez `supersedes`.
5. Tekst i ocena pozostają w jednej rodzinie artefaktów v1. Mogą się rozdzielić
   później, jeśli rozbiegną się polityki moderacji.
6. Pierwsze dołączone medium dyskusji to referencja archiwalnego forum/wątku,
   nie efemeryczny kanał przypominający czat.
7. Przyszłe artefakty dyskusji oznaczają wkład człowieka i agenta jawnymi flagami
   autorstwa/pochodzenia, ponownie używając wzorca proweniencji P004/P011.

## Konsekwencje {#consequences}

Pozytywne:

- jeden mały przenośny kontrakt ocen zasobów,
- czyste rozdzielenie od reputacji,
- generyczny model tożsamości do ponownego użycia w wielu klasach zasobów,
- warstwowanie koperta–treść utrzymuje kształt treści `resource-opinion.v1`
  niezależny od przenoszenia tożsamości, autorstwa i routingu, dzięki czemu
  ten sam schemat treści działa przez relaye Agory, eksporty archiwalne
  i przyszłe transporty,
- jasne miejsce rozszerzenia o późniejsze powierzchnie dyskusji.

Kompromisy:

- `resource/kind` pozostaje otwarte, a poszczególne kontrakty rodzajów mogą
  wymagać późniejszej pracy nad normalizacją,
- propozycja celowo pozostawia moderację i deduplikację nierozstrzygnięte,
- `resource/key` jest pochodne, nie autorytatywne, więc konsumenci muszą je
  walidować zamiast ślepo mu ufać,
- implementatorzy muszą pamiętać, że tożsamość przedmiotu **nie** jest
  w treści – każde narzędzie czytające opinie musi czytać ją z `record/about[0]`
  koperty, nie z pól `resource-opinion.v1`, które celowo już jej nie niosą.

## Dalsze działania {#follow-up}

Bezpośredni slice konsumentów to P026-001 i P026-002, a następnie P026-003.
Szersza lista poniżej obejmuje istniejące artefakty i późniejszą pracę;
nie jest dowodem ukończenia nowych zadań konsumentów:

1. jeden schemat `resource-opinion.v1`,
2. jedna nota wymagań dotycząca normalizacji i polityki rewizji,
3. opcjonalnie osobna propozycja semantyki forum lub kanału dołączonego do zasobu,
4. propozycja 040 (ponowne dostarczanie w ramach pieczy i tombstones) określa,
   jak opinie przetrwają utratę danych relaya i jak uczestnicy umieszczają kopie
   w innych węzłach pod pieczą opartą na capability passport; przepływy
   retencji opinii lub prawa do zapomnienia budują na tym podłożu.
5. Zachować jawne reguły walidacji rodzajów i cyklu życia aliasów bez zmiany
   otwartego katalogu `resource/kind` w zamknięty enum rdzenia. Krajowe przestrzenie
   nazw podążają za §1.1; walidatory pozostają poza generycznym rdzeniem.
6. Dodać warunki moderacji dla `resource/kind = node` i `resource/kind = org`:
   jawne reguły przeciwdziałania nękaniu, odwołań lub moderacji muszą istnieć
   przed udostępnieniem publicznych agregatów.
7. Określić kontrakt klucza GPS o ograniczonej precyzji dla `resource/kind = gps`;
   surowe `lat,lon` nie jest domyślnym publicznym identyfikatorem zasobu.
8. Udokumentować semantykę jednej aktywnej opinii na autora: rewizje są tylko
   dopisywane, powiązane przez `supersedes` i projektowane jako najnowsza aktywna
   opinia oraz tylko dopisywana historia.
9. Potwierdzić unifikację v1: `opinion/text` i `opinion/rating` pozostają w jednej
   rodzinie artefaktów, chyba że później rozbiegną się polityki moderacji.
10. Wymagać, by przyszłe artefakty dyskusji forum/wątku/kanału oznaczały wkład
    człowieka i agenta jawnymi flagami autorstwa/pochodzenia, ponownie używając
    wzorca proweniencji P004/P011.


Checkpoint krytycznego przeglądu P026-012a (2026-10-25): czyste Node `9b2e3b47` / Orbidocs `298671c5` kwalifikują osiem przypadków zwykłego daemona/aplikacji/przeglądarki po naprawie terminalnej utraty zegara przy awarii P066, admisji aktywacji/statusu po konsumpcji i kontroli świeżego źródła. Przechodzi 16 testów właściciela i dziewięć przypięć źródeł; weryfikacja normalnie/-O oraz luźnych/rozpakowanych plików zgadza się z 67 kontrolami negatywnymi na lokalizację. Zachowano cztery starsze luki weryfikatora i początkowe niepowodzenia. Natywne dowody zegara/SQLite/pochodzenia z kolejki pozostają osobne od obserwacji zwykłych procesów. Zob. `node:docs/evidence/agent-runtime/2026-10-25-p026-012a-review/README.md` i `node:docs/audits/REVIEW-P026-012A-2026-10-25.md`. Egzekwuje to przyjęty kontrakt bez dodawania władzy; stare receipty nie są wstecz promowane do silniejszych twierdzeń o świeżości źródła. P026-012a pozostaje done w profilu lokalnym; nadrzędne P026-012/P073 pozostają partial, a 012b – todo.

Korekty przeglądu P026-012b-r1 zamrożono w [kontrakcie rewizji](026-assessment-agent-consumer-r1.md). Jego checkpoint run-04 new-wire zalicza dziesięć przypadków i 93 kontrole normalnie/-O na luźnych/rozpakowanych plikach (372 odmowy), przy Node `f5838744` / Orbidocs `4cc2f494`; zob. `node:docs/evidence/agent-runtime/2026-10-25-p026-012b-r1/README.md`. Przebieg 10 pozostaje historycznym dowodem pierwotnego źródła i profilu. Retencja historycznych metadanych pozostaje otwarta przed 012c; nie wynika z tego promocja rodzica/wydania.


### Checkpoint integracji głównej P026 (2026-10-26) {#p026-primary-integration-checkpoint-2026-10-26}

Scalony profil lokalny zalicza dziesięć przypadków zwykłych procesów przy czystym Node `660c4a1d` / Orbidocs `4a8a6d4e`, z kwalifikacją normalnie/-O przed i po rozpakowaniu oraz 93 kontrolami negatywnymi na wariant (372 odmowy). Zob. `node:docs/evidence/agent-runtime/2026-10-26-rate-exposure-integration/README.md` i `node:docs/audits/P026-PRIMARY-INTEGRATION-2026-10-26.md`. Bieżące buildery wybierają dokładny plik binarny Cargo; dwie wcześniejsze próby pozostają niezakwalifikowane, w tym nierozstrzygnięty timeout hydratacji UI i poprawnie odrzucony receipt niewłaściwego pliku binarnego. Historyczne dowody i zachowane gałęzie funkcjonalne pozostają bez zmian. Checkpoint nie promuje nadrzędnych P026-012/P073, 012c, replikacji, modeli ani gotowości wydania.


Lokalne domknięcie P026-012c-02/03 (2026-10-30): Node `da1d14a7` / Orbidocs `127843fb`
kwalifikują pięć zwykłych przypadków, 172 kontrole komponentów i 70 kontroli
na tryb/lokalizację (280 odmów normalnie/-O na luźnych/rozpakowanych plikach).
Kopie/fencing całego właściciela, trwałe S029, ograniczone kapsuły/checkpointy,
S020 i dokładny dispatch są zamknięte tylko dla tego lokalnego profilu.
[Tracker etapów](026-assessment-dependent-context.md#local-stages-0203-closeout-2026-10-30)
zapisuje zachowane niepowodzenia, bezstratną korektę kapsuły i ograniczenia
fizyczne/legacy/modelu. Nadrzędne P026-012c/P073 i wszystkie prace kontekstu/
pamięci/odbiorców pozostają partial.

### Kwalifikacja przeglądu P026-012c-02/03 (2026-11-01) {#p026-012c-0203-review-qualification-2026-11-01}

Node `1e264cab` / Orbidocs `bc62fab1` kwalifikują naprawiony profil lokalny: sześć zwykłych przypadków przeglądarki/ChannelJson, 234 kontrole komponentów w 11 grupach związanych bajtowo i 81 odrzucających kontroli na wariant normalnie/`-O`, luźny/rozpakowany (324). Zwykły restart z oczekującą zgodą osiąga timeout właściciela przed zamrożeniem i zwalnia oba oczekujące sloty. Poprzedni daemon odmawia bariery wersji właściciela pytań bez zmiany populacji właścicieli. Zachowany dowód to `node:docs/evidence/agent-runtime/2026-11-01-p026-012c-retention-review/README.md`.

Naprawiono odzyskiwanie osieroconych elementów, replay w tym samym procesie, bariery właścicieli i zamrażanie wyłącznie terminalnych elementów. Retencja zwiększa wyłącznie zaobserwowany kredyt czasu monotonicznego ograniczony przez UTC, bez starzenia offline; rozbieżność zegarów wymaga przeglądu i nie znika po restarcie. S020 publikuje raz na przebieg, z trwałymi wskaźnikami planu/koszyka przed skutkami. Obserwacje blokad 347/545 ms nie są twardą gwarancją opóźnienia 250 ms. Receipty SQLite nadal dopuszczają pozostałości bajtów. Pozostaje bezstratna kompresja metadanych; zastąpienie jej grafem wspólnych referencji jest osobną pracą projektową. Historyczne dowody pozostają bez zmian; proweniencja kontekstu i późniejsze etapy 012c, nadrzędne P073 i kwalifikacja wydania pozostają partial.
