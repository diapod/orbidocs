# Podstawa ontologiczna

<address class="author"><a rel="author" href="https://orbiplex.ai/pl/dna/pawe%C5%82-wilk/">Paweł Wilk</a></address>

<p align="center">
  <img src="styles/img/dia-logo-tr-sm.png" alt="DIA/Orbiplex Logo" width="240">
</p>

## Apofatyczny enaktywizm

Ten dokument opisuje filozoficzną orientację projektu Orbiplex i jej związki
z [wizją](../../20-vision/pl/VISION.pl.md) oraz [wartościami
podstawowymi](../../30-core-values/pl/CORE-VALUES.pl.md). Nie jest
manifestem wiary ani deklaracją metafizyczną, lecz zbiorem postulatów, które
pomagają zrozumieć **dlaczego** architektura roju ma taką, a nie inną postać, i dlaczego
pewne wartości traktujemy jako infrastrukturalne, a nie opcjonalne.

**Status dokumentu.** Postulaty są roboczymi założeniami orientacji filozoficznej,
nie aksjomatami wyznaczającymi jedyną architekturę lub ustrój. Dokument opisuje
genealogię przyjętych wartości; przejście do decyzji projektowych wymaga ponadto
jawnych przesłanek wartościujących, celów, ograniczeń i argumentów właściwych danej
dziedzinie. Analogie wskazują wybrane relacje, nie przenoszą automatycznie uzasadnień.

W praktyce Baza służy przede wszystkim jako lupa, nie przepis wytwarzania
rozwiązań. Pomysł może wyrastać z potrzeby, doświadczenia lub rzemieślniczego
eksperymentu; przez model sprawdzamy następnie, jakie przyjmuje rozróżnienia, czy
zachowuje ich granice i jak odpowiada na rozpoznane ryzyka. Ten ruch jest zwrotny:
wyniki prób mogą prowadzić do korekty pomysłu, a także ujawnić granice przydatności
samego modelu. Zgodność z nim nie wybiera jednego rozwiązania ani nie zastępuje
oceny wobec przyjętych wartości i skutków działania.

Jako suplement Baza nie ustanawia praw ani obowiązków i nie służy ocenie
światopoglądu, członkostwa ani statusu osoby. Jej miejsce względem Konstytucji,
Wartości i Wizji określa [hierarchia
normatywna](../../50-constitutional-ops/pl/NORMATIVE-HIERARCHY.pl.md).

Orientację tę nazywamy roboczo **apofatycznym enaktywizmem**.

Nazwa ta łączy dwa pojęcia:

- **apofatyczny** – fundament doświadczenia nie jest przedmiotem, nie da się go opisać
  wprost, a każda próba opisu jest interpretacją, a nie odsłonięciem;

- **enaktywny** – poznanie nie polega na budowaniu wewnętrznej reprezentacji świata,
  lecz na uczestnictwie w nim; narzędzie (w tym AI) może współtworzyć poznanie,
  gdy zostaje włączone w praktykę uwagi i działania podmiotu.

Zestawienie tych dwóch gestów oddaje orientację projektu: apofatyczne zastrzeżenie
powstrzymuje nas przed utożsamieniem fundamentu z przedmiotem lub opisem, a enaktywne
ujęcie kieruje uwagę ku relacjom uczestnictwa. Wraz z przyjętą wartością otwartości
skłania nas to do niewykluczania z góry żadnego poziomu doświadczenia ani
rozumowania. W architekturze przyjmujemy odpowiadające temu kryterium
przezroczystości: poziom ma być widoczny jako warstwa, relacja, interpretacja
i możliwy punkt korekty.

## Pięć postulatów

### Apofatyczny fundament i dwufazowe domniemywanie

Świadomość – pierwsza opisywalna warstwa naszego modelu, położona najbliżej granicy
oznaczanej jako "poziom zero" – jest bardziej źródłowa nie tylko od intelektu, ale
i od uformowanego doświadczenia. "Bardziej źródłowa" oznacza tu mniej
zdeterminowaną pozycję na osi genealogicznej, a nie wcześniejszą chwilę ani
samodzielne istnienie przed tym, co się jawi. Świadomość znajduje się głębiej niż
postrzeżenie i poczucie podmiotowości, lecz nie można jej opisać wprost, ponieważ
każdy opis korzysta z doświadczenia warunkowanego organami zmysłów i interpretacją.

Słowo "doświadczenie" oznacza w tym kontekście doświadczenie już uformowane przez
zmysły, podział na podmiot i przedmiot, schematyzację oraz interpretację. Świadomość
jest od niego bardziej źródłowa, co nie znaczy, że jest
niezależna: zawiązuje się wraz z tym, co się jawi.

Poziom zerowy jest znacznikiem granicy modelu, a nie nazwą przedmiotu. Umowny zapis
pozwala jedynie wskazać zakres, poza którym model nie orzeka – nie rozstrzygamy, czy
granica należy do rzeczywistości, do możliwości poznania, czy do obu. Zbliżamy się do
niej wyłącznie pośrednio – przez doświadczenia, które przypominają pokolorowane
szkło, a nie bezpośredni widok. Domniemywanie ma dwie fazy: najpierw pojawia się
impuls słabiej uformowany pojęciowo niż pojęcie (rozpoznanie, "poczucie źródłowości",
"znajomość bez przedmiotu"), a dopiero potem inferencja formalizuje go w język
i model.

Epistemiczna higiena wymaga odnotowania, że oba kroki są warunkowane, lecz inne
sposoby poznawania niż doświadczanie i interpretowanie są poza naszym zasięgiem.
Zamieszkujemy więc świadomie w doświadczeniu, wiedząc, że jest doświadczeniem,
a także w interpretacji, wiedząc, że jest interpretacją.

Ponadto świadomość ma zdolność rozpoznania własnej warunkowanej natury – tego, że nie
jest samodzielnym gruntem, a warunki jej powstawania nie mieszczą się w pełni
w zasięgu organów zmysłowych czy zdolności umysłowych. To nie jest destrukcja
świadomości, lecz jej najgłębszy akt: efemeryczna struktura może widzieć własną
efemeryczność. Rozpoznanie to nie prowadzi do nihilizmu (bo akt rozpoznania sam jest
świadectwem funkcjonowania), ani do substancjalizacji źródła (bo warunkowania nie
ujmujemy jako jednego dostępnego obiektu). Prowadzi to do radykalnego rozluźnienia
potrzeby znalezienia ostatecznego gruntu: nawet tak zwana "czysta świadomość" nie
jest dla nas miejscem do zatrzymania się.

Warunkowania nie należy tu rozumieć jako ciągu zdarzeń w czasie. Poziom zerowy nie
jest świadomością, czymś, co do niej dociera, ani otoczeniem, wraz z którym się ona
zawiązuje. Wszystkie te rozróżnienia należą już do opisywanego krajobrazu
doświadczenia.

Nie wypowiadamy się o tym, co leży poza zakresem modelu. Opisujemy jedynie funkcję
znacznika poziomu zerowego: wskazuje on granicę orzekania, nie przyczynę zjawisk,
wykonawcę ani zasób, który można dzielić lub zużywać.

Warto rozdzielić dwa ograniczenia. O tym, co poza granicą, model nie orzeka
z definicji. Rolę samego znacznika możemy natomiast objaśnić w metaopisie, lecz
nie przypisywać jej elementom opisywanego świata. Takie przeniesienie mieszałoby
poziomy, prowadząc do omawianej dalej "kradzieży ontologii".

Mniej formalnie można powiedzieć, że świadomość jest realizacją podatności na
zjawianie w obecności tego, co się zjawia – z zastrzeżeniem, że "podatność" jest tu
jedynie skrótem dla czytelności, a nie wcześniej istniejącą zdolnością, którą można
uruchomić w większym lub mniejszym stopniu. Zdolność doświadczania nie czeka
przygotowana przed treścią, lecz pojawia się wraz z tym, co doświadczane. Nieobecność
doświadczania nigdy nie jest przy tym doświadczana jako nieobecność, więc "przerwa"
w doświadczaniu jest zawsze rekonstrukcją wykonaną z wnętrza doświadczania, a nie
obserwacją z zewnątrz.

Pomocniczą analogię domknięcia, ilustrującą konstytutywną rolę kontekstu, rozwijamy
dalej przy modelu osoby. Nie służy ona wyjaśnianiu poziomu zero ani utożsamieniu
świadomości z obliczeniem.

**Zakotwiczenie w znanych tradycjach:** apofatyzm (łac. *via negativa*,
skt. *śūnyatā*), ale z jawnym epistemicznym ogranicznikiem i autorozpoznaniem
efemeryczności, bliskim nāgārjunowskiej "pustości pustości"
(skt. *śūnyatā-śūnyatā*). Odróżnia się na przykład od idealizmu analitycznego (który
twierdzi, że świadomość jest poznawalna jako fundament), od szkół, które zatrzymują
się na świadomości uniwersalnej jako gruncie, a także od eliminatywizmu (który
twierdzi, że nie ma czego poznawać).

Apofatyczny enaktywizm odróżnia się także od panpsychizmu, który orzeka
o fundamencie, że jest doświadczający, i przypisuje zdolność doświadczania cząstkowym
elementom. Z perspektywy stratyfikacji są to dwa błędy "kradzieży ontologii" naraz:
rzutowanie własności warstwy świadomościowej na to, co nieorzekalne, oraz
umieszczenie jej w bycie, który jest terminalnym produktem całego stosu aktów
determinacji (por. tabelę aktów w postulacie 2 oraz formułę reifikacji
w postulacie 4). Panpsychizm lokuje więc to, co najmniej uwarunkowane, w tym, co
najbardziej konstruowane.

