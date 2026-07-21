# FAQ JSON-e i JSON-e Flows

## Jaki problem rozwiązują JSON-e i JSON-e Flow?

Wypełniają przestrzeń pomiędzy zachowaniem zaszytym w hoście a pełnym procesem
middleware. JSON-e przekształca jawnie wyprojektowany kontekst JSON w inną wartość
JSON. JSON-e Flow otacza takie przekształcenia małą, statyczną sekwencją kroków
interpretowanych przez hosta. Operator lub autor pakietu może dzięki temu budować
czytelne adaptery bez dokładania procesu, portu, prywatnego API ani ogólnego runtime'u
skryptowego.

Kanoniczny projekt opisuje [Proposal 049](../../project/40-proposals/049-json-e-middleware-transformer-executor.md).
Konfiguracja i wykonywalne przykłady znajdują się w [HOWTO JSON-e i JSON-e
Flows](../howto/json-e-and-json-e-flows-howto.pl.md).

## Czym różni się JSON-e od JSON-e Flow?

`json_e` jest czystym transformatorem danych:

```text
wyprojektowany kontekst -> szablon JSON-e -> wartość JSON po schema gate
```

`json_e_flow` jest ograniczonym przejściem należącym do hosta:

```text
wyprojektowany kontekst -> render/validate/call/extract/... -> odpowiedź
```

JSON-e interpretuje szablony. Runtime przepływu interpretuje statyczną listę kroków i
jest właścicielem każdego efektu. Szablon nie może zmienić się w przepływ przez
wyrenderowanie nazwy capability ani nowego kroku.

## Gdzie znajdują się na mapie architektury?

Są klasami executorów middleware w [Solution
019](../../project/60-solutions/019-middleware/019-middleware.md). Konkretna
konfiguracja pozostaje pełnoprawnym komponentem middleware: ma własne identyfikatory,
bindingi, limity, tożsamość śladu, pochodzenie pakietowe i cykl operatorski.

Nie zastępują organów domenowych. Inquirium nadal odpowiada za zapytania do modeli,
Sensorium za sygnały i sprawcze działanie, Memarium za fakty, Artifact Delivery za
dostarczanie, a Agent za cykl życia agentów. JSON-e może kształtować wartości na tych
granicach; JSON-e Flow może je przekraczać wyłącznie przez dopuszczone host
capabilities.

Implementacja ma dziś jedną asymetrię operacyjną: `middleware-runtime` implementuje
oba executory, lecz daemon rejestruje providery z konfiguracji operatora tylko przez
`middleware_json_e_flow_services`. Czystą transformację można osadzić bezpośrednio
przez runtime executor; aby wdrożyć równoważne zachowanie jako provider daemona, należy
dziś użyć bezefektowego przepływu z krokami `render`, `validate` i `respond`.

## Czy szablon JSON-e ma jakąkolwiek władzę?

Nie. Widzi tylko pola wybrane przez operatorskie `context_projection` oraz jawnie
udostępnione czyste helpery. Nie może czytać plików, otwierać gniazd, uruchamiać
procesów, zmieniać storage, oglądać wnętrza daemona ani wywoływać capability.

To własność bezpieczeństwa, a nie tylko wygoda implementacyjna. Wartość obecna w
pierwotnym żądaniu nie staje się automatycznie widoczna dla szablonu.

## Czy `allowed_calls` nadaje przepływowi uprawnienie do efektu?

Nie. `allowed_calls` dopuszcza jedynie statyczny kształt kroku `call`. Przed efektem
host nadal sprawdza komponent wywołujący, bieżący hook, paszport lub grant capability,
lokalną politykę, rozmiar żądania, timeout i stan odwołania.

Niektóre rodziny capabilities dokładają osobną warstwę. `inquirium.generate` wymaga
pasującego wpisu `inference_grants`, natomiast wywołania `agent.*` wymagają
`agent_grants`. Przepływ nie może poszerzyć takiego grantu przez wyrenderowane dane.

## Jakie rodzaje kroków obsługuje JSON-e Flow?

Obecny profil ma sześć statycznych rodzajów:

