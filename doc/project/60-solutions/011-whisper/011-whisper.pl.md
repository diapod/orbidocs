# Orbiplex Whisper

`Orbiplex Whisper` jest komponentem warstwy rozwiązań związanym z Node, służącym
wymianie sygnałów społecznych z jawnymi granicami prywatności oraz niewielkich
oświadczeń o pochodzeniu. Przygotowuje sygnały o charakterze pogłoski do publikacji,
zachowuje ich słabszy status epistemiczny, koordynuje inicjowanie zrzeszeń po
przekroczeniu progu i może przenosić ograniczone twierdzenia `whisper-trace.v1`,
bez niejawnego awansowania sygnałów ani śladów do rangi dowodów.

`Whisper` nie jest właścicielem anonimowości transportu. Deklaruje jedynie intencję
routingu i prywatności w wychodzących artefaktach, a jej realizację powierza
warstwie wyjścia Node, korzystającej z dostępnego capability prywatności wyjścia.

Dla sygnałów publicznych lub o zakresie federacyjnym `Whisper` może używać
`Orbiplex Agora` jako trwałego podłoża rekordów publicznych/federacyjnych. Agora
przenosi przyjęte koperty `agora-record.v1` i zasila projekcje; Whisper pozostaje
właścicielem semantyki sygnałów społecznych, cyklu życia progów i granicy zgody.

Kwalifikacja transportu z 2026-10-19 należy do P035-007/009/010, nie do Whisper:
34 przypadki Matrix i pięć SQLite na czystych rewizjach Node `1bc523a6` / Orbidocs
`5993f7d0` kwalifikują pogłoski o pewności 0,5 i dopuszczone rodziny
`whisper-signal.v1`, `whisper-trace.v1` oraz `whisper-threshold-reached.v1`,
dokładne bajty autora, niezależną historię pokoju, admisję według czasu lokalnego,
restart i replay nośnika. Bramki pełnego PDU przechodzą zarówno dla Node, jak
i niezmodyfikowanego Synapse; świeże pobranie z przyjętego lokalnego magazynu
zachowanych danych daje identyczną rekwalifikację. Dowody:
`node:docs/evidence/matrix-opaque-envelope/2026-10-19-room-recovery-full/README.md`.
Nie kwalifikuje to wszystkich przepływów Whisper/wystawiania, nie podnosi statusu
epistemicznego sygnałów, nie dowodzi federacji homeserverów ani nie oznacza
niezależnych kopii zapasowych czy gotowości produkcyjnej.

## Certyfikowane autorstwo kontekstowe {#certified-contextual-authorship}

Przyjęty profil fazy 1 P015 ma osobno zakwalifikowaną ścieżkę z 2026-11-04:
lokalny nym w Vault, certyfikację przez AD/INAC szyfrowaną dla odbiorcy, chroniony
przegląd/podpis po stronie hosta, UI bez JS oraz sygnały/progi kontekstowe na
SQLite i dopuszczonym Synapse. Zlicza źródła uczestników dopuszczonych przez radę,
a nie nymy ani węzły źródłowe. Zwykła publikacja confidence0.5, status/wygaśnięcie/
reset, zaufany późny czas, prywatność, restart/replay i akceptacja pełnego PDU są
objęte A30/B31 oraz sześcioma osobnymi zobowiązaniami zgodności. Dokładne wyniki
kwalifikacji luźnych/wypakowanych materiałów oraz świeżego źródła pierwotnego/
wtórnego są zgodne. Dowody: `node:docs/evidence/matrix-opaque-envelope/2026-11-04-whisper-authorship/README.md`.

To ograniczona kompozycja właściwa źródłu, z payloadem dostępnym wyłącznie
operatorowi; nie odnawia historycznego zakresu M4 zliczającego węzły. Host/Vault
odpowiada za klucze i podpisy, opcjonalny wystawca za politykę, AD za dostarczanie
szyfrogramów, Agora za niezmienne fakty admisji, a ewaluator kontekstowy za bieżącą
kwalifikowalność i zatrzask pierwszej emisji. Czas Matrix opiera się na zaufaniu do
uwierzytelnionego, dopuszczonego homeservera; podpisy, hashe i rozmiar PDU są
sprawdzane w acceptance. Opcjonalny runtime stay-ready, inni konsumenci P015/P081,
pokoje/opt-in, Anon, LLR/ADC, federacja oraz gotowość globalna/wydania pozostają
poza tą kwalifikacją. Status komponentu pozostaje częściowy.

