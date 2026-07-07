# Artifact Delivery FAQ

## Czym jest Artifact Delivery?

Artifact Delivery jest host-owned płaszczyzną delivery i inbound admission dla
artefaktów związanych schemą. Komponent wysyła `artifact-delivery-envelope.v1` przez
`artifact.delivery.send`; daemon waliduje kopertę, sprawdza outbound authority,
rozwiązuje odbiorców, wybiera adaptery transportu, zapisuje delivery i pokazuje status
operatorowi.

Pełny opis operacyjny i diagram są w [Artifact Delivery
HOWTO](../howto/artifact-delivery-howto.pl.md).

## Po co istnieje Artifact Delivery?

Artifact Delivery zapobiega temu, aby każdy komponent stawał się właścicielem własnego
transportu. Komponenty wyrażają intencję delivery; host posiada trasy, wybór adaptera,
retry/recovery, inbound admission, własność acceptorów i status operatorski. Dzięki temu
INAC, Agora, Matrix mailbox, object-store indirection i domenowe acceptory pozostają
warstwami zamiast mieszać się w każdej paczce middleware.

Uzasadnienie i granice warstw są w [sekcji rationale w Artifact Delivery
HOWTO](../howto/artifact-delivery-howto.pl.md).

## Jakie komponenty używają Artifact Delivery?

Główne warstwy to `artifact-delivery-core` dla czystych kontraktów oraz logiki
routingu/autoryzacji, `artifact-delivery` dla runtime ledgerów, recovery i admission,
`ad-host` dla adapterów i acceptorów składanych przez daemon oraz route'y daemona/UI
operatorskie dla statusu. Obecne adaptery obejmują Agora publish, INAC direct, Matrix
mailbox, object-store indirect i node-local loopback tam, gdzie są skonfigurowane.

Mapa komponentów jest w [Artifact Delivery
HOWTO](../howto/artifact-delivery-howto.pl.md).

## Jak middleware może używać Artifact Delivery?

Middleware używa Artifact Delivery w dwóch kierunkach. Outbound delivery oznacza
wywołanie `artifact.delivery.send` z kopertą i przejście hostowej polityki outbound
allow. Inbound delivery oznacza rejestrację acceptora, którego host wywoła dopiero po
wspólnych checkach admission. Instalacja paczki sama z siebie nie nadaje authority AD.

Przykłady dla Rust, supervised HTTP, Sensorium OS Actions i JSON-e Flow są w [sekcji
użycia middleware w Artifact Delivery HOWTO](../howto/artifact-delivery-howto.pl.md).

## Jak konfigurowane jest Artifact Delivery?

Konfiguracja jest własnością hosta. Główne grupy konfiguracji to `artifact_delivery`
routes/allows, `artifact_delivery_adapters`, `inac_peer_transport`,
`artifact_delivery_recovery`, `artifact_delivery_acceptors`,
`artifact_delivery_profiling` i `artifact_delivery_observers`. Koperta kontroluje
pojedyncze żądanie delivery, a nie model authority.

Referencja opcji jest w [Artifact Delivery configuration
HOWTO](../howto/artifact-delivery-howto.pl.md).

## Jakich kształtów danych używa Artifact Delivery?

Główne publiczne kształty to `artifact-delivery-envelope.v1`,
`artifact-delivery-result.v1`, `artifact-delivery-status.v1`,
`artifact-delivery-recovery.v1`, `deferred-operation.v1`,
`deferred-operation-status.v1`, `artifact-object-pointer.v1`, `inac-control.v1` oraz
domenowe artefakty takie jak `agora-record.v1`, `contact-request.v1` czy
`memarium-blob.v1`.

Linki do wygenerowanych schem i lokalnych kształtów daemon admission są w [sekcji data
shapes w Artifact Delivery HOWTO](../howto/artifact-delivery-howto.pl.md).

## Jak Artifact Delivery podejmuje decyzje routingowe?

Routing zaczyna się od `delivery/plan`: referencji do hostowej trasy albo inline stages.
Selektory odbiorców rozwiązywane są do konkretnych celów, polityka outbound jest
sprawdzana względem rozwiniętego planu, a adapter scheme każdego celu wybiera transport.
Ramki transportu przychodzącego wracają potem do wspólnej ścieżki AD admission przed
trafieniem do jednego authoritative acceptora.

Szczegóły selektorów i przykłady sekwencyjne są w [sekcji routingu w Artifact Delivery
HOWTO](../howto/artifact-delivery-howto.pl.md).