| Rodzaj | Odpowiedzialność |
| :--- | :--- |
| `render` | Interpretuje szablon JSON-e do nazwanej wartości przepływu. |
| `validate` | Waliduje nazwaną wartość według kontraktu znanego hostowi. |
| `call` | Prosi hosta o wywołanie literalnej, dozwolonej capability. |
| `extract` | Wybiera podwartość z wcześniejszego nazwanego wyniku. |
| `respond` | Zwraca nazwaną wartość wywołującemu. |
| `fail` | Kończy przejście jawną, kontrolowaną porażką. |

Obecny profil nie ma dynamicznych kroków, nazw capabilities wybieranych z wejścia,
niejawnych pętli ani dowolnego kodu.

## Kiedy używać czystego JSON-e?

Do deterministycznego konstruowania wartości: normalizacji, wyboru pól, adnotacji,
decyzji routingowych, małych przepisów i odpowiedzi o określonym schemacie. Jest dobrym
wyborem, gdy zachowanie da się przejrzeć jako transformację danych i nie wymaga efektu,
retry, długowiecznego stanu ani prywatnej integracji.

## Kiedy używać JSON-e Flow?

Gdy transformacja pozostaje krótka i statyczna, lecz potrzebuje kilku efektów
należących do hosta, na przykład odpytania Inquirium, wywołania dyrektywy Sensorium,
zapisu faktu Memarium, publikacji ukończenia kroku workflow albo wysłania artefaktu
przez Artifact Delivery.

Jeżeli definicja przeradza się w dynamiczną orkiestrację, szerokie rozgałęzienia,
rozbudowaną politykę domenową, powtarzalne pętle albo mutowalny scratch state, należy
przejść do middleware opartego na kodzie. Podnoszenie limitów, aż JSON-e Flow zacznie
przypominać język programowania, pogarsza poznawalność bez odzyskania narzędzi
prawdziwego języka.

## Czy JSON-e Flow jest silnikiem workflow?

Nie. Jest ograniczonym przejściem należącym do pojedynczego wywołania middleware. Nie
jest właścicielem workflow domenowego, schedulingu, odkrywania providerów, konsensusu
rozproszonego ani trwałego stanu biznesowego. Trwałe czekanie i wznowienie deleguje do
hostowego mechanizmu bounded deferred operations; historia domenowa pozostaje w
komponencie domenowym.

## Jak obsługiwane są odroczone odpowiedzi host capability?

Przy `deferred_response_mode = "surface-to-caller"` (wartość domyślna) oczekujące
`deferred-operation.v1` staje się wynikiem control-plane. Obecny daemon zapisuje
pierwotne wywołanie i identyfikator odroczonego kroku. Gdy nadejdzie ukończony
`deferred-operation-status.v1`, ponownie interpretuje statyczny przepływ i wstrzykuje
status w pasującym wywołaniu. Wywołania poprzedzające odroczony krok muszą więc być
idempotentne. Przepływ nie prowadzi prywatnego pollingu ani nie wybiera częstotliwości
retry i TTL.

Przy `reject-as-failure` każda odpowiedź odroczona kończy synchroniczne przejście
błędem `deferred-not-accepted`. Zobacz [Solution 029: Bounded Deferred
Operations](../../project/60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md).

## Czy przepływ może bezpośrednio wołać usługę middleware?

Nie powinien. Należy wywoływać stabilną host capability, nie loopback endpoint lub
prywatną trasę providera. Daemon wybiera providera, stosuje politykę, waliduje kontrakt
i zapisuje ślad. Bezpośrednie wywołanie sprzęgłoby przepływ z jedną implementacją i
omijało granicę władzy hosta.

## Czy JSON-e Flow może razem używać Inquirium i Sensorium Workbench?

Tak, lecz warstwy pozostają rozdzielone. Inquirium może wytworzyć poradę albo
ustrukturyzowaną intencję. JSON-e Flow może wyrenderować z niej dyrektywę Sensorium.
Sensorium i Workbench sprawdzają potem i wykonują tylko to, na co pozwala ich własna
polityka. Wynik modelu nie staje się władzą wykonawczą tylko dlatego, że szablon umieścił
go w żądaniu.
[FAQ Sensorium](sensorium-faq.pl.md) wyjaśnia rozróżnienie Action/Operation i pełną
ścieżkę władzy.

## Czy JSON-e Flow może wysyłać lub przyjmować artefakty Artifact Delivery?

Dla wysyłki przepływ może wyrenderować `artifact-delivery-envelope.v1` i wywołać
`artifact.delivery.send`, jeżeli capability jest statycznie dopuszczona i
autoryzowana.