Artefakty progu i zrzeszenia są publicznymi metasygnałami, nie publicznymi
pogłoskami. `whisper-threshold-reached.v1` stwierdza, że wystawca lub projekcja
zaobserwowali korelację określoną polityką. `association-room-proposal.v1`
stwierdza istnienie zredagowanej propozycji koordynacji służącej wyłącznie jej
zainicjowaniu. Żaden z tych artefaktów nie jest publiczną opowieścią społeczną;
awans do `public-gossip.v1` wymaga późniejszej, jawnej decyzji o publikacji.

`public-gossip.v1` jest jawnym aktem publikacji, nie automatycznym produktem
projekcji. Może być publikowany niezależnie na publicznej ścieżce słabych sygnałów
albo po decyzji dobrowolnego pokoju zrzeszenia o wydaniu publicznego oświadczenia.
`association-room-proposal.v1` może więc poprzedzać publiczną pogłoskę, ale nie
jest jej warunkiem wstępnym.

## Cel {#purpose}

Komponent odpowiada za ścieżkę wykonania na poziomie rozwiązania obejmującą:
- przyjmowanie pogłosek i lokalne przygotowanie,
- redakcję, parafrazę i neutralizację idiolektu za zgodą użytkownika,
- publikację ograniczonych artefaktów `whisper-signal`,
- odbieranie sygnałów zainteresowania,
- rozpoznawanie progów,
- inicjowanie pokojów zrzeszeń z dobrowolnym uczestnictwem.

## Zakres {#scope}

Dokument definiuje odpowiedzialności komponentu Whisper na poziomie rozwiązania.

Nie definiuje:
- konkretnego układu modułów w repozytorium implementacyjnym,
- implementacji prywatności transportu ani przekaźników typu onion,
- docelowego zarządzania sprawami dowodowymi,
- automatycznego zapisywania ludzi do wspólnych pokojów,
- semantycznego wykrywania duplikatów pogłosek w v1.

## Rozszerzenia po MVP {#post-mvp-extensions}

### Oświadczenia o śladach artefaktów {#artifact-trace-statements}

Powiązany schemat:
- `whisper-trace.v1`

Oświadczenia o śladach Whisper pozwalają niskim kosztem ujawnić, że artefakt
został utworzony, przekazany transportowi, odebrany lub jest posiadany. Są to
podpisane twierdzenia autora koperty, a nie receipty, poświadczenia, dowody
posiadania czy dowody prawdziwości treści artefaktu.

Domyślna postać zawiera tylko SHA-256, długość w bajtach oraz opcjonalny typ
treści lub schemat. Ujawnienie samego digestu ogranicza transfer, ale nie jest
anonimowe: przewidywalną treść nadal można odgadnąć lub skorelować przez digest.
Pełne bajty inline są dozwolone wyłącznie w `digest-and-content`, z jawnym
`consent/ref` zwalidowanym przez host nadawcy, twardym limitem 32 KiB na łączu
oraz weryfikacją dokładnego digestu i długości. Cały JSON śladu ma limit 128 KiB,
a jawna przestrzeń nazw rozszerzeń – 8 KiB, przed podpisaniem lub admisją.
Przywołana decyzja musi wiązać digest, zakres, podmiot/autorytet i okno ważności;
sama referencja tekstowa nie nadaje uprawnień. Jest lokalnym powiązaniem audytowym
nadawcy, nie sieciowo widocznym dowodem zgody, i nie powinna ujawniać identyfikatora
uczestnika. Ślad może odsyłać przez `evidence/refs` do `execution-receipt.v1`, faktu
dostarczenia AD lub innego poświadczenia; to te artefakty pozostają źródłami
autorytetu dowodowego.

Tworzenie śladów korzysta ze zwykłej podpisanej koperty i istniejących nośników:

- ślady publiczne lub federacyjne używają `record/kind = "whisper-trace"`
  i `content/schema = "whisper-trace.v1"` pod
  `ai.orbiplex.whisper-traces/<trace-kind>`;
- ślady prywatne/bezpośrednie korzystają z Artifact Delivery i INAC;
- rekordy śladów są wyłączone z projekcji podobieństwa, progów i zrzeszeń Whisper.

Status: `implemented`. Zaimplementowano kanoniczne schematy i fixture'y, Schema
Gate Node, niezależną od transportu walidację integralności, dokładne rozstrzyganie
zgody przez host nadawcy, powierzchnie tworzenia i inspekcji, lokalny model odczytu
samych metadanych oraz testy smoke publicznego nośnika Agora i prywatnego AD/INAC.
Ponowienia publikacji śladów używają atomowej rezerwacji idempotencji: aktywne
żądanie zwraca konflikt, ukończone odtwarza wynik, a tylko nieudane może być
zarezerwowane ponownie. Lokalny model odczytu stosuje domyślną retencję 30 dni,
czyszcząc dane przy starcie i zapisach; nigdy nie zachowuje treści inline.

