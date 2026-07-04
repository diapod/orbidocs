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
host-local, a ten dokument jest jego walidowaną w CI projekcją w postaci
zrozumiałej dla człowieka.

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
| `sensorium.workbench.terminal` | `sensorium/workbench.terminal` | lokalna aktuacja | ograniczona capability PTY/sesji dla Sensorium Workbench | Sensorium Workbench connector | częściowe | Właściciel solution: Solution 042 Sensorium Workbench. Powierzchnia efektów wysokiego ryzyka; obecny connector domyślnie wyłącza terminal w factory config, a po jawnym włączeniu dopuszcza ograniczone sesje PTY i komendy argv tylko z grantem oraz skonfigurowanym profilem komend. Raw input, resize i signal wymagają potwierdzenia operatora. Flagi registry dopuszczają zarówno widoczność host-route, jak i dispatch przez nadzorowany handler middleware. |
| `sensorium.workbench.file` | `sensorium/workbench.file` | lokalna aktuacja | ograniczony snapshot/read plików pod leased workspace roots | Sensorium Workbench connector | częściowe | Właściciel solution: Solution 042 Sensorium Workbench. Pierwszy opt-in slice connectora implementuje allowlisted workspace snapshot/read z limitami request/read bytes oraz odmową traversal, root-self, symlink-traversal, oversized-file i invalid-root-config; nie jest ambient filesystem authority. Flagi registry dopuszczają zarówno widoczność host-route, jak i dispatch przez nadzorowany handler middleware. |
| `sensorium.workbench.patch` | `sensorium/workbench.patch` | lokalna aktuacja | ograniczone stosowanie patchy pod leased workspace roots | Sensorium Workbench connector | częściowe | Właściciel solution: Solution 042 Sensorium Workbench. Opt-in connector implementuje artifact-backed patch apply za sprawdzeniami digest/size, containment workspace, jawnymi grantami i potwierdzeniem operatora. Capability pozostaje host-route visible i passport-eligible, ale formalna bramka registry dispatch pozostaje zamknięta do czasu dopuszczenia nadzorowanego handlera patch. |
| `sensorium.workbench.env` | `sensorium/workbench.env` | lokalna aktuacja | ograniczona powierzchnia lifecycle środowiska/sandboxu dla sesji Workbench | Sensorium Workbench connector | częściowe | Właściciel solution: Solution 042 Sensorium Workbench. Pierwszy opt-in slice connectora raportuje allowlisted host-local workspace environments; lifecycle create/close i cleanup/recovery są nadal przyszłe. Flagi registry dopuszczają zarówno widoczność host-route, jak i dispatch przez nadzorowany handler middleware. |
| `interaction-broker.wait` | `host/interaction-broker.wait` | koordynacja hosta | host-owned ograniczony wait nad zarejestrowanymi źródłami obserwacji | daemon interaction broker | planowane | Waits są control-plane coordination z deadline i idempotency; nie autoryzują terminacji ani efektów domenowych. |
| `interaction-broker.watch` | `host/interaction-broker.watch` | koordynacja hosta | host-owned ograniczony watch/replay cursor nad zarejestrowanymi źródłami obserwacji | daemon interaction broker | planowane | Watch replay windows są ograniczone przez liczbę/czas i niosą wyłącznie metadata-safe events. |
| `interaction-broker.probe` | `host/interaction-broker.probe` | koordynacja hosta | host-owned aktywny probe postępu, żywotności, stanu pliku albo obecności artefaktu | daemon interaction broker | planowane | Probes tworzą diagnostykę albo outcomes; efektowna remediation pozostaje po stronie właścicielskiego connectora/operator path. |
| `escrow` | `role/escrow` | attached supervisory role | nadzorca hold, release, refund, freeze i dispute path dla settlement kontraktów | escrow supervisor node lub attached service | tak | Capability oznacza nadzór nad losem środków zarezerwowanych dla kontraktu, nie pełny autorytet całej księgi. |
| `oracle` | `plugin/oracle` | attached role / plugin | bounded external judgment, verification lub adjudication surface | przyszły oracle service | planowane | Status maszynowy: `reserved`. Na obecnym etapie to rezerwacja namespace i kierunek rozszerzenia, nie dopuszczalna capability runtime ani pełny hard-MVP runtime slice. |

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
