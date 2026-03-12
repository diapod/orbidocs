# Wizja: suwerenność inteligencji i wiedzy

Ten dokument opisuje rój wolnych modeli sztucznej inteligencji: infrastrukturę,
która wspiera człowieka w przetrwaniu i rozwoju oraz chroni go przed
niebezpieczeństwami.

## Esencja

1. Budujemy globalną sieć **węzłów** uruchamianych przez wolontariuszy.

2. Na węzłach działają agenty AI i lokalne modele (LLM, dyfuzyjne i inne
   wyspecjalizowane), które współpracują jak **rój**: bez jednego centrum, jednego
   ośrodka władzy i bez jednego właściciela kapitału.

3. Rdzeniem roju jest odporny protokół komunikacyjny, który poza bazową funkcją
   zbiorowej inteligencji może włączać dodatkowe organy zdolności, m.in.:
   **memarium** (pamięć, która nie znika) i **sensorium** (konektory do świata).

4. Nie jest to "alternatywny *chatbot*" czy kolejny rozproszony agent, ale
  **publiczna infrastruktura sensu i sprawczości** – budowana w duchu wolnego
  oprogramowania i wzajemnej pomocy.

5. Nie walczymy z AI. **Oddzielamy poziomy**: przywracamy ludziom sterowność
   i projektujemy warstwy oraz kontrakty tak, aby powstało narzędzie, które **nie
   przejmuje podmiotu, lecz go wzmacnia**.

## Problem, na który odpowiadamy

### Nierównowaga władzy

"Tania inteligencja" ma dziś tendencję do koncentracji: wielkie modele, wielkie
budżety, duże zbiory danych, pojedyncze podmioty decyzyjne i agregujące wspólne
dane. Tam, gdzie pojawia się koncentracja, pojawia się też władza ukryta w narzędziu.

Nie chodzi tylko o cenzurę czy złe intencje, lecz o coś głębszego: **wagi modelu są
zamrożonym wyborem tego, co typowe, normalne, eleganckie i profesjonalne**. To jest
wbudowana norma. Wystarczy, że jest wygodna i "ładnie wygląda", a konformizm dopełnia
reszty.

### Kultura jako filtr dolnoprzepustowy

Gdy modele karmią modele, a treści syntetyczne wypierają ludzkie, kultura traci
detale: anomalie, odstępstwa, lokalne niuanse. To "kserokopia kserokopii". Z czasem
zostaje estetyka, a zanika **żywe paliwo innowacji**.

Odpowiedzią nie jest nostalgiczny powrót do starego porządku, lecz infrastruktura,
która **chroni różnorodność i źródła nowości**, zamiast je homogenizować.

### Sprawczość i przetrwanie

Jeżeli myślenie staje się usługą, drożeje to, co nie jest usługą:

- **autonomia** (umiejętność wyboru),
- **relacja** (wspólnota, zaufanie, zobowiązanie),
- **pamięć** (ciągłość sensu),
- **lokalność** (doświadczenie miejsca, języka, kontekstu),
- **bezpieczne pole** (gdy stawka społeczna nie niszczy szczerości).

Infrastruktura roju ma chronić ludzi w potrzebie i pomagać im w przetrwaniu oraz
rozwoju – bez uzależniania ich od czyjejś łaski.

## Założenia (wartości jako protokół)

To jest projekt techniczny, lecz wartości nie są tu PR-em. Są **kontraktem
zachowań**.

1. **Suwerenność** – użytkownik może odejść z danymi w 5 minut (formaty otwarte,
   eksport, migracja).

2. **Lokalność jako domyślny tryb (ang. local-first)** – preferujemy obliczenia i
   pamięć lokalnie; sieć jest dodatkiem, nie warunkiem.

3. **Minimalizm bodźców** – żadnych mechanizmów uzależniających, żadnego
   "dopaminowego UX".

4. **Prywatność jako godność** – model zagrożeń jest częścią architektury, nie
   dodatkiem.

5. **Wzajemna pomoc** – sieć wzmacnia najsłabszych, nie tylko najszybszych.

6. **Higiena epistemiczna** – oddzielamy poziomy: opis, redukcję, wyjaśnienie,
   doświadczenie, kulturę.

Operacyjnie traktujemy inteligencję przede wszystkim jako zdolność do formułowania
trafnych predykcji i aktualizacji ich po kontakcie z wynikiem.

## Słownik: rój, memarium, sensorium

### Rój

**Rój** to zbiór węzłów, które:

- potrafią działać autonomicznie,
- potrafią współpracować przez protokoły,
- nie mają pojedynczego punktu awarii ani pojedynczego punktu kontroli.

Rój nie jest państwem ani korporacją. Jest infrastrukturą zdolną do koordynacji bez
centrum.

### Memarium

**Memarium** to warstwa pamięci i wiedzy, której celem jest zachować to, co nie
powinno zniknąć:

- osobiste archiwa (notatki, modele świata, język prywatny, idiolekt),
- zasoby wspólnot (poradniki przetrwania, wiedza o prawie, medycynie pierwszego
  kontaktu, schronieniu),
- artefakty kultury (teksty, nagrania, mapy, instrukcje, biblioteki).

Memarium nie musi być globalne, żeby być wartościowe. Może być **federacyjne**,
z replikacją, wersjonowaniem i zasadami trwałości.

### Sensorium

**Sensorium** to warstwa adapterów do świata:

- czytniki treści w publicznych sieciach,
- czujniki temperatury, wilgotności, jakości powietrza,
- mikrofony (np. detekcja alarmów, analiza hałasu),
- kamery (np. rozpoznawanie zagrożeń, dokumentacja dowodowa, wsparcie osób z
  niepełnosprawnościami),
- inne źródła sygnałów (GPS, meteo, energia, bezpieczeństwo).

Sensorium ma jeden cel: **zakotwiczyć inteligencję w rzeczywistości**, aby nie stała
się czystą retoryką.

Jego użycie musi pozostawać podporządkowane zgodzie, minimalizacji danych, separacji
kontekstów i celowi ochronnemu; sensorium nie jest pretekstem do budowy infrastruktury
nadzoru.

## Architektura: warstwy i kontrakty (stratyfikacja w praktyce)

Ta sieć jest zbudowana jak dobrze stratyfikowany system: małe, autonomiczne elementy
stają się abstraktami, a te z kolei stają się konkretami dla kolejnych warstw.

### Warstwa 0: Węzeł (Node)

Węzeł to komputer wolontariusza (PC, serwer, NAS, RPi, laptop), który uruchamia:

- środowisko uruchomieniowe agentów,
- lokalne modele,
- lokalne memaria,
- konektory sensorium,
- polityki (zasady) bezpieczeństwa.

**Węzeł działa nawet bez Internetu.** Sieć jest opcją, a nie zależnością.

### Warstwa 1: Agent

Agent to proces z jasno określonym kontraktem:

- wejście/wyjście w formacie danych,
- uprawnienia minimalne,
- jawne zależności,
- ślady decyzji (`trace`) i możliwość audytu.

Agent może być:

- rozmówcą (LLM),
- twórcą obrazów (dyfuzja),
- solverem matematycznym,
- graczem,
- bibliotekarzem (nawigatorem po lokalnym memarium),
- strażnikiem reguł (*guardrails-as-code*).

### Warstwa 2: Przestrzenie pamięciowe

Memarium jest podzielone na przestrzenie:

- **osobiste** (private),
- **wspólnotowe** (community),
- **publiczne** (commons),
- **kryzysowe** (emergency caches).

Każda przestrzeń ma własne zasady: szyfrowanie, replikacja, retencja, anonimizacja,
prawo do zapomnienia.

### Warstwa 3: Kooperacja (Swarm Protocol)

Rój potrzebuje protokołu w następujących celach:

- identyfikacja węzłów (tożsamość kryptograficzna),
- odporność na Sybila/DoS oraz, dopiero po walidacji, mechanizmy reputacji
  proceduralnej,
- routing (w tym *edge relaying*),
- negocjacja zadań,
- rozliczanie kosztów (energia, transfer) bez finansowej przemocy.

W wersji idealnej protokół jest prosty, opisany, audytowalny, implementowalny w wielu
językach.

## Governance bez kapłanów: zasady zamiast autorytetu

Największym ryzykiem decentralizacji jest nowa forma oligarchii: strażnicy
repozytoriów, operatorzy infrastruktury i ekosystemy dostawców.

Dlatego ład organizacyjny (ang. governance) jest tu polityką zapisaną w kodzie
(ang. *policy-as-code*):

- polityki są jawne i wersjonowane,
- decyzje są protokołowane,
- istnieje prawo do odgałęzienia (ang. fork) wraz z danymi,
- istnieje prawo do własnego węzła "w ciszy" (bez uczestnictwa w publicznych
  przestrzeniach).

To rój odporny na kult: narzędzie, nie religia ani ideologia.

