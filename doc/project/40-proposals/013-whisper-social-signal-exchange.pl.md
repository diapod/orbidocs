# Whisper: wymiana sygnałów społecznych i inicjowanie współpracy po przekroczeniu progu

<a id="whisper-social-signal-exchange-and-threshold-bootstrap"></a>

Based on:
- `doc/project/20-memos/orbiplex-whisper.md`
- `doc/project/20-memos/orbiplex-anon.md`
- `doc/project/30-stories/story-005-whisper-rumor-intake.md`

Powiązane:
- `doc/project/40-proposals/078-weak-signal-harvester.md`
- `doc/project/40-proposals/079-cross-federation-alliance.md`
- `doc/project/30-stories/story-014-dormant-contest-entry.md` (scenariusz akceptacyjny
  [rezonansu uśpionych faktów](#dormant-fact-resonance-2026-10-27))

## Status {#status}

Proponowany (szkic). Wersja bazowa i kontynuacje po MVP mają osobne trackery;
żadna z poniższych kontynuacji nie stanowi deklaracji ukończenia runtime'u.

## Data {#date}

2026-03-23

Rewizja: 2026-10-28 ([przegląd kontraktów i rozstrzygnięcia F-01–F-24](013-whisper-social-signal-exchange/contract-review-2026-10-28.md)).

## Streszczenie {#executive-summary}

Proposal definiuje kształt v1 `Orbiplex Whisper`: warstwę wymiany sygnałów
społecznych z jawnymi granicami prywatności, służącą pogłoskom, wczesnemu
wykrywaniu wzorców i późniejszemu inicjowaniu zrzeszeń.

Kluczowe decyzje:

1. Whisper wymienia słabe sygnały społeczne, a nie potwierdzone fakty.
2. Whisper musi zachowywać jawną semantykę pogłoski w całym przepływie.
3. Przed publikacją Whisper lokalnie redaguje treść i przepisuje ją za zgodą użytkownika.
4. Kontrole antysybilowe v1 powinny opierać się na budżetach i politykach, a nie
   semantycznym wykrywaniu duplikatów.
5. Przekroczenie progu powinno prowadzić do deterministycznej propozycji rozpoczęcia
   współpracy, a nie automatycznego dołączania ludzi.
6. Anonimowość typu onion lub oparta na przekaźnikach powinna znajdować się za
   osobnym capability prywatności wyjścia. Whisper żąda jej przez intencję routingu,
   zamiast implementować ją we własnym wnętrzu.
7. Whisper przenosi też ograniczone oświadczenia `trace` o utworzeniu, wysłaniu,
   otrzymaniu lub posiadaniu artefaktu. Domyślnie ślad ujawnia tylko digest;
   treść inline wymaga jawnej zgody i nadal jest twierdzeniem, a nie receiptem
   ani poświadczeniem.

## Kontekst i problem {#context-and-problem-statement}

Orbiplex ma już wymianę odpowiedzi w pokojach, przepływy zamówień, koncepcje
archiwizacji i rosnące wsparcie dla artefaktów z bogatą informacją o pochodzeniu.
Brakuje jednak ograniczonego sposobu wymiany między węzłami słabych sygnałów
istotnych społecznie, takich jak:

- "ludzie w różnych miejscach mogą doświadczać tego samego nadużycia organizacyjnego",
- "użytkownicy mogą napotykać ten sam szkodliwy wzorzec moderacji",
- "problem godności lub bezpieczeństwa może mieć charakter rozproszony, a nie odosobniony",
- "odmowa wysłania karetki, po której występują ciężkie powikłania, może powtarzać się jako systemowy problem ratownictwa, a nie pojedynczy pech",
- "niezależni wynalazcy w różnych krajach zdają się dochodzić do tego samego podejścia technicznego bez wcześniejszego kontaktu",
- "kilka społeczności niezależnie uruchomiło strukturalnie podobne rozwiązania niezaspokojonej potrzeby".

Druga klasa sygnałów – zbieżność pomysłów – jest równie ważna jak pierwsza.
Sygnały problemowe służą wczesnemu wykrywaniu i zbiorowej reakcji, a sygnały idei
służą współtworzeniu: łączeniu ludzi, którzy niezależnie doszli do podobnego
pomysłu, zanim ich drogi nieodwracalnie się rozejdą. Obie polaryzacje wymagają
pełnoprawnej obsługi.

Bez jawnej warstwy sygnałów społecznych węzły albo:

- zachowują takie sygnały wyłącznie lokalnie i nie korelują ich,
- albo improwizują komunikację ad hoc, ryzykując nadmierne ujawnienie, słabe
  pochodzenie danych i przypadkowe wzmacnianie pogłosek.

System potrzebuje warstwy pośredniej:

- słabszej niż dowód,
- mocniejszej niż prywatna intuicja,
- na tyle ograniczonej, by uwzględniała prywatność,
- i na tyle jawnej, by umożliwiała progowanie i inicjowanie zrzeszeń.

## Cele {#goals}

- Zdefiniować `Whisper` jako osobną rodzinę protokołów wymiany sygnałów o charakterze pogłoski.
- Zachować jawną semantykę pogłoski i nigdy przypadkowo nie spłaszczać jej do dowodu.
- Włączyć lokalną redakcję i zgodę użytkownika do ścieżki publikacji.
- Obsłużyć rejestrację zainteresowań i wykrywanie progów bez przedwczesnego ujawnienia.
- Umożliwić deterministyczne inicjowanie zrzeszeń po osiągnięciu masy krytycznej.
- Zachować modułową anonimowość transportu dzięki capability prywatności wyjścia.

## Poza zakresem {#non-goals}

- Proposal nie definiuje pełnego zarządzania sprawami dowodowymi.
- Nie definiuje ostatecznych procedur zarządzania ani orzekania.
- Nie definiuje semantycznego wykrywania duplikatów pogłosek w v1.
- Nie wymaga transportu typu onion dla każdego komunikatu Whisper.
- Nie definiuje całego kontraktu dostawcy przekaźnika/prywatności poza jego granicą z Whisper.
- Nie definiuje zbierania korpusów źródłowych z dokumentów, poczty ani
  skonfigurowanych kanałów. Weak Signal Harvester (Proposal 078) jest wcześniejszym
  narzędziem wykrywania, które może przygotować lokalne ustalenia do przeglądu przed
  przyjęciem ich przez Whisper.

## Decyzja {#decision}

Orbiplex powinien traktować `Whisper` jako wyspecjalizowaną warstwę wymiany
sygnałów społecznych z następującym cyklem życia v1:

1. lokalne przyjęcie pogłoski
2. lokalna redakcja i redukcja idiolektu
3. zatwierdzenie oczyszczonego wyniku przez użytkownika
4. publikacja `whisper-signal`
5. opcjonalna rejestracja `whisper-interest` na węzłach odbiorczych
6. `whisper-threshold-reached`
7. `association-room-proposal`
8. jawne, lokalne dołączenie człowieka do pokoju lub procesu następnego etapu

Anonimowość transportu pozostaje osobną odpowiedzialnością:

- `Whisper` wyraża intencję routingu i wymagany poziom prywatności,
- wyjście Node realizuje ten poziom przez zainstalowane capability prywatności
  wyjścia lub przekaźnika,
- Node rozstrzyga, czy wymagany poziom można spełnić, zdegradować, czy należy odmówić.

## Proponowany model {#proposed-model}

### Klasy komunikatów {#message-classes}

Rodzina protokołów Whisper ma dwie pełnoprawne klasy komunikatów o różnej semantyce:

- **sygnał społeczny** – `whisper-signal.v1`, którego `signal/polarity` ma wartość
  `problem` lub `idea`; może uczestniczyć w korelacji, progowaniu i inicjowaniu zrzeszeń;
- **oświadczenie o śladzie** – `whisper-trace.v1`, ograniczone twierdzenie o pochodzeniu:
  artefakt został utworzony, przekazany transportowi, odebrany lub był posiadany we
  wskazanym czasie. Nigdy nie uczestniczy w progowaniu sygnałów społecznych.

`public-gossip.v1` pozostaje osobnym, jawnym kontraktem publikacji publicznej.
Nie jest klasą komunikatu Whisper i nie powstaje niejawnie ani z sygnału, ani ze śladu.

Ślad jest słabszy niż `execution-receipt.v1`, receipt dostarczenia lub poświadczenie.
Podpis obejmującej go koperty identyfikuje autora twierdzenia; nie dowodzi zajścia
opisywanego zdarzenia. Opcjonalna lista `evidence/refs` może wskazywać niezależnie
weryfikowalne receipts lub poświadczenia bez kopiowania ich payloadów.

Ujawnianie śladu ma dwa tryby:

- domyślny `digest-only` przenosi digest artefaktu, długość w bajtach oraz opcjonalne
  metadane formatu/schematu;
- `digest-and-content` dodatkowo przenosi ograniczone bajty base64 i wymaga
  `consent/ref` zwalidowanego przez host autora przed publikacją.

Ujawnienie samego digestu oznacza minimalizację danych, nie anonimowość. Digest
przewidywalnego materiału lub materiału o małej entropii nadal może umożliwiać
odgadywanie i korelację między kontekstami. Klasyfikacja, odbiorca i polityka
ujawniania dotyczą więc obu trybów, nie tylko treści inline.

W trybie `digest-and-content` wskazany fakt zgody lub autoryzacji musi wiązać
konkretny digest artefaktu, zakres ujawnienia, autora lub reprezentowany podmiot
oraz okno ważności. Gdy treść dotyczy kilku osób, lokalna polityka może wymagać
uprawnienia od wszystkich właściwych podmiotów albo odmówić ujawnienia inline.
Sam ciąg referencji nie nadaje uprawnień. Limit formatu v1 wynosi 32 KiB;
polityka hosta/federacji może go obniżyć, ale nie podwyższyć.

V1 celowo nie definiuje widocznego w sieci artefaktu zgody. `consent/ref` jest
lokalnym uchwytem audytowym nadawcy i nie musi dawać się zdalnie rozwiązać;
nie powinien ujawniać identyfikatora uczestnika ani prywatnego rekordu polityki.
Federacja, która w przyszłości potrzebuje przenośnego dowodu zgody, musi zdefiniować
osobny podpisany kontrakt, zamiast reinterpretować tę nieprzezroczystą referencję.

Schemat wymaga SHA-256 i zadeklarowanej długości bajtowej. Implementacja musi
zdekodować bajty inline, egzekwować limit hosta i porównać długość oraz digest
przed przyjęciem lub publikacją śladu. Publiczny relay może zwalidować kontrakt
i podpis, lecz nie może wywnioskować, że nieprzezroczysta referencja zgody wskazuje
ważną lokalną decyzję; ten autorytet pozostaje na hoście nadawcy.

### 0. Polaryzacja sygnału {#0-signal-polarity}

`whisper-signal` ma jedną z dwóch podstawowych polaryzacji:

- **`problem`** – sygnał opisuje rozproszoną szkodę, usterkę lub zagrożenie godności.
  Celem cyklu życia jest wczesna korelacja, a po osiągnięciu masy krytycznej –
  zbiorowa reakcja lub działanie ochronne. Stopień sygnału wyraża ryzyko ochronne
  i pilność. Można uruchomić ścieżki pomocy w nagłych przypadkach.
- **`idea`** – sygnał opisuje zbieżny pomysł, twórcze odkrycie lub wyłaniające się
  podejście, do którego wiele osób lub grup zdaje się dochodzić niezależnie.
  Celem cyklu życia jest zaproponowanie współtworzenia lub współpracy stronom,
  które jeszcze się nie odnalazły. Stopień sygnału wyraża siłę zbieżności,
  potencjał współtworzenia lub pilność skojarzenia zainteresowanych uczestników.
  Protokoły alarmowe nigdy nie są uruchamiane.

`signal/polarity` jest obowiązkowym polem `whisper-signal.v1`. Obie polaryzacje
współdzielą cykl życia, lecz różnią się pilnością, podejściem do redakcji
i charakterem powstającego pokoju zrzeszenia:

- problem → pokój wsparcia, koordynacji lub reakcji ochronnej,
- idea → pokój współtworzenia lub współpracy.

### 1. Semantyka pogłoski pozostaje jawna {#1-rumor-semantics-remain-explicit}

Artefakty Whisper nie są artefaktami dowodowymi.

Protokół musi zachowywać niższą klasę epistemiczną, taką jak:

- pogłoska,
- słaby sygnał,
- skorelowany sygnał,
- dopiero później, gdy uzasadnia to procedura, potwierdzona sprawa.

To granica bezpieczeństwa semantycznego. System nie może uznać pogłoski za
"potwierdzoną" tylko dlatego, że powtórzyło ją wiele węzłów.

### 2. Lokalna redakcja przed publikacją {#2-local-redaction-before-publication}

Surowy tekst wprowadzony przez użytkownika lub operatora powinien domyślnie pozostawać lokalnie.

Lokalny Weak Signal Harvester (Proposal 078) może wcześniej przygotować kandydackie
ustalenia z dokumentów, poczty lub innych skonfigurowanych źródeł. Takie ustalenia
nie są artefaktami Whisper. Trafiają do Whisper dopiero po lokalnym imporcie,
grupowaniu, przeglądzie i jawnym działaniu użytkownika/operatora. Harvester nie
może bezpośrednio publikować `whisper-signal.v1`.

Przed publikacją Whisper powinien wykonać ograniczony lokalny workflow obejmujący:

- anonimizację,
- parafrazę,
- spłaszczenie idiolektu,
- przegląd prywatności i ryzyka.

Wynik tego workflowu powinien zostać przejrzany i zaakceptowany przez użytkownika,
zanim zostanie wyemitowany jakikolwiek artefakt kierowany do sieci.

Anonimizacja ochronna w tym workflowie dotyczy ludzi i chronionych lokalnych kontekstów. Nie powinna bezrefleksyjnie usuwać nazw firm, szpitali, operatorów karetek ani innych instytucji, gdy podmioty te mogą być częścią szkodliwego wzorca i nie wymagają ochrony.

Gdy szkic przygotował lokalny pomocnik, taki jak `Monus`, polityka dalszych etapów
nadal powinna rozróżniać sygnały autorstwa użytkownika, zaobserwowane przez operatora,
wyprowadzone przez Monusa oraz wyprowadzone przez Monusa wraz z Sensorium.

W zakresie semantyki ról wychodzący `whisper-signal` powinien zachowywać obie informacje:

- `sender/node-id` dla aktora infrastrukturalnego przenoszącego publikację,
- pseudonimową rolę autorską przez `rumor/nym`, dołączony `nym-certificate`
  i podpis `nym` obejmujący ciało wychodzącego artefaktu.

Gdy Whisper korzysta ze ścieżki nymu, bazowy `participant-id` powinien pozostawać
po lokalnej lub wystawiającej stronie granicy, zamiast być ujawniany w samym
artefakcie sieciowym `whisper-signal`.

### 2.1. Pochodzenie webowe zachowane przy publikacji {#web-origin-publication}

Przyjęte rozszerzenie projektu, 2026-11-04; P013-WEB-001/002 mają status `todo`.
Nie jest to twierdzenie o obecnych formatach sieciowych ani wcześniejszej akceptacji M4.
Whisper konsumuje [przejrzane szkice P078](078-weak-signal-harvester.md#web-source-retention-and-origin)
wsparte [pieczą P084 nad oryginałem](084-sensorium-web-observation-connector.md#web-original-custody).
Przy admisji publikacji profil wymaga aktualnego, potwierdzonego przez właściciela
sprawdzenia pieczy nad oryginałem oraz dokładnie przejrzanego podsumowania pochodzenia.
Publikacja nie może niejawnie usuwać pochodzenia ani zastępować pochodzenia webowego
wartością `direct-user`. Tożsamość przeglądu wiąże zatwierdzoną treść, podsumowanie
pochodzenia i deklarację pieczy; zmiana któregokolwiek wymaga nowego przeglądu,
a nie niejawnego ponowienia.

P013 jest właścicielem wspólnego, ograniczonego podsumowania pochodzenia dla lokalnych
szkiców, podpisanych sygnałów Whisper i publikacji `public-gossip`. Proponowane osie:

| Proponowane pole | Semantyka / początkowy słownik |
|---|---|
| `origin/source-kinds` | Niepusty, ograniczony zbiór: `web`, `personal-report`, `document`, `mail`, `sensorium`, `unknown`; mieszane pochodzenie pozostaje jawne |
| `origin/collection-method` | `manual-selection`, `configured-monitoring`, `media-monitoring`, `mixed`, `unknown`; sam web nie oznacza monitoringu ani mediów dziennikarskich |
| `origin/processing` | Ograniczony zbiór istotnych przekształceń: `extracted`, `summarized`, `grouped`, `model-assisted`, `redacted`; pusty oznacza brak zadeklarowanej transformacji, nie dowód nienaruszonego źródła |

Te nazwy/słowniki są zaleceniami do zamrożenia schematu w P013-WEB-001.
Należy ponownie używać jednego zamkniętego podkontraktu podsumowania pochodzenia
oraz czystego walidatora/projektora we właściwych rodzinach publikacji, zamiast
kopiować pola lub kodować semantykę w dowolnych `gossip/tags`. Istniejące
`source/class` i `gossip/source-kind` pozostają odrębnymi osiami autorstwa/postawy
źródłowej; kontekstowe `source/ref` pozostaje tożsamością źródła-uczestnika P015,
a nie URL-em, digestem ciała ani identyfikatorem artykułu. Etykieta pochodzenia
nie zmienia `epistemic/class`, pewności ani autorytetu.

Podsumowanie obejmuje zwykły podpis publikacji; zapisuje ono uwierzytelnione
twierdzenie publikującego, nie niezależnie dowiedzione pochodzenie webowe.
Widoki publiczne wyświetlają stałą etykietę, np. "Źródło webowe" lub "Monitoring
mediów", a osobno "Przy wsparciu AI", gdy to zadeklarowano. W starszych rekordach
pochodzenie jest nieznane, nigdy domyślnie osobistym świadectwem. Promocja do
`public-gossip` zachowuje przejrzane podsumowanie przez tę samą ścieżkę
publikującego/Schema Gate. Odczytujący nie pobiera materiału źródłowego, by je
wyświetlić. Surowe oryginały, dokładne URL-e, lokalne identyfikatory ustaleń,
prywatne referencje artefaktów, digesty ciał i czas zbierania nie towarzyszą
etykiecie automatycznie; każdy element wymaga niezależnego przeglądu ujawnienia.

Przed commitem publikacji ponownie zweryfikuj ograniczoną czasowo deklarację
pieczy u jej właściciela i powiąż wynik z konkretną przygotowaną publikacją.
Wygasły/brakujący materiał oznacza odmowę nowej promocji w tym profilu. Jeśli
zacommitowana publikacja jest później dostarczana lub odtwarzana po wygaśnięciu,
nie przepisuj podpisanych bajtów ani nie udawaj dalszej dostępności źródła;
bieżąca dostępność należy do osobnego uprawnionego widoku. Wygaśnięcie retencji
nie wycofuje rekordu publicznego ani nie daje bezterminowej pieczy. Ewentualny
silniejszy minimalny horyzont retencji publikacji musi być jawną dopuszczoną
polityką, a nie wnioskiem z czasu życia pogłoski.

Zebranie nie jest potwierdzeniem: kopie lub streszczenia jednego artykułu nie
stają się niezależnymi relacjami dlatego, że publikują je różne węzły. Wykorzystaj
lokalne pochodzenie/deduplikację Harvestera i istniejące polityki korelacji;
nie publikuj prywatnych hashy do globalnej deduplikacji ani nie utożsamiaj
pochodzenia treści ze zliczaniem różnych uczestników P015. Rozszerzenie ujawnia
pochodzenie; nie rozwiązuje niezależności kopii syndykowanych ani Sybili.
Pilna ochrona zachowuje dotychczasową ścieżkę i autorytet, bez niejawnego
uchylania znaczenia deklaracji pochodzenia.

### 3. Ograniczone kontrole antysybilowe w v1 {#3-bounded-anti-sybil-controls-in-v1}

Wersja bazowa v1 powinna stosować prostsze kontrole zamiast semantycznej deduplikacji:

- budżety pogłosek według zakresu autora i okna czasowego,
- budżety przekazywania,
- limity głębokości nymów pochodnych,
- TTL przeskoków,
- opcjonalny deterministyczny `signal/similarity-key` do progowania na poziomie
  fixture'ów lub jawnie zdefiniowanego polityką,
- progowanie uwzględniające zaufanie i politykę.

Proposal jawnie odrzuca twardą semantyczną bramkę duplikatów w v1, ponieważ:

- równoważność semantyczna jest kosztowna i niejednoznaczna,
- fałszywe trafienia byłyby operacyjnie szkodliwe,
- system najpierw potrzebuje czytelnych kontraktów klasyfikacji pogłosek,
  budżetów i zakresu ujawniania.

### 4. Zainteresowanie bez ujawnienia {#4-interest-without-disclosure}

Węzły odbiorcze powinny móc powiedzieć:

- "to może mieć znaczenie lokalnie"
- "interesuje mnie dalsza korelacja"

bez ujawniania osoby, sprawy ani wewnętrznych notatek.

Pozwala to korelować sygnały, zanim zostaną ujawnione tożsamości.

### 5. Deterministyczne inicjowanie po przekroczeniu progu {#5-deterministic-threshold-bootstrap}

Po osiągnięciu masy krytycznej system nie powinien:

- automatycznie łączyć ludzi w pokoju,
- ani wybierać ad hoc autorytetu inicjującego.

Zamiast tego uczestniczące węzły powinny deterministycznie wyznaczyć mały zbiór
inicjujący, który publikuje `association-room-proposal` zawierające:

- początkową politykę pokoju,
- założenia ujawnienia,
- termin wygaśnięcia inicjacji,
- oczekiwania dotyczące moderacji lub świadków.

Dla Agora M4 pierwsza funkcja progowa jest celowo wąska: co najmniej dwa różne
uprawnione węzły publikują publiczne/federacyjne rekordy `whisper-signal.v1`
z tym samym `topic/class` i deterministycznym `signal/similarity-key` w ograniczonym
oknie czasowym. To reguła testu smoke implementacji, a nie deklaracja semantycznego
wykrywania duplikatów w produkcyjnym Whisper.

Rekordy progu i propozycji są publicznymi metasygnałami, nie publicznymi pogłoskami.
`whisper-threshold-reached.v1` oznacza, że projekcja lub wystawca twierdzi, iż
zaobserwowano korelację określoną polityką. `association-room-proposal.v1` oznacza
propozycję zredagowanej powierzchni koordynacji służącej tylko inicjacji. Żaden
z tych rekordów nie publikuje bazowej narracji społecznej; `public-gossip.v1` jest
osobnym, późniejszym krokiem publikacji wymagającym jawnego uprawnienia człowieka,
zbiorowości lub polityki. Krok ten może być niezależny od Whisper albo następować
po dobrowolnym zrzeszeniu. `association-room-proposal` jest zatem możliwym
poprzednikiem publicznej pogłoski, nie warunkiem koniecznym.

Role podpisujących są celowo rozdzielone. Źródłowy `whisper-signal.v1` podpisuje
nym źródła lub inny dopuszczony autor. Pochodny `whisper-threshold-reached.v1` lub
`association-room-proposal.v1` podpisuje autorytet projekcji, ponieważ jest to
twierdzenie o wyniku projekcji, a nie pierwszoosobowa wypowiedź społeczna.
Pierwsza implementacja może używać jednego węzła projekcji lub delegowanego klucza
projekcji, lecz protokół powinien pozostać zgodny z przyszłymi autorytetami
komitetowymi, stałymi lub wyłanianymi reputacyjnie, które dołączają dowody wyboru
i kworum inline.

### 6. Jawna bramka zgody {#6-explicit-consent-gate}

Przekroczenie progu może uzasadniać pokój następnego etapu, ale nie niejawne dołączenie.

Człowiek musi dobrowolnie wyrazić zgodę w chwili, gdy:

- ujawnia się więcej informacji,
- tożsamości są korelowane bardziej bezpośrednio,
- lub następuje dołączenie do dedykowanego pokoju.

## Dystrybucja i lokalne przechowywanie {#distribution-and-local-storage}

Pogłoska jest artefaktem treści; sposób dotarcia do odbiorców jest osobną kwestią.
Proposal zamraża dwa równorzędne mechanizmy dystrybucji i jedną regułę lokalnego
przechowywania.

### Agora jako jedna z powierzchni dystrybucji {#agora-as-one-distribution-surface}

Pogłoska MOŻE zostać opublikowana jako pełnoprawny rekord Agory (proposal 035), z:

- `record/kind = "whisper"`,
- `content/schema = "whisper-signal.v1"`,
- `author/participant-id` przenoszącym `rumor/nym` jako tożsamość
  `nym:did:key:...` (proposal 035 §2, inwariant 9),
- `author/nym-proof` przenoszącym w pierwszej kolejności inline materiał
  `nym-certificate.v1` wystarczający do weryfikacji bieżącego nymu bez zdalnego
  wyszukiwania oraz opcjonalne referencje do dłuższego rodowodu, audytu lub historii reputacji,
- `signature` koperty wytworzonym kluczem prywatnym nymu,
- przyjęciem dopuszczonym przez bramkę poświadczeń (proposal 041), która przyjmuje
  certyfikat nymu jako artefakt poświadczenia w skonfigurowanym trybie ingestu tematu.

Gdy pogłoska podróżuje przez Agorę, tożsamość, autorstwo, czas, kanoniczny identyfikator
rekordu i podpis znajdują się w **kopercie**, a nie w ciele treści `whisper-signal.v1`.
Odpowiada to uzgodnieniu granicy koperta–treść zastosowanemu do `resource-opinion.v1`
w proposalu 026 §2.

| Odpowiedzialność | Miejsce |
|---|---|
| pseudonimowa tożsamość autora | koperta `author/participant-id` = `nym:did:key:...` |
| powiązanie autoryzacji nymu | koperta `author/nym-proof` z materiałem certyfikatu preferującym inline i opcjonalnymi referencjami |
| czas autorstwa | koperta `authored/at` |
| kanoniczny identyfikator sygnału | koperta `record/id` |
| podpis kanonicznych bajtów | koperta `signature` (Ed25519 kluczem nymu) |
| routing tematu | koperta `topic/key` (konwencjonalnie `ai.orbiplex.whispers/<topic-class>` dla pogłosek publicznych/federacyjnych; `private/<name>` dla artefaktów wyłącznie bezpośrednich INAC, których Agora nigdy nie może przenosić) |
| semantyka pogłoski | ciało treści walidowane przez `whisper-signal.v1` |

Dystrybucja przez Agorę jest odpowiednia, gdy:

- `disclosure/scope` pogłoski to `federation-scoped`, `cross-federation`
  lub `public-aggregate-only`,
- autor chce adresowalnej obecności w indeksie podmiotów pod publicznym tematem,
- polityki ingestu operatorów relayów (proposal 041 §4–§5) odpowiadają ryzyku
  i wymaganiom routingu pogłoski.

Przy ujawnieniu `cross-federation` jednym z lokalnych wejść admisji może być
`alliance-policy.v1` z Proposala 079. Nie zastępuje ona własnych kontroli Whisper
dotyczących autora, ujawnienia, redakcji ani publikacji i nie przenosi autorytetu
Seed Directory ani Agory.

Dystrybucja przez Agorę NIE jest odpowiednia dla pogłosek o `disclosure/scope` równym `private-correlation`; POWINNY one podróżować w bezpośredniej
wymianie między węzłami.

Jest to celowo **POWINNO, a nie MUSI**. W publicznych wdrożeniach Agory semantyka
`private-correlation` jest niezgodna z właściwościami publikacji Agory (publiczne
wyliczanie tematów, obecność w indeksie podmiotów, digest tematu), dlatego takie
wdrożenie POWINNO odmawiać ingestu tych pogłosek. Zamknięta/wewnątrzorganizacyjna
federacja (np. wdrożenie firmowe z uwierzytelnionym, niepublicznym relayem Agory
pod własną polityką ingestu) MOŻE przenosić pogłoski `private-correlation`
wewnętrznie, ponieważ powierzchnia ekspozycji relaya jest już zawężona do
organizacji. Reguła dotyczy zatem semantyki ujawnienia, nie mechanicznie koperty
`agora-record.v1` – ufamy operatorom niepublicznych federacji w tej decyzji.

### Bezpośrednia wymiana między węzłami jako druga powierzchnia dystrybucji {#direct-node-to-node-exchange-as-the-second-distribution-surface}

Pogłoska MOŻE podróżować bezpośrednio między uczestniczącymi węzłami, bez relaya
Agory. **Format sieciowy pozostaje tą samą kopertą `agora-record.v1`**, więc
kanonikalizacja, reguły podpisu i samodzielna weryfikacja są identyczne;
różnią się tylko transport i zakres adresowalności:

- transport: uwierzytelniony kanał między węzłami realizowany przez capability
  prywatności wyjścia (zob. niżej "Granica transportu"),
- zakres: zbiór odbiorców wynika z bezpośredniego wyboru węzłów lub rejestracji
  zainteresowania (`whisper-interest.v1`), nie z subskrypcji tematu publicznego,
- retencja: podlega lokalnej polityce Memarium każdego odbiorcy; nie istnieje
  wspólne podłoże egzekwujące jednolitą retencję u wszystkich odbiorców.

Wymiana bezpośrednia jest odpowiednia, gdy:

- `disclosure/scope = "private-correlation"`,
- routing wymaga anonimowości z `hard-fail`, a żaden relay Agory jej nie gwarantuje,
- pogłoska jest wczesną sondą wzorca i nie przekroczyła jeszcze progu
  uzasadniającego trwałą obecność publiczną.

### Odkrywanie zainteresowań i ograniczone prywatne rozpowszechnianie {#interest-discovery-and-bounded-private-dissemination}

Dla pogłosek `private-correlation` zainteresowanie tematem odkryte przez Agorę
stanowi **kwalifikowalność, nie uprawnienie do dostarczenia**.

Rekord zainteresowania tematem Agory może wskazywać, że węzeł chce i potrafi
odbierać prywatne pogłoski danej klasy tematu przez INAC lub inną dopuszczalną
ścieżkę prywatnej wymiany. NIE MOŻE oznaczać obowiązku dostarczenia mu każdej
pasującej prywatnej pogłoski. Węzeł źródłowy odpowiada tylko za **ograniczone
początkowe rozpowszechnienie** zgodnie z lokalną polityką wyjścia.

Węzeł wybierający odbiorców prywatnej pogłoski POWINIEN wybrać mały, ograniczony
polityką zbiór, korzystając z kryteriów takich jak:

- zgodność klasy tematu,
- akceptowany `disclosure/scope`,
- obsługa prywatnego transportu,
- lokalny budżet wyjścia,
- zadeklarowana pojemność przyjęć,
- poziom zapewnień węzła lub operatora,
- różnorodność federacji, jurysdykcji, klasy operatora lub przedziału reputacji,
- deterministyczne próbkowanie epok, aby popularne tematy nie trafiały zawsze
  do tych samych odbiorców.

Szerszą świadomość POWINNO się osiągać przez progowane artefakty zagregowane
oraz kontynuację bramkowaną zgodą, nie przez rozsyłanie surowych prywatnych sygnałów.
Milion węzłów wyrażających ogólne zainteresowanie popularnym tematem nie tworzy
zatem obowiązku dostarczenia miliona komunikatów.

### Redystrybucja wspomagana przez posiadacza {#holder-assisted-redistribution}

Węzeł, który odbiera i przechowuje prywatną pogłoskę, MOŻE później działać jako
dodatkowy posiadacz i redystrybutor, ale tylko gdy spełnione są wszystkie warunki:

- podpisana pogłoska i lokalna polityka Memarium pozwalają na przekazywanie
  lub ponowne dostarczenie z przechowania,
- operator odbiorcy jawnie włącza dostępność posiadacza dla właściwej klasy pogłosek,
- węzeł publikuje w Agorze wyłącznie ograniczony sygnał dostępności, nie samą
  prywatną pogłoskę,
- węzeł egzekwuje te same ograniczenia ujawnienia, routingu, budżetu, zgody
  i audytu, które obowiązywały węzeł źródłowy.

Sygnał dostępności posiadacza jest wskazówką odkrywania, a nie publiczną kopią-cieniem
pogłoski. POWINIEN unikać surowego `signal/text`, surowych słów kluczowych, czasów
właściwych dla sprawy i innych metadanych umożliwiających rekonstrukcję. Bezpieczny
kształt v1 powinien zawierać raczej:

- klasę tematu lub zgrubną rodzinę tematów,
- akceptowany profil prywatnego transportu,
- zakres ujawnienia akceptowany przez posiadacza,
- limity pojemności i tempa,
- klasę zapewnień / relaya / świadka,
- opcjonalny nieprzezroczysty token dostępności do korelacji z bezpośrednią kontynuacją.

Publikacja dostępności posiadacza prywatnej pogłoski sama jest aktem ujawnienia.
Publiczne wdrożenia Agory POWINNY traktować dostępność posiadacza konkretnego
sygnału jako wrażliwą i mogą odmówić, jeśli nie jest dostatecznie zgrubna,
opóźniona, progowana lub jawnie autoryzowana polityką pogłoski. Zamknięte /
wewnątrzorganizacyjne federacje MOGĄ używać dokładniejszych beaconów dostępności,
gdy ich polityki wejścia i widoczności czynią tę ekspozycję dopuszczalną.

Redystrybucja wspomagana przez posiadacza nie wymaga rekordu dostępności w Agorze.
Zaufany węzeł MOŻE skontaktować się bezpośrednio z peerem przez INAC i zaoferować
transfer prywatnej pogłoski z ograniczoną wskazówką tematu, np. "mam prywatną
pogłoskę dla klasy tematu X w zakresie ujawnienia Y". Peer MOŻE następnie zażądać
artefaktu, zignorować ofertę lub poprosić o przegląd operatora przed żądaniem.

Ścieżka oferta/żądanie/transfer jest niezależna od pochodzenia pogłoski:
przechowywana pogłoska mogła powstać lokalnie, przyjść bezpośrednio lub przez
zaufany relay, zostać przywrócona z pieczy Memarium albo uzyskana od późniejszego
posiadacza. Istotne są podpisany artefakt, jego polityka przekazywania, lokalna
polityka posiadacza i polityka przyjęć odbiorcy.

Polityką decyzji odbiorcy MOŻE być:

- **polityka domyślna** – deterministyczne lokalne reguły automatycznie żądają
  oferowanej pogłoski lub odmawiają,
- **zgoda operatora** – węzeł powiadamia operatora i żąda dopiero po jawnej zgodzie,
- **automatyzacja doradcza** – lokalny model doradczy przez Inquirium ocenia ofertę
  względem polityki i zaleca lub uruchamia żądanie, podlegając skonfigurowanym
  limitom autonomii i rejestrowaniu audytowemu.

Sama oferta NIE MOŻE zawierać surowego `signal/text`, surowych słów kluczowych ani
innych metadanych umożliwiających rekonstrukcję. Nie powinna być bardziej szczegółowa,
niż wymaga minimum potrzebne peerowi do decyzji o zażądaniu artefaktu.

Ta sama pogłoska MOŻE z czasem przechodzić między powierzchniami dystrybucji:
to, co zaczęło się jako wymiana bezpośrednia między węzłami, a potem przekroczyło
próg (§5), MOŻE zostać ponownie opublikowane w Agorze jako `whisper-durable`
(rodzaj rekordu zarejestrowany w proposalu 035 §3), z przejściem bramkowanym
jawnym krokiem zgody (§6).

### Memarium jako magazyn lokalny {#memarium-as-local-storage}

Niezależnie od powierzchni dystrybucji **lokalnym magazynem pogłoski** – zarówno
własnej, jak i odebranej – jest Memarium węzła (proposal 036). Memarium przechowuje:

- podpisaną kopertę `agora-record.v1` bez zmiany bajtów (requirements-014
  NFR-004), tak aby pogłoska pozostawała weryfikowalna i możliwa do ponownego
  wysłania niezależnie od tego, czy najpierw podróżowała przez Agorę, czy bezpośrednio,
- ślad działań cyklu życia pogłoski (szkic, redakcja, zgoda, publikacja,
  przekazanie, zliczanie zainteresowań, wykrycie progu),
- polityki prywatności określające, czy pogłoskę można odtworzyć, przekazać
  lub ujawnić poza węzłem.

Memarium jest autorytatywnym lokalnym archiwum; Agora (jeśli używana) jest
replikowaną powierzchnią publikacji. Pogłoska nigdy niezapisana w Memarium nie
istniała z perspektywy lokalnego węzła. Pogłoska zapisana w Memarium pozostaje
odtwarzalna dla przepływu ponownego dostarczenia z przechowania (proposal 040),
zależnie od bieżącej polityki retencji i ujawnienia węzła; zgoda autora i bieżąca
polityka ingestu odbierającego relaya zachowują moc przy każdym ponownym wysłaniu.

### Profil ekspozycji ocen {#assessment-exposure-profile}

**Częściowa kontynuacja lokalna, 2026-10-24; osobna względem istniejącej
kwalifikacji M4.** [Lokalny checkpoint P026](026-resource-opinions-and-discussion-surfaces.pl.md#local-pilot-evidence-checkpoint-2026-10-24)
zapisuje ograniczoną implementację wspólnego widoku oraz jej rzeczywistą akceptację
lokalnego hosta/przeglądarki. Fixture runtime'u zachowuje pola wiarygodności/odrzucenia
pogłoski przy ogólnej otwartej referencji zasobu. Nie kwalifikuje nowego samodzielnego
schematu overlayu pogłoski ani pełnego workflowu kuracji i propagacji Whisper.
Oceny wiarygodności/odrzucenia pogłoski już korzystają z `resource-opinion.v1`
z polami właściwymi dla pogłoski. Wybierają więc wspólny
[kontrakt ekspozycji P026](026-resource-opinions-and-discussion-surfaces.pl.md#6-assessment-exposure-and-sealed-rounds),
a nie drugi silnik głosowania lub prywatności Whisper. Istniejący klucz podmiotu
pogłoski i `opinion/subject-kind = rumor` identyfikują wiązanie; kanoniczna walidacja
kind/id oraz dopuszczony overlay pogłoski muszą być zgodne z kontraktem ciała opinii.

Profil lokalny wstrzymuje oceny wiarygodności, uzasadnienia, liczniki i kolejność
popularności innych osób na granicy odczytu hosta do czasu przyjętej oceny widza,
jawnego pominięcia lub upływu lokalnego okna kontaktu. UI kuracji, Agent,
wyszukiwanie, powiadomienia i SSE konsumują projekcję związaną z widzem;
przybycie zwykłej pogłoski i przybycie oceny innej osoby są odrębnymi zdarzeniami.
Skrzynka może liczyć dopuszczalne pogłoski, ale nie może maskować ukrytej aktywności
ocen jako nowej aktywności pogłosek. Surowy dostęp do publicznego relaya pozostaje
poza tą lokalną gwarancją.

Progi rozprzestrzeniania Whisper, tłumienie spamu, budżety i reguły różnorodności
źródeł nadal działają niezależnie. Ukrycie ocen nie opóźnia pilnej ochrony ani
nie zamienia braku ocen w zerową wiarygodność. Powiadomienia ochronne korzystają
z dopuszczonych kontraktów wyjątków, nigdy z samodzielnie nadanej przez nadawcę
flagi bezpieczeństwa. Opcjonalna zamknięta runda ocen używa podpisanej bariery
i wyników P026; nie wstrzymuje transmisji pogłoski w oczekiwaniu na kworum ani
nie poświadcza społecznej niezależności.

### Kuracja pogłosek za pośrednictwem operatora {#operator-mediated-rumor-curation}

Węzeł subskrybujący publiczne pogłoski (Agora) lub przyjmujący prywatne pogłoski
(bezpośrednio między węzłami) gromadzi odebrane pogłoski w Memarium w normalnej
ścieżce ingestu. Z perspektywy koperty Memarium jest append-only – odebrana
koperta pogłoski nigdy nie jest wstecznie zmieniana ani usuwana – lecz lokalny
stan kuracji tej koperty **jest** mutowalną projekcją, przechowywaną jako osobne
fakty Memarium pod kluczem identyfikatora odebranego rekordu.

Węzeł pokazuje zgromadzone pogłoski operatorowi w lokalnym widoku skrzynki
(np. "masz 5 nowych pogłosek"). Operator może zastosować do każdej pogłoski
jeden z werdyktów kuracji:

Rozróżnienie skrzynki i powiadomienia jest współdzielone z Proposalem 057
(`057-user-and-operator-notifications.md`): pogłoski tworzą lokalne elementy
uwagi, a skrzynka jest tylko ich projekcją.

- **ocena wiarygodności** w skali 1..5,
- **oznaczenie jako spam**,
- **oznaczenie jako naruszające politykę** (np. obraźliwe, bezprawne lub poza
  tematyką przyjętą przez federację węzła).

Każdy werdykt jest wyrażony jako `resource-opinion.v1` (proposal 026), którego
koperta `record/about` wskazuje `record/id` pogłoski – tę samą tożsamość, pod którą
pogłoska jest adresowalna w Agorze i Memarium. Kuracja pogłosek pozostaje dzięki
temu w tym samym mechanizmie opinii, którego podłoże używa już dla zasobów, proposali,
i tożsamości; nie wprowadza się osobnego schematu "przeglądu pogłoski".

Celem kuracji jest rekord pogłoski, nie osoba ani inny zasób wspomniany w niej.
Przestrzenie nazw zasobów o zakresie krajowym i zwarte referencje zasobów
powiązanych podlegają [P026 §1.1–1.2](026-resource-opinions-and-discussion-surfaces.pl.md#11-country-scoped-identifier-namespaces);
nie zmieniają klasy epistemicznej pogłoski ani polityki ujawnienia.

Konkretne mapowanie (według `rumor-opinion.overlay.v1` z proposala 026 §2.4):

- **ocena wiarygodności** → `opinion/subject-kind: "rumor"` oraz
  całkowite `rumor/credibility` w `1..5`. Bazowe pole `opinion/rating`
  pozostaje niewykorzystane przy kuracji pogłoski; wiarygodność jest wymiarem
  właściwym dla rodzaju, niezależnym od ogólnej skali ocen podłoża.
- **oznaczenie jako spam** → `opinion/subject-kind: "rumor"` oraz
  `rumor/rejection-reason: "spam"`.
- **oznaczenie jako naruszające politykę** → `opinion/subject-kind: "rumor"`
  oraz `rumor/rejection-reason: "policy-violation"` (lub jedna z dokładniejszych
  wartości enuma: `abusive`, `off-topic`, `duplicate`, `fabricated`, gdy operator
  wybiera węższy powód).

Jedna opinia kuracyjna MOŻE łączyć ocenę wiarygodności i powód odrzucenia oraz
MOŻE dodatkowo zawierać `opinion/text`, gdy operator chce uzasadnić werdykt.

Domyślny wpływ werdyktu na propagację, stosowany przez własną politykę wyjścia
węzła (nie przez protokół):

- **oceniona**: bez zmiany propagacji; ocena jest pełnoprawną opinią, którą inne
  węzły mogą konsumować lub pomijać przez temat opinii Agory dla tego rekordu,
- **spam**: koperta pozostaje lokalnie do audytu, ale **nie** jest rozgłaszana,
  przekazywana przez redystrybucję wspomaganą przez posiadacza (§Redystrybucja
  wspomagana przez posiadacza) i jest wyłączona ze zliczania progu na tym węźle,
- **naruszająca politykę**: takie samo tłumienie wyjścia jak dla spamu,
  a dodatkowo opinia kuracyjna węzła jest publikowana, aby peery polegające
  na jego osądzie mogły obniżyć wagę pogłoski.

Opinia kuracyjna sama jest zwykłym rekordem Agory i podlega regułom ujawniania
oraz podpisu proposala 026; **nie** dziedziczy `disclosure/scope` oryginalnej
pogłoski. Operator oceniający pogłoskę `private-correlation` nadal może opublikować
publiczną opinię "to spam" o jej identyfikatorze rekordu bez ujawnienia ciała
pogłoski, ponieważ opinia wskazuje identyfikator, nie treść.

Nie jest wymagane usunięcie oryginalnej pogłoski na poziomie protokołu.
Tłumienie jest lokalną decyzją propagacji; weryfikowalna koperta i jej werdykty
kuracji współistnieją w Memarium jako odrębne fakty na tej samej osi czasu.

### Pogłoski w przyszłym kliencie perspektyw zasobów {#resource-perspectives-client}

Przyszły profil projektu, 2026-11-04; kontrakt klienta należy do
[P026](026-resource-opinions-and-discussion-surfaces.pl.md#resource-perspectives-client).
Whisper wnosi dostępne relacje oraz ich kurację, odpowiedzi i korekty do widoku
skupionego na zasobie. Może to wspierać społeczną funkcję plotki jako rozproszonej,
korygowalnej pamięci, bez zamieniania agregacji pogłosek w werdykt o osobie.
P013-AE-003 jest odłożone i nie blokuje bieżącej alfy ani slice'a retencji webowej.

[Przykład pamięci obywatelskiej i wymagania osi czasu P026](026-resource-opinions-and-discussion-surfaces.pl.md#resource-perspectives-client)
łączą tę pamięć z odpowiedzialnością mimo zmian stanowiska lub instytucji.
Pogłoski i opinie zachowują odrębny status obok odpowiedzi, korekt i naprawy;
Whisper dostarcza rekordy do wspólnej projekcji, a nie osobną chronologię ani
automatyczny werdykt o tym, komu ufać.

Wykorzystaj `record/about` koperty publicznej pogłoski i `gossip/see-also`, opinie
o zasobach kierowane do pogłoski oraz istniejące ścieżki odpowiedzi/rewizji Agory.
Zachowaj rozróżnienie między pogłoską o działaniu w roli, opinią o wiarygodności
tej pogłoski i opinią o bazowym zasobie. Żadna nie przechodzi automatycznie
w osąd osoby, innej roli, reputacji ani sankcji. Same odwołania do powiązanych
zasobów nie oznaczają ani oskarżenia, ani potwierdzenia.

To wiązanie publicznej pogłoski nie rozszerza zamkniętego ciała `whisper-signal.v2`
ani nie uogólnia planowanego kontraktu `signal/related-to`. Dostęp do chronionego
sygnału nie uprawnia do publicznego powiązania zasobu ani ujawnienia istnienia
sygnału przez indeks, licznik lub link. Wykorzystaj istniejące bramki
ujawnienia/publikacji i ekspozycję związaną z widzem; prywatne korelacje wymagają
własnego dopuszczonego zakresu odczytu, bez publicznego fallbacku. Pilna ochrona
zachowuje istniejącą ścieżkę.

Zachowuj w tym zakresie widoczność sprzecznych relacji, odpowiedzi, korekt,
kontekstu czasowego i dostępnego pochodzenia/rodowodu; nieznane pochodzenie
pozostaje nieznane. Spełnienie progu, podpis lub wiele kopii nie ustanawia prawdy
ani niezależnego potwierdzenia. Klient raportuje ograniczone pokrycie, nie pełny
konsensus sieci. P013-AE-003 kwalifikuje wiązanie fixture'ami offline dopuszczonych
rekordów obejmującymi sporne działanie, odpowiedź/korektę, przedruki, niedostępną
referencję i materiał wstrzymany/chroniony. Potwierdź brak werdyktu o całej osobie,
niejawnej publikacji i wycieku prywatnych referencji; wspólny dowód UI klienta
należy do P026-013, bez drugiego renderera ani harnessu akceptacyjnego.

## Scenariusz akceptacyjny M4 {#m4-acceptance-scenario}

Agora M4 używa Story-005 jako pierwszego pełnego testu smoke publicznej/federacyjnej ścieżki Whisper:

```text
node A user -> sanitized public/federated whisper signal -> node C Agora relay
node B user -> similar sanitized public/federated whisper signal -> node C Agora relay
node C relay -> replay-fed Whisper projection -> threshold -> association-room proposal
```

Smoke dowodzi tylko bezpiecznej pod względem ujawnienia ścieżki publicznej/federacyjnej.
Pogłoska `private-correlation` podana na publiczną ścieżkę relaya musi zostać
odrzucona lub zatrzymana poza Agorą, ponieważ prywatne pogłoski należą do wymiany
bezpośredniej, INAC lub innej ograniczonej ścieżki prywatnego transportu z lokalną
pieczą Memarium. Matrix może później działać jako opcjonalny adapter prywatnego
transportu, ale pokoje Matrix nie są częścią modelu domenowego Whisper ani INAC.
Wynik progu może utworzyć `association-room-proposal`, lecz nie może automatycznie
dołączać ludzi. Nie wolno też traktować go jako `public-gossip.v1`; jest wyłącznie
rekordem koordynacji, dopóki nie istnieje osobna decyzja publikacji. Publiczna
pogłoska nadal może być publikowana niezależnie na publicznej ścieżce słabych
sygnałów; cykl życia propozycji nie jest obowiązkowym warunkiem wstępnym.

## Granica transportu z capabilities prywatności wyjścia {#transport-boundary-with-outbound-privacy-capabilities}

`Whisper` nie powinien być właścicielem routingu onion ani topologii relayów.

Zamiast tego `whisper-signal` może przenosić intencję routingu, taką jak:

- żądana anonimowość,
- wymagana anonimowość,
- maksymalna liczba przeskoków,
- dopuszczalne klasy relayów.

Node realizuje tę intencję przez dostępne capability prywatności wyjścia.
`Orbiplex Anon` jest jednym z możliwych dostawców takiego capability, lecz
Whisper nie powinien potrzebować znajomości nazwy tego modułu.

Zachowanie v1 powinno obsługiwać co najmniej:

- `soft-fail`: preferowany routing anonimowy, lecz transport nieanonimowy może
  być użyty, jeśli polityka na to pozwala,
- `hard-fail`: wymagany routing anonimowy; nie wolno wysłać pogłoski, jeśli nie
  można spełnić żądanego poziomu ochrony.

Oddziela to znaczenie protokołu od realizacji transportu.

Planowanym miejscem integracji jest wybór transportu AD, nie nadawca należący
do Whisper. [S010 Anon](../60-solutions/010-anon/010-anon.md#ad-privacy-integration-planned-direction)
jest właścicielem zaleceń implementacyjnych i trackera `S010-001`–`S010-003`
dotyczących wymagań prywatności, limitów metadanych, odmowy trasy i akceptacji.
Istniejące dostarczanie Whisper przez AD/INAC nie dowodzi dostarczania anonimowego.
Wymagana anonimowość musi pozostać bramką przed wysłaniem przy ponowieniach
i fallbacku, także gdy żądany dostawca jest niedostępny.

Ostre osobiste zagrożenia wykryte przez lokalne Sensorium nadal powinny preferować
lokalny tryb pomocy lub ścieżkę pomocy ratunkowej. Whisper służy rozproszonym
wzorcom wartym korelacji, nie domyślnej pierwszej reakcji na prawdopodobne
zatrzymanie krążenia lub podobną zapaść.

Uzupełnienie doradcze: Proposal 077 (Swarm Broadcast Assistance) definiuje ścieżkę
pomocy, którą Whisper celowo nie jest – ograniczone, inicjowane przez użytkownika
rozgłoszenie prośby o pomoc – oraz, wraz z `doc/project/20-memos/whisper-corpus-composition.md`, sposób, w jaki pokój zrzeszenia
powstały dzięki Whisper może później zamówić zbiorową ekspertyzę.

## Kandydackie artefakty {#candidate-artifacts}

Prawdopodobna pierwsza rodzina kontraktów:

1. `whisper-signal.v1`
2. `whisper-trace.v1`
3. `whisper-interest.v1`
4. `whisper-threshold-reached.v1`
5. `association-room-proposal.v1`

`whisper-signal.v1` jest **schematem ciała treści** koperty rekordu Agory
(proposal 035) i tej samej koperty używanej w bezpośredniej wymianie między
węzłami (zob. "Dystrybucja i lokalne przechowywanie"). Ciało treści niesie
wyłącznie semantykę na poziomie pogłoski:

- `signal/polarity` (`problem` | `idea`),
- `epistemic/class`, `signal/text`, `topic/class`, `context/facets`,
- opcjonalne `signal/similarity-key` do deterministycznego smoke progu i jawnego
  dopasowania zdefiniowanego polityką,
- `confidence`, `disclosure/scope`, `signal/grade`, przypisanie źródła,
- intencję routingu (`routing/profile`, `routing/failure-mode`,
  `forwarding/max-hops`, ...).

Tożsamość i autoryzacja, które szkic sprzed uzgodnienia umieszczał wewnątrz ciała,
przechodzą do otaczającej koperty:

- `rumor/nym` → koperta `author/participant-id` jako `nym:did:key:...`,
- dołączony `nym-certificate` → koperta `author/nym-proof`, preferująca materiał
  certyfikatu inline, z opcjonalnymi referencjami do dłuższego rodowodu, audytu
  lub historii reputacji,
- podpis nymu nad ciałem → koperta `signature` nad pełnymi kanonicznymi bajtami
  koperty (Ed25519 kluczem nymu).

Dzięki temu `whisper-signal.v1` pozostaje małym przenośnym kształtem niezależnym
od tego, czy pogłoska podróżuje przez Agorę, czy bezpośrednio między węzłami;
domena podpisu nie zostaje rozdzielona między dwa artefakty.

`whisper-trace.v1` stosuje ten sam podział koperty. Ciało treści zawiera rodzaj
śladu, deklarowany przez autora czas zajścia, deskryptor artefaktu, tryb ujawnienia,
referencję zgody przy bajtach inline, opcjonalne referencje przyczynowe/dowodowe
oraz wymagania routingu. Tożsamość koperty, podpis, czas publikacji i routing tematu
pozostają poza ciałem. Ślady publiczne/federacyjne używają
`record/kind = "whisper-trace"`, `content/schema = "whisper-trace.v1"` i konwencjonalnego
prefiksu tematu `ai.orbiplex.whisper-traces/<trace-kind>`; ślady prywatne/bezpośrednie
korzystają z Artifact Delivery i INAC zamiast publicznego tematu Agory. Osobny
rodzaj rekordu jest celowy: projekcje Agory mogą wyłączyć oświadczenia śladu
z podobieństwa i progowania sygnałów społecznych bez analizy ciała treści.

`whisper-interest.v1` nie powinien powielać tego wzorca. Pozostaje deklaracją
lokalnego zainteresowania o zakresie węzła:

- zliczaną i ocenianą per uczestniczący węzeł,
- z `interested/node-id`, a nie autorem-uczestnikiem lub nymem,
- odpowiednią do koordynacji progu bez przekształcania lokalnej gotowości
  w pseudonimową tożsamość widoczną w transporcie.

Późniejsze dodatki mogą obejmować:

- `whisper-topic-interest.v1`
- `whisper-holder-availability.v1`
- `whisper-disclosure-request.v1`
- `whisper-disclosure-decision.v1`
- `whisper-forward.v1`

Przynajmniej jeden z wczesnych kontraktów powinien też zachowywać informację,
czy sygnał napisał bezpośrednio użytkownik, zaobserwował operator, czy przygotował
lokalny pomocnik taki jak `Monus`, aby dalsza polityka odróżniała pogłoski
użytkowników od pochodzących z monitoringu. Jeżeli Sensorium istotnie wpłynęło
na szkic przez `Monus`, to również powinno pozostać widoczne.

## Korzyści i koszty {#trade-offs}

1. Whisper zamiast ogólnej komunikacji:
   - Korzyść: czytelniejsza semantyka i bezpieczniejsza obsługa pogłosek.
   - Koszt: dodatkowa rodzina protokołów i cykl życia do utrzymania.
2. Lokalna redakcja i zgoda zamiast bezpośredniej publikacji:
   - Korzyść: silniejsza prywatność i mniejszy wyciek idiolektu.
   - Koszt: większy wysiłek przed publikacją.
3. Budżetowe kontrole antysybilowe zamiast semantycznej deduplikacji:
   - Korzyść: możliwe do wdrożenia teraz, łatwiejsze rozumowanie.
   - Koszt: przepuszczają część niemal identycznych pogłosek.
4. Osobny moduł `Anon` zamiast wbudowanego routingu onion:
   - Korzyść: czytelniejsze warstwy i szerszy re-use.
   - Koszt: polityka routingu staje się kontraktem między modułami.
5. Deterministyczna inicjacja zamiast centralnego koordynatora:
   - Korzyść: większa federacyjność i mniejsza monopolizacja.
   - Koszt: większa staranność przy projektowaniu progów i kworum.
6. Oświadczenia śladu zamiast receipts:
   - Korzyść: węzły tanio ujawniają pochodzenie adresowane treścią bez ujawniania
     treści ani wymagania pełnego receiptu workflowu.
   - Koszt: konsumenci muszą odróżniać podpisane twierdzenie od niezależnie
     zweryfikowanego dowodu.

## Rozstrzygnięte pytania {#resolved-questions}

1. Sygnały `idea` używają w v1 tej samej funkcji progowej co sygnały `problem`.
   Zapewnia to deterministyczny kontrakt progu i unika drugiej powierzchni polityki,
   zanim dowody produkcyjne wykażą potrzebę różnicowania.
2. Reguła progu M4 pozostaje bazą produkcyjną v1: dwa różne uprawnione węzły
   o tym samym `topic/class` i `signal/similarity-key` w ograniczonym oknie czasu.
   Ważenie poziomami zaufania i ograniczenia różnorodności źródeł są późniejszymi
   overlayami, nie wymaganiami v1.
3. Nymy pogłosek i pochodne nymy przekazywania są deterministyczne w kontekście
   pogłoski. Daje to stabilną korelację w obrębie jednego kontekstu bez globalnego
   wiązania między kontekstami.
4. `whisper-threshold-reached` zawiera tylko statystyki zagregowane. Ograniczone
   referencje świadków są pomijane w publicznym artefakcie progu dla minimalizacji
   ryzyka korelacji i ujawnienia.
5. Wrażliwe klasy pogłosek odmawiają rozgłaszania w trybie fail-closed, jeśli
   brak odpowiedniego capability prywatności wyjścia. Sama klasyfikacja i redakcja
   nie wystarczają tym klasom.
6. Whisper emituje artefakty progu i propozycji zrzeszenia. Cykl życia pokoju
   zrzeszenia, dołączanie, moderacja, zarządzanie transkrypcją/sprawą i późniejszy
   runtime pokoju należą do wyspecjalizowanej warstwy zrzeszeń/pokojów.
7. Werdykty kuracji wyraża `resource-opinion.v1` z `opinion/subject-kind: "rumor"`
   i polami `rumor-opinion.overlay.v1` (`rumor/credibility` w `1..5`;
   `rumor/rejection-reason` jako zamknięty enum). Nie wprowadza się nowego podtypu
   opinii. Domyślna polityka propagacji v1 tłumi po K niezależnych werdyktach spamu
   od zaufanych peerów; K i zakres zaufanych peerów są lokalnymi parametrami polityki.
8. Ślady artefaktów mają osobny kontrakt treści `whisper-trace.v1`, a nie trzecią
   `signal/polarity`. Są wyłączone z projekcji progów i zrzeszeń. Domyślny jest
   sam digest; treść inline wymaga walidacji `consent/ref` na hoście nadawcy,
   twardego limitu bajtów i sprawdzenia digestu/rozmiaru.

## Otwarte pytania {#open-questions}

Brak dla slice'a hard-MVP v1/M4. Przyszłe wdrożenia produkcyjne mogą ponownie
otworzyć ważenie progów, różnorodność źródeł, ujawnienie referencji świadków
oraz bogatszą politykę cyklu życia pokoju zrzeszenia jako pytania po MVP.

## Tracker ekspozycji ocen {#assessment-exposure-tracker}

| ID | Zadanie | Status | Zależności | Bramka ukończenia |
|---|---|---|---|---|
| P013-AE-001 | Powiązać kurację pogłosek ze wspólną lokalną bramką | partial | P026-005/006/007; P057-014 | Wykorzystać klucz podmiotu opinii, walidację overlayu i projekcję hosta dla kuracji, Agenta, wyszukiwania i ścieżek uwagi. Zachować fixture'y dowodzące braku wycieku ocen/liczników/kolejności innych osób przy działającym zwykłym dostarczaniu pogłosek, tłumieniu propagacji i pilnej ochronie. Bez nowego magazynu przeglądu pogłosek ani ukrywania tylko w kliencie; wspólne dowody trafiają do P026-008. Lokalny checkpoint P026 z 2026-10-24 dowodzi wstrzymywania i późniejszego renderowania pól rozszerzeń pogłosek we wspólnym widoku. Samodzielna admisja overlayu i pełna rzeczywista macierz kuracji/Agenta/uwagi/propagacji Whisper pozostają poza kwalifikacją; dowody M4 bez zmian. Przegląd run 01 ponownie kwalifikuje ograniczone pola pogłosek przez wspólny widok; zakres pełnego workflowu Whisper bez zmian. |
| P013-AE-002 | Opcjonalny profil zamkniętej rundy ocen pogłosek | todo | P026-010/011 | Wybrać dopuszczoną politykę rundy/otwierającego i wykorzystać cztery rodzaje Agory; przetestować brak ujawnienia, duplikaty, niepełną historię i niezależną propagację. Osobne od ukończenia lokalnej bramki i bez zależności alfy. |
| P013-AE-003 | Powiązać pogłoski z przyszłym klientem perspektyw zasobów | deferred | Istniejące kontrakty public-gossip/referencji i kuracji; P013-AE-001 dla wybranej powierzchni widza | Zaimplementować [wiązanie pogłoski](#resource-perspectives-client) względem kontraktu klienta P026; zachować rozróżnienia pogłoska/kuracja/zasób i osoba/rola/działanie, odpowiedzi, rewizje, pochodzenie i niepewność. Wykorzystać admisję/ekspozycję i istniejące API odczytu; fixture'y offline dowodzą braku wycieku chronionych referencji, niejawnego ujawnienia, podwójnego potwierdzenia i werdyktu o całej osobie. Dostarcza wejście P026-013 bez zależności od ukończenia jego UI; bez nowej zależności alfy. |

## Tracker publikacji pochodzenia webowego {#web-origin-publication-tracker}

P084 jest właścicielem pieczy nad oryginałem i jej bramki offline; P078 – przekazania
przeglądu/szkicu; P013 – publicznego kontraktu pochodzenia i zachowania go w publikacji.
Istniejące ukończone bazy pozostają ograniczone do swoich historycznych dowodów.

| ID | Zadanie | Status | Zależności | Bramka akceptacji |
|---|---|---|---|---|
| P013-WEB-001 | Zamrozić wspólne podsumowanie pochodzenia i granicę publikacji/pieczy | todo | Istniejące kontrakty publikacji P013, ustalenia/przeglądu P078 i snapshotu P084 | Zamrozić ograniczone wspólne słowniki, wersjonowanie/migrację zamkniętych schematów, niezmienioną tożsamość źródła P015, pola lokalne/prywatne wobec publikowalnych i dokładne wiązania podpisu/przeglądu. Objąć przypadki unknown, mixed i media-monitoring; bez automatycznej wagi wiarygodności, publicznego surowego digestu ani twierdzenia, że podpis dowodzi pochodzenia. Schematy kanoniczne, lustra Node i konsumenci zmieniają się dopiero podczas implementacji. |
| P013-WEB-002 | Zachować przejrzane pochodzenie przez podpisaną publikację i widoki odbiorców | todo | P013-WEB-001; P078-015/016; P084-015 | Wykorzystać przygotowaną publikację, Schema Gate, signer, istniejące nośniki Agora/INAC i projekcje UI. Akceptacja offline ścieżki właściciela dowodzi zachowania szkic→sygnał→public-gossip, odmowy po zmianie pochodzenia lub wygaśnięciu/braku pieczy przed admisją, wyświetlania unknown dla starszych danych, odtworzenia zacommitowanej publikacji po wygaśnięciu bez przepisania, braku wycieków surowych danych/URL-i/digestów i niejawnego pobierania. Kopie/streszczenia nie uzyskują twierdzenia o niezależnym potwierdzeniu; pilna ochrona pozostaje operacyjna. Przy zamknięciu zaktualizować solutions właścicieli, ledger Node i zachowany zakres akceptacji. |

## Następne działania {#next-actions}

1. Utrzymywać synchronizację schematów v1 `whisper-signal`, `whisper-interest`,
   `whisper-threshold-reached` i `association-room-proposal` z bramką schematów implementacji.
2. Dodać jeden komponent solution skierowany do implementacji `Whisper`.
3. Dodać jeden komponent solution dla dostawcy prywatności wyjścia, takiego jak `Anon`.
4. Zdefiniować lokalny kontrakt usługi Node dla redakcji wspieranej przez
   Inquirium/model i workflowów zgody użytkownika.
5. Wrócić do produkcyjnej polityki progów i reguł nymów pochodnych po wykazaniu
   przez M4 deterministycznej reguły smoke dwóch węzłów.
6. Rozstrzygnąć, czy przyszły lokalny moduł taki jak `Orbiplex Monus` powinien
   móc przygotowywać półautomatyczne lub automatyczne szkice Whisper na podstawie
   lokalnych sygnałów ważonych dobrostanem.
7. Zachować `whisper-signal.v1.schema.json` jako schemat wyłącznie ciała treści
   (z `signal/id`, `created-at`, `rumor/nym`, `auth/nym-signature`
   i `author/nym-proof` w otaczającej kopercie `agora-record.v1`, zgodnie z sekcją
   dystrybucji), analogicznie do kształtu samego ciała zastosowanego już do
   `resource-opinion.v1.schema.json` w proposalu 026.
8. Zarejestrować `whisper` jako rozpoznawany `record/kind` i `whisper-signal.v1`
   jako rozpoznawany `content/schema` w referencyjnym relayu Agory;
   zarejestrować `ai.orbiplex.whispers/<topic-class>` jako konwencjonalny prefiks
   klucza tematu publicznego/federacyjnego, a `private/<name>` zarezerwować dla
   artefaktów wyłącznie bezpośrednich INAC poza Agorą.
9. W [P013-PEX-001](#private-exchange-tracker) użyć istniejącego AD/INAC
   z zadeklarowaną prywatnością wyjścia i admisją odbiorcy/roli. Memarium jest
   jedynym trwałym magazynem chronionych rekordów Whisper po obu stronach.
   Typowane wymiany spraw są utrwalane u właścicieli domenowych (autorytet LLR-008
   i workflow S026), z zachowaniem dokładnych przygotowanych bajtów wraz z decyzją.
   PEX nie ma trwałego magazynu; AD odpowiada za pieczę transportową i ponowienia.
   Zob. [kontrakt uporządkowania spraw](013-whisper-social-signal-exchange/case-authority.md).
10. Podłączyć kurację pogłosek za pośrednictwem operatora (§Kuracja pogłosek za
    pośrednictwem operatora) do skrzynki Whisper w Node UI: działania per pogłoska
    dla `rumor/credibility` (1..5), `rumor/rejection-reason: spam`
    i `rumor/rejection-reason: policy-violation`; każde emituje
    `resource-opinion.v1` z `opinion/subject-kind: "rumor"` kierowane do
    `record/id` pogłoski, utrwalane jako fakt Memarium i kierowane zwykłą ścieżką
    publikacji opinii węzła. Polityka propagacji wyjściowej konsumuje lokalne
    werdykty jako wejścia tłumienia (dowolne obecne `rumor/rejection-reason` →
    brak rozgłaszania, brak redystrybucji przez posiadacza, wyłączenie ze zliczania progu).
11. Opublikować `rumor-opinion.overlay.v1.schema.json` jako samodzielny overlay
    walidujący przestrzeń `rumor/*` (`rumor/credibility`, `rumor/rejection-reason`)
    i dodać parę przykładów w `doc/schemas/examples/`: werdykt samej wiarygodności
    (bez tekstu, `rumor/credibility: 2`) oraz werdykt spamu
    (`rumor/rejection-reason: "spam"` z krótkim uzasadnieniem w `opinion/text`).
12. Dodać ograniczoną ścieżkę tworzenia `whisper-trace.v1`, która waliduje zgodę
    przed `digest-and-content`, sprawdza dokładne bajty inline względem digestu
    i rozmiaru, podpisuje zwykłą kopertę i kieruje ją przez Agorę lub AD/INAC
    zgodnie z zakresem ujawnienia. Wykluczyć ślady z progowania sygnałów społecznych.
    Kolejność implementacji: czysta walidacja dekodowania/digestu/rozmiaru;
    rozwiązywanie zgody na hoście nadawcy; admisja kind/schema i ujawnienia Agory;
    prywatna akceptacja AD/INAC; tworzenie i inspekcja operatora/użytkownika;
    testy smoke nośników. Żadna faza nie wprowadza transportu swoistego dla śladu.

    **Ukończono 2026-07-13.** Referencyjny runtime implementuje czyste reguły
    integralności/prywatności, dokładne wiązanie zgody hosta nadawcy dla ujawnienia
    inline, ścisłe wejście Agory i projekcję wyłącznie metadanych, prywatną akceptację
    AD/INAC, ograniczone UI tworzenia/inspekcji oraz smoke nośników Story-005
    obejmujący ślady publiczne i prywatne. Runtime nie przechowuje treści inline
    śladów w modelach odczytu śladów Whisper ani Agory. Atomowo rezerwuje również
    klucze idempotencji, odrzuca współbieżne duplikaty skutków ubocznych, ogranicza
    pełny JSON śladu i rozszerzenia niezależnie od limitu 32 KiB artefaktu inline,
    domyślnie przycina lokalny model odczytu metadanych po 30 dniach i w smoke
    potwierdza użycie zadeklarowanych nośników Agora i INAC przez ślady publiczne
    i prywatne bez wycieku prywatnej projekcji.

## Zalecenia implementacyjne: współdzielone mechanizmy {#implementation-reuse}

Doprecyzowanie projektu, 2026-10-28. Reguły abstrakcji danych do ponownego użycia
oraz retrospektywnej konwergencji z `node:DEV-GUIDELINES.md` dotyczą łącznie
kontynuacji kontekstowej, DFR, ADC, CIM i LLR. Poniższe decyzje wykorzystują
sprawdzone prymitywy Node lub konsolidują dwóch nazwanych konsumentów projektu.
Nie twierdzą, że kontynuacje są zaimplementowane, ani nie otwierają ponownie
historycznych dowodów M4.

Celem jest mały słownik z wieloma operacjami. Czyste reguły Whisper pozostają
w `whisper-core`, weryfikacja nymów w `nym-core`, a efekty w istniejącym hostowanym
komponencie/adapterach. Wspólna funkcja lub mały moduł wewnętrzny jest lepszy niż
nowy crate albo uniwersalna hierarchia rekordów. Kierunek zależności musi być
poprawny; czysty właściciel nie może importować usługi wystawcy, bazy, transportu
ani UI tylko po to, by uzyskać helper.

### Rozstrzygnięcia re-use {#reuse-dispositions}

| Wspólny mechanizm i dowód | Abstrakcja odbiorcza i zachowana granica | Konsumenci i właściciel ukończenia |
|---|---|---|
| `node:canonical-json/src/lib.rs`, `node:crypto/src/lib.rs` i istniejące funkcje podpisu per użycie w `node:nym-core/src/lib.rs` | Kanoniczne bajty i ścisła weryfikacja podpisu, z zamkniętym wrapperem preimage/użycia podpisu per artefakt. Zachować dokładną domenę, pomijane pola podpisu, rolę klucza i limity bajtów; poprawność kryptograficzna nie dodaje uprawnień. | P015-004/005 i ADC-001/004: wykorzystać prymitywy i wspólny zestaw fixture'ów praw bajtowych; zachować admisję właściwą celowi. |
| `nym-core::PublicationTimeVerifier`, `PublicationAnchor` i `SignalBinding`; czysty ewaluator admisji P035 | Port czasu pozostaje wąskim wiązaniem rekord/bajty autora/czas. Projektuje się do niego zweryfikowany pełny token admisji; sam dowód czasu Matrix daje `insufficient-claim` dla LLR-002. P035 jest właścicielem osobnych tokenów pełnych i odłączonych, niezależnego lokalnego zaufania i historii względem snapshotu. | P035-019 i pierwszy konsument LLR-002: inspekcja Agory tylko do odczytu. ADC-004 i Memarium zachowują własne bramki runtime'u. Nigdy nie fabrykować wiązania pełnego sygnału z publicznego manifestu. |
| Międzyartefaktowy kontrakt weryfikacji P032; istniejący konsumenci dowodów inline i kwalifikowany nośnik P076 jako przykłady | Ograniczone dokładne dowody, niezależne lokalne zaufanie, osobne wyniki historyczne/bieżące i akceptacja bez pobierania. Wspólne operacje są poniżej adapterów rodzin; autorytet i świeżość sprawy pozostają własnością Whisper. | [Macierz profili Whisper](#portable-verification-profiles) dotyczy sygnałów, embarga i artefaktów sprawy. LLR-009 składa P015-004, P035-019 i LLR-008; ADC-005 jest drugim konsumentem pakietu dowodowego. Bez ujawnienia prywatnego ciała i rozszerzenia zakresu P076-038. |
| Kwalifikowalność kontekstowa P015 i dwóch konsumentów liczników źródeł P013 | Jeden ograniczony widok wkładów per kontekst/epoka, a potem osobne decyzje koordynacji i ujawnienia. Zachować tożsamość i dowody źródła; zredukować powtarzane kopie do jednego uprawnionego źródła. Redukcja nie daje twierdzenia o prawdzie, tożsamości między epokami ani zgody. | P015 Gate B i ADC-004: jeden ewaluator wkładów, osobny zatrzask emisji i polityka commitu uwolnienia; [szczegóły zliczania](013-whisper-social-signal-exchange/author-disclosure-conditions.md#implementation-recommendations). |
| Porównanie zakresu/rewizji/digestu w `node:nym-core/src/status.rs` (`StatusCursor::advance`) i reguła najwyższego statusu sprawy LLR | Małe czyste porównanie uwierzytelnionego czoła, używane przez dwa kursory domenowe. Zachować prawa zakresu, równości, cofnięcia i ekwiwokacji; skumulowane odwołania, ciągłość łańcucha, świeżość i skutki terminalne pozostawić właścicielom. | LLR-008 wydziela tylko to porównanie, dodając drugiego konsumenta i zachowując wektory regresji P015; [szczegóły sprawy](013-whisper-social-signal-exchange/long-lived-rumors.md#implementation-recommendations). |
| Sukcesja/kontrola sprawy LLR oraz poprawki, potwierdzenia i commity uwolnienia ADC | Jeden nagłówek żądania sprawy, rekord przyjęcia, fold i transakcyjny właściciel przyjęcia. Typowane ciała operacji zachowują różnych podpisujących i warunki wstępne. Wspólna rewizja porządkuje efekty, nie uprawnia do nich. | LLR-008 odpowiada za kolejność i replay; ADC-005 wnosi przejście uwolnienia do tego właściciela, nie drugi magazyn stanu. |
| Plany potrzeb/wabików DFR i zaakceptowane żądania osłony CIM | Jedna lokalna abstrakcja wpisu planu i jeden wykonywalny kształt zadania bucketu. Lokalne przyczyny wspierają planowanie, lecz są odrzucane na granicy sieci; pozostaje tylko zgrubny temat/okno. | DFR-002 jest właścicielem wykonawcy; CIM-001/003 dodają przez niego wejścia i harmonogram; [szczegóły planu](013-whisper-social-signal-exchange/cooperative-interest-masking.md#implementation-recommendations). |
| `node:nym-issuer-service/src/prepared_exchange.rs` (`PreparedPhase`, `prepare`) oraz `InboundArtifactAcceptor` AD | Bezpośrednio wykorzystać acceptor/runtime AD. Użyć prawa przygotowanego wyjścia: dokładna tożsamość wejścia wiąże jedną zachowaną sekwencję bajtów przed przekazaniem. Sam `PreparedPhase` jest właściwy rodzinie wystawiania, nie jest ogólnym nośnikiem Whisper. | PEX-001 i ADC-005 wykorzystują prawo i fixture'y recovery. Rozważyć wydzielenie wyłącznie mechaniki magazynu, gdy istnieją oba konkretne adaptery; bez kopiowania polityki pieczy kluczy wystawcy i drugiego właściciela ponowień. |

PEX-001 zaczyna też od `artifact_delivery_envelope_for_private_record`
i `admit_private_agora_record` w `node:whisper-intake/src/lib.rs` oraz istniejącego
wywołania acceptora AD przez hosta. To konkretne szwy obecnych rodzin prywatnych
sygnałów/śladów, nie admisja payloadów embarga v2, spraw ani osłony. Rozszerzaj
adaptery rodzin i fixture'y odmów za tą granicą; zachowaj zachowanie starszych
rodzin i nie kieruj dowolnych nowych komunikatów przez liberalny parser starego sygnału.

Ostatni wiersz celowo zachowuje odrębne rekordy domenowe. Checkpoint wydzielenia
to implementacja PEX-001/ADC-005: albo współdzielić z oboma adapterami prymityw
pożyczający transakcję, albo zapisać konkretny kontrakt/koszt uzasadniający separację.
`RevisionStore` wystawcy wiąże też dziennik SQL z niezależnym fencingiem dostawcy
kluczy; to precedens recovery, nie gotowa baza spraw. Rewizja bazy, podpisana
rewizja statusu źródła i rewizja sprawy są różnymi licznikami.

### Profile przenośnej weryfikacji {#portable-verification-profiles}

Właścicielem ogólnej reguły jest
[wspólny kontrakt weryfikacji P032](032-key-delegation-passports.md#shared-verification-operations),
przywoływany też przez S014 i `node:DEV-GUIDELINES.md`. Whisper stosuje go do każdej
podpisanej rodziny, nie tylko sukcesji. Słownikiem pozostają istniejące klucze
publiczne, certyfikaty nymów, dowody delegacji i receipts. Preferuj adapter rodziny
zamiast nowego wrappera dla każdego artefaktu; wykorzystuj obejmujący dopuszczony
pakiet, jeśli już przenosi dokładnie wymagane dowody w tym samym audytorium.

| Rodzina / właściciel ukończenia | Minimalny przenośny materiał weryfikacyjny | Odrębne twierdzenie |
|---|---|---|
| Sygnały kontekstowe i powiadomienia korelacyjne (P015-001/005, P013-ADC-007) | Istniejący materiał autorstwa/certyfikatu nymu z dozwoloną krotką użycia publikacji; materiał weryfikacyjny rady pod lokalną admisją. Przy twierdzeniu o historycznej ważności dołączyć istniejący dowód admisji P035. | Poprawna publikacja nymu nie czyni treści prawdziwą ani nie liczy jej jako bieżącego odrębnego źródła. Prywatnego sygnału nie wolno dołączać do publicznego notice. |
| Manifesty embarga i uwolnione rekordy (P013-ADC-001/004/005, P035-019) | Manifest podpisany nymem i dowód certyfikatu/użycia, podpisane wiązanie admisji, zatwierdzony payload uwolnienia, poświadczenie licznika i przyjęty commit uwolnienia; publiczne dowody podpisującego/delegacji wyłącznie w zakresie profilu artefaktu. | Dopuszczony licznik poświadcza ukryte wejścia; odbiorca nie weryfikuje samodzielnie prywatnego ciała. Historyczna ważność commitu jest odrębna od dzisiejszego statusu sprawy i dostarczenia AD. |
| Żądania kontroli sprawy i przyjęte zdarzenia (P013-LLR-006/008) | Publiczny klucz ciągłości ze zweryfikowanym wiązaniem pierwotnej kotwicy; własne podpisane bajty każdego żądania. Przyjęte zdarzenia niosą dodatkowo dokładne przyjęcie autorytetu związane z żądaniem oraz dozwolone publiczne dowody podpisującego. | Poprawny podpis polecenia nie jest uporządkowanym przyjęciem. Właściciel sprawy nadal sprawdza stan bieżący i warunki właściwe operacji; przenośny dowód nigdy nie commituje przejścia. |
| Sukcesja sprawy (P013-LLR-007/009, P015-004) | Ograniczona [prezentacja sukcesji](013-whisper-social-signal-exchange/long-lived-rumors.md#portable-case-succession-verification): wiązanie kotwicy, oba podpisy, certyfikat/dowód źródła następcy, dokładne przyjęcie i świeży status sprawy. | Historyczne autorstwo, autentyczna sukcesja i bieżący autorytet sprawy to niezależne wyniki. Nie wynika z nich scalenie tożsamości źródła ani transfer reputacji. |
| Współpracujące żądania osłony (P013-CIM-001) | Istniejące dowody uwierzytelnionej prywatnej wymiany/sesji; żądanie pozostaje niepodpisane w warstwie aplikacji/nymu. | Ogólna preferencja przenośnych podpisów nie wymaga dodawania publicznego podpisu ani trwałego powiązania tożsamości do żądania celowo uwierzytelnianego sesją. |

Zamroź limity bajtów/elementów/głębokości/pracy, obsługiwane postacie dowodów,
regułę ujawnienia i typowane wyniki braku/nieświeżości każdej nowej rodziny
w zadaniu właściciela kontraktu. Bajty sieciowe i kwalifikacje M4 pozostają bez
zmian. Te same czyste operacje mogą obsługiwać różne reprezentacje: dokładne
lokalne rozwiązywanie, rozliczanie budżetu, kanoniczne sprawdzanie podpisu
i porównanie zweryfikowanych wiązań. Przed powieleniem ich w ADC i LLR użyj
checkpointu konwergencji P032 i zachowaj wspólne fixture'y praw. Bieżący autorytet,
zliczanie, polityka świeżości, zachowana wiedza negatywna i uprawnienie ujawnienia
pozostają decyzjami domenowymi.

`ScopedClaimSuiteVerifier` P081 jest właściwy, gdy wywołujący rzeczywiście żąda
jego predykatów związanych z żądaniem/nonce. Nie jest ogólnym weryfikatorem dowolnych
zapisanych podpisów; sukcesja nie staje się niejawnie nowym scoped claim.
Testy P076 są użytecznym precedensem braku pobierania, podobnie jak weryfikatory
nymów inline i delegacji Agory. Żaden nie wymaga zależności od Messagingu.

### Małe operacje, jawne dowody {#small-operations-explicit-evidence}

Sugerowane operacje wewnętrzne to `verify_publication_evidence`,
`evaluate_epoch_sources`, `evaluate_disclosure_condition`, `fold_case_event`
i `compile_pull_jobs`. Są to nazwy projektowe, nie deklaracje istniejącego API.
Używaj zwykłych funkcji nad zwalidowanymi wartościami/iteratorami; wprowadzaj trait
wyłącznie tam, gdzie rzeczywiste reprezentacje potrzebują tych samych operacji,
jak przy dowodach czasu publikacji. Nadaj identyfikatorom odrębne typy tam, gdzie
pomylenie sprawy, warunku, audytorium, żądania lub dostarczenia narusza kontrakt.
Nie modeluj wszystkich artefaktów jedną mapą z opcjonalnymi polami autorytetu.

Schema Gate pozostaje na granicach sieciowych/middleware. Czyste operacje otrzymują
jawny czas ewaluacji, dopuszczoną politykę i zweryfikowane dowody; nie pobierają
brakujących dowodów ani nie czytają zegara. Wyniki wiążą ocenione wejścia
i rozróżniają odmowę, niedostateczny dowód oraz spełniony predykat. Spełniony
predykat nie jest autoryzowanym efektem zewnętrznym. Właściciele ponownie sprawdzają
czas i właściwe rewizje w określonym punkcie commitu efektu.

Nie konsoliduj tych pozornych podobieństw:

- `WhisperContributor.node_id` M4 i kontekstowe `source/ref`: różne jednostki
  zliczania. Wykorzystuj operacje na kolekcjach, nigdy nie podstawiaj jednej
  tożsamości za drugą ani nie reinterpretuj zachowanych identyfikatorów progów.
- Pełny prywatny dowód publikacji i odłączony publiczny receipt: drugi ufa
  dopuszczonemu autorytetowi co do ukrytej treści. Nie może deklarować niezależnej
  weryfikacji podpisu tej treści.
- Ważność certyfikatu, epoka zliczania, retencja, termin zgody i termin przekazania
  AD: współdziel arytmetykę czasu, zachowaj osobne pola polityki.
- Status nymu/źródła, status sprawy i status dostarczenia AD: niezależne domeny
  autorytetu i recovery. Nowszy status lub receipt dostarczenia nie jest zgodą.
- Zamknięte wystawianie P015 i żądania osłony CIM: pierwsze używa podpisanych
  prywatnych wymian, drugie celowo unika przenoszalnego podpisu aplikacyjnego.
  Re-use AD nie może niejawnie dodać takiego podpisu ani rozszerzyć domeny kryptograficznej wystawiania.

### Bramka konwergencji kamienia milowego {#milestone-convergence-gate}

Przed zamknięciem P015-004, DFR-000, ADC-000, CIM-000 lub LLR-000 porównaj
wdrożone funkcje i abstrakcje danych z tą tabelą i istniejącymi odpowiednikami.
Zapisz konsolidację, celową różnicę lub odłożone wydzielenie z właścicielem
w dowodach kamienia milowego. Uruchom wspólne fixture'y praw dla każdego adaptera,
w tym zły zakres/cel, zmienione bajty pod jednym id, replay po restarcie i brak
materiału. Fixture'y odmów domenowych pozostają obowiązkowe. To kontrola zamknięcia
implementacji, nie dodatkowa usługa runtime'u ani zależność alfy od kontynuacji po MVP.

## Tracker prywatnej wymiany {#private-exchange-tracker}

Proponowana integracja nośnika; bez nowego transportu. Zadanie czyni wykonalnym
punkt 9 następnych działań. Profile aplikacyjne odpowiadają za payload/pieczę/autorytet;
wykorzystaj S023 AD, S017 INAC, Schema Gate i szyfrowaną wymianę P015 związaną
z odbiorcą. Sukces transportu nigdy nie oznacza przyjęcia sprawy, admisji źródła
ani zgody na ujawnienie.

| ID | Zadanie | Status | Zależności | Bramka ukończenia |
|---|---|---|---|---|
| P013-PEX-001 | Prywatna wymiana Whisper związana z odbiorcą | done | Kontrakty admisji S023/S017; wiązanie prywatnej wymiany P015 | Dowody AD/INAC z dwóch węzłów dla chronionych sygnałów i ograniczonych profili żądanie/odpowiedź, nazwanej admisji odbiorcy/roli, replay, restartu, utraconej odpowiedzi i wygaśnięcia. Użyć jednej ścieżki nośnika/acceptora; szyfrować przed pieczą AD. Odmowa przy złym odbiorcy lub zakresie; logi, powiadomienia, zapytania relaya i fallbacki nie ujawniają chronionego tekstu ani trasy autora. Bez publicznego fallbacku, nowego listenera i drugiego właściciela ponowień. Użyć istniejącego szwu wywołania AD Whisper Intake z zamkniętymi adapterami rodzin; zachować testy odmów starszych prywatnych sygnałów/śladów i związać zapisane bajty z dokładną tożsamością żądania przed przekazaniem. |
| P013-PEX-002 | Żywotność AD przy współbieżnej obserwacji statusu | todo | P013-PEX-001 | Odtworzyć zachowany odłączony timeout przy rytmie obserwatora 40 ms i aktywnym oczekiwaniu 15 ms, obok kwalifikowanego rytmu 200 ms. Instrumentować admisję kolejki, każdy skok AD/INAC, pieczę/ponowienie i odbiór domenowy ograniczonymi etykietami faz/czasu, bez principals ani identyfikatorów spraw. Rozdzielić hipotezy harmonogramu CPU, oczekiwania na blokadę właściciela i SQLite/WAL; raportować pomiary zamiast wybierać przyczynę z samego czasu. Zadeklarować skończony budżet żywotności end-to-end przy odczytach współbieżnych, sprawdzić timeout/anulowanie i zachować odmowne runy. Przegląd zamknięcia odtworzył też przekroczenie terminu wyniku przy odpytywaniu co 200 ms po trwałym zamknięciu rewizji 3: bezczynne odczyty WSS utrzymywały timeout połączenia i opóźniały pracę wyjściową. Poprawiony budżet odczytu workera i regresja skupiona nie ustalają same przyczyny wcześniejszej odmowy 40 ms ani nie zamykają tej bramki obciążenia. Kontynuacja nie rozszerza niejawnie istniejącej lokalnej kwalifikacji transportu. |

## Kontekstowe autorstwo źródła-uczestnika (2026-10-25) {#contextual-participant-source-authorship-2026-10-25}

Przyjęty [profil kontekstowy P015](015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)
wprowadza sygnały v2 oraz zagregowane artefakty progu/propozycji. Liczy dopuszczone
przez radę źródła-uczestników w jednym kontekście pogłoski i epoce, bez fallbacku
do węzła źródłowego, ciągu autora ani record/about. To nowa kwalifikacja;
historyczne wyniki M4 liczące węzły pozostają bez zmian. Dnia 2026-11-04 ograniczone
Gate A fazy 1 (certyfikacja) i Gate B (zwykły host oraz autorstwo UI na
SQLite/dopuszczonym Synapse) przechodzą A30/30, B31/31 i sześć osobnych zobowiązań
zgodności C, z identycznymi odczytami loose/extracted/fresh z dwóch magazynów.
Kompozycję właściwą źródłu i pieczę wyłącznie operatora zapisano w `node:docs/evidence/matrix-opaque-envelope/2026-11-04-whisper-authorship/README.md`.
Opcjonalne stay-ready, LLR/ADC, Anon, pełny Whisper i gotowość wydania są osobne.

## Rezonans uśpionych faktów (2026-10-27) {#dormant-fact-resonance-2026-10-27}

Status: proponowana funkcja po MVP; bez deklaracji runtime'u. Ta sekcja jest
właścicielem funkcji i zadania zbiorczego `P013-DFR-000`. Zadania mechanizmów
pozostają w dokumentach ich właścicieli. Scenariuszem akceptacyjnym jest
[Story 014](../30-stories/story-014-dormant-contest-entry.md).

### Podsumowanie {#summary}

Ludzie zapisują zwykłe fakty bez napięcia społecznego, np. "wysłałem wiersz na
konkurs". Taki fakt nie jest pogłoską ani opinią. Może później nabrać znaczenia
społecznego, gdy inni opublikują pogłoskę, którą on potwierdza. Rezonans uśpionych
faktów pozwala węzłowi odkryć powiązanie bez publikowania faktu ani zapytania
wyprowadzonego z jego szczegółów:

1. fakt pozostaje neutralnym osobistym rekordem w Memarium;
2. lokalne zadanie uogólnia go do terminów zamkniętego słownika dekorelacji;
3. raz na epokę węzeł pobiera kompletne zgrubne buckety tematyczne z relayów pogłosek;
4. węzeł lokalnie ocenia pobrane pogłoski względem pełnego prywatnego faktu;
5. uczestnik rozstrzyga, czy pogłoska dotyczy faktu, a wszelkie ujawnienie używa
   istniejących ścieżek Whisper.

Zasada przewodnia: przynoś wspólne pytania do prywatnej pamięci, zamiast wysyłać
prywatną pamięć jako pytania.

### Kontekst i problem {#context-and-problem}

- **Fakt.** Memarium już może przechowywać takie rekordy, ale fakty osobiste nie
  mają horyzontu czasowego per fakt
  ([P036](036-memarium.md#fact-retention-horizons-and-personal-records-2026-10-27)),
  a nic nie wiąże późniejszej pogłoski z wcześniejszym rekordem.
- **Wniosek.** Publikowanie każdego faktu jako pogłoski dodaje szum i ujawnia
  osobistą historię. Dostarczanie push wymaga, by sieć wiedziała, kto jest
  zainteresowany. Zapytania z dowolnych słów kluczowych rzadkiego faktu są
  fingerprintami, a digesty pól o małej entropii, takich jak instytucja i data,
  można odwrócić słownikowo, co S022 odnotowuje już dla danych pochodnych.
- **Tło, niezweryfikowane w tym repozytorium.** Wzorzec przypomina information
  escrow (Ayres i Unkovic, 2012) oraz dopasowanie w stylu Callisto,
  w którym prywatnie przechowywane zgłoszenie nabiera znaczenia, gdy pasuje do
  niego niezależne zgłoszenie. Pobieranie kluczy powiadomień o ekspozycji oraz
  filtry bloków po stronie klienta z BIP157/158 ilustrują, że najbezpieczniejszym
  zapytaniem jest pobranie publicznych danych i dopasowanie ich lokalnie.

### Model {#model}

| Warstwa | Właściciel | Rozdzielczość | Treść | Co opuszcza węzeł |
|---|---|---|---|---|
| 0. Rekord osobisty | Memarium ([P036-007](036-memarium.md#fact-retention-horizons-and-personal-records-2026-10-27)) | pełna | rodzaj, kontrahent, czasy, tytuł, załączniki, horyzont retencji | nic przez tę funkcję |
| 1. Profil zainteresowań | Harvester ([P078-011](078-weak-signal-harvester.md#memarium-dormant-fact-profile-2026-10-27)) | zgrubna | identyfikatory terminów słownika wyprowadzone z bieżących rekordów | nic |
| 2. Plan pobierania | Whisper (`P013-DFR-002`) | koszyk | rzeczywiste terminy, atrapy, okna i budżet bajtów na epokę | identyfikatory terminów, okien i kursory |
| 3. Lokalne dopasowanie | Harvester ([P078-012](078-weak-signal-harvester.md#memarium-dormant-fact-profile-2026-10-27)) | pełna | wyniki punktowe, wyjaśnienia, ustalenia kandydujące do powiązania | nic |
| 4. Decyzja | Memarium i powiadomienia ([P036-008](036-memarium.md#fact-retention-horizons-and-personal-records-2026-10-27), [P057-015](057-user-and-operator-notifications.md#tracking)) | pełna | potwierdzone, odrzucone albo odroczone powiązanie | nic |
| 5. Ujawnienie | Whisper ze Story 005, P015 i P070 | wybrana przez uczestnika | powiązana pogłoska, zainteresowanie, udział w pokoju | tylko po jawnym działaniu |

#### Słownik dekorelacji {#decorrelation-vocabulary}

Whisper jest właścicielem semantyki `topic/class`; słownik ujawnia jej zgrubny,
współdzielony podzbiór. `whisper-decorrelation-vocabulary.v1`
(`P013-DFR-001`) jest dokumentem JSON walidowanym przez JSON Schema,
wersjonowanym i opatrywanym digestem postaci JCS. JSON odpowiada plikom
konfiguracji P091, bramce schematów i istniejącym kanonicznym digestom. Jest to
[ustawienie P091](091-file-backed-configuration-and-explainable-composition.md#p013-decorrelation-vocabulary-consumer)
o zakresie węzła:

- **Źródło fabryczne.** Dystrybucja Node dostarcza wersjonowany słownik jako
  fabryczne źródło ustawienia. Aktualizacja zastępuje to źródło, nigdy warstwy
  lokalne.
- **Warstwy lokalne.** Operatorzy i zaawansowani użytkownicy przeciążają je
  przez zwykłe warstwy P091. Słownik jest identyfikowaną kolekcją indeksowaną
  identyfikatorem terminu, składaną według kluczy. Warstwa może dodawać terminy,
  zmieniać etykiety, aliasy lub rodziców oraz wycofać termin przez jawne
  `term/status` równe `retired`, ponieważ `null` niczego nie usuwa. Może też
  zadeklarować pustą bazę, by zbudować całkowicie własny słownik. Każda warstwa
  wskazuje wersję fabryczną, względem której ją napisano. Po aktualizacji
  przeciążenia terminów, które zniknęły, dają typowaną diagnostykę zamiast
  cichego pominięcia.
- **Stabilne powiązania.** Warstwa lokalna nie może zmienić klucza tematu
  istniejącego identyfikatora terminu; następuje odmowa i trzeba użyć nowego
  identyfikatora. Lokalne identyfikatory mają prefiks lokalnej przestrzeni nazw,
  np. `local.`, aby późniejszy termin fabryczny nie mógł z nimi kolidować.
- **Zastosowanie.** Zmienione rozstrzygnięcie konfiguracji stosuje się od
  następnej granicy epoki, a plan pobierania zapisuje użyte `resolution/id`.
  Niedostępność rozstrzygnięcia zatrzymuje planowanie zamiast powodować powrót
  do nieaktualnej kopii.

Każdy termin ma identyfikator, etykiety, aliasy, opcjonalnego rodzica, klucz tematu
Agory pod prefiksem `ai.orbiplex.whispers/` (P046) oraz pochodzenie (`factory`
lub `local`; warstwa dostarczana przez federację może pojawić się później).
Terminy fabryczne niosą też zgrubną wskazówkę o liczebności populacji i flagę
spełnienia minimum liczebności dla planów pobierania.

Dostosowywanie ma konsekwencje dla prywatności, które kontrakt wyraża jawnie:

- Rozstrzygnięty słownik, jego wersja i digest pozostają lokalne. Nigdy nie
  trafiają do żądań pobierania ani rekordów pogłosek, ponieważ digest
  dostosowanego słownika byłby fingerprintem. Pogłoski niosą tylko identyfikator
  terminu w `topic/class`.
- Terminy lokalne nie mają zaufanej wskazówki o populacji, więc są nieocenione.
  Plany pobierania wykluczają je, chyba że operator jawnie je dopuści po
  ostrzeżeniu, że takie pobrania mogą identyfikować węzeł. W trybie pobierania
  wszystkiego ograniczenie nie ma znaczenia.
- Atrapy losuje się wyłącznie spośród ocenionych terminów.
- Przy autorstwie z użyciem lokalnego terminu pojawia się ostrzeżenie, że
  czytelnicy korzystający ze słownika fabrycznego nie pobiorą tego koszyka.

To samo rozstrzygnięcie służy obu stronom:

- Autorzy oznaczają `topic/class` pogłoski jednym terminem, a szczegóły
  pozostawiają w `signal/text`, `context/facets` i `signal/similarity-key`.
  Ciężar szczegółowości spoczywa na pogłosce, nie na jej czytelnikach.
- Czytelnicy wybierają wyłącznie identyfikatory terminów. Lokalny model może
  pomóc je wybrać, ale nigdy nie emituje zapytań tekstowych. Termin poniżej
  minimum zastępuje się jego rodzicem.

#### Plan pobierania i koszyki {#pull-plan-and-buckets}

Plan pobierania (`P013-DFR-002`) jest przeliczany na granicach epok, nie podczas
zapisu faktu. Zawiera ograniczoną liczbę rzeczywistych terminów i atrap
próbkowanych ze wskazówek o populacji, aby każdy plan miał ten sam kształt.
Węzeł pobiera kompletne wycinki `(term, window)` przez listowanie Agory
rozszerzone w [P035-016](035-agora-topic-addressed-record-relay.md#decorrelated-bucket-pull-2026-10-27).
Zbyt duży koszyk dzieli się według okna czasu albo potomka w słowniku, nigdy
według prywatnego aspektu. Gdy cały prefiks Whisper mieści się w budżecie,
węzeł pobiera wszystko i w ogóle nie wyraża zainteresowania (P035-017).

#### Koniunkcje w transmisji {#conjunctions-on-the-wire}

Story 014 pyta, czy terminy można łączyć operatorem AND. Domyślna reguła v1 to
suma pojedynczych terminów, z koniunkcjami stosowanymi lokalnie po pobraniu:

- przy pobieraniu koszyków AND oszczędza pasmo tylko wtedy, gdy relay filtruje
  wewnątrz koszyków, co wymaga przesłania koniunkcji;
- koniunkcja oznacza mniejszą populację niż każdy z jej terminów, a powtarzanie
  tej samej koniunkcji w kolejnych epokach ułatwia ataki przez przecięcie zbiorów;
- złożony termin słownika oznaczający przecięcie jest zwykłym terminem
  z własnym minimum liczebności, więc ta możliwość pozostaje dostępna.

`P013-DFR-005` porównuje wariant wyłącznie OR ze złożonymi terminami
koniunkcyjnymi na korpusie fixture’ów i zapisuje decyzję tutaj.

#### Decyzje i ujawnienie {#decisions-and-disclosure}

Dopasowanie jest hipotezą istotności, zapisywaną jako kandydat
`weak-signal-finding.v1`. Nie jest dowodem i nigdy nie wlicza się do progu.
Uczestnik potwierdza je, odrzuca dla tej pogłoski albo całego kontekstu pogłosek
bądź odracza. Memarium zapisuje decyzję raz, a widok rekordu i widok pogłoski
ją projektują. Potwierdzone powiązanie pojawia się w lokalnym widoku „Moje
pogłoski” (`P013-DFR-003`) obok własnych pogłosek uczestnika.

Każdy dalszy krok jest zwykłym ujawnieniem: powiązaną pogłoską utworzoną przez
przepływ redakcji Story 005 w profilu kontekstowym P015 (`P013-DFR-004`),
rejestracją zainteresowania albo dołączeniem do pokoju zrzeszenia
i udostępnieniem tam materiałów (`P013-DFR-006`). Powiązana pogłoska dziedziczy
`topic/class` i `signal/similarity-key` z widocznego sygnału albo opcjonalnego
publicznego powiadomienia. Relacja wiąże record/id tego rekordu i rodzaj celu,
nigdy ukryty sygnał za powiadomieniem. Dołącza do kontekstu i wnosi najwyżej
jedno zakwalifikowane źródło; sama relacja nie zwiększa licznika.

### Inwarianty {#invariants}

1. Podczas odkrywania żaden tekst faktu, szczegółowy aspekt, załącznik, ścieżka
   ani digest pól faktu nie opuszcza węzła.
2. Wyrażanie zainteresowania jest związane z epoką i niezależne od czasu
   zapisania faktu.
3. Odkrywanie pobiera kompletne wycinki. Nigdy nie żąda pojedynczych rekordów
   wybranych przez lokalne dopasowanie.
4. Uśpione fakty nigdy nie wyprowadzają rekordów zainteresowania tematami Agory
   (zob. „Odkrywanie zainteresowań i ograniczone prywatne rozpowszechnianie”);
   takie rekordy są publicznymi oświadczeniami o kwalifikowalności.
5. Dopasowania są ustaleniami do przeglądu, nigdy wejściem do zliczania progu.
6. Artefakty pochodne (terminy, plany, wyniki, kandydaci do powiązania) wygasają
   nie później niż rekord źródłowy.
7. Każde ujawnienie jest osobnym, jawnym działaniem przez istniejącą ścieżkę
   z własną kontrolą autorstwa, klasyfikacji i zgody.

### Kompromisy {#trade-offs_1}

- Zgrubne terminy zwiększają prywatność i pełność wyszukiwania, ale kosztują
  pasmo oraz lokalną pracę; budżety i próg pobierania wszystkiego ujawniają koszt.
- Rytm epok opóźnia odkrywanie o godziny lub dni. Pasuje to do słabych sygnałów;
  nie jest to ścieżka alarmowa.
- Słownik staje się punktem koordynacji. Słaby słownik fragmentuje korelację,
  lokalne dostosowanie może rozdzielić czytelników i autorów, a błędnie oznaczone
  pogłoski trafiają do koszyków, których czytelnicy mogą nie pobrać.
- Relaye nadal poznają zgrubne zainteresowania i ich rozkład w czasie; atrapy
  zużywają pasmo, by je rozmyć.
- Autorstwo powiązanej pogłoski ujawnia wystawcy autorstwa kontekstowego
  przynależność uczestnika do tego kontekstu pogłosek, zgodnie z P015.

### Tryby awarii i środki zaradcze {#failure-modes-and-mitigations}

| Awaria | Skutek | Środek zaradczy |
|---|---|---|
| Rzadki lub lokalny termin identyfikuje uczestnika | Relay wiąże węzeł z niszowym tematem | Minimum liczebności, fallback do rodzica, domyślne wykluczenie nieocenionych lokalnych terminów, pobieranie wszystkiego |
| Stabilny zestaw terminów w kolejnych epokach | Fingerprint przez przecięcie zbiorów | Ograniczony rozmiar planu, atrapy, powolna zmiana planu |
| Rozróżnialne atrapy | Ujawnienie rzeczywistych zainteresowań | Atrapy próbkowane z ocenionych wskazówek o populacji, z identycznym zachowaniem pobierania |
| Digest słownika wysłany w transmisji | Dostosowane węzły stają się unikatowe | Wersja i digest pozostają lokalne; rekordy niosą tylko identyfikatory terminów |
| Zmęczenie alertami | Uczestnik ignoruje lub wyłącza funkcję | Próg wyniku, grupowane powiadomienia, limit na epokę, wyciszenie po odrzuceniu |
| Pozorne powiązanie wspomagane modelem | Fałszywy alarm | Ustalenia są doradcze, wyjaśnienia widoczne, potwierdzenie wymagane |
| Spreparowana pogłoska-przynęta | Prowokuje ujawnienia | Dopasowanie niczego nie wysyła; redakcja Story 005; widoczne etykiety relaya i źródła |
| Dopasowanie do wygasłego rekordu | Naruszenie retencji | Artefakty pochodne wygasają ze źródłem; matcher czyta tylko bieżące rekordy |
| Asystent potajemnie zapisuje fakty | Ukryta pamięć | Przechwycenie jest bezczynną propozycją wykonywaną przez hosta po akceptacji (P066-DFR-003) |

### Otwarte pytania {#open-questions_1}

1. Wskazówki o populacji: jak słowniki fabryczne, a później federacyjne mają
   je szacować bez obserwowania czytelników i jak często je aktualizować.
2. Wartości minimum liczebności, domyślna długość epoki i próg pobierania
   wszystkiego.
3. Reguła koniunkcji, do rozstrzygnięcia przez `P013-DFR-005`.
4. Czy źródła dołączające przez jawną relację powinny mieć w progach
   produkcyjnych inną wagę niż te odkryte niezależnie.

### Tracker rezonansu uśpionych faktów {#dormant-fact-resonance-tracker}

Wszystkie wiersze mają status post-MVP `todo`. Wiersze mechanizmów zamyka się
na podstawie ich własnych dowodów w dokumentach właścicieli; wiersz grupujący
zamyka się dopiero po złożonym przebiegu Story 014.

| ID | Zadanie | Status | Zależy od | Bramka ukończenia |
|---|---|---|---|---|
| P013-DFR-000 | Grupowana akceptacja Story 014 | todo | P013-DFR-001–006; [P036-004–008](036-memarium.md#fact-retention-horizons-and-personal-records-2026-10-27); [P078-010–013](078-weak-signal-harvester.md#implementation-tracker); [P035-016–017](035-agora-topic-addressed-record-relay.md#decorrelated-bucket-pull-2026-10-27); [P057-015–016](057-user-and-operator-notifications.md#tracking); [P066-DFR-001–004](066-inquirium-assistant-channel.md#dormant-fact-capture-and-rumor-suggestions-2026-10-27); [Bramki A i B P015](015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md#acceptance-contract) | Jeden zachowany przebieg [Story 014](../30-stories/story-014-dormant-contest-entry.md) na jego profilu fixture’ów, przez relay SQLite i mirror, dowodzi S014-A1 do S014-A11. Obejmuje skanowanie canary każdej powierzchni wyjścia i trwałej kopii AD oraz warianty: brak powiązania, wygaśnięcie, poniżej minimum, błędna etykieta, termin lokalny i pobranie wszystkiego. |
| P013-DFR-001 | Zamrożenie słownika dekorelacji | todo | P091; P046 | JSON Schema `whisper-decorrelation-vocabulary.v1` i fabryczny JSON dostarczany z dystrybucją Node. Deskryptor P091 zapewnia składanie według kluczy, jawne wycofanie, zastąpienie pustą bazą i niezmienne powiązania id z kluczem tematu; lokalne id mają przestrzeń nazw. Po aktualizacjach fabrycznych powstaje typowana diagnostyka, rozstrzygnięcia stosuje się na granicach epok, a wersja ani digest słownika nie trafia do transmisji. Autorstwo i pobieranie walidują względem tego samego rozstrzygnięcia; golden fixtures obejmują każdą regułę. |
| P013-DFR-002 | Plan epoki i zaplanowane pobieranie koszyków | todo | P013-DFR-001; P078-011; P035-016–017; S020 | `whisper-pull-plan.local.v1` na epokę, jedna abstrakcja wpisu z lokalnym `origin` równym `need`, `decoy` albo `cover` ([P013-CIM-001](013-whisper-social-signal-exchange/cooperative-interest-masking.md#cooperative-interest-masking)): ograniczona liczba rzeczywistych terminów, atrapy z ocenionych terminów, budżet bajtów i pobieranie wszystkiego, gdy kwalifikująca się objętość mieści się w budżecie. Zadanie S020 pobiera kompletne wycinki ze skonfigurowanych relayów i mirrorów do lokalnego magazynu pogłosek. Testy dowodzą niezależności od czasu zapisu faktu i nierozróżnialności pobrań atrap. Skompilować scalone zadania raz na epokę; zachować lokalne przyczyny poza wykonawcą, utrwalać wylosowane przesunięcia i objąć fixture’y mieszanych źródeł pochodzenia, restartu i niekompletnego wycinka ze wspólnych zaleceń implementacyjnych. |
| P013-DFR-003 | Widok „Moje pogłoski” i projekcja powiązań od strony pogłoski | todo | P036-008; P013-PA-003; P095-012 | Lokalny widok wymienia własne pogłoski i pogłoski potwierdzone jako dotyczące rekordów uczestnika, wraz ze stanem progu, propozycji, pokoju i kuracji. Widok kuracji otrzymanych pogłosek pokazuje decyzje o powiązaniach według `record/id`. Dane powiązań nigdy nie trafiają do propagacji wychodzącej. Związać listę, szczegóły i decyzje ze zweryfikowanym uczestnikiem; bez domniemanego autorstwa, odwrotnego indeksu między nymami ani referencji między uczestnikami. Wykorzystać kontrakty chronionych widoków P095. Dostarcza wejście P098-006; ten konsument nie jest warunkiem wstępnym. Projektować opcjonalne stany pokoju/ADC/LLR wyłącznie od ich właścicieli; rozróżniać nie dotyczy, jeszcze niedostępne i nieznane. Widok nie tworzy tych workflowów ani nie kwalifikuje ich kontroli operacyjnych; wybrane profile, które ich wymagają, zachowują osobne warunki wstępne. |
| P013-DFR-004 | Autorstwo powiązanej pogłoski | todo | P015 Gate B; Story 005 | Sygnał v2 niesie ograniczoną listę `signal/related-to`, ustawianą tylko przez jawne działanie autora. Każda relacja wiąże publiczne record/id i zamknięty rodzaj celu (`whisper-signal` albo `whisper-correlation-notice`). Czytelnik widzący tylko powiadomienie wskazuje powiadomienie, nigdy id ukrytego sygnału. Powiązany szkic dziedziczy `topic/class` i `signal/similarity-key`, więc digest kontekstu się zgadza. Relacja nie dodaje wagi ponad jedno źródło, a reguły pochodzenia zapobiegają zliczaniu własnych rekordów pochodnych pogłoski. |
| P013-DFR-005 | Decyzja o koniunkcji w transmisji | todo | P013-DFR-001; P078-011–012 | Porównanie wyłącznie OR ze złożonymi terminami koniunkcyjnymi na korpusie fixture’ów raportuje pełność i precyzję lokalnych dopasowań, bajty na epokę oraz szacowaną liczebność zbioru anonimowości na zapytanie. Decyzję zapisuje się w tej sekcji; do tego czasu domyślne pozostaje wyłącznie OR. |
| P013-DFR-006 | Przekazanie do pokoju zrzeszenia z udostępnianiem prac | todo | P070; S018; P036-007 | Po opt-in przekazanie do Room oferuje wklejony tekst, powiązany wątek wiadomości i linki zewnętrzne. Udostępnienie załącznika Memarium wymaga jawnego obniżenia klasyfikacji dla każdego udostępnienia i pokazuje audytorium Room; linki zewnętrzne niosą ostrzeżenie o wyjściu poza gwarancje. Dołączenie do pokoju niczego nie udostępnia automatycznie. |

### Tracker dostępu uczestnika – 2026-11-06 {#participant-access-tracker-2026-11-06}

Te proponowane zadania implementują domenowe warunki wstępne
[P098 §8](098-alpha-ui.md#8-participant-access-contract-memarium-and-whisper).
P013 jest właścicielem pieczy nad intake i przejrzanego kandydata, P015/S026
odpowiadają za zachowane operacje kryptograficzne aktora, a P026 za projekcję
widza. Uzgodnienie kontraktów poprzedza obie ścieżki runtime. P098 pozostaje
integracją UI na dalszym etapie; żadne zadanie właściciela nie wymaga jego
ukończenia. P013-DFR-003 używa wynikowych lokalnych referencji dla „Moich
pogłosek”, zamiast wprowadzać kolejny magazyn autorstwa. Poniższe wektory granicy
odbiorcy i przekazania zewnętrznego używają fixture’ów dopuszczonych przez
właściciela; nie czekają na adapter Web/Harvester. P078-018 odpowiada za faktyczną
integrację producenta i odbiorcy. P013-PA-002 obejmuje autoryzowane podsumowanie
szkicu i odczyt wyniku, zanim dostępne staną się certyfikacja lub publikacja.

| ID | Pozycja | Status | Zależności | Rezultat i bramka | Konsumenci (nie warunki wstępne) |
|---|---|---|---|---|---|
| P013-PA-001 | Zamrożenie intake uczestnika i przekazania kandydata | todo | P024-009; P036-012 | Zamrozić własność uczestnika, powiązania producenta/widoku oraz retencję/pieczę nad surowym wejściem, szkicami, rewizjami kandydatów, lokalnym SQLite i synchronizacją Memarium. Zdefiniować wykluczenie/migrację legacy, ograniczone API list/szczegółów/mutacji i dokładne przekazanie kandydata/proweniencji/audytorium/digestu przeglądu do P015. Aktor pochodzi z dopuszczonego kontekstu; ID nie są grantami. Zamrozić mapowania schematów/tras/rejestru i negatywne fixture’y. Publiczne przeglądanie nie tworzy intake, nie wydaje nymu ani nie odblokowuje klucza. Uwzględnić ograniczoną aktywność/status uczestnika i referencje do odzyskiwalnych szkiców z rewizją właściciela, retencją, dozwoloną kontynuacją i semantyką nieznanego wyniku; są to domenowe projekcje odczytu, nie magazyn historii UI. Uwzględnić przekazanie od zewnętrznego, przejrzanego producenta: dokładne digesty źródła/reprezentacji i przeglądu, klasyfikację, skończoną pieczę/wygaśnięcie, zamierzonego uczestnika-właściciela i wersje kontraktów producenta/odbiorcy. Przyjmować tylko referencje dopuszczone przez właściciela; ustalenie, intencja szkicu ani receipt źródła nie przenoszą władzy podpisania/publikacji. Zamrozić osobne wyniki szkicu/przeglądu/podpisu/przedłożenia/ujawnienia i autorytatywne wyszukiwanie po utracie odpowiedzi; niezgodne wersje lub wygasła piecza odmawiają bez ponownego pobrania lub odtwarzania skutku. | P013-PA-002; P015-009; P098-010c |
| P013-PA-002 | Izolacja intake uczestnika i zachowanych etapów | todo | P013-PA-001; P024-010; P036-014; P080-049 | Wdrożyć intake związany z uczestnikiem, zabezpieczenia odczytu/edycji oraz synchronizację/czyszczenie etapów pod władzą modułu i uczestnika. Dowieść izolacji O/P/Q w SQLite i Memarium, jawnej atrybucji legacy, restartu/replayu, retencji i odmowy przy niedostępności właściciela. Etapy surowe/szkicowe pozostają wewnątrz dopuszczonej prywatnej granicy redakcji i poza ogólnym odkrywaniem pamięci. Użyć fixture’ów kandydatów; zadanie nie wymaga certyfikacji/podpisywania ani ukończonego UI. Dodać jawną, nullable kolumnę właściciela-uczestnika do SQLite intake: istniejące wiersze NULL pozostają wyłącznie legacy/operatorskie i nigdy nie są przypisywane na podstawie bieżącego logowania. Ścieżki uczestnika wymagają właściciela nie-NULL. Podzielić klucze operacji/idempotencji i czyszczenie etapów według właściciela; przejrzeć migrację i rollback bez ujawniania uczestnika przez cudzą przestrzeń nazw. Dostarczyć ograniczoną projekcję aktywności/statusu/wznowienia z tego samego magazynu właściciela, z niezależnym zachowaniem kontynuacji i wygasłego szkicu. Retencja intake nadal jest tu wymagana; oddzielenie powiązań producenta od odczytów eksploratora nie odracza czyszczenia. Ponownie walidować powiązania podmiotu, źródła i pieczy producenta/odbiorcy przed przyjęciem zewnętrznego szkicu; ograniczyć klucz operacji i wyszukiwanie wyniku do uczestnika. Zachować dokładne wcześniejsze wyniki po utracie odpowiedzi i oddzielić awarie źródła/właściciela od braku szkicu. | P013-PA-003; P098-006; P098-014 |
| P013-PA-003 | Złożenie przeglądania i wkładu uczestnika | todo | P013-PA-002; P015-010; P026-015 | Zintegrować dopuszczone przeglądanie pogłosek i prywatny intake przez dokładny przegląd/certyfikację/podpis/publikację/odczyt wyniku v2. Zachować osobne skutki, wersje źródła/śladu i zgodę; nigdy nie wracać do autora local-primary ani widza operatorskiego. Dowieść rzeczywistego workflowu właściciela/modułu z O/P/Q, zmienionym przeglądem, zablokowanym kluczem, utratą odpowiedzi, referencjami operacji innych uczestników i ukrytymi polami kuracji. Zachować lokalne referencje własnych wyników dla DFR-003. Przekazać odpowiednie dowody ekspozycji do P013-AE-001/P026-008; szersze macierze pozostają otwarte. Whisper odpowiada za orkiestrację wkładu i autoryzowaną projekcję wyniku; konsumuje wyniki kryptograficzne P015 bez ich dublowania. Rozróżniać stany podpisany, przedłożony, potwierdzony transportowo i ujawniony, włącznie z niepewnością. | P013-DFR-003; P098-006; P098-014 |

## Warunki ujawnienia określane przez autora {#author-disclosure-conditions}

Proponowana kontynuacja po MVP; bez twierdzenia o działaniu runtime.
[Projekt właścicielski i tracker](013-whisper-social-signal-exchange/author-disclosure-conditions.md#author-disclosure-conditions)
znajdują się obecnie w pliku towarzyszącym. Domena, decyzje i identyfikatory zadań
pozostają bez zmian.

Opcjonalny [poufny przegląd powiązań](013-whisper-social-signal-exchange/author-disclosure-conditions.md#confidential-affiliation-review)
może wspierać decyzję autora o ujawnieniu. P015 odpowiada za zgodę, powiązanie
tożsamości i ograniczone poświadczenie; P013-ADC-010 za jego prywatną
prezentację. Powiązanie nie jest dowodem przynęty ani podstawą dyskredytowania
sygnalisty. Ten profil post-MVP nie zmienia zliczania źródeł i nie blokuje
istniejącej ścieżki ujawnienia.

<!-- Kotwice zgodności dla dawnej sekcji w tym pliku i jej podsekcji. -->
<a id="author-disclosure-conditions-2026-10-27"></a>
<a id="summary_1"></a>
<a id="context-and-problem_1"></a>
<a id="roles-and-payloads"></a>
<a id="same-matter-descriptor-grouping-rule-and-key"></a>
<a id="ambiguous-reports-proposals-not-merges"></a>
<a id="counting-rule"></a>
<a id="attestation-and-verification"></a>
<a id="release"></a>
<a id="amendments-and-withdrawal"></a>
<a id="custody-obligations"></a>
<a id="coordination-independence"></a>
<a id="optional-public-notice"></a>
<a id="confidentiality-from-correlators"></a>
<a id="condition-states"></a>
<a id="condition-proposal-and-execution-states"></a>
<a id="invariants_1"></a>
<a id="trade-offs_2"></a>
<a id="failure-modes-and-mitigations_1"></a>
<a id="open-questions_2"></a>
<a id="author-disclosure-condition-tracker"></a>

[Przejdź do pełnej sekcji](013-whisper-social-signal-exchange/author-disclosure-conditions.md#author-disclosure-conditions).

## Wspólne maskowanie zainteresowań {#cooperative-interest-masking}

Proponowana kontynuacja po MVP; bez twierdzenia o działaniu runtime.
[Projekt właścicielski i tracker](013-whisper-social-signal-exchange/cooperative-interest-masking.md#cooperative-interest-masking)
znajdują się obecnie w pliku towarzyszącym. Domena, decyzje i identyfikatory zadań
pozostają bez zmian.

<!-- Kotwice zgodności dla dawnej sekcji w tym pliku i jej podsekcji. -->
<a id="cooperative-interest-masking-2026-10-27"></a>
<a id="summary_2"></a>
<a id="context-and-problem_2"></a>
<a id="one-plan-three-origins"></a>
<a id="cover-requests"></a>
<a id="delivery-through-artifact-delivery"></a>
<a id="shared-timing"></a>
<a id="multi-epoch-cover"></a>
<a id="participation-and-budgets"></a>
<a id="not-memory-not-support"></a>
<a id="effect-recovery-classes"></a>
<a id="effectiveness-must-be-measured"></a>
<a id="invariants_2"></a>
<a id="trade-offs_3"></a>
<a id="failure-modes-and-mitigations_2"></a>
<a id="open-questions_3"></a>
<a id="cooperative-interest-masking-tracker"></a>

[Przejdź do pełnej sekcji](013-whisper-social-signal-exchange/cooperative-interest-masking.md#cooperative-interest-masking).

## Długowieczne pogłoski i historyczne autorstwo {#long-lived-rumors-and-historical-authorship}

Proponowana kontynuacja po MVP; bez twierdzenia o działaniu runtime.
[Projekt właścicielski i tracker](013-whisper-social-signal-exchange/long-lived-rumors.md#long-lived-rumors-and-historical-authorship)
znajdują się obecnie w pliku towarzyszącym. Domena, decyzje i identyfikatory zadań
pozostają bez zmian.

<!-- Kotwice zgodności dla dawnej sekcji w tym pliku i jej podsekcji. -->
<a id="long-lived-rumors-and-historical-authorship-2026-10-27"></a>
<a id="summary_3"></a>
<a id="context-and-problem_3"></a>
<a id="four-periods"></a>
<a id="historical-admission-evidence"></a>
<a id="meeting-a-twin-after-a-year"></a>
<a id="case-continuity-key-and-case-bound-succession"></a>
<a id="case-state-and-currency"></a>
<a id="signature-uses-and-certificate-scope"></a>
<a id="invariants_3"></a>
<a id="trade-offs_4"></a>
<a id="failure-modes-and-mitigations_3"></a>
<a id="open-questions_4"></a>
<a id="long-lived-rumor-tracker"></a>

[Przejdź do pełnej sekcji](013-whisper-social-signal-exchange/long-lived-rumors.md#long-lived-rumors-and-historical-authorship).


### Migracja schematu przed wydaniem: przenośna piecza nad sprawą (2026-11-02) {#pre-release-schema-migration-portable-case-custody-2026-11-02}

Krotka sprawy w whisper-signal.v2 występuje w całości albo wcale i jest
niezależna od ADC. Embargo wymaga pełnej krotki; wartości manifestu i sygnału
muszą się zgadzać. Rozszerza to v2 w miejscu zgodnie z polityką przedwydaniową.
Starszy walidator odmawia sprawie bez ADC; dokładny poprzedni schemat jest
przypięty w wektorze migracji Node. Zamrożone manifesty źródeł i historyczne
dowody zachowują pierwotne digesty schematów.

Ten etap usunął również line/succession osadzone w nym-certificate.v1, zabronił
succession w nym-renew-request.v1 (zastępując je osobnym dowodem kontroli
związanym z domeną) i zastąpił aktywne nym-succession.v1 wersją v2. Przed
pierwszym wydaniem rozszerzenie wymaga jawnej noty i wektorów; zawężenie wymaga
ponadto, by żaden dopuszczony artefakt/dowód nie używał usuwanej postaci. Po
wydaniu należy użyć nowej wersji albo jawnego profilu, nigdy semantycznej zmiany
w miejscu.


### Kwalifikacja nośnika PEX-001 w określonym zakresie, 2026-11-07 {#pex-001-scoped-carrier-qualification-2026-11-07}

Dopuszczony profil S010 z jednym relayem przeszedł kwalifikację niezależnie od
semantyki sprawy: rzeczywiste fixture’y WSS/AD/INAC obejmują oba kierunki, brak
relaya, wycofanie polityki przy ponowieniu, wygaśnięcie, złą rolę/odbiorcę,
restart i utratę odpowiedzi. Zwykli natywni aktorzy źródła/autorytetu/audytorium
dowodzą rzeczywistego odbioru domenowego i dokładnego odtworzenia zapisanego
szyfrogramu. Przeszły także regresje odmowy starszego chronionego sygnału/śladu.
Tylko AD ponawia próby; nie ma obniżenia do bezpośredniej trasy/onion. Wyjątek
wyłącznie loopback jest jawny i nie stanowi dowodu z fizycznych hostów ani
wobec globalnego obserwatora. Skany odbiorcy obejmują canary trasy źródłowej;
relay zgodnie z uprawnieniami zna sąsiadujące źródło. Ograniczone skany
raw/JSON/base64/SQLite nie badają zaszyfrowanych ani forensic nośników.
Przypięcia źródeł i ograniczenia podano w `node:docs/evidence/portable-admission/2026-11-07-case-continuity-qualified` i `node:docs/audits/ACCEPTANCE-LLR007-LLR008-PEX001-2026-11-07.md`.
P015-011 śledzi istniejącą wcześniej lukę retencji replayu autorstwa; Memarium
pozostaje przyjętym projektem wyłącznej pieczy nad chronionymi rekordami, a nie
twierdzeniem, że bramka transportu PEX usunęła tę lukę.


### Bezpośrednia bramka wymiany PEX-001 — 2026-11-08

Dodatkowy [profil ciągłości sprawy](013-whisper-social-signal-exchange/private-case-continuity.md)
przeszedł niezależną bramkę A: rzeczywiste dwa endpointy AD/INAC, oferty P037,
chroniona piecza Memarium, skrzynka żądań i osobno dopuszczone przetwarzanie S020,
odmowy, utrata ACK/odpowiedzi, restart oraz ograniczone kontrole prywatności.
Kwalifikacja luźna, po ekstrakcji i świeżym odczycie z obu magazynów jest identyczna.
Dowód: `node:docs/evidence/private-case-continuity/2026-11-08-direct-gate-a/README.md`.
PEX-001 jest ukończone dla tego zakresu. Zwykła ścieżka v1 SQLite/Synapse bramki B,
S023-002 i PEX-002 pozostają otwarte; wcześniejsze dowody zachowują swój zakres.