## Wymagana implementacja {#must-implement}

### Przyjmowanie i publikowanie pogłosek {#rumor-intake-and-publication}

Based on:
- `doc/project/20-memos/orbiplex-whisper.md`
- `doc/project/30-stories/story-005-whisper-rumor-intake.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.pl.md`

Powiązane schematy:
- `whisper-signal.v1`

Odpowiedzialności:
- przyjmować wejście o charakterze pogłoski bez sprowadzania go do dowodu,
- wykonywać ograniczone lokalne workflowy redakcji i redukcji idiolektu,
- wymagać zatwierdzenia przez użytkownika przed publikacją,
- implementować ograniczoną ścieżkę przyjmowania/redakcji jako osobno nadzorowany
  pakiet middleware w Rust, z własną powierzchnią UI operatora, bez włączania
  surowych prywatnych danych wejściowych do Agory ani zaufanego rdzenia daemona,
- przechowywać surowe dane użytkownika i pośrednie szkice redakcyjne przed
  publikacją wyłącznie w lokalnym/prywatnym stanie Memarium, pod jawną polityką
  retencji i kwarantanny,
- utrwalać prywatne etapy przyjmowania jako zapieczętowane fakty Memarium w przestrzeni
  `personal` przez capabilities hosta, zamiast osadzać kryptografię w `whisper-intake`;
  stabilne rodzaje faktów/artefaktów to `whisper-intake.raw-private.v1`,
  `whisper-intake.redaction-draft.v1`, `whisper-intake.quarantine.v1`
  i `whisper-intake.candidate-ready.v1`, z kluczami idempotencji wyprowadzonymi
  z `intake_id + stage`,
- pozwalać dostarczać krok redakcji/sanityzacji przez inny skonfigurowany pakiet
  middleware, aby deterministyczne fixture'y, akcje JSON-e/Sensorium i przyszła
  redakcja wspomagana modelem przez Inquirium współdzieliły ten sam dalszy kontrakt,
- udostępniać redakcję wspomaganą modelem przez wąską granicę capability,
  najlepiej `whisper.redaction.prepare`, gdzie dostawca zwraca lokalny szkic
  redakcyjny i nigdy nie publikuje do Agory ani nie oznacza kandydata jako zatwierdzonego,
- umożliwiać implementację `whisper.redaction.prepare` przez JSON-e Flow oparty
  na ograniczonej akcji Sensorium OS, aby pierwsza implementacja mogła uruchamiać
  deterministyczny skrypt lub lokalne polecenie modelu, zachowując przyszłą ścieżkę
  do silniejszych dostawców Inquirium/model-runtime,
- emitować artefakty `whisper-signal` z jawną klasą epistemiczną, routingiem
  o zakresie węzła, pseudonimowym uczestnictwem z autorstwem nymu,
  `author/nym-proof` na poziomie koperty i intencją routingu/prywatności,
- dla Agory M4 publikować `whisper-signal.v1` bezpośrednio jako publiczny/federacyjny
  payload, z autorstwem koperty `nym:did:key:...` i dowodem nymu dołączonym na
  granicy koperty/polityki; preferować dowód inline, z opcjonalnymi referencjami
  dla dłuższej historii pochodzenia lub reputacji,
- nie umieszczać prywatnych pogłosek korelacyjnych ani pogłosek wyłącznie
  bezpośrednich w publicznych tematach Agory,
- publikować przez Agorę wyłącznie oczyszczone sygnały publiczne/federacyjne,
  gdy polityka ujawniania dopuszcza tę powierzchnię.

Status:
- `done` dla Agory M4. Wspólna granica implementacyjna `whisper-core` odpowiada
  teraz za niezależne od Agory parsowanie publicznego/prywatnego trybu ujawniania,
  odmowę ujawniania w publicznej Agorze sygnałów `private-correlation`
  i wyłącznie bezpośrednich oraz deterministyczne wyprowadzanie identyfikatorów
  progów/propozycji M4. Agora korzysta z tego rdzenia przy wejściu/podpisywaniu
  i w projekcjach zasilanych replayem. Workspace Node zawiera też pierwszy
  ograniczony, nadzorowany zalążek middleware Rust `whisper-intake`: odpowiada on
  za lokalne/prywatne przyjmowanie, szkice redakcyjne, metadane kwarantanny/retencji,
  powierzchnię UI należącą do serwera, opcjonalne egzekwowanie nadzorowanego tokenu
  uwierzytelniającego middleware na trasach innych niż health oraz strażnika
  kandydata do publikacji wykorzystującego `whisper-core`. Granica prywatnego
  utrwalania jest już domknięta na poziomie middleware: prywatne etapy są
  pieczętowane przez `sealer.seal` hosta, zapisywane jako fakty Memarium
  w przestrzeni `personal` przez `memarium.write`, śledzone lokalnym stanem/błędem
  synchronizacji i ponawiane akcją operatora. Workspace Node dostarcza także
  `whisper-intake` jako dołączony, nadzorowany pakiet middleware włączany przez
  opt-in, aby profile Story-005 mogły go używać bez ręcznego podłączania binarek.
  M4 celowo kończy się na granicy deterministycznego dostawcy lokalnego: JSON-e
  Flow może kierować `whisper.redaction.prepare` do Sensorium OS, a Sensorium OS
  uruchamiać lokalny fixture lub lokalnie skonfigurowane polecenie modelu. Slice
  przygotowania do użycia produktowego po M4 dodaje należący do hosta kształt
  polityki dostawców Inquirium/model-runtime oraz pozbawiony sekretów most
  akceptacyjny lokalnego symulatora Inquirium. Produkcyjne wdrożenia modeli
  zdalnych pozostają kwestią konfiguracji operatora i runtime'u.

