# Współpraca agentów: HOWTO

Ten HOWTO składa jeden przepływ z Room, Corpus, Agent, Inquirium, Sensorium Interfaces
i Workbench. Nie tworzy nowego superkomponentu: każde przejście pozostaje własnością
warstwy, która rozumie jego skutek. Krótsze wyjaśnienia znajdują się w
[FAQ współpracy agentów](../faq/collaborative-agents-faq.pl.md).

Jeżeli polecenie nie stanowi inaczej, wszystkie poniższe komendy `cargo` i
`tools/...` uruchamiaj z katalogu głównego workspace'u `node/`.

## Zacznij od mapy odpowiedzialności

| Komponent | Wnosi do przepływu | Nie może przejąć |
|---|---|---|
| Shared Offer Catalog | topic-indexed oferty providerów | selekcji zwycięzcy i Roomu |
| Corpus | query, bidy, wybór, role, answer acceptance | transportu live i model runtime |
| Room | membership, policy, attestation, relay epoch, live carrier | authority odpowiedzi i feedu |
| Agent | bounded lifecycle, binding, kontroler, trace, inert outcomes | ambient effects i publikacji |
| Inquirium | semantyczne operacje inference i neutralność providera | pętli Agent i narzędzi |
| Sensorium Interfaces | read/subscribe oraz osobne actuation grants | członkostwa Roomu |
| Workbench | izolowany terminal i jawne profile komend/plików | zdalnej authority bez lease |
| Interaction Broker | bounded wait/watch zasobów | domenowego stanu Corpusu |

P083 oznacza w tym dokumencie
[Sensorium Interactive Interfaces](../../project/40-proposals/083-sensorium-interactive-interfaces.md):
kontrakt aktuacji uzupełniający powierzchnię read/subscribe wypromowaną jako
[Solution 046](../../project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md).

## Sprawdź prerequisite'y i granicę dowodu

Przed uruchomieniem przepływu sprawdź:

1. zaufany Seed Directory i aktualne passporty `corpus.provider`;
2. topic taxonomy oraz aktywne oferty o zgodnym taxonomy digest;
3. skonfigurowany outbound AD i admission query/answer;
4. aktywny Room relay profile oraz membership-attestation signer;
5. routowalny Inquirium runtime z aktualnym conformance evidence;
6. dla live feedu: descriptor Sensorium Interface, source authority i osobne grants;
7. dla terminala: lokalny Workbench profile oraz proces fixture.

Story-011/012 używają trzech adresów loopback na jednym hoście. To mocniejsza izolacja
niż trzy porty jednego adresu, lecz nadal wspólny kernel, zegar, filesystem i failure
domain. Nie opisuj takiego wyniku jako production federation E2E.

## Opublikuj oferty providerów Corpusu

Provider publikuje zwykłe `service-offer.v1` z rozszerzeniem Corpus, canonical topic i
taxonomy digest. Shared Offer Catalog odpowiada za supersession, expiry, full
withdrawal i partial-topic removal. Corpus nie utrzymuje równoległego katalogu ofert.

Przed query sprawdź, czy topic index zwraca tylko aktywne wersje ofert i czy provider
ma świeży passport `corpus.provider` odkrywalny przez Seed Directory.

## Utwórz i dispatchuj query

Requester tworzy `corpus-reasoning-query.v1` przez:

```http
POST /v1/corpus/queries
POST /v1/corpus/queries/dispatch
```

Query wiąże `question-envelope.v1`, canonical `topic/term`, taxonomy digest, keywords,
przedział ceny w minor units, deadline, limit kandydatów oraz reply target. Dispatch
używa AD `capability-many`; brak odpowiedzi, odmowa polityki, timeout i błąd transportu
pozostają odrębnymi stanami read-modelu.

## Zbierz bidy i wybierz providera

Provider przyjmuje query przez Corpus acceptor i zwraca podpisany
`corpus-reasoning-bid.v1`. Requester odczytuje rundę, a potem jawnie wybiera bid:

```http
GET  /v1/corpus/rounds/{query_id}
POST /v1/corpus/rounds/{query_id}/select
```

Wybór sprawdza query bracket, walutę, taxonomy, provider identity, expiry i podpis.
Counter price poza przedziałem nie przechodzi przez przypadkową normalizację; wymaga
jawnej akceptacji requestera. Wybrany bid przechodzi do zwykłej ścieżki procurement.

## Otwórz Room i aktywuj relay epoch

Po wyborze uczestników otwórz Room powiązany z rundą:

```http
POST /v1/corpus/rounds/{query_id}/room
POST /v1/corpus/rounds/{query_id}/room/relay/activate
```