Dla przyjęcia artefaktu skonfigurowany acceptor JSON-e Flow jest celowo czysty: musi
zwrócić `InboundAdmissionResult` i nie może deklarować host-capability calls. Predykat
przyjęcia wykonujący efekty splatałby decyzję o dopuszczeniu artefaktu z działaniem na
nim. Zobacz [HOWTO Artifact Delivery](../howto/artifact-delivery-howto.pl.md#json-e-flows).

## Czy przepływ może widzieć surowe wejście lub wcześniejsze I/O komponentów?

Tylko przez jawny kontrakt [Raw Signal Access](../../project/40-proposals/053-raw-signal-access.md).
Konkretny przepływ musi zadeklarować `raw_signal_access`, lokalna polityka musi na to
pozwolić, a `context_projection` nadal musi wyprojektować dozwoloną wartość do
kontekstu autorskiego. Deklaracja, zachowanie i projekcja są trzema osobnymi bramkami.

Jeżeli wystarcza digest, klasyfikacja albo wąski wybór pól, należy preferować tę
postać. Ślady nie mogą stawać się drugim magazynem wejść zawierających sekrety.

## Jakie cechy JSON-e i helpery są dostępne?

Profil zachowuje rozpoznawalny JSON-e, w tym interpolację oraz ograniczone konstrukcje
`$eval`, `$if`, `$switch`, `$match`, `$let`, `$map`, `$reduce`, `$merge`,
`$mergeDeep`, `$flatten` i `$json`. Obecny profil helperów hosta to
`orbiplex.json_e.helpers.basic.v1`; jawnie wybiera się w nim helpery spośród
`sha256_json`, `sha256_text`, `default`, `has`, `pick` i `idempotency_key`.

Helpery są czyste i wersjonowane. Profil nie może po cichu zmieniać ich semantyki;
zmiana wpływająca na wynik wymaga nowej wersji profilu i jawnej migracji.

## Jak klasyfikowane są awarie?

Runtime rozdziela błędy konfiguracji i ładowania szablonu, projekcji kontekstu,
ewaluacji, limitów zasobów, walidacji kontraktu wyjściowego, braku władzy,
niepowodzenia capability call, odpowiedzi odroczonej i jawnej odmowy przepływu. To
rozróżnienie ma znaczenie operacyjne: edycja szablonu nie naprawi odwołanego paszportu,
a retry nie naprawi wyjścia niezgodnego ze schematem.

Każda definicja niesie również limity bajtów, głębokości, kolekcji, tekstu i czasu.
Przepływ dodaje budżet wszystkich kroków i kroków pętli. Limity są częścią kontraktu
komponentu, nie wskazówką wydajnościową.

## Jak obserwować i debugować przepływ?

Najpierw należy zwalidować cały profil poleceniem `orbiplex-node-daemon check-config`,
a potem użyć `json-e-flow-dry-run` z jawnymi mockami odpowiedzi. Dry-run nigdy nie
wywołuje prawdziwych host capabilities. W runtime dostępne są
`orbiplex-node-launcher json-e-flow-middleware`, strona `/operator/json-e-flow` i
endpointy śladów daemona. Zachowane ślady pokazują identyfikatory, digesty, czasy,
wyniki kroków i zredagowaną diagnostykę zamiast surowych payloadów.

## Jak bezpiecznie dystrybuować definicje JSON-e?

Definicje przepływów mogą żyć w konfiguracji operatora albo w pakiecie middleware.
Pakiet może dostarczać fragmenty konfiguracji i przykłady, lecz nie nadaje sam sobie
władzy. Operator nadal kontroluje aktywację, zaufanie do pakietu, projekcję kontekstu,
paszporty capabilities, granty i lokalną politykę. Story-009 pokazuje podpisany pakiet,
którego pięciu providerów ról jest in-process JSON-e Flows zamiast nadzorowanych usług
HTTP.

## Kiedy lepsze jest middleware oparte na kodzie?

Gdy zachowanie wymaga streamingu, trwałego stanu lokalnego, nietrywialnych algorytmów,
dynamicznych grafów pracy, rozbudowanych retry, adapterów protokołów, integracji z OS
albo logiki domenowej zasługującej na zwykłe typy i testy jednostkowe. JSON-e jest
najmniej potężnym narzędziem do kształtowania danych; używanie go po przekroczeniu tej
granicy nie jest samo w sobie zaletą.