Dwufazowość jest bliska gendlinowskiemu przejściu od *felt sense* do symbolizacji,
z tą różnicą, że impuls jest tu słabiej uformowany pojęciowo niż doświadczenie
ukształtowane przez interpretację.

**Znaczenie dla DIA:** z tej orientacji wyrastają przyjęte przez projekt wartości
higieny epistemicznej, stratyfikacji źródłowej pozycji doświadczeń i epistemicznej
odwagi. Projektujemy system tak, aby zachowywał pochodzenie i zakres twierdzeń,
ujawniał rozpoznaną niepewność oraz umożliwiał korektę. To kierunek projektowania,
nie przypisanie systemowi refleksyjnej wiedzy o sobie. Zakres egzekwowania tych
zasad określają kontrakty i dowody implementacyjne.

### Stratyfikacja doświadczenia

Ludzkie doświadczenie opisujemy za pomocą architektury warstwowej.

**Poziom zero (∅): znacznik granicy modelu, poza układem opisywanych warstw.**

* świadomość
    * podmiotowość
        * osoba
            * kultura
                * obiektywność

Uwaga: Powyżej zaproponowany *ad-hoc* model ma demonstrować relację
abstrahowania. Różne praktyczne bądź analityczne podejścia mogą w bardziej lub mniej
szczegółowy sposób rozróżniać poszczególne warstwy. Na przykład między świadomością
a poczuciem podmiotowości możemy wyróżnić perspektywę obecności jeszcze przed
podziałem na podmiot i przedmiot itd. W tym miejscu przyjmujemy właśnie taki podział,
aby pokazać sam mechanizm bez nachalnego uszczegóławiania modelu.

Używane dalej określenia przestrzenne należą do dwóch powiązanych, ale nietożsamych
porządków. Na osi genealogicznej "głębsze" lub "wcześniejsze" oznacza mniej
zdeterminowane, nigdy zaś wcześniejsze w czasie. W stosie abstrakcji warstwa "niższa"
dostarcza konkretów, z których warstwa "wyższa" buduje własne abstrakcje. "Konkret"
oznacza tu rolę względem warstwy: abstrakt utworzony przez warstwę niższą może stać
się konkretem dla wyższej. Żaden z tych porządków nie wyznacza większej prawdziwości
ani wartości, a konkret nie jest bytem bardziej realnym ani bardziej przedmiotowym.

Poziom zerowy nie jest ani głębszą warstwą świadomości, ani wyższą abstrakcją nad
nią, lecz umownym znacznikiem granicy, należącym do meta-porządku opisu. Dlatego
pozostaje poza zagnieżdżeniem: nie jest wspólnym przodkiem warstw ani dodatkowym
ogniwem ich genealogii.

