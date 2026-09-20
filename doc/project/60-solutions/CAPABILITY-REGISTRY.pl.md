# Rejestr capability IDs

Ten dokument jest rejestrem capability IDs używanych na granicy Node <-> Node
oraz Node <-> Seed Directory, zapisanym w postaci zrozumiałej dla człowieka.

Nie jest to pełna macierz zdolności rozwiązania. To węższy artefakt:

- mapuje `capability_id` na jego semantykę,
- pokazuje odpowiadającą rolę lub klasę runtime,
- wskazuje wire-visible name,
- pomaga utrzymać spójność między `orbidocs`, `node` i kontraktami passportów.

## Zakres

Rejestr obejmuje capability IDs używane jako:

- identyfikatory w `capability-passport.v1`,
- identyfikatory w `capability-advertisement.v1`,
- kryteria routingu lub odkrywania capability w Node.

Historycznie nie obejmował host-local capabilities typu `recovery.sign` czy
`catalog.local.query`. Ta granica jest już nieaktualna: `node/capability/capability-registry.v1.json`
jest egzekwowanym maszynowym źródłem prawdy dla capabilities federacyjnych i
host-local, a ten dokument jest jego mechanicznie sprawdzaną projekcją w postaci
zrozumiałej dla człowieka. Ręczna tabela semantyczna obejmuje wpisy wybrane przez
`docs.human-registry`; generowany [pełny katalog host-local](#host-local-capabilities)
obejmuje wszystkie host capabilities.

## Warstwy deklarowania capability

Capability advertisement i capability passport są powiązane, ale nie są
wymienne.

Używamy następujących warstw:

| Warstwa | Artefakt | Znaczenie | Podstawa zaufania | Przykłady |
|---|---|---|---|---|
| Capability natywna dla protokołu | `capability-advertisement.v1` z self-issued passport-form assertion | "ten peer aktualnie mówi tą bazową powierzchnią protokołu" | podpis node'a, self-issued capability passport i poprawnie zestawiona sesja peer | `core/messaging`, `core/keepalive` |
| Capability oparta o passport | `capability-passport.v1` niesiony w advertisement albo indeksowany przez Seed Directory | "ten node jest uprawniony albo zaakceptowany dla tego profilu capability" | profilowa polityka passportu, podpis wystawcy, sprawdzenie revocation | `network-ledger`, `seed-directory`, `escrow` |
| Usługa rekomendowana w federacji | passport-backed capability plus polityka federacji | "ta passport-backed capability jest rekomendowana lub bezpieczna w tej federacji" | wystawca wysokiej atestacji, allowlist federacji, lokalna polityka | zatwierdzony ledger, zaufany seed directory, certyfikowany offer catalog |
| Capability suwerenna/prywatna | sovereign capability id, opcjonalnie oparta o passport | "ten node oferuje capability zakotwiczoną w tożsamości poza globalnym bare-name namespace" | tożsamość kotwicząca plus opcjonalny passport i lokalna polityka | `audio-transcription@participant:did:key:...`, `~audio-transcription@participant:did:key:...` |
| Custom capability ogłoszona samodzielnie | `capability-advertisement.v1` z self-issued passport-form assertion | "ten node twierdzi, że to potrafi; weryfikuj przez użycie protokołu albo lokalną politykę" | podpis node'a plus self-issued passport; bez endorsementu federacji, jeśli nie jest dołączony osobno | eksperymentalny plugin, niekrytyczna wskazówka discovery |

W konsekwencji:

- `capability-advertisement.v1` jest żywym widokiem discovery i routingu i może
  być wymieniany bezpośrednio bez Seed Directory,
- `capability-passport.v1` jest trwałym dowodem uprawnienia, zgody albo
  endorsementu dla profili capability, które tego wymagają,
- `capability-schema.v1` jest opcjonalnym kontraktem maszynowo-czytelnym dla
  profilu capability i jest wskazywana przez content-addressed `schema/ref`,
- Seed Directory indeksuje passport-backed capabilities dla discovery sieciowego,
- a konsumenci muszą zastosować lokalną politykę, zanim potraktują jakąkolwiek
  advertised capability jako zaufaną.

## Klasy publicznych passportów

Rejestr rozróżnia publikację w publicznej sieci od zamkniętych katalogów
deploymentowych.

Dla publicznie rozgłaszanych capability passports:

| Klasa | Passport `capability_id` | Projekcja wire/query | Oczekiwanie wobec wystawcy |
|---|---|---|---|
| Oficjalna / rozpoznana przez społeczność | zarejestrowany formalny bare id, np. `network-ledger`, `seed-directory`, `offer-catalog` | stabilna nazwa mapowana, np. `core/network-ledger`, `role/seed-directory`, `role/offer-catalog` | klucz participanta, organizacji, rady albo federacji z najwyższą atestacją wymaganą przez politykę społeczności |
| Kompatybilna implementacja sovereign | sovereign id bez `~`, np. `offer-catalog@participant:did:key:...`, plus `capability_profile.compatible_with` | `sovereign/...` plus filtrowanie po anchorze | tożsamość kotwicząca albo delegowany signer; konsumenci weryfikują deklarację kompatybilności względem schematu/profilu i lokalnej polityki |
| Custom / operatorska | sovereign id z `~`, np. `~article-review@participant:did:key:...` albo `~article-review@org:did:key:...` | `sovereign/...` plus filtrowanie po anchorze | tożsamość kotwicząca albo delegowany signer; konsumenci stosują lokalną politykę endorsementu i reputacji; `schema/ref` opisuje własny protokół |

Publiczna usługa customowa NIE POWINNA tworzyć nowego niezakotwiczonego
formalnego bare `capability_id` i publikować go tak, jakby był capability
rozpoznaną przez społeczność. Powinna użyć istniejącego zarejestrowanego
formalnego id albo sovereign id zakotwiczonego w tożsamości.

Zamknięte deploymenty operatorskie są inną kategorią. Mogą używać lokalnego
Seed Directory jako katalogu deploymentowego dla znanego zestawu formalnych
capabilities, gdzie zaufanie wynika z jawnej konfiguracji, allowlisty node ids
i ustanowionych sesji peer, a nie z publicznego endorsementu federacji.
Story-009 używa tej zamkniętej reguły deploymentowej dla passportów
`offer-catalog` na node B/C.

## Źródła prawdy

Źródłem prawdy jest:

- `node:capability/capability-registry.v1.json`

Ten dokument, legacy projekcja Rust w `node:capability/src/lib.rs` oraz fixture'y
passport/advertisement są sprawdzane względem tego źródła przez
`orbidocs:scripts/check-capability-registry.py`.

Jeżeli zmienia się:

- `capability_id`,
- wire name,
- semantyka capability,
- eligibility flags,
- albo jej główny owner runtime,

to najpierw aktualizujemy maszynowy registry, a dopiero potem jego ludzką projekcję.

## Capability Registry

Kolumna `Passport w MVP` jest notą implementacyjną/readiness, a nie maszynowym
statusem registry. Kanoniczny status maszynowy to `active`, `deprecated` albo
`reserved` w `node:capability/capability-registry.v1.json`; wpisy `reserved`
są tutaj widoczne tylko po to, aby zapobiec zajęciu namespace, i nadal są
odrzucane na admission gate.

| capability_id | Wire name | Klasa | Rola semantyczna | Typowy owner runtime | Passport w MVP | Uwagi |
|---|---|---|---|---|---|---|
| `core/messaging` | `core/messaging` | infrastrukturalna natywna dla protokołu | bazowa szyfrowana komunikacja peer/session wymagana dla sesji peer | protokół Node / peer supervisor | self-issued advertisement/passport-form assertion | Obowiązkowa bazowa capability; peer bez niej jest odrzucany podczas walidacji handshake/sesji. |
| `core/discovery` | `core/discovery` | infrastrukturalna natywna dla protokołu | bazowa powierzchnia peer discovery i wymiany advertisementów | protokół Node / discovery runtime | self-issued advertisement/passport-form assertion | Używana dla semantyki discovery i advertisementów; formalny wpis utrzymuje zgodność stałych kodu z dokumentacją. |
| `core/keepalive` | `core/keepalive` | infrastrukturalna natywna dla protokołu | bazowa powierzchnia keepalive/reconnect dla żywotności sesji | protokół Node / peer supervisor | self-issued advertisement/passport-form assertion | Capability natywna dla protokołu; nie jest attached service role. |
| `network-ledger` | `core/network-ledger` | infrastrukturalna | zdalny autorytet settlement ledger dla innych node'ów | settlement-capable Node | tak | Capability oznacza autorytet księgi, nie tylko pojedynczy hold czy politykę. |
| `seed-directory` | `role/seed-directory` | infrastrukturalna | katalog capability passports, revocations i advertisementów używany do bootstrapu i discovery | Seed Directory service lub embedded Node service | tak | Capability dotyczy katalogu i zaufanego publikowania/odczytu wpisów katalogowych. |
| `node-primary-operator` | `role/node-primary-operator` | binding / governance | wystawione przez participanta wiązanie autorytetu wskazujące primary operator node'a | capability / Seed Directory / ścieżka akceptacji daemona | tak | Capability wyłącznie wiążąca; konsumenci muszą weryfikować artefakt node-operator binding, a nie traktować jej jak zwykłą usługę. |
| `offer-catalog` | `role/offer-catalog` | rola domenowa | federacyjna powierzchnia ofertowa używana do responder-side fetch i discovery | Dator jako strona podaży, Arca jako strona popytu/discovery | tak, jeśli capability jest delegowane przez passport | Capability jest domenowa; konkretna implementacja może rozdzielać supply i observed/discovery na różne moduły. |
| `corpus.provider` | `app/corpus-provider` | rola aplikacyjnego rozumowania | topic-scoped provider rozumowania Corpus uprawniony do odbioru `corpus-reasoning-query.v1` i zwracania `corpus-reasoning-bid.v1` | acceptor AD providera Corpus / oferta z rozszerzeniem Corpus | hard-MVP done | Capability autoryzuje operacyjną rolę providera; kompetencja tematyczna pozostaje w polach rozszerzenia Corpus w `service-offer.v1`, nigdy w capability id. |
| `contact-catalog` | `role/contact-catalog` | rola domenowa | opt-in contact discovery zwracające route candidates albo invitation-required results dla zewnętrznych uchwytów kontaktowych | Contact Catalog middleware | tak | Seed Directory może reklamować providerów Contact Catalog, ale nie może przechowywać surowych map people-directory. MVP lookup jest invitation-only z uwierzytelnionymi callerami. |
| `email-attestation` | `role/email-attestation` | rola usługi contact-control | usługa, która wykonuje challenge kanału email i orkiestruje wystawienie passportów `email-control@v1` | attestation service odkrywany przez Seed Directory | tak | Capability autoryzuje rolę providera atestacji, nie kontrolę konkretnego adresu email. |
| `phone-attestation` | `role/phone-attestation` | rola usługi contact-control | usługa, która wykonuje challenge kanału telefonicznego i orkiestruje wystawienie passportów `phone-control@v1` | attestation service odkrywany przez Seed Directory | tak | Capability autoryzuje rolę providera atestacji, nie kontrolę konkretnego numeru telefonu. |
| `email-control` | `proof/email-control` | dowód kontroli kontaktu | dowód, że subject aktualnie kontroluje jeden adres email dla wybranych celów | attestation service odkrywany przez Seed Directory | tak | To dowód kontroli kontaktu, nie legal identity assurance. Contact Catalog admission traktuje go jako freshness-bound input evidence. |
| `phone-control` | `proof/phone-control` | dowód kontroli kontaktu | dowód, że subject aktualnie kontroluje jeden numer telefonu dla wybranych celów | attestation service odkrywany przez Seed Directory | tak | To dowód kontroli kontaktu, nie legal identity assurance. Oczekiwane są krótkie TTL-e i polityka świadoma reassignment. |
| `agora-vault` | `app/agora-vault` | zaszyfrowany storage artefaktów | zakresowa authority do put, list, get albo delete opaque zaszyfrowanych artefaktów pod subjectem Agora Vault | Agora service / daemon host capability bridge | tak | Używa profilu `agora-vault@v1`. Publiczny lookup działa tylko po opaque `artifact/id`; vault subject, participant, nym, topic i metadane plaintext nie są publiczną częścią entry. |
| `messaging.accept` | `app/messaging.accept` | advertisement aplikacyjny | advertisement node'a, że aktualnie przyjmuje dostarczanie wiadomości z użyciem kanonicznego profilu zgody odbioru `messaging-receive@v1` | messaging middleware / Node capability advertisement | self-issued advertisement plus evidence profilu odbioru | Publikowane tylko wtedy, gdy messaging service i inbound acceptor są gotowe. Domyślna polityka trasy to `privacy = private-direct`, a konsumenci lookup mogą filtrować po tej capability przed wysłaniem contact request. |
| `messaging-receive` | `app/messaging-receive` | zgoda aplikacyjna | wąska authority wystawiana przez recipienta, pozwalająca jednemu sender subject dostarczać wiadomości do jednej zaakceptowanej trasy | messaging middleware / Contact Catalog contact-request acceptor | tak | Używana w Story 010 jako konkretny passport mintowany po zaakceptowaniu contact request. Nie przyznaje friend-class capabilities. |
| `messaging-send` | `app/messaging-send` | autorstwo aplikacyjne | authority po stronie participanta do podpisywania i kolejkowania outbound messaging envelopes dla lokalnego klienta wiadomości | messaging middleware / host podpisujący Node | tak | Delegacja podpisu używa `signing/messaging-send`; zgoda odbiorcy pozostaje osobnym passportem `messaging-receive`. |
| `room.open` | `app/room.open` | koordynacja aplikacyjna | authority do otwarcia trwałego szkieletu Room i początkowej projekcji polityki pokoju | Room primitive / daemon room host | planowane | To capability domeny Room, nie grant adaptera transportowego. Adaptery live-plane WSS i Matrix konsumują wynikową projekcję pokoju. |
| `room.join` | `app/room.join` | koordynacja aplikacyjna | authority do żądania albo zaakceptowania członkostwa w istniejącym Room zgodnie z jego polityką | Room primitive / daemon room host | planowane | Join authority jest oceniana względem polityki pokoju, grantów, expiry i atestowanego członkostwa; sama z siebie nie oznacza prawa wysyłania live-message. |
| `room.membership-query` | `app/room.membership-query` | zapytanie aplikacyjne | authority do żądania signer-backed atestacji członkostwa albo grantów w Room | Room primitive / daemon room host | tak | Zaimplementowane jako uwierzytelnione query projekcji `agora-service` wspierane lokalnym host signerem; middleware nie mintują atestacji bezpośrednio. |
| `sensorium.workbench.terminal` | `sensorium/workbench.terminal` | lokalna aktuacja | ograniczona capability PTY/sesji dla Sensorium Workbench | Sensorium Workbench connector | częściowe | Właściciel solution: Solution 042 Sensorium Workbench. Terminal pozostaje domyślnie wyłączony, a po jawnym włączeniu dopuszcza ograniczone sesje PTY i strukturalne argv tylko z grantem oraz dokładnym lub ograniczonym profilem prefiksowym walidowanym przez most Rust actuation. Raw input, resize, signal i cancel wymagają potwierdzenia operatora. Flagi registry dopuszczają widoczność host-route i dispatch przez nadzorowany handler middleware. |
| `sensorium.workbench.file` | `sensorium/workbench.file` | lokalna aktuacja | ograniczony snapshot/read plików pod leased workspace roots | Sensorium Workbench connector | częściowe | Właściciel solution: Solution 042 Sensorium Workbench. Connector implementuje allowlisted snapshot/read dla host-local i managed-copy z limitami request/read bytes, walidacją ścieżek przez Rust oraz odmową traversal, root-self, symlink, oversized-file i invalid-root; nie jest ambient filesystem authority. Flagi registry dopuszczają widoczność host-route i dispatch przez nadzorowany handler middleware. |
| `sensorium.workbench.patch` | `sensorium/workbench.patch` | lokalna aktuacja | ograniczone stosowanie patchy pod leased workspace roots | Sensorium Workbench connector | częściowe | Właściciel solution: Solution 042 Sensorium Workbench. Connector implementuje artifact-backed patch apply za sprawdzeniami digest/size, containment workspace, jawnymi grantami i potwierdzeniem operatora dla korzeni host-local i managed-copy; zweryfikowane artefakty można jawnie przekazać do Artifact Delivery i/lub metadanych proweniencji Memarium. Formalna bramka registry dispatch pozostaje zamknięta. |
| `sensorium.workbench.env` | `sensorium/workbench.env` | lokalna aktuacja | ograniczona powierzchnia lifecycle środowiska/sandboxu dla sesji Workbench | Sensorium Workbench connector | częściowe | Właściciel solution: Solution 042 Sensorium Workbench. Connector raportuje środowiska host-local i implementuje ograniczoną alokację `fixture-copy.v1`, eksport artefaktu, trwały lifecycle i teardown potwierdzany przez operatora, odmawiając PTY bez izolacji procesu. Backend container i microVM pozostają przyszłe. Flagi registry dopuszczają widoczność host-route i dispatch przez nadzorowany handler middleware. |
| `sensorium.interface.read` | `sensorium/interface.read` | obserwacja | ograniczony odczyt one-shot jednego jawnie udostępnionego Sensorium Interface | Sensorium Interfaces runtime | tak, `sensorium-interface@v1` | Solution 046 jest właścicielem zaimplementowanej operacji; każde wywołanie pozostaje ograniczone do dokładnego zasobu interfejsu, zdalnego node'a tam, gdzie ma to zastosowanie, pułapu klasyfikacji, limitów batcha, bieżącej polityki hosta i evidence odwołań. Ogólna reklama obsługi nie ujawnia deskryptora ani grantu. |
| `sensorium.interface.subscribe` | `sensorium/interface.subscribe` | obserwacja | utworzenie, odnowienie, konsumpcja i zamknięcie ograniczonej dzierżawy interfejsu związanej z callerem | Sensorium Interfaces runtime | tak, `sensorium-interface@v1` | Uprawnienie subskrypcji jest odrębne od odczytu one-shot i jest zaimplementowane z dokładnym ograniczeniem interfejsu, callera, dzierżawy, cursora, klasyfikacji, batcha i bieżącego stanu odwołań. |
| `sensorium.interface.remote-feed` | `sensorium/interface.remote-feed` | koordynacja hosta | uruchomienie jednego ograniczonego uwierzytelnionego feedu wychodzącego do peera w imieniu lokalnego callera | Sensorium Interfaces runtime | nie; tylko host-local | Ten grant zezwala na recipient-side peer egress, ale nie niesie source authority. Każda operacja zdalna nadal wymaga osobnego bieżącego Passportu `sensorium.interface.subscribe` ograniczonego do dokładnego zdalnego node'a i interfejsu. |
| `sensorium.interface.invoke` | `sensorium/interface.invoke` | aktuacja | wywołanie dokładnej metody jednego jawnie grantowanego interfejsu aktuacji oraz koordynacja jego ograniczonego współdzielonego lub wyłącznego sterowania | Sensorium Interfaces runtime | tak, `sensorium-interface-actuation@v1` | Zaimplementowana podstawa P083 wiąże każdy efekt z uwierzytelnionym callerem, dokładnym interfejsem, metodą, klasyfikacją, nieprzezroczystą generacją źródła, grantem i limitami; efekt wyłączny wymaga dodatkowo bieżącej dzierżawy, epoki i sekwencji callera. Obserwacja, członkostwo w Room ani dołączenie nośnika nie dają uprawnienia invoke. |
| `sensorium.interface.manage` | `sensorium/interface.manage` | sterowanie hosta | lokalne dla źródła publikowanie obserwacji i aktuacji, lifecycle, granty, revocation, inspekcja, metryki i preempcja wynikająca z polityki | Sensorium Interfaces runtime | nie; tylko host-local | Zaimplementowana capability nie jest reklamowana i nie kwalifikuje się do Passportu. Jej polityka autoryzacji wylicza zamknięty zbiór akcji, w tym `control.preempt`; wymagane pozostają uwierzytelnione związanie callera, aktywny dokładny grant invoke dla dzierżawy operatora, niezmienne fakty zarządcze i rekonstrukcja po restarcie. |
| `http.fetch.bounded` | `host/http.fetch.bounded` | efekt sieciowy hosta | jedno ograniczone pobranie HTTP(S) dopuszczone dla dokładnego konsumenta middleware, akcji, polityki originu i klasy celu | daemon bounded HTTP fetch host | nie; tylko host-local | Zaimplementowany reużywalny prymityw należący do daemona, którego pierwszym konsumentem jest P084. Rozwiązuje i klasyfikuje każdy adres, pinuje wybrane połączenie, ponownie waliduje redirecty w tym samym originie, egzekwuje przecięte limity bajtów, czasu i współbieżności oraz zwraca wyłącznie ograniczone bajty albo wskaźnik Artifact Delivery. Nie jest publicznym proxy i nie nadaje władzy obserwacji ani publikacji Sensorium. |
| `inference.policy.evaluate` | `host/inference.policy.evaluate` | ocena danych | ograniczona ocena jawnej polityki odbiorcy względem deklaracji lub dowodu wykonania | inference provenance core przez daemon | nie; tylko host-local | Zwraca admit, warn lub deny dla dokładnych podmiotów. Nie uwierzytelnia źródeł, nie instaluje polityki, nie uruchamia inferencji i nie nadaje uprawnień do efektów. |
| `service.order.result.prepare` | `host/service.order.result.prepare` | wyprowadzenie danych | przygotowanie koperty wyniku procurement z wiązaniem niezmienionego produktu źródłowego | procurement core przez daemon | nie; tylko host-local | Zachowuje granicę i czas źródła. Nie obserwuje wykonania, nie uwierzytelnia źródła, nie zapisuje commitu, nie dostarcza artefaktów i nie rozlicza płatności. |
| `artifact.delivery.retain` | `host/artifact.delivery.retain` | efekt składowania hosta | zachowanie jednego uwierzytelnionego, należącego do callera i content-bound obiektu w Artifact Delivery | daemonowy object store Artifact Delivery | nie; tylko host-local | Zaimplementowany dla retencji reprezentacji P084. Host przed zapisem sprawdza dokładne powiązanie caller/owner, digest, rozmiar, klasyfikację, kontekst przyczynowy i idempotency związane z digestem, po czym zwraca niezmienny ref oraz receipt P081. Nie nadaje władzy odczytu, dostarczania, publikacji ani wyboru odbiorcy. |
| `interaction-broker.wait` | `host/interaction-broker.wait` | koordynacja hosta | host-owned ograniczony wait nad zarejestrowanymi źródłami obserwacji | daemon interaction broker | nie; tylko host-local | Zaimplementowana koordynacja control-plane z deadline, idempotency, grant-context wystawianym przez daemon, trwałym recovery/retention oraz aktywnymi providerami wbudowanymi i dynamicznymi. |
| `interaction-broker.watch` | `host/interaction-broker.watch` | koordynacja hosta | host-owned ograniczony watch/replay cursor nad zarejestrowanymi źródłami obserwacji | daemon interaction broker | nie; tylko host-local | Zaimplementowane ograniczone zasoby watch, stabilne cursory providerów, admission grant-context, retention-backed replay oraz aktywne providery Workbench, Room, Artifact Delivery, approval, Memarium-query i Sensorium Interface. |
| `interaction-broker.probe` | `host/interaction-broker.probe` | koordynacja hosta | host-owned aktywny probe postępu, żywotności, stanu pliku albo obecności artefaktu | daemon interaction broker | nie; tylko host-local | Zaimplementowane ograniczone probe'y i diagnostyka nad zarejestrowanymi providerami; efektowa remediation pozostaje po stronie właścicielskiego connectora lub operator path. |
| `whisper.trace.publish` | `host/whisper.trace.publish` | lokalne autorstwo | waliduje i publikuje jedno ograniczone oświadczenie `whisper-trace.v1` przez istniejący carrier Agora albo AD/INAC | provider autorstwa trace w Whisper Intake | tak | Capability jest host-local i niepaszportowalna. Ujawnienie treści wymaga dokładnie związanej zgody operatora po stronie hosta; wynikowy podpisany `agora-record.v1` nadal podlega polityce disclosure, podpisu i admission carriera. |
| `escrow` | `role/escrow` | attached supervisory role | nadzorca hold, release, refund, freeze i dispute path dla settlement kontraktów | escrow supervisor node lub attached service | tak | Capability oznacza nadzór nad losem środków zarezerwowanych dla kontraktu, nie pełny autorytet całej księgi. |
| `oracle` | `plugin/oracle` | attached role / plugin | bounded external judgment, verification lub adjudication surface | przyszły oracle service | planowane | Status maszynowy: `reserved`. Na obecnym etapie to rezerwacja namespace i kierunek rozszerzenia, nie dopuszczalna capability runtime ani pełny hard-MVP runtime slice. |

<!-- BEGIN GENERATED HOST CAPABILITIES -->

<a id="host-local-capabilities"></a>

## Pełny katalog host-local

Wygenerowano z `node:capability/capability-registry.v1.json`; nie edytuj tego bloku ręcznie.
Obie wersje językowe odświeża `make capability-registry-docs`.
Katalog obejmuje każdy wpis z powierzchnią `host-local`, niezależnie od statusu
i `docs.human-registry` (ta flaga wybiera tylko ręczną tabelę powyżej).

Wpisy: **186** host-local / **218** ogółem; grupy właścicieli: **25**.

Grupowanie zachowuje dokładne wartości `owner` z rejestru; wpisy są sortowane po `capability/id`.
`dispatchable` i `host-route` to niezależne flagi kwalifikacji; ostatnia kolumna
wymienia pozostałe flagi ustawione na `true` (pominięte mają wartość `false`).
Wpis może mieć również powierzchnię `federated`, pokazaną jawnie w tabeli.

Ani obecność wpisu, ani status `active` nie gwarantują zainstalowanego handlera,
działającego endpointu lub uprawnienia wywołującego. Dostępność runtime, granty,
zgody i polityka domenowa pozostają odrębnymi kontrolami. Nazwy wire nie są URL-ami endpointów.

### <code>Sensorium Interfaces runtime</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>sensorium.interface.invoke</code> | <code>sensorium/interface.invoke</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |
| <code>sensorium.interface.manage</code> | <code>sensorium/interface.manage</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.interface.read</code> | <code>sensorium/interface.read</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |
| <code>sensorium.interface.remote-feed</code> | <code>sensorium/interface.remote-feed</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.interface.subscribe</code> | <code>sensorium/interface.subscribe</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |

### <code>Sensorium Workbench connector</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>sensorium.workbench.env</code> | <code>sensorium/workbench.env</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |
| <code>sensorium.workbench.file</code> | <code>sensorium/workbench.file</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |
| <code>sensorium.workbench.patch</code> | <code>sensorium/workbench.patch</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | false | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |
| <code>sensorium.workbench.terminal</code> | <code>sensorium/workbench.terminal</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |

### <code>Whisper Intake trace authoring provider</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>whisper.trace.publish</code> | <code>host/whisper.trace.publish</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>capability/passport domain</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>memarium.read</code> | <code>app/memarium.read</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |

### <code>daemon Agent host runtime</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>agent.assistant.draft.accept</code> | <code>host/agent.assistant.draft.accept</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.assistant.escalate</code> | <code>host/agent.assistant.escalate</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.binding.create</code> | <code>host/agent.binding.create</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.controller.run</code> | <code>host/agent.controller.run</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.effect.dispatch</code> | <code>host/agent.effect.dispatch</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.effect.propose</code> | <code>host/agent.effect.propose</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.fork</code> | <code>host/agent.fork</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.inference-flow.bind</code> | <code>host/agent.inference-flow.bind</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.inference-passage.admit</code> | <code>host/agent.inference-passage.admit</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.inference-passage.commit</code> | <code>host/agent.inference-passage.commit</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.inference-passage.invoke</code> | <code>host/agent.inference-passage.invoke</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.inference-terminal.select</code> | <code>host/agent.inference-terminal.select</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.product.read</code> | <code>host/agent.product.read</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.resume</code> | <code>host/agent.resume</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.spawn</code> | <code>host/agent.spawn</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.status</code> | <code>host/agent.status</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.stop</code> | <code>host/agent.stop</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.suspend</code> | <code>host/agent.suspend</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.turn-order.resolve</code> | <code>host/agent.turn-order.resolve</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon Artifact Delivery host capability</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>artifact.delivery.retain</code> | <code>host/artifact.delivery.retain</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon Corpus Agent effect bridge</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>corpus.room.turn</code> | <code>host/corpus.room.turn</code> | <code>active</code> | <code>host-local</code> | true | false | — |

### <code>daemon Corpus Agent moderation effect bridge</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>corpus.room.moderate</code> | <code>host/corpus.room.moderate</code> | <code>active</code> | <code>host-local</code> | true | false | — |

### <code>daemon Inquirium host runtime</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>inquirium.assistant.feedback.append</code> | <code>host/inquirium.assistant.feedback.append</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.assistant.transcript.export</code> | <code>host/inquirium.assistant.transcript.export</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.assistant.transcript.import</code> | <code>host/inquirium.assistant.transcript.import</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.assistant.transcript.rebuild</code> | <code>host/inquirium.assistant.transcript.rebuild</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.assistant.transcript.search</code> | <code>host/inquirium.assistant.transcript.search</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.context-grant.issue</code> | <code>host/inquirium.context-grant.issue</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.context-grant.revoke</code> | <code>host/inquirium.context-grant.revoke</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.operator-question.transition</code> | <code>host/inquirium.operator-question.transition</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.training-grant.issue</code> | <code>host/inquirium.training-grant.issue</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.training-grant.revoke</code> | <code>host/inquirium.training-grant.revoke</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon Sensorium Virt host broker</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>sensorium.virt.host</code> | <code>host/sensorium.virt.host</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon bounded HTTP fetch host</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>http.fetch.bounded</code> | <code>host/http.fetch.bounded</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon capability host capability</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>capability.passport.publish</code> | <code>host/capability.passport.publish</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>capability.passport.revocation.sign</code> | <code>host/capability.passport.revocation.sign</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>capability.passport.revocation.verify</code> | <code>host/capability.passport.revocation.verify</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>capability.passport.verify</code> | <code>host/capability.passport.verify</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon capability passport publication reconciler</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>capability.passport.reconcile</code> | <code>host/capability.passport.reconcile</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon gateway control</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>gateway.sovereign-manual-receipt</code> | <code>host/gateway.sovereign-manual-receipt</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon host capability</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>memarium.promote</code> | <code>host/memarium.promote</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon identity host capability</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>identity.nym.create</code> | <code>host/identity.nym.create</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.org.create</code> | <code>host/identity.org.create</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.participant.create</code> | <code>host/identity.participant.create</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.participant.import</code> | <code>host/identity.participant.import</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.participant.recovery-bundle-export</code> | <code>host/identity.participant.recovery-bundle-export</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.participant.recovery-bundle-import</code> | <code>host/identity.participant.recovery-bundle-import</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.participant.recovery-export</code> | <code>host/identity.participant.recovery-export</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.pseudonym-vault.export</code> | <code>host/identity.pseudonym-vault.export</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.pseudonym-vault.import</code> | <code>host/identity.pseudonym-vault.import</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon interaction broker</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>interaction-broker.probe</code> | <code>host/interaction-broker.probe</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>interaction-broker.wait</code> | <code>host/interaction-broker.wait</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>interaction-broker.watch</code> | <code>host/interaction-broker.watch</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon operator settlement control</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>ledger.operator-credit</code> | <code>host/ledger.operator-credit</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon operator-extension lifecycle host</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>operator.extension.inspect</code> | <code>host/operator.extension.inspect</code> | <code>active</code> | <code>host-local</code> | false | true | — |
| <code>operator.extension.lifecycle</code> | <code>host/operator.extension.lifecycle</code> | <code>active</code> | <code>host-local</code> | false | true | — |
| <code>operator.extension.safe-mode</code> | <code>host/operator.extension.safe-mode</code> | <code>active</code> | <code>host-local</code> | false | true | — |

### <code>daemon or supervised middleware host capability</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>agora.publish.authorize</code> | <code>host/agora.publish.authorize</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agora.record.admit</code> | <code>host/agora.record.admit</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agora.record.sign</code> | <code>host/agora.record.sign</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agora.record.verify</code> | <code>host/agora.record.verify</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agora.relay</code> | <code>host/agora.relay</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |
| <code>agora.subscribe.authorize</code> | <code>host/agora.subscribe.authorize</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agora.trace.append</code> | <code>host/agora.trace.append</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agora.vault.delete</code> | <code>host/agora.vault.delete</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>passport/eligible</code> |
| <code>agora.vault.get</code> | <code>host/agora.vault.get</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>passport/eligible</code> |
| <code>agora.vault.list</code> | <code>host/agora.vault.list</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>passport/eligible</code> |
| <code>agora.vault.put</code> | <code>host/agora.vault.put</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>passport/eligible</code> |
| <code>artifact.delivery.send</code> | <code>host/artifact.delivery.send</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>artifact.delivery.status</code> | <code>host/artifact.delivery.status</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>artifact.delivery.submit</code> | <code>host/artifact.delivery.submit</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>capability.passport.issue</code> | <code>host/capability.passport.issue</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>capability.passport.lookup</code> | <code>host/capability.passport.lookup</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>capability.passport.sign</code> | <code>host/capability.passport.sign</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>capability.revocation.snapshot</code> | <code>host/capability.revocation.snapshot</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>contact.lookup</code> | <code>host/contact.lookup</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.messaging-recovery.mirror</code> | <code>host/identity.messaging-recovery.mirror</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.recovery</code> | <code>host/identity.recovery</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.routing-subject.create</code> | <code>host/identity.routing-subject.create</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inac.offer</code> | <code>host/inac.offer</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inac.push</code> | <code>host/inac.push</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inac.request</code> | <code>host/inac.request</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.assistant.activity.feed</code> | <code>host/inquirium.assistant.activity.feed</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.assistant.transcript.excise</code> | <code>host/inquirium.assistant.transcript.excise</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.assistant.turn</code> | <code>host/inquirium.assistant.turn</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.classify</code> | <code>host/inquirium.classify</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.embed</code> | <code>host/inquirium.embed</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.generate</code> | <code>host/inquirium.generate</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.image.edit</code> | <code>host/inquirium.image.edit</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.image.generate</code> | <code>host/inquirium.image.generate</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.rerank</code> | <code>host/inquirium.rerank</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.summarize</code> | <code>host/inquirium.summarize</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.transform</code> | <code>host/inquirium.transform</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>local-recipient-mailbox.resolve</code> | <code>host/local-recipient-mailbox.resolve</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>local-relationship.group.resolve</code> | <code>host/local-relationship.group.resolve</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>local-relationship.membership.append</code> | <code>host/local-relationship.membership.append</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>local-relationship.membership.latest</code> | <code>host/local-relationship.membership.latest</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>local-relationship.predicate.evaluate</code> | <code>host/local-relationship.predicate.evaluate</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>memarium.cache</code> | <code>host/memarium.cache</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>memarium.crisis.resolve</code> | <code>host/memarium.crisis.resolve</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>memarium.crisis.status</code> | <code>host/memarium.crisis.status</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>memarium.declassify</code> | <code>host/memarium.declassify</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>memarium.forget</code> | <code>host/memarium.forget</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>memarium.index</code> | <code>host/memarium.index</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>memarium.write</code> | <code>host/memarium.write</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>middleware.rewrite.broadcast</code> | <code>host/middleware.rewrite.broadcast</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>middleware.rewrite.peer-message</code> | <code>host/middleware.rewrite.peer-message</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>middleware.snooper.observe</code> | <code>host/middleware.snooper.observe</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>middleware.snooper.test</code> | <code>host/middleware.snooper.test</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>notification.create</code> | <code>host/notification.create</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>offer-catalog.query</code> | <code>host/offer-catalog.query</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>offers.local.query</code> | <code>host/offers.local.query</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>peer.message.dispatch</code> | <code>host/peer.message.dispatch</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>peer.session.establish</code> | <code>host/peer.session.establish</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>recovery.hsm.store</code> | <code>host/recovery.hsm.store</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>recovery.hsm.unseal</code> | <code>host/recovery.hsm.unseal</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>recovery.sign</code> | <code>host/recovery.sign</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sealer.derive-aead-key</code> | <code>host/sealer.derive-aead-key</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sealer.master.init</code> | <code>host/sealer.master.init</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sealer.open</code> | <code>host/sealer.open</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sealer.seal</code> | <code>host/sealer.seal</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sealer.unlock</code> | <code>host/sealer.unlock</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>seed.directory.query</code> | <code>host/seed.directory.query</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.audit.read</code> | <code>host/sensorium.audit.read</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.connector.invoke</code> | <code>host/sensorium.connector.invoke</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.connector.operation.cancel</code> | <code>host/sensorium.connector.operation.cancel</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.connector.operation.status</code> | <code>host/sensorium.connector.operation.status</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.connector.os.action</code> | <code>host/sensorium.connector.os.action</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.directive.invoke</code> | <code>host/sensorium.directive.invoke</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.directive.list</code> | <code>host/sensorium.directive.list</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.health</code> | <code>host/sensorium.health</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.observation.get</code> | <code>host/sensorium.observation.get</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.observe.query</code> | <code>host/sensorium.observe.query</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.observe.submit</code> | <code>host/sensorium.observe.submit</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.operation.cancel</code> | <code>host/sensorium.operation.cancel</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.operation.status</code> | <code>host/sensorium.operation.status</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.os.catalog.reload</code> | <code>host/sensorium.os.catalog.reload</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.os.catalog.status</code> | <code>host/sensorium.os.catalog.status</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.topic.summary</code> | <code>host/sensorium.topic.summary</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>signer.derive-shared-secret</code> | <code>host/signer.derive-shared-secret</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>signer.lock</code> | <code>host/signer.lock</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>signer.sign</code> | <code>host/signer.sign</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>signer.status</code> | <code>host/signer.status</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>signer.unlock</code> | <code>host/signer.unlock</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>whisper.intake</code> | <code>host/whisper.intake</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>whisper.redaction.prepare</code> | <code>host/whisper.redaction.prepare</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>workflow.orchestrate</code> | <code>host/workflow.orchestrate</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>workflow.step.completed.publish</code> | <code>host/workflow.step.completed.publish</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>workflow.test.trigger</code> | <code>host/workflow.test.trigger</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>inference-provenance-core through daemon host boundary</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>inference.policy.evaluate</code> | <code>host/inference.policy.evaluate</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>procurement core through daemon host boundary</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>service.order.result.prepare</code> | <code>host/service.order.result.prepare</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>supervised JSON-e Flow acceptance capability</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>role.agent.inference-passage.acceptance</code> | <code>host/role.agent.inference-passage.acceptance</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>supervised middleware Corpus turn-order flow</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>role.corpus.turn-order.resolve</code> | <code>host/role.corpus.turn-order.resolve</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>supervised middleware or test fixture capability</code>

| capability_id | Nazwa wire | Status | Powierzchnie | `dispatchable` | `host-route` | Pozostałe włączone flagi |
|---|---|---|---|---|---|---|
| <code>base.rumor-rewrite</code> | <code>host/base.rumor-rewrite</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>base.whisper-redaction</code> | <code>host/base.whisper-redaction</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.adapter.anthropic</code> | <code>host/inquirium.adapter.anthropic</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.adapter.openai</code> | <code>host/inquirium.adapter.openai</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.adapter.simulator</code> | <code>host/inquirium.adapter.simulator</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>other.minimal</code> | <code>host/other.minimal</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>other.operator-hinting</code> | <code>host/other.operator-hinting</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>other.test</code> | <code>host/other.test</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.bielik-editor-in-chief.execute</code> | <code>host/role.bielik-editor-in-chief.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.bielik-git-publisher.execute</code> | <code>host/role.bielik-git-publisher.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.bielik-illustrator.execute</code> | <code>host/role.bielik-illustrator.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.bielik-publication-verifier.execute</code> | <code>host/role.bielik-publication-verifier.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.bielik-researcher.execute</code> | <code>host/role.bielik-researcher.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.example-summarizer.execute</code> | <code>host/role.example-summarizer.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.example.execute</code> | <code>host/role.example.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.inquirium.generate</code> | <code>host/role.inquirium.generate</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.raw-signal.execute</code> | <code>host/role.raw-signal.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.raw.component2</code> | <code>host/role.raw.component2</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.raw.component3</code> | <code>host/role.raw.component3</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.raw.component4</code> | <code>host/role.raw.component4</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.test.execute</code> | <code>host/role.test.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.test.success.execute</code> | <code>host/role.test.success.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |

<!-- END GENERATED HOST CAPABILITIES -->

## Rozróżnienie semantyczne

### `network-ledger` vs `escrow`

- `network-ledger` odpowiada na pytanie: "kto jest autorytetem księgi?"
- `escrow` odpowiada na pytanie: "kto nadzoruje warunkowe uwolnienie środków dla tego kontraktu?"

Te role mogą być współlokowane, ale nie są tożsame semantycznie.

### `offer-catalog`

`offer-catalog` jest capability domenową, nie nazwą konkretnego procesu.
W obecnym MVP:

- Dator odpowiada za stronę podaży i responder-side fetch,
- Arca odpowiada za stronę popytu, observed catalog i discovery.

Capability pozostaje jedna, choć runtime może ją realizować przez więcej niż jeden
moduł.

### `contact-catalog`

`contact-catalog` odkrywa opt-in contact routes, nie ludzi. Provider może być
odkrywany przez Seed Directory, ale domenowa polityka katalogu odpowiada za:

- dopuszczone dowody kontroli kontaktu,
- indeksy lookup,
- ujawnianie route candidates,
- rate limiting,
- audyt no-match,
- oraz revocation albo expiry contact claims.

Profil MVP jest invitation-only. Konsumenci powinni oczekiwać, że
`contact-lookup-result.v1` nazwie `routing-subject`, `contact_nym` albo ścieżkę
zaproszenia, nigdy surowego root participanta jako domyślnej odpowiedzi.

## Następne kroki

- Rozszerzyć ten rejestr, gdy pojawią się kolejne capability IDs o stabilnym
  znaczeniu między-node.
- Dopisać bardziej precyzyjną tabelę `issuer -> consumer -> scope`, jeżeli
  attached-role passports zaczną mieć bogatsze zakresy (`scope`) niż obecne MVP.