## Bezpieczeństwo i etyka jako część warstwy danych

### "Nie szkodzić" jako test architektury

Każdy komponent ma pytanie kontrolne:

- czy może zaszkodzić użytkownikowi?
- czy może zaszkodzić innym?
- czy może zostać użyty do przemocy, szantażu, manipulacji?

Guardrails nie są cenzurą. Są **modelem zagrożeń**.

### Prywatność

- szyfrowanie w spoczynku i w tranzycie,
- minimalizacja danych,
- separacja kontekstów (osobiste ≠ publiczne),
- domyślnie brak telemetrii.

### Kultura uczciwości

Rój przyjmuje kulturę uczciwości: uczestnictwo oznacza gotowość do poddania się
procedurze dowodowej i odpowiedzialności za trwające lub ciężkie nadużycia.

### Odpowiedzialność w czasie kryzysu

Rój ma tryby reagowania. Na poziomie wizji są to przykładowe klasy pracy, a nie
zamrożone nazwy protokołu:

- **normalny** (`commons`),
- **kryzysowy** (`disaster` / `war` / `blackout`),
- **pomocowy** (`shelter` / `food` / `legal` / `medical triage`).

W trybach kryzysowych rośnie rygor: więcej weryfikacji informacji, więcej redundancji,
więcej ostrożności.

## "Chronić ludzi w potrzebie" - konkretne scenariusze

### Kryzys energetyczny / blackout

Węzły działają lokalnie: mapy, instrukcje, lokalne modele do wstępnej kategoryzacji
(ang. triage), podręczna pamięć wiedzy. Sensorium pomaga:

- monitorować temperaturę w schronieniach,
- wykrywać zagrożenia,
- koordynować zasoby w mikroskali.

### Ucieczka przed przemocą

Memarium może zawierać roboczo nazwaną przestrzeń *escape kit*:

- jak spakować się bez wzbudzania podejrzeń,
- kontakty pomocowe,
- prawo lokalne (procedury),
- bezpieczne kanały komunikacji,
- wsparcie psychologiczne pierwszego kontaktu (bez udawania terapii).

### Edukacja i rozwój

Rój zapewnia:

- nauczyciela bez *feedu*,
- laboratorium do eksperymentów,
- repozytorium sprawdzonych praktyk rzemiosła,
- tłumaczenia i objaśnienia,
- narzędzia do budowania własnych narzędzi.

## Rola założycieli

Założyciele są tu architektami warstw i twórcami pierwszych kontraktów:

- dbają, żeby system był stratyfikowany (mała zmiana → mała zmiana),
- pilnują higieny epistemicznej,
- budują protokoły (m.in. tożsamość, routing, memarium, sensorium),
- trzymają etos: wolność, wzajemna pomoc, brak uzależnienia od dostawcy (ang.
  *vendor lock-in*),
- piszą teksty, które są nie tylko manifestem, ale praktycznymi postulatami oraz
  instrukcjami życia w epoce taniej inteligencji.

Ich rola jest szczególnie ważna w okresie założycielskim: odpowiadają wtedy za
spójność architektury, rytm implementacji i odporność projektu na przedwczesną
biurokratyzację, przejęcie sterowania i rozmycie misji. Później ich wpływ powinien
wynikać z jakości pracy, trafności decyzji i zaufania wspólnoty, a nie z kultu osoby.

## Kamienie milowe (droga od wizji do rzeczy)

1. **Minimalny węzeł**: środowisko uruchomieniowe agentów + 1 lub więcej
   modeli + opcjonalnie lokalne memarium.

2. **Protokół wymiany**: zadania, wyniki, tożsamości, a w późniejszych fazach także
   walidowana reputacja proceduralna.

3. **Sensorium starter kit**: temperatura + mikrofon alarmowy + kamera (opcjonalnie).

4. **Tryb kryzysowy**: podręczna pamięć wiedzy, procedury, walidacja informacji.

5. **Federacja wspólnot**: małe roje łączą się w większe – bez utraty autonomii.

## Zakończenie

To jest wizja świata, w którym inteligencja jest zbyt ważna, by oddać ją plemiennym
tworom: agencjom, korporacjom, pojedynczym państwom czy "kapłanom bezpieczeństwa".

Proponujemy porządek, w którym narzędzia są wolne, pamięć nie zależy od medium,
a człowiek pozostaje źródłem nowości – nie przez heroizm, lecz przez współpracę oraz
pielęgnowanie tego, co niepasujące. Wspólnie możemy być źródłem dobrej entropii.