Polityka powinna ustalać accountable chair, access list, classification, bounded
retention metadanych oraz live limits. Relay epoch porządkuje efemeryczne frames, lecz
nie tworzy membership ani answer authority. Produkcyjny deployment publikuje podpisany
`room-relay-endpoint.v1`; testowy locator `.invalid` jedynie ogrodzi lokalną epokę i nie
udaje publicznego TLS endpointu.

## Zaproś uczestników i potwierdź gotowość

Utwórz podpisany, content-addressed invite i dostarcz go przez AD:

```http
POST /v1/corpus/rounds/{query_id}/room/invites
POST /v1/corpus/room-invites/{invite_id}/join
POST /v1/corpus/room-invites/{invite_id}/ready
```

Join wymaga świeżej `room-membership-attestation.v1`. Dokładny replay invite'a powinien
zwrócić tę samą identity; zmiana treści pod tym samym idempotency key jest konfliktem.
Raw model binding nie jest uczestnikiem Roomu. Uczestnikiem jest accountable subject,
ewentualnie reprezentowany przez node-local Agent.

## Zwiąż node-local Agent z uczestnikiem

Na każdym węźle utwórz Agent z bounded profilem, budżetem i grantami, a następnie binding
do konkretnej rundy, Roomu, uczestnika i output sink. Binding powinien wskazywać
przyjęte Room evidence; nie interpoluj authority refs z model outputu ani z dowolnego
JSON-e Flow.

Agent controller może żądać Inquirium, obserwacji lub efektu. Host wykonuje każdą
operację dopiero po odrębnej admission. Child Agent może wyłącznie zawężać authority i
budżet rodzica.

## Nadaj rolę i instruction overlay

Chair proponuje role oraz instrukcje przez osobne append-only powierzchnie:

```http
POST /v1/corpus/rounds/{query_id}/role-assignments
POST /v1/corpus/rounds/{query_id}/role-assignments/{assignment_id}/decide
POST /v1/corpus/rounds/{query_id}/instruction-overlays
POST /v1/corpus/rounds/{query_id}/instruction-overlays/{overlay_id}/decide
```

Przykładowa semantyka roli to „audytor konfiguracji” albo „administrator Postfix”, nie
nowy capability grant. Lokalny host lub uczestnik przyjmuje assignment. Overlay source
pozostaje inert; host renderuje bounded `instruction/rendered` według zarejestrowanej
polityki i ponownie weryfikuje digest przed każdym wywołaniem Inquirium.

## Prowadź deliberację przez inert turns

Agent wywołuje Inquirium przez host capability, otrzymuje wynik i proponuje
`corpus-reasoning-turn-proposal.v1`. Dopiero admitted efekt `corpus.room.turn` wysyła
turę do Roomu. Pierwszy profil przyjmuje `text/plain`, ale wymaga strukturalnego
envelope z assignmentem, `turn/no`, digestem, classification, expiry i idempotency.

```http
POST /v1/corpus/room-invites/{invite_id}/messages
```

Chair obserwuje przyjęte tury przez Interaction Broker watch. Polling adaptera modelu
nie powinien stać się drugim event loopem ani źródłem Room authority.

## Dołącz live Sensorium feed

Źródło publikuje immutable Sensorium Interface descriptor i status. Dla terminala
użyj cursor-free `latest-state`, jeżeli odbiorcom wystarczy bieżący viewport. Następnie:

1. wydaj dokładny observe grant dla B i C;
2. uruchom projekcję przez aktualny Room relay;
3. zwiąż opaque Agent observation need z konkretnym source ref;
4. przy każdym odczycie sprawdź Room membership, interface grant, source generation,
   effective publication, classification, freshness i byte cap;
5. zachowaj w trwałym trace tylko refs, digests i causal context.

Room membership bez interface grantu oraz interface grant bez Room membership muszą
zostać odrzucone. Zmiana generacji źródła lub supersession publikacji czyni stary widok
stale; Agent nie może sam wybrać wcześniejszej, łagodniejszej klasy operational impact.

## Zachowaj lokalną kontrolę nad terminalem

W profilu read-only propozycje B/C i chaira pozostają poradami. Tylko lokalny operator
lub jawnie autoryzowany kontroler węzła A wpisuje komendy do Workbench i interpretuje
rezultat. Nie przesyłaj keystrokes jako zwykłych Room messages.

Jeżeli potrzebujesz zdalnego sterowania, użyj oddzielnej ścieżki Sensorium Interface
actuation: exact grant, control request, lease, generation, epoch, sequence i typed
terminal operation. Direct peer może obniżyć latencję, lecz relay fallback zachowuje
ten sam fencing i nie przejmuje authority.

## Utwórz, zaakceptuj i opublikuj answer draft

Chair Agent syntetyzuje tury i tworzy content-addressed draft. Przyjęcie draftu nie
publikuje odpowiedzi:

```http
POST /v1/corpus/rounds/{query_id}/agent-drafts/accept
POST /v1/corpus/rounds/{query_id}/agent-drafts/publish
```

Pierwsza operacja sprawdza Agent binding, Room evidence, embedded schemas i actor-bound
idempotency. Druga wymaga osobnej authority, podpisuje
`corpus-reasoning-answer.v1` i wiąże answer z selected bid oraz policy digest. Dzięki
temu model, Agent i chair nie mogą pomylić „gotowego tekstu” z „opublikowanym faktem”.

## Rozlicz i zakończ rundę

Po przyjęciu odpowiedzi przeprowadź zwykłe procurement settlement, a gdy requester
uzna wynik za wystarczający, zakończ rundę:

```http
POST /v1/corpus/rounds/{query_id}/settle
POST /v1/corpus/rounds/{query_id}/satisfy
```

`requester-satisfied` jest jawne i idempotentne. Nie kończ rundy na podstawie samego
braku nowych messages, disconnectu relaya albo deklaracji modelu.

## Obsłuż rewokację, restart i relay failover

Po revocation observera poczekaj, aż source-side audience projection potwierdzi nowy
zbiór odbiorców, zanim opublikujesz kolejny stan. Recipient restart odtwarza trwały
Agent binding i Room invitation, lecz process-local latest-state inbox startuje pusty.
Source restart wymaga ponownego uruchomienia efemerycznej projection pump.

Relay failover tworzy nową epokę bez merge'a efemerycznych sekwencji. Klient pobiera
aktualny endpoint niezależną ścieżką, rewaliduje authority i odświeża current state.

## Uruchom Story-011

Na macOS przygotuj aliasy loopback jawnie; runner nigdy nie uruchamia `sudo`:

```sh
sudo python3 tools/acceptance/loopback_aliases.py ensure 127.0.0.2 127.0.0.3
```

Następnie uruchom zarządzany smoke:

```sh
python3 tools/acceptance/story-011-corpus-fish/story-011-local-profiles.py \
  --home /tmp/orbiplex-story011 --regenerate-peer-certs \
  ad-smoke --timeout-seconds 180
```

Bez uprawnień do aliasów wybierz słabszy profil jawnie, przed subcommandem:

```sh
python3 tools/acceptance/story-011-corpus-fish/story-011-local-profiles.py \
  --network-profile single-address-single-host \
  --home /tmp/orbiplex-story011-single-address ad-smoke
```

## Uruchom Story-012

Najpierw sprawdź composition gate, potem wykonaj smoke:

```sh
python3 tools/acceptance/story-012-shared-chair-terminal/profile_plan.py preflight
python3 tools/acceptance/story-012-shared-chair-terminal/profile_plan.py \
  smoke --timeout-seconds 180
```

Wariant bez aliasów:

```sh
python3 tools/acceptance/story-012-shared-chair-terminal/profile_plan.py \
  smoke --timeout-seconds 180 \
  --network-profile single-address-single-host
```

## Diagnozuj od authority do carriera

| Objaw | Najpierw sprawdź |
|---|---|
| brak providerów | taxonomy digest, aktywne oferty, passporty i Seed Directory trust |
| bid nie przechodzi | podpis, query binding, deadline, currency i price bracket |
| join odrzucony | invite digest, membership attestation, epoch i subject |
| Agent nie może wysłać tury | assignment, overlay decision, grant i effect admission |
| chair nie widzi tury | Room high-water, Interaction Broker watch i replay cursor |
| observer nie widzi feedu | przecięcie membership i interface grant, generation i publication |
| terminal jest widoczny, lecz nie sterowalny | to poprawne dla profilu read-only; sprawdź osobny actuation grant |
| draft istnieje, lecz brak answer | oddzielne Corpus publish authority i podpis |
| reconnect traci live content | live content jest efemeryczny; odśwież fakty i current state |

Najpierw wskaż warstwę, która odmówiła. Omijanie jej przez ręczne wywołanie późniejszego
endpointu niszczy dowód związania i zwykle tworzy nieodtwarzalny read model.

## Dokumenty źródłowe

- [Solution 036: Room](../../project/60-solutions/036-room/036-room.md)
- [Solution 038: Corpus](../../project/60-solutions/038-corpus/038-corpus.md)
- [Solution 042: Sensorium Workbench](../../project/60-solutions/042-sensorium-workbench/042-sensorium-workbench.md)
- [Solution 044: Inquirium](../../project/60-solutions/044-inquirium/044-inquirium.md)
- [Solution 046: Sensorium Interfaces](../../project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md)
- [Solution 047: Agent](../../project/60-solutions/047-agent/047-agent.md)
- [Story-011](../../project/30-stories/story-011-corpus-fish.md)
- [Story-012](../../project/30-stories/story-012-agents-share-chair-terminal.md)