Redakcja/parafraza wspomagana modelem ma już stabilną granicę capability hosta.
Pierwsza konkretna ścieżka dostawcy M4 jest celowo sterowana konfiguracją
i wyłącznie lokalna: JSON-e Flow wywołuje `sensorium.directive.invoke`, a Sensorium
OS uruchamia ograniczoną, deterministyczną akcję `whisper.redaction.prepare`, która
zwraca szkic do przeglądu przez człowieka. Docelowy kontrakt:

```text
whisper-intake
  -> host capability whisper.redaction.prepare
  -> configured provider
  -> redaction draft
  -> operator approval
  -> publishable candidate
```

Dostawcą może być JSON-e Flow wraz z `sensorium.directive.invoke`, gdzie
[Sensorium](../030-sensorium/030-sensorium.md) OS wywołuje skończony skrypt lub
lokalne polecenie modelu z limitem czasu. Wybór algorytmu redakcji pozostaje dzięki
temu poza daemonem i Agorą. `whisper-core` nadal waliduje końcowy tryb ujawniania
kandydata, więc dostawca nie może ominąć strażników `private-correlation` ani
trybu wyłącznie bezpośredniego.

Granica korzysta z `whisper-redaction-prepare-request.v1`
i `whisper-redaction-prepare-response.v1`. W implementacji M4 `whisper-intake`
przesyła surowy prywatny materiał przez wartość w wywołaniu capability hosta na
loopbacku, waliduje odpowiedź dostawcy, utrwala zwrócony szkic lokalnie i blokuje
publikację do jawnego zatwierdzenia przez operatora. `raw/private-material` celowo
przyjmuje dowolną wartość JSON, gdy kontrakt przygotowania redakcji wciąż się
stabilizuje między deterministycznymi fixture'ami, JSON-e Flow, akcjami Sensorium
OS i przyszłymi dostawcami wspomaganymi modelem przez Inquirium. Gdy stabilny
interfejs dostawcy zostanie sprawdzony, pole powinno zostać zawężone do
`object|string`; wartości skalarne, tablice i `null` stanowią margines zgodności,
nie zamierzony kształt długoterminowy.
Gdy przygotowanie wspomagane modelem jest jawnie włączone, brak obsługi
`whisper.redaction.prepare` powinien skutkować bezpieczną odmową przez stan
gotowości, zamiast pokazywać mylący przycisk przygotowania.

Przygotowanie do użycia produktowego po M4 jest śledzone w
`doc/project/60-solutions/011-whisper/011-whisper-impl.md`. Domknięty slice
zachowuje rozdział kontraktu domenowego Whisper od adapterów modeli: wywołujący
nadal żąda `whisper.redaction.prepare`, a polityka hosta wybiera dostawców lokalnych
deterministycznych, lokalnego modelu, nadzorowanego adaptera modelu HTTP lub
zewnętrznego adaptera modelu. Wywołania dostawców Inquirium/model-runtime są
autoryzowane przez należące do hosta `runtime/ref` lub politykę profilu i nie mogą
przyjmować surowej nazwy modelu od wywołującego jako nadpisania. Pozostały tracker
produktowy znajduje się w nocie implementacyjnej Whisper, nie w roboczym pliku
w katalogu głównym workspace'u.

### Koordynacja zainteresowania i progów {#interest-and-threshold-coordination}

Based on:
- `doc/project/20-memos/orbiplex-whisper.md`
- `doc/project/30-stories/story-005-whisper-rumor-intake.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.pl.md`

Powiązane schematy:
- `whisper-interest.v1`
- `whisper-threshold-reached.v1`
- `association-room-proposal.v1`

