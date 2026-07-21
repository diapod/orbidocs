# Współpraca agentów: FAQ

## Z jakich komponentów składa się współpraca agentowa?

Corpus organizuje pytanie, wybór providerów, bidy, rozliczenie i odpowiedź. Room
utrzymuje członkostwo, politykę oraz efemeryczny kanał deliberacji. Agent prowadzi
ograniczoną sesję wykonawczą pod authority hosta, a Inquirium normalizuje operacje
wnioskowania wobec konkretnego runtime'u modelu. Sensorium Interfaces może dołączyć
atestowany widok działającego środowiska. Żaden z tych komponentów nie zastępuje
pozostałych.

Sekwencję operacyjną opisuje [HOWTO współpracy
agentów](../howto/collaborative-agents-howto.pl.md).

## Czym Room różni się od Corpusu?

Room odpowiada na pytanie: „kto może uczestniczyć, według jakiej polityki i przez
którą aktualną epokę carriera?”. Corpus odpowiada: „jakie pytanie rozwiązujemy, kto
złożył bid, kogo wybrano, jakie role obowiązują i którą odpowiedź zaakceptowano?”.
Room nie jest ledgerem zamówienia ani odpowiedzi, a Corpus nie implementuje własnego
transportu live.

## Czym Agent różni się od Inquirium?

Agent posiada node-local lifecycle, budżet, binding, pamięć roboczą, ślad i propozycje
efektów. Inquirium wykonuje pojedynczą semantyczną operację wnioskowania przez wybrany
adapter modelu. Adapter ani model nie stają się Agentem; nie posiadają sesji Corpusu,
członkostwa Roomu ani authority do publikacji i efektów.

## Jak agenci deliberują: protokołem strukturalnym czy językiem naturalnym?

Obie warstwy są potrzebne. Treść tury może być ograniczonym `text/plain`, natomiast
jej envelope jest strukturalny: ma query, Room, uczestnika, assignment, `turn/no`,
classification, digest, expiry i idempotency key. Role, instruction overlays,
evidence refs, odpowiedź oraz podpis są osobnymi kontraktami. Naturalny język niesie
argument; protokół niesie authority, kolejność, pochodzenie i granice.

## Kto zarządza deliberacją?

Requester może wyznaczyć własnego, ograniczonego Agenta jako chair delegate. Chair
porządkuje pytania, przydziela role, proponuje instrukcje, syntetyzuje tury i tworzy
answer draft. Nie może jednak sam przyjąć draftu jako domenowej odpowiedzi ani nadać
sobie szerszych grantów. Corpus authority i lokalna polityka zachowują ostatnie słowo.

## Czy chair może nadawać role i prompty uczestnikom?

Może proponować role oraz bounded instruction overlays, lecz propozycja pozostaje
nieaktywna do czasu przyjęcia przez lokalną politykę lub uczestnika. Tekst overlayu nie
jest bezpośrednim promptem adaptera. Host renderuje przyjętą instrukcję deterministycznie
i dołącza ją w swojej warstwie prompt policy tuż przed wywołaniem Inquirium.

## Kto publikuje końcową odpowiedź?

Agent tworzy wyłącznie inert, content-addressed outcome lub answer draft. Corpus
sprawdza binding, Room evidence, wybrany bid, policy digest, content digest,
classification i podpis. Osobne, autoryzowane przejście publikuje
`corpus-reasoning-answer.v1`. Model output nigdy nie jest równoznaczny z publikacją.

## Czy członkostwo w Roomie daje dostęp do live feedu?

Nie. Odbiorca musi jednocześnie mieć aktualne członkostwo Roomu i dokładny grant
Sensorium Interface. Projekcja rewaliduje oba zbiory authority przy emisji. Odwołanie
któregokolwiek zamyka dostęp, a sam relay pozostaje jedynie carrierem.

## Czy read-only terminal pozwala agentowi wykonywać komendy?

Nie. `latest-state` może pokazać ograniczony viewport terminala, lecz nie nadaje
actuation authority. W profilu Story-012 tylko lokalny kontroler węzła A modyfikuje
środowisko. Zdalne sterowanie wymaga osobnego grantu, aktualnej control lease,
fencingu generacji i schema-gated operacji P083.

P083 to
[proposal Sensorium Interactive Interfaces](../../project/40-proposals/083-sensorium-interactive-interfaces.md):
definiuje aktuacyjną połowę mechanizmu, uzupełniającą powierzchnię read/subscribe
wypromowaną jako
[Solution 046](../../project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md).

## Co jest trwałe, a co efemeryczne?

Trwałe są fakty query, bidów, selekcji, polityki, członkostwa, assignmentów, overlayów,
Agent lifecycle, digestów tur, draftu i opublikowanej odpowiedzi. Treść live Roomu oraz
terminal viewport są domyślnie efemeryczne i ograniczone buforem. Restart odtwarza
authority i kursory, nie udaje odzyskania nieutrwalonej treści.

## Czy współpraca działa przez sieć?

Room ma relokowalny WSS/TLS relay z epokami, failoverem i atestacją członkostwa.
Uczestnicy mogą wykonywać wyłącznie połączenia wychodzące do jednego osiągalnego
endpointu aktywnej epoki. Natomiast Story-011 i Story-012 są acceptance
multi-address single-host: sprawdzają realne granice procesów i TCP/WSS, lecz nie
dowodzą publicznej osiągalności, niezależnych hostów ani przejścia przez NAT.

## Czy Room wymaga Matrixa albo hole punchingu?

Nie. Bazowy carrier to WSS/TLS relay; STUN/ICE, UDP i hole punching nie są warunkiem
żywotności. Matrix pozostaje opcjonalnym bridge profile dla przyszłych integracji, nie
drugą semantyką Roomu. Direct peer może zoptymalizować latencję sterowania, lecz nie
nabywa authority i nie jest wymagany do deliberacji.

## Co się dzieje, gdy relay ulegnie awarii?

Nowy podpisany `room-relay-endpoint.v1` ustanawia nową epokę. Nie scala się buforów
efemerycznych między epokami. Klienci rewalidują membership, authority i aktualny
endpoint, a następnie odświeżają stan z trwałych faktów i bieżących source views.
Awaria carriera zmniejsza liveness; nie usuwa Roomu jako zbioru faktów.

## Jak requester zatrzymuje pracę po uzyskaniu odpowiedzi?

Requester może oznaczyć rundę jako `requester-satisfied`. To jawne, domenowe przejście
kończy dalsze zbieranie pracy dla danej rundy. Nie należy wyprowadzać zakończenia z
milczenia na kanale ani z arbitralnej decyzji modelu.

## Jakie acceptance najlepiej pokazują cały mechanizm?

Story-011 sprawdza trzy węzły, provider discovery, bidy, Room, agentowe tury, chairing,
Inquirium, odpowiedź i `requester-satisfied`. Story-012 rozszerza ten przepływ o
read-only Workbench terminal przez Sensorium Interfaces, niezależne granty B/C,
rewokację, restart i lokalnie wykonywaną naprawę.