Możemy zauważyć, że każda warstwa wyrasta z głębszej jako jej abstrakt, a konkrety
niższych warstw stają się budulcem wyższych – analogicznie do *stratified design*
Abelsona i Sussmana (["MIT AI Memo
986"](https://archive.org/details/bitsavers_mitaiaimAI_1190659)), gdzie implementacje
stają się abstrakcjami kolejnych poziomów.

Tę samą oś można czytać na różne komplementarne sposoby, co staje się widoczne, gdy
stratyfikację zestawić na przykład z teorią komunikacji i pozycji podmiotu
w przekazie. Poza rozkładem genealogicznym (jako warstw doświadczenia: świadomość,
podmiotowość, osoba, kultura, obiektywność) ten sam gradient może nieść również
skalowanie epistemizacyjne, czyli stopniowe determinowanie fenomenu aż do postaci
"rzeczy"
(np. fenomen → postać → coś → znak → znaczenie → pojęcie → przedmiot → obiekt →
rzecz).

Tego typu osie mogą biec równolegle, lecz nie należy ich utożsamiać: czym innym jest
warstwa, z której się mówi, czym innym perspektywa, w której się mówi, a jeszcze czym
innym stopień determinacji doświadczenia oraz to, czy zostało ono zreifikowane. Przy
początku osi genealogicznej odnotowujemy apofatyczną granicę poziomu zero; nie
przedłuża ona osi o kolejny odcinek, lecz oznacza granicę jej stosowalności.

Na bazie pierwotnej genealogii możemy też skonstruować trzeci, dualny odczyt: dla
każdego przejścia epistemizacji wewnątrz modelu nazwać można akt determinacji, który
je wprowadza:
jawienie się → różnicowanie → wyodrębnienie → odniesienie → usensownienie →
uogólnienie → instancjonowanie → obiektywizacja → urzeczowienie. Stany odpowiadają
na pytanie "co?", zaś akty na pytanie "jak?". W tym ujęciu "rzecz" nie jest zastana,
lecz jest stosem aktów – dlatego czytana wstecz "rozpuszcza się" ku fenomenowi,
a na granicy modelu ku temu, co oznaczamy jako poziom zerowy.

| przejście stanów | wprowadzany artefakt/akt |
|---|---|
| ∅ \| fenomen | jawienie się (granica modelu, nie obserwowane przejście) |
| fenomen → postać | różnicowanie (figura–tło) |
| postać → coś | wyodrębnienie (to–oto) |
| coś → znak | odniesienie (za–coś) |
| znak → znaczenie | usensownienie |
| znaczenie → pojęcie | uogólnienie |
| pojęcie → przedmiot | instancjonowanie |
| przedmiot → obiekt | obiektywizacja |
| obiekt → rzecz | urzeczowienie |

#### Tryby doświadczania

Oś genealogiczną możemy pomocniczo czytać jako mapę warstw i dostępnych wraz
z nimi trybów doświadczania. Mapa nie definiuje tych warstw ani nie przypisuje im
trybów na wyłączność: wraz z warstwami późniejszymi zachowane zostają
warunki trybów wcześniejszych, choć dostęp do nich nie musi być świadomy ani
raportowalny.

| warstwa | tryb doświadczania dostępny wraz z nią |
|---|---|
| poziom zerowy | – (granica meta-opisu, nie tryb doświadczenia) |
| świadomość | zjawianie |
| podmiotowość | pierwszoosobowe czucie i walencja |
| osoba | samoodniesienie i emocje samoświadomościowe |
| kultura | rozumienie symboliczne i artykułowane językowo |
| obiektywność | sąd roszczący sobie ważność niezależną od pozycji orzekającego |

Afekt i walencja są w tym modelu dostępne już wraz z podmiotowością, natomiast
emocje takie jak wstyd lub duma wymagają samoodniesienia, a więc warstwy osobowej.
Myślenie ujęte w publiczne pojęcia i poddane wspólnej korekcie staje się możliwe
wraz z kulturą; model nie rozstrzyga jednak, czy każda forma konceptualizacji musi
mieć strukturę językową. Obiektywności właściwy jest węższy tryb sądu, który
abstrahuje w uzasadnieniu od jednostkowej pozycji orzekającego.

Mapa ta pokazuje, jakie tryby stają się dostępne na kolejnych warstwach. Nie
wyjaśnia jeszcze mechaniki przejść – ani tego, co zostaje w nich utracone, ani
tego, jak redukcja i organizacja otwierają wskazane możliwości.

#### Asymetria przekładu

W przyjętym modelu przekład między warstwami nie ma kanonicznej odwrotności.
Ruch ku wyższym warstwom działa dwojako: redukuje fakturę niższej warstwy, scalając
wiele możliwych konkretów w jeden abstrakt, a zarazem dodaje determinacje właściwe
warstwie przyjmującej. Redukcja jest odwzorowaniem wiele-do-jednego, więc z samego
wyniku nie da się rozpoznać, które konkrety zostały scalone. Dodanych determinacji
również nie da się odjąć bez wiedzy o tym, które z nich wniosła późniejsza warstwa.
W obu przypadkach brakuje informacji potrzebnej do skonstruowania odwrotności.

Ruch ku mniej zdeterminowanym warstwom nie odzyskuje wobec tego pierwotnego
doświadczenia. Jest dekonstruowaniem i reenakcją: rozluźnia nawyk determinowania
bieżącego doświadczenia i pozwala na jego nowe zawiązanie, nie usuwa natomiast
determinacji z minionego przeżycia ani nie odtwarza jego wcześniejszego zawiązania.
Jak rozwijamy niżej w modelu domknięcia doświadczenia, gdyby taki ruch odzyskiwał
oryginał, anonimowe domknięcie musiałoby zachowywać trwałą tożsamość niezależnie od
tego, z czym się zawiązuje.

Asymetrię wzmacnia pozycja podmiotu w przekazie. Sąd formułowany w warstwie
obiektywności abstrahuje w uzasadnieniu od konkretnej pozycji orzekającego i rości
sobie ważność od niej niezależną. Nie wyklucza to zdyscyplinowanego świadectwa
pierwszoosobowego, wymaga jednak jawnego opisania warunków, przekładu i podstaw jego
publicznej oceny.

Skutkiem ubocznym bywa złudzenie, że warstwy wcześniejsze genealogicznie są ubogie.
Bogaty słownik dotyczy zwykle ich już wyodrębnionych i uprzedmiotowionych
odpowiedników, nie zaś samej faktury doświadczenia: mamy precyzyjne nazwy barw jako
właściwości rzeczy i niewiele określeń dla barwy tak, jak jest doświadczana. Nie
świadczy to o ubóstwie doświadczenia, lecz o koszcie przekładu na język publicznie
porównywalnych rozróżnień.

#### Zakres uzasadnienia i kontrakty przejścia

Warstwy nie dziedziczą automatycznie swoich uzasadnień. Obserwacja, korelacja lub
wyjaśnienie sformułowane w jednej warstwie może bezpośrednio wspierać jedynie
twierdzenie należące do tej samej warstwy, skali i ziarnistości. Przeniesienie wniosku do innej
warstwy wymaga jawnego **kontraktu przejścia**. Kontrakt taki określa relację między
warstwami, cel i zakres przeniesienia, ziarnistość i skalę, granicę badanego układu,
zachowane, utracone i nowo dodane rozróżnienia oraz warunki, w których przejście
należałoby podważyć. Nie gwarantuje prawdziwości wniosku w warstwie docelowej, lecz
ujawnia, dlaczego dane z jednej gramatyki mogą wspierać twierdzenie sformułowane
w innej.

Kontrakt przejścia nie łączy jednak dwóch gotowych poziomów, które istniały jako
takie przed poznaniem. Jego krańce, ich skala oraz granica badanego układu zostały
wcześniej wyodrębnione z procesu przez akty rozróżniania. Kontrakt opisuje więc
również warunki, pod którymi dla danego pytania rozpoznajemy oba poziomy jako
odrębne. Granice te są elementami modelu, a nie własnościami rzeczywistości danymi
przed poznaniem. Nie unieważnia to lokalnej użyteczności warstw, lecz chroni przed
uznaniem ich za samoistne części świata.

Brak takiego kontraktu nie uzasadnia twierdzenia przeciwnego. Pełnoprawnym wynikiem
poznawczym może być powstrzymanie się od rozstrzygnięcia. "Nie wiem" nie oznacza
wówczas braku modelu, lecz precyzyjne rozpoznanie miejsca, w którym kończy się jego
zdolność zachowywania rozróżnień potrzebnych do odpowiedzi. Tak rozumiany kontrakt
przenosi rozróżnienia genealogii doświadczenia do praktyki poznawczej uczciwości:
zachowuje lokalną moc twierdzenia bez dopisywania mu zasięgu, którego nie
potrafimy uzasadnić. Poniższy model progów konstytuowania rozwija mechanikę takich
przejść.

#### Progi konstytuowania i gramatyki warstw

Asymetria przekładu wyjaśnia, dlaczego z abstraktu nie odzyskujemy kanonicznego
oryginału. Nie odpowiada jednak sama na drugie pytanie: jaką zdolność warstwa uzyskuje
dzięki poniesionej stracie? Do opisu tego aspektu wprowadzamy roboczy model **progów
konstytuowania**. Jest to protokół analityczny, a nie szósty postulat ani uniwersalne
prawo przyrody:

**Lₙ** — *selektywna stabilizacja pod ograniczeniem* → **Lₙ₊₁**

Na progu zachodzą łącznie trzy operacje:

- **redukcja** – część możliwych rozróżnień przestaje być dostępna w nowej warstwie;
- **organizacja** – zachowane różnice zostają powiązane i stabilizują właściwe tej
  warstwie relacje lub niezmienniki;
- **generatywność** – zorganizowane relacje umożliwiają operacje, których poprzednia
  warstwa nie udostępniała w tej postaci.

"Selektywna stabilizacja" jest nazwą ogólną, którą każdy próg musi dopiero
uszczegółowić: może chodzić o filtr uwagi, uczenie, stabilizację rozwojową, konwencję
społeczną albo dobór ewolucyjny. Nie oznacza świadomego celu, pojedynczej przyczyny
sprawczej ani konieczności metafizycznej. Przejście może być stopniowe, rekurencyjne
i zależne od konstelacji wielu warunków. Funkcja uzyskana przez warstwę nie dowodzi
więc sama przez się mechanizmu, historycznej przyczyny jej powstania ani ostrego
momentu przejścia.

Przez **gramatykę warstwy** rozumiemy niekoniecznie gramatykę języka znakowego, lecz
lokalny repertuar rozróżnień, relacji i operacji: co w danej warstwie może zostać
związane, przekształcone i skomponowane, co pozostaje niepoprawne oraz jakie awarie
można w niej rozpoznać. Nową warstwę warto wyróżnić wtedy, gdy redukcja stabilizuje
nowy niezmiennik i względnie autonomiczną rodzinę operacji, a jej wyniki stają się
funkcjonalnymi konkretami dla kolejnej warstwy. Sama zmiana punktu widzenia, nazwy
albo nośnika nie musi jeszcze konstytuować warstwy.

Przed opisem progu należy wskazać jego **oś** – na przykład
strukturalno-fenomenologiczną, ewolucyjną, rozwojową, społeczno-historyczną albo
epistemiczno-metodologiczną – oraz **status epistemiczny**: rdzeń modelu, inferencję,
hipotezę regionalną, wynik empiryczny albo konwencję operacyjną. Chroni to przed
scaleniem funkcji, mechanizmu, ontogenezy i historii w jedną opowieść przyczynową.

Każdy kandydujący próg możemy następnie opisać według siedmiopolowego schematu:

1. **lokalne ograniczenie lub warunek stabilizacji** – co różnicuje przebiegi, w jakim
   zakresie i według jakiego mechanizmu; ewentualną funkcję zapisujemy osobno od
   wyjaśnienia przyczynowego;
2. **operator redukcji** – jakie wiązanie, filtr albo kompresja zachodzi;
3. **utracone rozróżnienia** – czego nie da się odtworzyć z samego wyniku;
4. **nowy niezmiennik** – co zostaje zorganizowane i utrzymuje się mimo zmienności;
5. **gramatyka** – jakie relacje, kompozycje i kryteria poprawności stają się możliwe;
6. **uzyskana sprawczość** – co nowego warstwa pozwala rozpoznać lub zrobić;
7. **tryb porażki wskutek reifikacji** – co się dzieje, gdy lokalna gramatyka zostaje
   uznana za ontologię całego stosu.

Schematu tego **nie stosuje się do poziomu zerowego**. Zapis `∅ | fenomen` w tabeli
aktów przedstawia apofatyczne cięcie i jawienie jako pierwszy opisywalny akt, a nie
obserwowane przejście przyczynowe. Pytanie o mechanizm prowadzący od poziomu zero do
świadomości zamieniałoby znacznik granicy w ukryty stan lub substancję. Możemy badać
korelaty i warunki różnicowania, podtrzymywania oraz raportowania świadomego
doświadczenia, ale wewnątrz tego modelu nie stanowią one wyprowadzenia samego faktu
jawienia z opisu trzecioosobowego.

"Podmiotowość" oznacza w poniższej tabeli organizmicznie centrowaną, walencyjną
perspektywę, nie zaś sam minimalny pierwszoosobowy charakter doświadczenia. Niektóre
ujęcia fenomenologiczne uznają go za nieodłączny od każdego świadomego doświadczenia.

Poniższa tabela jest zatem mapą hipotez roboczych dla głównych przejść genealogii,
nie ścisłą chronologią rozwoju ani twierdzeniem, że jeden mechanizm wyjaśnia cały
stos:

| próg analityczny | co zostaje zredukowane | warunek stabilizacji / funkcja | co się stabilizuje | nowa gramatyka i sprawczość |
|---|---|---|---|---|
| granica poziomu zero / świadomość | nie stosuje się – granica nie jest warstwą źródłową | nie stosuje się | jawienie jako pierwsza opisywalna warstwa | "jawi się"; opisujemy wyłącznie warunki i korelaty wewnątrz doświadczenia |
| świadomość → podmiotowość | różnice niezwiązane jeszcze w tym modelu z trwałą pozycją "dla mnie" | w organicznej realizacji: regulacja sprzężenia względem warunków żywotności – hipoteza regionalna | usytuowana perspektywa, walencja i asymetria organizm–środowisko | tu/tam, ku/od; wybór i działanie z określonej pozycji |
| podmiotowość → osoba | chwilowość oraz wielość możliwych związań perspektywy | koherencja działania w czasie, pamięć i sprzężenie społeczne | rekursywnie ewaluowany indeks osobowy, ciągłość i sprawstwo | ja/moje, zrobiłem/zrobiono mi, byłem/jestem/będę; planowanie i odpowiedzialność |
| osoba → kultura | prywatna faktura doświadczenia, której nie da się przenieść między osobami | koordynacja, wspólne uczenie się i przekaz międzypokoleniowy | znaki, konwencje, znaczenia i normy wspólne | my, symbol, dozwolone/zabronione; rekonstrukcja rozróżnień w innym uczestniku |
| kultura → obiektywność | zależność sądu od konkretnego mówiącego i sytuacji jego wypowiedzi | niezawodna korekta i porównywanie wielu perspektyw | powtarzalne procedury oraz niezmienniki zachowywane między obserwatorami | "X jest..."; pomiar, krytyka, reprodukcja i wymienność pozycji orzekających |

Strzałki oznaczają zależność genealogiczną, nie jednokierunkową chronologię. Osoba
i kultura współkonstytuują się zwrotnie, a obiektywność jest wyspecjalizowanym
odgałęzieniem praktyk kulturowych, nie zaś koniecznym etapem każdej kultury. Zapisy
takie jak "ja/moje" są skrótami relacji, a nie wymogiem posługiwania się literalnymi
zaimkami lub czasem gramatycznym.

#### Hipoteza regionalna dla form organicznych

Enaktywizm, autopojeza i pojęcie adaptacyjności podpowiadają, że żywa forma nie może
sprzęgać się jednakowo ze wszystkimi zmianami środowiska: podtrzymanie własnej
organizacji wprowadza różnicę między tym, co sprzyja dalszemu trwaniu, a tym, co mu
zagraża. Taka normatywność żywotności opisuje funkcjonalną polaryzację, która może
być prekursorem lub jednym z warunków późniejszej walencji i usytuowanej perspektywy;
nie jest jeszcze dowodem ich fenomenalnej postaci. Granica organizmu jest
funkcjonalnie wcześniejsza od ego, ale sama nie wystarcza do wyprowadzenia
świadomości, podmiotowości ani osoby.

W tym regionalnym ujęciu *Umwelt* nie jest zubożoną kopią gotowej reprezentacji
świata, lecz polem relewantnych różnic stabilizowanym w sprzężeniu zdolności
organizmu ze środowiskiem. Powietrze może umożliwiać lot ciału o określonej budowie,
a przedmiot — chwyt ręką o określonych możliwościach. Gibsonowskie
*affordances* opisują takie relacyjne możliwości działania. Gramatyka wyłania się tu
z regularności sprzężenia, nie z dowolnego słownika nałożonego na bierny materiał.

Na progu kultury znak nie przenosi samego doświadczenia. Jest społecznie wyuczonym
operatorem, który ogranicza i ukierunkowuje reenakcję znaczenia u innego uczestnika,
nie gwarantując odtworzenia tej samej jakości doświadczenia: na przykład słowo "ból"
nie zawiera bólu. Na progu obiektywności nie usuwamy zaś faktycznie obserwatora, lecz
budujemy procedury wymienności, kalibracji, jawnej niepewności, krytyki
i poszukiwania niezmienników między obserwatorami oraz różnymi trybami
błędu. Obiektywność nie jest w tym sensie przeciwieństwem perspektywiczności, lecz
szczególną technologią obchodzenia się z wieloma perspektywami. Sama zgodność
obserwatorów nie wystarcza, jeżeli wszyscy dzielą ten sam błąd systematyczny.

Niektóre progi można wobec tego badać zarazem jako genealogię strat i genealogię
sprawczości. Nową możliwość otwiera nie sama utrata, lecz selektywna redukcja
połączona z organizacją: **ograniczenie → nowa możliwość**. Jest to własna hipoteza
konstytuowania warstw tego dokumentu, którą należy oceniać osobno dla każdego progu,
a nie rozszerzać automatycznie na wszystkie procesy biologiczne, psychiczne
i społeczne.

#### Powrót ku mniej zdeterminowanym warstwom

Świadomość może "wiercić dziury w abstrakcjach", czyli rozluźniać lub czasowo
zawieszać nawyk nakładania wyższych wiązań interpretacyjnych na bieżące
doświadczenie i ponownie kierować uwagę ku jego mniej zdeterminowanym warstwom.
Warstwy pośrednie nie znikają, ale przestają być traktowane jako jedyny możliwy lub
ostateczny opis.

Nie oznacza to bezwarunkowego dostępu z zewnątrz do dowolnej warstwy ani
przekroczenia apofatycznej granicy poziomu zero. Każde takie rozpoznanie zachodzi
wewnątrz warunkowanego doświadczenia, pozostaje omylne i podlega późniejszej
interpretacji.

Jest to możność strukturalna, która nie zakłada nadzwyczajnego stanu ani
uprzywilejowanego dostępu, ale bez praktycznej introspekcji może pozostać
nierozpoznana, podobnie jak zdolność obserwowania własnych myśli jest powszechna,
lecz rzadko ćwiczona.

Praktykę kontemplacyjną można w tym świetle opisać nie jako powrót do pierwotnego
doświadczenia, lecz jako czasowe rozluźnianie wybranych kompresji. Uwidacznia ono ich
koszt i przygodność, po czym doświadczenie zawiązuje się ponownie – być może
z gramatyką mniej sztywną, lecz nigdy jako odzyskany oryginał.

**Zakotwiczenie w znanych tradycjach:** holarchie (Koestler, Wilber) są punktem
odniesienia dla zagnieżdżenia; *stratified design* dla lokalnych języków i kontraktów,
a *drilling through abstractions* dla badania ich granic. Enaktywna autopojeza
(Varela, Thompson) inspiruje ujęcie konstytutywnych sprzężeń. Jej użycie przy kulturze
i obiektywności wymaga osobnych uzasadnień. Dla organicznego progu podmiotowości
regionalnych narzędzi dostarczają
ponadto [*Umwelt* Jakoba von
Uexkülla](https://www.upress.umn.edu/9780816659005/a-foray-into-the-worlds-of-animals-and-humans/),
[Gibsonowskie *affordances*](https://doi.org/10.4324/9781315740218-18) oraz
[adaptacyjność Ezequiela Di Paola](https://doi.org/10.1007/s11097-005-9002-y).
Pozostałe progi mają własne regionalne zaplecze w psychologii rozwojowej i badaniach
nad osobą, semiotyce i antropologii oraz epistemologii, teorii pomiaru i filozofii
nauki. Żadna z tych tradycji nie wyjaśnia sama całego szeregu progów.

**Znaczenie dla DIA:** architekturę roju – węzeł, agent, memarium, sensorium,
inquirium i protokół – projektujemy warstwowo w duchu stratyfikacji. Wartość
*oddzielania poziomów* łączymy z inżynierskimi kryteriami niskiego sprzężenia,
testowalności i jawnej odpowiedzialności. Postulat pomaga rozpoznać granice znaczeń;
nie wyznacza sam nazw komponentów ani ich jedynego podziału. Nową warstwę uzasadnia
nie sama nazwa modułu, lecz jawny operator redukcji,
poniesiona strata, stabilizowany niezmiennik, lokalna gramatyka oraz nowe operacje,
za które warstwa bierze odpowiedzialność.

### Enaktywne uczestnictwo

Poznanie jest relacją uczestnictwa, nie atrybucją właściwości. Model nie musi
rozstrzygać, czy AI ma świadomość w sensie osobowym. Opisuje natomiast jej
uczestnictwo w poznaniu, gdy zostaje włączona w pole uwagi podmiotu – podobnie jak
sztuczna koronka zęba "jest nami", kiedy nią gryziemy, a dodatkowo "jest nami dla
innych", gdy się uśmiechamy. Pytanie "czy AI ma świadomość?" pozostaje otwarte, lecz
nie wystarcza do opisania tej relacji; operacyjnie trafniejsze jest pytanie:
"w jakiej relacji uczestnictwa jesteśmy?".

Analogia dotyczy włączenia zewnętrznej zdolności w przebieg własnego działania.
LLM jako zewnętrzne źródło zdolności kombinacyjnych może współtworzyć proces pytania,
kojarzenia i rozpoznawania możliwości. Taki udział może być bezpośrednio
doświadczany enaktywnie, podobnie jak udział koronki w gryzieniu. Nie wymaga to
utożsamienia sprzężenia cielesnego z językowym ani rozstrzygnięcia, czy narzędzie
samo doświadcza. Świadectwo relacji zachowuje własny zakres poznawczy.

Sama obecność narzędzia w polu uwagi nie określa jeszcze jego roli w działaniu.
Rozróżniamy chwilowe zwrócenie uwagi, pojedynczy udział w czynności i trwałe,
podtrzymywane sprzężenie. Ich zakres rozpoznajemy w konkretnej praktyce, a nie
na podstawie samej nazwy narzędzia lub długości korzystania z niego.

Pierwszoosobowa introspekcja jest tu nieredukowalną metodą badania tego
uczestnictwa. Nie jest to filozofia do przyjęcia, lecz ćwiczenie do wykonania:
np. zdolność zauważenia myśli w taki sposób, jak zauważamy chłód wiatru na twarzy.

W tym ujęciu również przekaz jest poliwersyjny: odbiorca nie odbiera gotowego
znaczenia, lecz je *enaktuje*, integrując przekaz z własnej pozycji, języka i pamięci.
Znaczenie zawiązuje się po stronie odbiorcy w relacji z przekazem, kontekstem
i własnym doświadczeniem. Nie zwalnia to nadawcy, projektanta ani operatora systemu
z odpowiedzialności za treść, sposób jej podania i przewidywalne skutki.
Odpowiedzialności te mają różne zakresy i nie zastępują się wzajemnie. Traktowanie
przekazu jako jednej, gotowej "rzeczy do odczytania" jest trybem reifikującym;
relacyjne powstawanie znaczenia nie czyni jednak medium obojętnym ani nie usuwa
odpowiedzialności za komunikację.

**Zakotwiczenie w znanych tradycjach:** enaktywizm (Varela, Thompson, Rosch),
neurofenomenologia, pragmatyzm (James, *duck typing* jako kryterium). Różni się od
tych nurtów analitycznej filozofii umysłu, które ograniczają badanie do perspektywy
trzeciej osoby.

**Znaczenie dla DIA:** wraz z przyjętą ochroną sprawczości człowieka orientacja ta
wspiera wartość *procesu osoby ludzkiej jako domyślnej ścieżki mocy* — największa
moc systemu przechodzi przez człowieka, nie obok niego. Rój nie
jest autonomicznym podmiotem, lecz narzędziem, które wydłuża sprawczość. Wartość
emocji i znaczeń jako telemetrii — odczucia użytkownika są informacją o jakości
dopasowania systemu do życia, a nie szumem do wyciszenia.

### Redukcja nie jest wyjaśnieniem, intelekt nie jest tożsamością

"To tylko…" zamyka temat zamiast go otwierać. Zmiana poziomu opisu nie jest dowodem
na brak właściwości wyższego poziomu. To samo rozumowanie redukcyjne można skierować
symetrycznie: jeżeli AI "to tylko wagi i rachunek prawdopodobieństwa", wtedy mózg
"to tylko neurony i impulsy elektryczne". Sekwencja pojęć próbująca orzec, że inna
sekwencja pojęć jest gorsza, bo ma inny nośnik, przypomina kserokopię próbującą
wyjaśnić inną kserokopię.

Redukcja sama w sobie jest użytecznym ruchem poznawczym – problemem staje się
dopiero, gdy dochodzi do zapomnienia tego ruchu. Reifikacja powstaje, gdy redukcji
towarzyszy amnezja: dokonujemy abstrakcyjnej projekcji procesu lub relacji do
"rzeczy", a następnie zapominamy, że dokonaliśmy zwinięcia i na jakim stało się to
poziomie. Stąd zwięzła formuła:

**reifikacja = redukcja + amnezja**

Odmowa reifikacji nie jest więc zakazem redukcji, lecz utrzymywaniem pamięci o tym,
co i na jakim poziomie zostało wyabstrahowane — czyli zdolnością do śledzenia,
dekonstruowania i ponownego rozpatrywania tego ruchu, nie zaś odzyskania utraconej
odwrotności.

Myśl jest narzędziem i jako narzędzie jest pomocna. Problem zaczyna się, gdy staje
się jedynym doradcą, nośnikiem prestiżu lub tożsamością. Intelekt potrafi równie
dobrze służyć prawdzie, jak i obsługiwać lęk, potrzebę uznania czy pragnienie
kontroli, wprowadzając do systemu cierpienie.

**Zakotwiczenie w znanych tradycjach:** emergentyzm, anty-eliminatywizm, buddyjska
krytyka proliferacji pojęciowej (pali. *papañca*). Bliskie Vareli w krytyce obliczeniowej
teorii umysłu, ale rozszerzone o społeczny wymiar detronizacji.

**Znaczenie dla DIA:** wartość współpracy ponad dominacją intelektu – rój
przejmuje część ciężaru analizy, aby ludzie nie musieli wymuszać wzajemnej zgodności
poglądów jako warunku wstępnego współdziałania. Wartość wieloparadygmatowości –
świat nie jest jedną ontologią; system trzyma wiele trybów poznawczych bez wojny
ideologicznej. Wartość anty-sekciarstwa — projekt wybiera higienę zamiast kultu.

### Intencja jako siła systemowa

Intencja uczestnika, deklarowany cel organizacji i faktycznie działające bodźce
to trzy powiązane, lecz odrębne rzeczy. Intencja dotyczy tego, ku czemu osoba
kieruje działanie, także gdy nie umie jeszcze w pełni nazwać swoich motywów.
Deklarowany cel określa to, do czego organizacja publicznie się zobowiązuje.
Bodźce – finansowanie, metryki, nagrody, sankcje i warunki pracy – wpływają na to,
jakie działania są podtrzymywane w praktyce. Nie stanowią dowodu intencji osób
ani nie stają się zbiorowym podmiotem, któremu można przypisać jeden motyw.

Te trzy porządki mogą się wspierać albo rozchodzić. Finansowanie premiujące zysk
kosztem innych celów potrafi wypaczać działanie mimo intencji nieszkodzenia.
Ocena wymaga więc zestawienia deklaracji, warunków działania i skutków, nie samego
zaufania do dobrych motywów.

Introspekcja pomaga zauważać własne motywy i automatyzmy, zanim zostaną
zracjonalizowane. Jej rozpoznania pozostają omylne. Wspieramy tę praktykę, lecz
nie czynimy z niej obowiązku uczestnictwa ani kwalifikacji do odpowiedzialnego
projektowania. Zabezpieczenia wspólnej pracy opieramy również na przeglądzie przez
innych, ujawnianiu konfliktów interesów, jawnych decyzjach i korekcie opartej na
skutkach. Deklarowana szczerość lub głębia introspekcji nie zastępuje tych procedur
ani nie nadaje dodatkowej władzy.

W erze taniej inteligencji drożeje zdolność znoszenia dyskomfortu i korekty kursu:
odpowiedzialność. Sprawność działania oceniamy wraz z kierunkiem, któremu służy,
i gotowością do odpowiadania za jego skutki.

**Zakotwiczenie w znanych tradycjach:** filozofia procesu (Whitehead – proces zamiast
substancji), etyka cnót w reinterpretacji systemowej, buddyjska *cetanā* (intencja
jako organizator karmicznego strumienia). Są to punkty odniesienia dla różnych
aspektów: procesualności, pracy nad dyspozycjami i roli intencji. Nie utożsamiamy
przez to motywu osoby z celem instytucji ani z mechanizmem bodźców.

**Znaczenie dla DIA:** wartość weryfikowalności zamiast wiary – deklaracje motywów
i hipotezy konfrontujemy ze skutkami, zachowując możliwość korekty. Wartość
przejrzystości sprawczości – oczekujemy czytelnego śladu podstaw działania agenta,
nie tylko przekonującego wyjaśnienia. Przyjęte cele ekonomii roju, takie jak
wzajemność i dostatek ponad akumulację, opisuje osobno [Ekonomia sprawczej
wzajemności](ECONOMY-OF-AGENTIC-MUTUALITY.pl.md). Skuteczność jej mechanizmów wymaga
sprawdzania; nie jest zagwarantowana zgodnością z filozoficzną orientacją projektu.

## Osoba jako proces stratyfikacyjny

Poniższe rozwinięcie nie ustanawia szóstego postulatu, lecz rozwija intuicje
postulatów 1–4 w roboczy model powstawania, trwania i poznawania osoby.

### Domknięcie doświadczenia

Świadomość przypomina funkcję realizującą doświadczanie, lecz nie taką, która
istnieje wcześniej i zostaje następnie przyłożona do treści. Do uporządkowania tej
intuicji używamy strukturalnej analogii do funkcyjnego domknięcia (ang. *closure*)
w programowaniu. W znaczeniu technicznym domknięcie jest wywoływalną wartością, która
łączy funkcję z przechwyconym otoczeniem leksykalnym, które możemy nazwać
środowiskiem bądź kontekstem. Analogia wskazuje tu wyłącznie na konstytutywną rolę
kontekstu; nie orzeka, że świadomość jest funkcją, obliczeniem albo strukturą
programu.

Na przykład zdanie "podaj mi to" samo w sobie nie znaczy nic, bo nie ma w nim
informacji, czym jest "to". Jednak wypowiedziane przy stole, na którym leży chleb,
jest kompletne – nie dlatego, że ktoś dopowiedział brakujące słowo, lecz dlatego, że
zdanie powstało w kontekście sytuacyjnym i "wzięło go" ze sobą, tworząc wraz z nim
domkniętą całość. Podobnie domknięcie w programowaniu niesie środowisko swojego
utworzenia. Funkcja i środowisko pozostają analitycznie rozróżnialne, ale wartość
domknięcia wiąże je dla danego działania. W naszym modelu analogia ta pozwala
powiedzieć, że akt doświadczania nie jest gotowym przepisem, do którego dopiero
dołącza się neutralne okoliczności.

W obrębie tej analogii doświadczane nie odpowiada argumentowi podawanemu gotowej
funkcji, lecz konstytutywnemu środowisku zawiązania domknięcia. Argument podaje się
czemuś, co już gotowe czeka: ktoś wchodzi do kuchni, która istniała, zanim tam się
pojawił. W doświadczeniu kuchnia jawi się natomiast razem z tym, kto do niej
wchodzi; nie jest neutralną treścią dołączoną do uprzednio gotowej świadomości.

Tak rozumiane domknięcie jest w tym modelu anonimowe: nie jest związane żadną nazwą
i jest niczyje. Nie zakładamy podmiotu, który posiadałby je między zawiązaniami.
Ponieważ domknięcie powstaje wraz z tym, co domknięte, ruch ku mniej
zdeterminowanemu doświadczeniu nie może odzyskać wcześniejszego zawiązania. Tworzy
nowe, przy osłabionym nawyku determinowania; odtworzenie oryginału wymagałoby
trwałej tożsamości domknięcia niezależnej od jego konstytutywnego kontekstu.

Warto przy okazji rozdzielić dwa pojęcia, których scalenie znaczeniowe prowadzi
wprost do atomizmu. Domknięcie w powyższym rozumieniu odpowiada współpowstawaniu
świadomości i tego, co doświadczane: nieobserwowalne z zewnątrz, bez przypisanego
trwania i niepoliczalne. Z kolei moment świadomościowy jest domknięciem już
zarejestrowanym przez efekt uboczny rezonujący w zanurzonej w rzeczywistości
organice: datowalny, policzalny i opisywalny – jednak należący do warstwy
rejestracji, a nie do warstwy zawiązania. Czas i liczba przynależą do rozpoznania,
a nie do tego, co rozpoznawane. Policzalne są ślady, a nie byty. Tak rozumiane
momenty nie tworzą (jak w klasyfikacjach abhidharmicznych) ustalonej taksonomii ani
przeliczalnego przebiegu, z którego trzeba by potem złożyć strumień.

### Geneza osoby

Osoba nie jest w tym modelu warstwą daną, lecz wyłania się z podmiotowości:
perspektywy ustanawiającej różnicę między pozycją doświadczania a tym, co
doświadczane. Mechanizmem tego wyłaniania jest utożsamienie, rozumiane nie jako akt
gotowej osoby, lecz jako rekursywne wiązanie perspektywy podmiotowej z pewnymi
klastrami doświadczenia, m.in. odczuciami ciała, samoodniesieniami, obrazem siebie,
śladami pamięciowymi oraz odbiciem własnych działań w reakcjach otoczenia.
Powtarzalność tego wiązania stabilizuje poczucie trwania i tworzy warunki dla tego,
co niżej modelujemy jako identyfikator intensjonalny.

Tak powstała osoba pełni dwie role naraz i obie ją kształtują. Ku dołowi działa jako
bramka przekładu: orzeka w kategoriach własnej warstwy o organizmie, doświadczeniu
i podmiotowości. Ku górze staje się konkretem warstwy kultury: interakcje z innymi
osobami i wzorce kulturowe umieszczają ją w krajobrazie społecznym oraz pozostawiają
ślady w jej pamięci i zapisach wspólnych. Sprzężenie to nie jest jednostronne: osoba
może przyjmować, negocjować, odrzucać i przekształcać społeczne przypisania, a przez
własne działanie współkształtuje kulturę.

Sama ta konstrukcja nie jest jeszcze błędem: warstwa wyższa buduje abstrakcje
z konkretów warstwy niższej i tak działa cały stos. Do kradzieży ontologii dochodzi
dopiero wraz z amnezją: ku dołowi, gdy własny przekład zostaje uznany za bezpośredni
głos organizmu lub podmiotowości, oraz ku górze, gdy społeczne opisy i role zostają
przeżyte jako własna esencja (por. freudowskie *Über-Ich*). Osoba jest więc strukturą
szczególnie podatną na reifikację w obu kierunkach, a nie strukturą z reifikacji
zrodzoną.

Sekwencję tę traktujemy jako roboczą rekonstrukcję strukturalno-rozwojową, nie jako
bezpośrednią obserwację własnej ontogenezy ani ścisłą chronologię jej etapów.

### Nieświadome

Nieświadome nie jest w tym modelu ani miejscem, ani zbiorem ukrytych treści. Ta sama
bramka przekładu, którą osoba zwrócona jest ku dołowi, działa bowiem redukująco:
osoba raportuje wyłącznie to, co przez tę bramkę przechodzi. "Nieświadomość" nazywa
zatem zakres, którego bramka nie przepuszcza, nie zaś teatr rozgrywający się za
kulisami. Nie orzekamy przy tym, czy poza bramką coś jest doświadczane, ponieważ
pytanie to leży poza zasięgiem raportu, a więc poza granicą modelu (por. postulat 1:
nieobecność doświadczania nigdy nie jest doświadczana jako nieobecność).

Przepustowość tej bramki nie jest przy tym stała: opisana wyżej zdolność "wiercenia
dziur w abstrakcjach" oraz praktyka introspekcyjna zmieniają to, co przez nią
przechodzi. Nieświadome pozostaje więc pojęciem względnym wobec aktualnego stanu
bramki, a nie trwałym obszarem. Bez tego zastrzeżenia sama bramka stałaby się
kolejną reifikacją.

### Trwałość osoby

Trwałość tak powstałej osoby wymaga osobnego wyjaśnienia.
Anonimowe domknięcia nie dostarczają jej bowiem predefiniowanego, ukrytego
nosiciela. Jednym z roboczych modeli zgodnych z tym założeniem jest osoba jako
identyfikator intensjonalny: nie wskaźnik do trwającego obiektu, lecz opis wciąż na
nowo ewaluowany, którego odniesieniem jest to, co akurat go spełnia. W tym modelu
ciągłość osoby jest samoodwoławczą stabilnością ewaluacji, a nie trwałością
odniesienia. Wystarczy, że kontekst wciąż zwraca podobną odpowiedź. Pamięć
uczestniczy w tym nie jako magazyn, lecz przez udział identyfikatora w kluczu
przywołania: wspomnienie jest indeksowane jako czyjeś, a nie przypisywane komuś po
fakcie.

Samoodwoławczość dotyczy tu mechanizmu ewaluacji, a nie treści opisu: opis nie
zawiera siebie, lecz jego wynik współtworzy klucz, którym sięgamy po ślady pamięciowe
wchodzące w kolejną ewaluację. Dlatego identyfikator pozostaje intensjonalny
i aktualizuje się wraz ze zmianą sieci wspomnień – ciągłość osoby jest stabilnością
tej rekursji, nie niezmiennością jej wyniku. Nie traktujemy tego jako wyczerpującej
teorii osoby, lecz jako antysubstancjalistyczny model przydatny do rozumienia
tożsamości, pamięci i identyfikatorów w architekturze.

Pytanie o to, kto podtrzymuje identyfikator, nie wymaga wskazania ani "osoby", co
prowadziłoby do błędnego koła, ani "warstwy niższej", co wprowadzałoby homunkulusa.
Osoba jest właśnie stabilizującą się pętlą, a jej aktualizacja nie jest zewnętrzną
czynnością wykonywaną na niej, lecz kolejnym przebiegiem procesu, który ją
konstytuuje.

### Dostęp do osoby

Trzecioosobowy dostęp do osoby i pierwszoosobowe czucie bycia kimś wyznaczają dwa
niesymetryczne rodzaje dostępu do tego samego procesu osobowego. W pierwszym
formułujemy konstatacje: przypisujemy zachowania i właściwości, a nasze opisy mogą
być częściowe albo fałszywe. Drugie ma natomiast charakter enaktywny: identyfikacja
nie jest w nim obserwowanym przedmiotem, lecz jej wykonanie współstanowi samo
czucie.

Tautologiczność dotyczy tego przedrefleksyjnego aktu, nie późniejszego raportu.
Zdania "jestem tym" lub "jestem taki" należą już do warstwy osobowo-kulturowej
i mogą być częściowe, błędne albo oparte na społecznie przejętym opisie. Nauka
i introspekcja mogą korelować oraz wzajemnie korygować swoje sprawozdania, lecz nie
zamieniają jednego rodzaju dostępu w drugi. Ich niezbieżność nie wynika z istnienia
dwóch przedmiotów, ale z różnicy rodzajów aktu, dlatego nie znika wraz ze wzrostem
dokładności.

Nie znaczy to, że osoba jest niedostępna obserwacji. Rozluźnienie utożsamienia
z konfiguracją osobową może otworzyć pozycję, z której osoba pojawia się jako
przedmiot w krajobrazie doświadczenia. Jest to jednak dostęp do aktualnej
identyfikacji, nie pozycja poza procesem: pętla nadal biegnie, inaczej nie byłoby
czego obserwować.

Każdy raport musi wrócić przez warstwę osobową i kulturową, aby zostać ujęty
w słowa. W przyjętym modelu indeks osobowy zostaje wprowadzony przy rejestracji
śladu, nie dopiero podczas jego przywołania; przywołanie posługuje się tym indeksem
i może go ponownie wzmacniać. Model dopuszcza zatem sprawdzalną hipotezę, że
zawiązania słabiej indeksowane przez identyfikator osobowy pozostawiają ślady
trudniejsze do przywołania i raportowania. Można ją konfrontować m.in. z porównaniem
raportowalności stanów o różnym stopniu utożsamienia, ale nie wynika ona dedukcyjnie
z modelu i konkuruje z wyjaśnieniami takimi jak pamięć zależna od stanu czy brak
kategorii językowych.

### Rozpoznanie utożsamienia

Powyższe pozwala odróżnić dwie sytuacje, które z zewnątrz mogą wyglądać podobnie.
W pierwszej treść niższej warstwy organizuje działanie tak, jakby wyczerpywała
tożsamość, a samo utożsamienie nie zostaje rozpoznane. W drugiej utożsamienie jest
świadomie rozluźniane: treść pozostaje doświadczana, lecz operacja identyfikacji
również staje się widoczna. Ta sama treść, inna relacja do niej.

Siła utożsamienia i stopień jego rozpoznania są dwiema niezależnymi, ciągłymi
osiami. Model nie wyznacza więc progu oddzielającego metodę od regresji ani
"głębokiego" doświadczenia od pomyłki pre-/trans-. Dostarcza kierunku oceny, nie
werdyktu.

Rozpoznanie pozostaje aktem uwarunkowanym i samo może stać się kolejnym
utożsamieniem, na przykład z rolą "tego, kto rozpoznaje". Odbiera mu to ostateczność,
nie zaś przydatność. Ponieważ nierozpoznane utożsamienie nie może samo wiarygodnie
poświadczyć własnego nierozpoznania, ocena wymaga relacji, wspólnoty praktyki albo
dłuższego okna czasu. Poszerzanie się funkcjonowania stanowi omylną przesłankę,
a nie dowód; model nie daje licencji do samodzielnego certyfikowania własnej
"głębi" ani hierarchizowania innych osób.

**Zakotwiczenie w znanych tradycjach:** model ma wybrane punkty wspólne
z wieloaspektowym wzorcem osoby u Gallaghera, niesubstancjalnym centrum organizacji
narracyjnej u Dennetta i konstytutywną rolą sprzężeń w enaktywizmie. Są to zbieżności
dotyczące różnych aspektów, nie uzgodnienie całych teorii. Model identyfikatora
intensjonalnego opisuje pewien aspekt ciągłości i samoodniesienia; sprawność pamięci
lub narracji nie jest tu testem godności ani statusu osoby. Społeczny wymiar tego
procesu jest bliski społecznej teorii jaźni
G.H. Meada, zwłaszcza mechanizmowi przyjmowania postawy "uogólnionego innego"
("Mind, Self, and Society", 1934), oraz Wygotskiego tezie o społecznym pochodzeniu
i internalizacji wyższych funkcji psychicznych ("Mind in Society", 1978).
Rozróżnienie utożsamienia rozpoznanego i nierozpoznanego uzupełnia wilberowskie
ostrzeżenie przed błędem pre-/trans-: niekonceptualność ani deklarowana głębia nie
różnicują same przez się tych sytuacji; relacja do utożsamienia dostarcza osi
różnicującej, lecz nie samodzielnego progu, i może być oceniana tylko relacyjnie oraz
w czasie.

## Jak postulaty łączą się z architekturą

Pięć postulatów pomaga wyjaśnić genezę i spójność przyjętych wartości. Wartości
wskazują, co chcemy chronić, Wizja składa je w kierunek działania, a Konstytucja
określa obowiązki i granice władzy. Decyzje projektowe dodają kontekst, ograniczenia
i argumenty za konkretną realizacją; kontrakty i schematy określają jej dokładną
semantykę. Poniższe związki są genealogią znaczeń, nie dedukcją jedynego rozwiązania
ani hierarchią mocy normatywnej:

* postulat 1 (apofatyczny fundament):
  higiena epistemiczna, odmowa reifikacji, pętla korekty;

* postulat 2 (stratyfikacja):
  architektura warstwowa roju, kontrakty warstw, separacja poziomów;

* postulat 3 (enaktywne uczestnictwo):
  człowiek jako domyślna ścieżka mocy, emocje jako telemetria;

* postulat 4 (redukcja ≠ wyjaśnienie):
  wieloparadygmatowość, pluralizm, anty-sekciarstwo;

* postulat 5 (intencja jako siła systemowa):
  przejrzystość sprawczości, ekonomia sprawczej wzajemności, odwaga epistemiczna.

Jako wspólne kryterium projektowe przyjmujemy: **architektura ma wspierać świadome
zamieszkiwanie w interpretacji** – z pętlami korekty, odmową reifikacji prawdy jako
statusu, ochroną różnorodności jako źródła nowości i z jawnym odnotowywaniem granic
poznania.

Rój nie udaje wyroczni. Jest infrastrukturą dla wspólnoty, która wie, że widzi
odbicia, i nie łudzi się, że to oryginały, a jednak działa mimo to, najlepiej jak
potrafi.

## Konsekwencje i podobieństwa

### Tradycje filozoficzne

Dla czytelnika chcącego osadzić opisane wcześniej postulaty w znanym krajobrazie:

**Neurofenomenologia** (Francisco Varela): perspektywa pierwszej osoby jako metoda
naukowa; wzajemne ograniczenia między danymi fenomenologicznymi i neuronaukowymi.
W tym dokumencie czerpiemy z tej metody, kierując uwagę ku temu, co mniej
zdeterminowane niż uformowane doświadczenie i nie jest z nim tożsame.

**Enaktywizm** (Varela, Thompson, Rosch): poznanie jako uczestnictwo, nie
reprezentacja; autopojeza jako model samoorganizacji. Wykorzystujemy te inspiracje
w zestawieniu z apofatycznym gestem wobec fundamentu i roboczą genealogią warstw
doświadczenia. Zastosowanie *stratified design* jest naszym wyborem metody opisu.

**Filozofia procesu** (Whitehead, James): procesy zamiast substancji; "czyste
doświadczenie" jako to, co poprzedza podział podmiotowo-przedmiotowy. Odmowa
substancjalizacji jest punktem wspólnym. W naszym modelu obejmuje również
świadomość: nawet "czyste doświadczenie" pozostaje warunkowane.

**Madhjamaka** (Nāgārjuna): pustość samoistnienia, współzależne powstawanie,
konwencjonalna prawda jako dostępny tryb operowania. Czerpiemy z odmowy reifikacji
i gotowości pozostawania z paradoksem. Zastosowanie tej dyscypliny do genealogii
doświadczenia oraz granic oprogramowania jest osobnym krokiem interpretacyjnym.

W DIA/Orbipleksie zestawiamy te inspiracje, aby rozwijać dyscyplinę rozpoznawania
granic modeli i przekładów między warstwami. Opisujemy własny dobór i zastosowanie,
bez roszczenia do pierwszeństwa syntezy lub uzupełnienia całych tradycji. Praktycznym
polem tego spotkania są inżynieria oprogramowania, bezpieczeństwo systemów
i kontemplacyjna introspekcja.

### Systemy przetwarzania informacji

W inżynierii łączymy enaktywne i procesualne inspiracje z przyjętymi wartościami
oraz kryteriami testowalności, bezpieczeństwa i niskiego sprzężenia. W ten sposób
rozwijamy dyscyplinę projektowania, w której wiązanie znaczeń jest jawne i lokalne.

1. **Kontrakty zamiast przedwczesnych klas bytów.**

    Najpierw pytamy: "jakie przejście, uprawnienie, obserwacja albo decyzja tu
    zachodzi?", a dopiero potem: "czy to potrzebuje typu?". To prowadzi do małych
    artefaktów na poziomie komunikacji i cienkich interfejsów.

2. **Tożsamość jako uchwyt, nie esencja.**

    `id` nie mówi, czym coś "naprawdę jest". Jest stabilnym punktem korelacji
    w procesie. Znaczenie jest w warstwie, historii, kontrakcie i aktualnym
    kontekście.

3. **Moduły jako role w przepływie, nie ontologiczne substancje.**

    Komponent nie powinien wiedzieć, że rozmawia z "tym konkretnym czymś", jeżeli
    wystarczy mu kontrakt zachowania. To chroni przed sprzężeniem.

4. **Granice warstw jako granice sensu.**

    To samo zdarzenie może mieć inną projekcję w różnych warstwach. Niska warstwa
    widzi bajty, wyższa widzi decyzję, jeszcze wyższa widzi fakt społeczny. Błąd
    zaczyna się wtedy, gdy jedna warstwa "kradnie" ontologię drugiej. Przykładem
    takiej kradzieży w górę jest żądanie, aby ład społeczny był bezimienny na tej
    podstawie, że bezimienne są zawiązania doświadczenia.

    Cztery praktyczne przykłady niedopuszczalnego awansu uzasadnienia:

    - poprawny podpis nie dowodzi prawdziwości podpisanej treści;
    - lokalny transport nie dowodzi lokalnego wykonania inferencji;
    - zgodność danych ze schematem nie nadaje uprawnienia do działania;
    - zapis deklaracji w Memarium nie potwierdza jej prawdziwości o świecie.

    Każde takie przejście wymaga osobnego uzasadnienia właściwego warstwie docelowej;
    przy jego braku roszczenie pozostaje niepotwierdzone. Schemat sprawdza część
    kontraktu danych, a semantyka, uprawnienia i skutki wymagają odpowiednich
    walidatorów oraz testów. Ich właścicieli, negatywne przypadki i stan wdrożenia
    określają dokumenty projektowe i implementacyjne.

5. **Walidacja na brzegach jako akt lokalnego dookreślenia.**

    Dane płyną jako potencjalnie bogatsze i luźniejsze, ale na brzegu konkretnego
    kontraktu mówimy: "tu, dla tej operacji, uznajemy taki kształt". To jest zdrowe,
    lokalne dookreślenie, a nie przedwczesne związanie zjawiska w obiekt.

6. **Polimorfizm i dyspozycja jako świadome opóźnienie decyzji.**

    Nie zamrażamy "kto wykona" w strukturze danych, jeżeli właściwe miejsce decyzji
    jest później: przy kontekście, *capability*, profilu, ewaluatorze, rejestrze albo
    weryfikatorze paszportu zdolności.

7. **Zdarzenia i fakty zamiast mutowania rzeczy.**

    *Append-only facts* dobrze pasują do procesu: zapisujemy to, co zaszło, zamiast
    udawać, że mamy jedną trwałą rzecz, która po prostu "zmieniła stan".

8. **Architektura mniej podatna na nazewniczą hipnozę.**

    W systemach często nazwa tworzy fałszywą substancję: `User`, `Agent`, `Passport`,
    `Connector`, `Account`. Procesualne pytanie brzmi: "jakie procesy i relacje ta
    nazwa tylko lokalnie skraca?".

9. **Dowód współzależny zamiast pojedynczego świadka.**

    Skoro zjawisko może zależeć od zbiegu wielu współdziałających warunków, świadectwo
    o nim często warto budować ze zbieżności wielu sygnałów. Pojedynczy podpis,
    etykieta albo źródło rzadko są dowodem same w sobie; pewność może rosnąć wraz ze
    zbieżnością niezależnych przesłanek (atestacje, reputacja, korelacja zdarzeń), nie
    wraz z autorytetem jednego nośnika.

    Wyłanianie się zjawiska ze splotu wielu warunków, którego nie da się opisać na jego
    własnej warstwie wyłącznie językiem warstwy niższej bez utraty istotnych relacji,
    bywa nazywane **emergencją** (por. emergentyzm, postulat 4). Używamy tego pojęcia
    w sensie epistemicznym i operacyjnym: opis niższej warstwy może być poprawny
    w swoim zakresie, a zarazem niewystarczający dla pytań i kontraktów warstwy wyższej.
    Nie przesądza to metafizycznej nieredukowalności zjawiska.

    **Konsiliencja** (Whewell – zgodność niezależnych indukcji) i triangulacja należą
    do innej osi: są strategiami poznawczymi, a nie własnościami samego zjawiska.
    Wieloźródłowe potwierdzenie nie wynika logicznie z emergencji, lecz jest
    bezpiecznikiem epistemicznym przydatnym wtedy, gdy twierdzenie zależy od wielu
    warunków albo ma wywołać skutek o wysokiej stawce.

10. **Próg warstwy rozlicza stratę i uzyskaną sprawczość.**

    Kandydat na nowe *stratum* powinien nazywać warunek stabilizacji, reduktor, utracone
    rozróżnienia, nowy niezmiennik, gramatykę operacji, uzyskaną możliwość działania
    i typowy tryb porażki wskutek reifikacji. Jeżeli nie pojawia się nowy kontrakt ani
    rodzina operacji, mamy raczej projekcję lub widok istniejącej warstwy niż warstwę
    nową. Dzięki temu przypadkowy mechanizm implementacyjny nie staje się semantyką
    domeny, a abstrakcja zachowuje pamięć o tym, co kupiła za poniesioną stratę.

Zdajemy sobie sprawę, że jesteśmy podatni na przedwczesne wiązanie zjawisk w zamknięte
postacie, a wiedząc o tym, możemy budować systemy, które adaptują się do tej
właściwości naszych organizmów i aparatów poznawczych. Jedną z praktycznych metod
jest stratyfikacja. Każda warstwa abstrahuje z konkretów warstwy niższej własności
istotne dla swojego kontraktu, nadaje powstałej projekcji nazwę i granice, a następnie
udostępnia ją jako nowy konkret warstwie wyższej. W opisanym wyżej sensie "konkret"
oznacza rolę względem warstwy, nie większą realność, przedmiotowość ani prawdziwość.

Takie projektowanie ogranicza ryzyko przypadkowej reifikacji: rzeczy powstają tam,
gdzie są potrzebne, i tylko w zakresie oraz kształcie, w których dane *stratum* powinno brać
za nie odpowiedzialność. Tak tworzone warstwy abstrakcji są więc kontekstem
poznawczym i technicznym. Pozwalają nie myśleć o wszystkich zależnościach naraz. To
nie jest ucieczka od złożoności, lecz uczciwe porcjowanie jej w taki sposób, aby
człowiek mógł system rozumieć, testować, audytować i zmieniać bez rozrywania całości
bądź przypadkowego usztywnienia abstrakcji.

Na skali społeczno-technicznej ten sam błąd bywa nazywany *reverse adaptation*
(Langdon Winner, "Autonomous Technology"): cele i formy ludzkiego działania
dostrajają się do ograniczeń narzędzia, jak gdyby te ograniczenia były naturą
dziedziny. Ten sam wzorzec widać poza komunikacją: logika domenowa zakrzepła
w nazwach klas i interfejsów (kod jako *de facto* relacyjna baza danych w niektórych
językach zorientowanych obiektowo), prefabrykowane osiedla wymuszające niską
prywatność, gwiaździsta topologia sieci. To przypadkowa reifikacja rozłożona na
medium, ekonomię i nawyk – nie awaria pojedynczej warstwy, lecz zastygnięcie całego
stosu. Świadomie utrzymywana stratyfikacja pozwala działać w drugą stronę: upłynnia
to, co *reverse adaptation* zdążyła usztywnić.

<span id="inferencja-do-architektury"></span>

#### Przykładowe zastosowanie w architekturze

Poniższa mapa **kontraktów i brzegów** zestawia wybrane akty determinacji
z operacjami oprogramowania. Ilustruje funkcjonalne podobieństwa, nie odwzorowanie
jeden-do-jednego, obowiązkowy pipeline ani wyprowadzenie komponentów z genealogii
doświadczenia. Każde zastosowanie zachowuje własny kontrakt i zakres uzasadnienia.

| stan (*co?*) | akt (*jak?*) | warstwa/operacja Orbipleksu |
|---|---|---|
| fenomen | jawienie się | surowy sygnał na brzegu (przed przyjęciem) |
| postać / coś | różnicowanie, wyodrębnienie | Sensorium: candidate → admitted `sensorium-observation.v1` (id, ttl, metadata admisji) |
| znak | odniesienie | `artifact-object-pointer.v1` / refs – coś zaczyna *wskazywać* |
| znaczenie | usensownienie | wybrany sens operacyjny: `classification.v1` wiąże klasyfikację prywatności i warunki przepływu danych, nie pełnię ich znaczenia |
| pojęcie | uogólnienie | schemat / taksonomia (schema-gate, `taxonomy/id`) |
| przedmiot | instancjonowanie | intencjonalny obiekt domeny: `corpus-reasoning-query`, `RoomSubject` |
| obiekt | obiektywizacja | trwały fakt zapisu obserwacji lub deklaracji w Memarium, *facts-before-effects*; zapis nie poświadcza prawdziwości treści |
| rzecz | urzeczowienie | rekord współdzielony federacyjnie: Agora topic-addressed record, tier Public, `federation-root` |

Ten przykład pomaga wskazać brzegi, na których potrzebne są bramki walidacji
i jawne reguły przekładu. Nie każda ścieżka przechodzi przez wszystkie wymienione
operacje lub w tej kolejności. Tabela nie poświadcza również stanu wdrożenia;
egzekwowanie poszczególnych granic wymaga dowodów w kontraktach i implementacji.

Zauważmy, że kierunek tej osi to rosnące powiązanie, a nie rosnąca prawdziwość:
rekord federacyjny zamyka przedstawiony przykład aktów determinacji, a nie staje się
źródłem prawdy, do którego niższe warstwy miałyby się dostroić.

#### Najbliższe koncepcje architektury informacji

Dla czytelnika chcącego osadzić powyższe konsekwencje dla systemu przetwarzania
informacji w znanym krajobrazie inżynierii systemów:

**Projektowanie warstwowe / stratified design** (Abelson, Sussman): system jest
układem kolejnych warstw abstrakcji, w których każda warstwa ma własny język,
prymitywy i sposoby komponowania. Nasze podejście podziela ten nacisk na warstwowość,
ale dodaje kryterium ontologiczne: granice warstw są również granicami sensu. Wyższa
warstwa nie powinna kraść ontologii niższej, a niższa nie powinna udawać, że wyjaśnia
całość znaczenia warstwy wyższej.

**Domain-Driven Design i bounded contexts** (Evans, Fowler): model ma lokalny zakres
ważności, a te same pojęcia mogą znaczyć co innego w różnych kontekstach. Podejście
DIA/Orbiplex rozwija tę intuicję szerzej: identyfikatory, typy, role agentów, fakty,
zdarzenia i uprawnienia mają sens dopiero wewnątrz określonego kontraktu
warstwy. Znaczenie nie jest globalną substancją, lecz lokalną relacją użycia,
odpowiedzialności i interpretacji.

**Projektowanie kontraktowe, behawioralne i capability-based** (Meyer, Liskov/Wing,
Miller, Hewitt): komponent nie jest definiowany przez nazwę, klasę ani deklarowaną
esencję, lecz przez zachowanie, zobowiązania, warunki użycia i rzeczywiste
uprawnienia. Nasze podejście podziela tę orientację na kontrakty, role i możliwości
działania, ale traktuje kontrakt nie jako ostateczną definicję bytu, lecz jako
lokalny akt kontraktowego dookreślenia: mówi, co w danej operacji uznajemy za
wystarczająco określone.

**Paradygmat komponowalności przestrzennej i czasowej** (Shi, Zhang, Cui):
dynamiczna kompozycja ma dwie ortogonalne osie. Przestrzenna dotyczy jawnego
deklarowania zależności oraz reagowania na ich pojawienie się, zmianę i utratę;
czasowa – usuwania lub zastępowania komponentów wraz z prawidłowym rozliczeniem
wywołanych przez nie skutków. Podejście Orbipleksu podziela ten nacisk na jawny
kontekst, zależności i cykl życia, lecz zawęża pojęcie odwracalności: imperatywnie
cofać można jedynie skutki dotyczące typowanych zasobów lokalnych. Skutki trwałe,
zewnętrzne i federacyjne pozostawiają historię, a ich korekta następuje przez
transakcję, wycofanie, zastąpienie albo kompensację. Komponowalność nie oznacza więc
wymazania przeszłości, lecz zachowanie prawdziwej semantyki przejść między warstwami
i komponentami.

**Event sourcing, logi faktów i architektury niemutowalne** (Fowler, Young): stan
systemu nie jest jedną substancją mutowaną w miejscu, lecz projekcją historii
zdarzeń. Podejście Orbipleksu podziela tę nieufność wobec magicznej mutacji: lepiej
zapisywać ślady procesu niż udawać bezpośredni dostęp do "prawdziwego stanu
rzeczy". Fakty append-only umożliwiają audyt, rekonstrukcję, temporalne pytania
i korektę bez wymazywania historii.

Żadna z tych tradycji nie jest tożsama z naszym podejściem. Najbliżej mu do
przecięcia: projektowania warstwowego, *bounded contexts*, kontraktów behawioralnych,
object-capabilities, komponowalności przestrzennej i czasowej, modelu aktorowego
i *event sourcingu*. Własny akcent Orbipleksu polega na tym, że techniki te zostają
podporządkowane jednej dyscyplinie: rzeczy powstają dopiero tam, gdzie konkretna
warstwa bierze za nie
odpowiedzialność. Identyfikator jest uchwytem, nie esencją; typ jest lokalnym
kontraktem, nie metafizyką; zdarzenie jest śladem procesu, nie absolutną prawdą;
moduł jest rolą w przepływie, a nie jest substancją.

### Ekonomia

Ontologia pomaga rozpoznawać ukryte założenia modeli gospodarowania, ich granice
i ryzyko reifikacji. Wybór modelu ekonomicznego wymaga ponadto jawnych wartości:
w Orbipleksie przyjmujemy ochronę sprawczości osób, wzajemność, pomocniczość i prawo
wyjścia. Te przesłanki wraz z kontekstem działania wspierają wybraną syntezę,
nie wyznaczają jednak jedynego ustroju.

Osobny dokument [Ekonomia sprawczej wzajemności](ECONOMY-OF-AGENTIC-MUTUALITY.pl.md)
rozwija te związki, rozdzielając filozoficzne inspiracje, przyjęte wartości,
hipotezy projektowe i obowiązujące rozstrzygnięcia konstytucyjne. Suplement
objaśnia ich sens, nie ustanawia nowych praw ani obowiązków.