Odpowiedzialności:
- rejestrować lokalną istotność bez przedwczesnego ujawniania,
- rozpoznawać przekroczenia progów zgodnie z polityką,
- implementować regułę smoke M4 jako dane: co najmniej dwa odrębne kwalifikowalne
  węzły, ta sama `topic/class`, ten sam deterministyczny `signal/similarity-key`
  i ograniczone okno czasowe,
- wyprowadzać deterministyczne zbiory inicjujące,
- publikować `association-room-proposal.v1` jako rekord Agory w publicznym/
  federacyjnym temacie propozycji, z treścią zredagowaną i służącą wyłącznie inicjowaniu,
- emitować deterministyczne pochodne rekordy Agory `whisper-threshold-reached.v1`
  i `association-room-proposal.v1` jako twierdzenia metasygnałowe podpisane przez
  autorytet projekcji, o zakresie wystawcy, gdy polityka dopuszcza automatyczną
  publikację pochodną o niewielkim wpływie,
- zapobiegać pętlom rekordów pochodnych przez deterministyczne identyfikatory
  pochodne, wykluczenie rodzajów rekordów źródłowych i referencje derywacji,
- zachowywać dobrowolny zapis i nigdy nie zapisywać ludzi automatycznie,
- udostępniać dość stanu projekcji dla trzywęzłowego testu smoke Story-005:
  węzły A i B publikują podobne sygnały, węzeł C uruchamia Agorę, a stan progu/
  propozycji jest odbudowywany z przyjętych publicznych rekordów,
- utrzymywać artefakty progu/propozycji semantycznie poniżej `public-gossip.v1`:
  mogą być odtwarzane, kwestionowane, moderowane, ważone reputacją lub ignorowane
  przez lokalną politykę, ale nie publikują leżącej u podstaw historii.

Status:
- `done` dla Agory M4. Magazyn projekcji Agory w Node potrafi projektować publiczne
  rekordy `whisper-signal.v1`, wyprowadzać deterministyczny stan progu dla dwóch
  odrębnych węzłów źródłowych w tej samej grupie `topic/class` +
  `signal/similarity-key`, tworzyć stan projekcji propozycji pokoju zrzeszenia
  i udostępniać pochodne szkice progu/propozycji do podpisu autorytetu projekcji.
  Usługa Agory może podpisywać i przyjmować te rekordy pochodne, gdy dostępny jest
  signer hosta. Pokrycie smoke Story-005 bezpośrednio i z hostowaniem przez daemona
  dowodzi tej samej ścieżki z rzeczywistym HostSignerem daemona.

<a id="planned-assessment-exposure-in-curation"></a>

### Lokalna ekspozycja ocen w kuracji {#local-assessment-exposure-in-curation}

[Profil i tracker P013](../../40-proposals/013-whisper-social-signal-exchange.pl.md#assessment-exposure-profile)
wiążą oceny pogłosek ze [wspólną bramką P026](../../40-proposals/026-resource-opinions-and-discussion-surfaces.pl.md#6-assessment-exposure-and-sealed-rounds).
P013-AE-001 ma status `partial`; P013-AE-002 pozostaje planowane, osobno od
zaimplementowanego Whisper M4. [Lokalny checkpoint P026](../../40-proposals/026-resource-opinions-and-discussion-surfaces.pl.md#local-pilot-evidence-checkpoint-2026-10-24)
kwalifikuje wstrzymywanie i późniejsze renderowanie pól rozszerzeń wiarygodności/
odrzucenia o kształcie pogłoski przez wspólny widok na ogólnej otwartej referencji
zasobu. Dowody te nie wprowadzają osobnego schematu admisji overlayu pogłoski ani
nie kwalifikują pełnego rzeczywistego workflowu kuracji, propagacji i uwagi Whisper.
Należy ponownie użyć walidacji tożsamości/overlayu opinii oraz projekcji hosta Agory
dla widza; nie dodawać magazynu ślepych głosów właściwego Whisper ani nie ukrywać
ocen wyłącznie w UI. [Checkpoint przeglądu](../../40-proposals/026-resource-opinions-and-discussion-surfaces.pl.md#local-pilot-review-evidence-checkpoint-2026-10-24)
ponownie kwalifikuje wspólny lokalny widok, zachowując wyłączenie pełnego workflowu
Whisper. Wiarygodność według innych osób, uzasadnienia, liczniki i kolejność
popularności pozostają konsekwentnie ukryte na powierzchniach kuracji, Agenta,
wyszukiwania i uwagi S039.

Polityka prezentacji nigdy nie wyłącza kontroli propagacji, tłumienia spamu ani
pilnych dowodów ochronnych. Liczniki napływu pogłosek nie są licznikami ocen.
Opcjonalne rundy zamknięte wykorzystują podpisane zamknięcie/wyniki, lecz nie
opóźniają dostarczania pogłosek w oczekiwaniu na kworum. Lokalne ukrywanie niczego
nie twierdzi o innych relayach ani niezależności werdyktu kuracji. Należy użyć
wspólnej macierzy odmów/replayu i fixture'ów Story-005/Agora, zamiast nowego
transportu lub frameworka akceptacyjnego.

### Autorytet projekcji dla twierdzeń o progach i propozycjach {#projection-authority-for-threshold-and-proposal-claims}

Rekordy źródłowe Whisper mają autorstwo nymu lub innej dopuszczonej tożsamości
źródłowej. Rekordy progów i propozycji pokojów zrzeszeń są inne: to pochodne
metasygnały, które muszą być podpisane przez autorytet projekcji.

Dla M4 tym autorytetem może być lokalny węzeł projekcji lub krótkotrwały delegowany
klucz projekcji. Podpis oznacza: "ten autorytet zastosował tę deterministyczną regułę
projekcji Whisper do tych rekordów źródłowych"; nie oznacza, że społeczność przyjęła
leżącą u podstaw historię jako publiczną prawdę.

Ten sam kontrakt powinien dopuszczać przyszły silniejszy autorytet bez zmiany
schematów Whisper. Stały komitet lub komitet wyłoniony na podstawie reputacji może
dostarczać dowody wyboru i kworum obok rekordu pochodnego, a lokalna polityka może
rozstrzygać, czy dla danego skutku w UI lub moderacji wymagany jest pojedynczy
autorytet, kworum zaufane przez społeczność czy bardziej rygorystyczna klasa autorytetu.

## Opcjonalna implementacja {#may-implement}

### Zbiorcze powiadomienia tematyczne {#aggregate-topic-notices}

Based on:
- `doc/project/20-memos/orbiplex-whisper.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.pl.md`

Powiązane schematy:
- `whisper-threshold-reached.v1`

Odpowiedzialności:
- emitować zgrubne powiadomienia zbiorcze po przekroczeniu progu,
- utrzymywać te powiadomienia jako słabsze niż ujawnienie sprawy,
- oddzielać zbiorcze wskazówki odkrywania od wymiany surowych pogłosek.

Status:
- `optional`

### Rezonans uśpionych faktów {#dormant-fact-resonance}

Based on:
- `doc/project/40-proposals/013-whisper-social-signal-exchange.pl.md`
- `doc/project/30-stories/story-014-dormant-contest-entry.md`

Odpowiedzialności:
- rozstrzygać wersjonowany słownik dekorelacji JSON (źródło fabryczne i lokalne
  warstwy P091) oraz walidować względem niego `topic/class`;
- wyprowadzać plan pobierania na epokę z atrapami i pobierać kompletne zgrubne koszyki;
- projektować decyzje o powiązaniu fakt–pogłoska oraz lokalny widok "Moje pogłoski";
- tworzyć powiązane pogłoski dołączające do istniejącego kontekstu pogłoski;
- przekazywać potwierdzone konteksty pokojom zrzeszeń z jawnymi kontrolami udostępniania.

Właściciel funkcji i zadanie grupowania znajdują się w
[rezonansie uśpionych faktów P013](../../40-proposals/013-whisper-social-signal-exchange.pl.md#dormant-fact-resonance-2026-10-27).

Status:
- `future`

### Warunki ujawnienia określane przez autora {#author-disclosure-conditions}

Based on:
- `doc/project/40-proposals/013-whisper-social-signal-exchange.pl.md`
- `doc/project/30-stories/story-014-dormant-contest-entry.md`

Odpowiedzialności:
- weryfikować manifesty embarga podpisane nymem i ich powiązania z chronionym
  sygnałem/admisją; odbiorcy weryfikują publiczny pakiet bez chronionego tekstu;
- wyprowadzać klucze podobieństwa z zatwierdzonych przez autora deskryptorów
  korelacji według wersjonowanych reguł grupowania;
- utrzymywać chroniony materiał w zakresie korelacji, zgodnie z obowiązkami pieczy;
- zliczać odrębne źródła kontekstowe per epoka i poświadczać wynik;
- uwalniać uprzednio zredagowane payloady po commicie uwolnienia przyjętym przez
  autorytet sprawy i domyślnie po potwierdzeniu autora, najwyżej raz na konkretny
  deskryptor audytorium objęty zgodą, niezależnie od tras dostarczenia;
- oddzielać warunki ujawnienia od progów koordynacji.

Projekt i tracker znajdują się w
[warunkach ujawnienia autora P013](../../40-proposals/013-whisper-social-signal-exchange/author-disclosure-conditions.md#author-disclosure-conditions).

Status:
- `future`

### Kooperacyjne maskowanie zainteresowania {#cooperative-interest-masking}

Based on:
- `doc/project/40-proposals/013-whisper-social-signal-exchange.pl.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`

Odpowiedzialności:
- utrzymywać jeden plan pobierania oznaczony pochodzeniem, którego wpisy `need`,
  `decoy` i `cover` obsługuje jeden wykonawca według jednej reguły czasu;
- wysyłać i przyjmować ograniczone żądania osłony bez ujawniania motywu przez
  prywatne Artifact Delivery pod profilem minimalnego śladu;
- wykluczać osłonę z profili zainteresowania, pamięci osobistej i liczników źródeł;
- wspierać mierzone porównanie z niezależnymi atrapami.

Projekt i tracker znajdują się w
[kooperacyjnym maskowaniu zainteresowania P013](../../40-proposals/013-whisper-social-signal-exchange/cooperative-interest-masking.md#cooperative-interest-masking).

Status:
- `future`

### Historyczne autorstwo długowiecznych pogłosek {#historical-authorship-of-long-lived-rumors}

Based on:
- `doc/project/40-proposals/013-whisper-social-signal-exchange.pl.md`
- `doc/project/40-proposals/041-agora-ingest-attestation.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`

Odpowiedzialności:
- zachowywać ważność certyfikatu, retencję, horyzont zliczania i ważność zgody
  jako osobne okresy;
- przechowywać przenośne receipty admisji obok bajtów koperty i weryfikować
  historyczne autorstwo osobno od bieżącego statusu;
- ponownie kontaktować się z autorem starej pogłoski, która napotyka podobną,
  zamiast ponownie zliczać starą pogłoskę;
- utrzymywać jeden klucz ciągłości na sprawę, uporządkowane zdarzenia sprawy
  i świeży status sprawy oraz obsługiwać sukcesję późniejszego nymu związaną ze
  sprawą, dostarczaną wyłącznie wybranemu audytorium.

Projekt i tracker znajdują się w
[długowiecznych pogłoskach P013](../../40-proposals/013-whisper-social-signal-exchange/long-lived-rumors.md#long-lived-rumors-and-historical-authorship).

Format przenośnego receiptu i uwierzytelnione twierdzenie o admisji należą do
[P035-019](../../40-proposals/035-agora-topic-addressed-record-relay.md#portable-admission-receipts-2026-10-27),
a nie do drugiej implementacji receiptów w Whisper. Niezmieniona reguła awansu
oparta wyłącznie na agregacie znajduje się w [warstwie implementacyjnej 7](011-whisper-impl.md#layer-7-threshold-detection-and-durable-promotion).

[P013-LLR-009](../../40-proposals/013-whisper-social-signal-exchange/long-lived-rumors.md#portable-case-succession-verification)
planuje ograniczoną przenośną weryfikację sukcesji przez tych właścicieli P015/P035.
Zachowuje rozdział historycznego dowodu kotwicy, autentycznej sukcesji i bieżącego
autorytetu sprawy, z akceptacją bez pobierania i bez ujawniania prywatnej kotwicy
jedynie w celu skompletowania pakietu. Stosuje międzyartefaktową regułę weryfikacji
P032; P076 jest przykładem zakwalifikowanego konsumenta, nie właścicielem profilu
Whisper. [Macierz rodzin](../../40-proposals/013-whisper-social-signal-exchange.pl.md#portable-verification-profiles)
obejmuje też sygnały, powiadomienia, dowody embarga i kontrolę sprawy, bez dodawania
podpisów do żądań osłony CIM celowo uwierzytelnianych sesyjnie.

Status:
- `future`

### Wspólne granice implementacyjne {#shared-implementation-boundaries}

Planowane kontynuacje współdzielą mechanizmy zgodnie z
[rozstrzygnięciami re-use P013](../../40-proposals/013-whisper-social-signal-exchange.pl.md#implementation-reuse):
jeden wykonawca pobierania na epokę, jeden ewaluator wkładów kontekstowych
z osobnymi politykami koordynacji/ujawniania, jeden właściciel porządku sprawy
oraz weryfikacja dowodów P015/P035. AD zachowuje odpowiedzialność za dostarczenie
i ponowienia. Zalecenia wskazują też małe granice ponownego użycia porównania czół
i przygotowanego wyjścia, bez scalania pieczy wystawcy, autorytetu sprawy ani
statusu transportu. Są to ograniczenia projektowe istniejących trackerów,
a nie dodatkowe zaimplementowane capabilities.

## Poza zakresem {#out-of-scope}

- anonimowość warstwy transportowej i topologia przekaźników
- docelowe zarządzanie ustrojowe lub rozstrzyganie sporów
- automatyczne ujawnianie sobie tożsamości
- twarde semantyczne tłumienie duplikatów w v1
- używanie Agory do prywatnych/bezpośrednich treści pogłosek lub treści `private-correlation`

## Konsumuje {#consumes}

- `whisper-signal.v1`
- `whisper-interest.v1`

## Wytwarza {#produces}

- `whisper-signal.v1`
- `whisper-interest.v1`
- `whisper-threshold-reached.v1`
- `association-room-proposal.v1`

## Powiązane dane capabilities {#related-capability-data}

- [Ustrukturyzowany katalog capabilities](011-whisper-caps.edn)

## Uwagi {#notes}

Przyjmowanie/redakcja Whisper są zaimplementowane jako nadzorowana usługa middleware
`channel_json`, z osobno zarządzaną powierzchnią HTTP przyjmowania/śladów/operatora.
Wspólna semantyka niezależna od transportu należy do `whisper-core`; Agora pozostaje
podłożem rekordów publicznych/federacyjnych, a daemon – hostem/supervisorem
oraz granicą capabilities.

Granica prywatnego utrwalania:

```text
whisper-intake
  -> host capability sealer.seal
  -> host capability memarium.write(space = personal)
```

`whisper-intake` powinien uwierzytelniać się wobec API capabilities hosta tokenem
capability dostarczonym przez host i identyfikować się jako `whisper-intake`, aby
daemon mógł zastosować kontekst komponentu runtime. Brak grantów `sealer.seal`
lub `memarium-space-access` dla `memarium/write` na `personal` powinien być widoczny
w lokalnej bramce gotowości. Synchronizacja w runtime jest automatyczna i działa
w trybie best-effort, ale UI musi udostępniać operatorom ręczną akcję ponowienia.

Granica przygotowania redakcji:

```text
whisper-intake
  -> host capability whisper.redaction.prepare
  -> configured provider
  -> whisper-redaction-prepare-response.v1
  -> local redaction draft
```

Dostawca nie jest autorytetem publikacji. Może zwrócić `draft-ready`,
`needs-human-review`, `unsafe-output`, `policy-denied`, `model-unavailable`,
`retryable-timeout` lub `failed`; tylko pierwsze dwa statusy mogą przenosić szkic,
a nawet wtedy przejście zatwierdzenia przez operatora pozostaje osobne.

P090-006e dodaje opcjonalne przenoszenie `middleware-observed-result.v1` wokół tej
niezmienionej odpowiedzi. Należący do hosta sidecar wiąże dokładne bajty;
przyjmowanie atomowo zapisuje prywatny wynik i szkic oraz weryfikuje odczyt
z zachowanego zapisu. Brak pochodzenia pozostaje niewiadomą, także dla
deterministycznych przekształceń dowolnego wejścia Sensorium. Ten częściowy
checkpoint nie daje uprawnień do publikacji ani nie deklaruje domknięcia cyklu
życia. Prywatna synchronizacja pieczętuje teraz dokładny zachowany wrapper pod
osobnym kluczem idempotencji adresowanym deskryptorem; nie uruchamia ponownie
redakcji. Ręczne zapisy szkicu usuwają powiązanie ze źródłem, także przy identycznych
bajtach. Pełna kwalifikacja transportu/odzyskiwania Memarium oraz odzyskiwanie
odroczone/terminalne pozostają w trackerze P090.
Schemat żądania celowo pozostawia na razie szerokie `raw/private-material`, aby
pierwsi dostawcy mogli przenosić ustrukturyzowane koperty wejściowe, surowe ciągi
znaków lub wartości fixture'ów przez tę samą granicę wyłącznie loopbackową.
Docelowy stabilny kontrakt ma zawęzić to pole do `object|string` po uzgodnieniu
zachowania dostawców i testów.

Gdy obecny jest `Monus`, Whisper powinien traktować go jako wcześniejszy lokalny
moduł przygotowania szkiców, a nie równorzędny autorytet publikacji. Monus może
przygotowywać kandydackie szkice obaw, ale Whisper i host nadal odpowiadają za
ograniczoną ścieżkę publikacji wychodzącej.

`whisper-core` zawiera już prymitywy polityki o kształcie produkcyjnym dla klasy
źródła, trybu błędu routingu, dowodów przekaźnika, budżetu przekazywania, decyzji
obniżenia prywatności, wyjaśnień polityki korelacji, cyklu życia propozycji pokoju
zrzeszenia i awansu do publicznej pogłoski. Są to kontrakty danych i czyste funkcje
decyzyjne; konkretne możliwości UI i rzeczywiste wykonanie przekaźników należą do
późniejszych warstw runtime/produktowych, które konsumują te same dane zamiast
zmieniać semantykę rdzenia Whisper.
