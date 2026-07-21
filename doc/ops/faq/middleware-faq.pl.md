# Middleware FAQ

## Jakie są rodzaje middleware'u?

Middleware to hostowane zachowanie rozszerzające, opisane jawnymi kontraktami. Główne
typy wykonania to Rust w procesie, czysty JSON-e, JSON-e Flow, command/stdio,
niezarządzany lokalny HTTP JSON, supervised HTTP, konektory Sensorium oraz
middleware-hosted adaptery runtime Inquirium. Dystrybucja jest osobną osią: middleware
może być dostarczone fabrycznie, przez profil albo jako paczka instalowana przez
operatora niezależnie od typu wykonania.

Szczegółowe opisy typów, kształty rejestracji i przykłady są w [Middleware
HOWTO](../howto/middleware-howto.pl.md).
Granica pomiędzy czystym interpreterem a krokami przepływu należącymi do hosta jest
opisana w [FAQ JSON-e i JSON-e Flows](json-e-and-json-e-flows-faq.pl.md).

## Kiedy moduł powinien używać `channel_json`?

Użyj `channel_json` dla kwalifikującego się nadzorowanego modułu, którego listener
loopback istnieje wyłącznie po to, aby host Node'a mógł wykonać attach, invoke,
observation albo wystawić powierzchnię operatorską przez własny most. Moduł inicjuje
uwierzytelnioną sesję do wspólnego listenera daemona; sesja nie nadaje trwałej
władzy ani nie jest kolejką replay.

Zachowaj jawny listener produktowy, peerowy, przeglądarkowy lub providerowy, jeśli
jest częścią kontraktu komponentu. Moduł mieszany migruje tylko host-control plane.
Nie rejestruj tej samej semantycznej route'y w obu executorach jako niejawnego
fallbacku. `channel_json` albo `http_local_json` wybiera konfiguracja, a rollback
powinien być testowany świadomie.

Moduły Pythonowe powinny używać wspólnego adaptera zamiast implementować framing
WebSocket. Zobacz [Tworzenie middleware channel_json](../howto/middleware-howto.pl.md#tworzenie-middleware-channel-json).

Dla Inquirium katalog model-runtime może wybrać `channel_json`, podając identyfikator
modułu, zadeklarowaną ścieżkę invoke i timeout. Zmienia to wyłącznie transport:
`runtime/ref`, model binding, polityka i walidacja odpowiedzi pozostają własnością hosta.

## Czym jest Role Middleware?

Role Middleware nie jest typem wykonania. To wzorzec specjalizacji: komponent middleware
przyjmuje request ukształtowany rolą i rozdziela go do zachowania wybranego po roli,
capability albo tożsamości usługi. Może być zaimplementowany jako supervised HTTP,
JSON-e Flow albo inna zarejestrowana forma middleware.

Konkretne przykłady dla supervised HTTP i JSON-e Flow są w [sekcji Role Middleware w
Middleware HOWTO](../howto/middleware-howto.pl.md).

## Gdzie middleware może wpinać się w ścieżkę danych node'a?

Obecne peer-message chains to `pre-input`, `inbound-peer`, `pre-send` oraz obserwatory
`post-chain`. Inne powierzchnie middleware obejmują zgłoszone lokalne route'y,
role/service dispatch, mosty host capability, obsługę broadcast, powierzchnie
operatorskiego UI oraz read-only hooki observer/audit. Kluczowa zasada: każde podpięcie
ma własny kontrakt requestu i własny zestaw dozwolonych decyzji; nie ma jednego
uniwersalnego kontraktu interceptora.

Pełna mapa hooków, decyzji, przykładów i kompatybilności jest w [Middleware hook
HOWTO](../howto/middleware-howto.pl.md).

## Jak jeden HTTP middleware rozróżnia wywołania z wielu hooków?

Supervised HTTP middleware może używać jednego endpointu dla wielu rejestracji, ale
ścieżka HTTP nie jest semantycznym rozróżnikiem. Middleware powinien sprawdzać kopertę
requestu, zwłaszcza `chain_kind`, `envelope_kind` i schema-specific kształt payloadu.
Oddzielne ścieżki są często czytelniejsze operacyjnie, lecz nawet wtedy źródłem prawdy
pozostaje koperta.

Przykłady requestów i szkice rozgałęziania są w [sekcji multiple-hook dispatch w
Middleware HOWTO](../howto/middleware-howto.pl.md).

## Gdzie opisane są zasady dystrybucji i paczkowania?

Typ wykonania i model dystrybucji są osobne. To samo zachowanie middleware może być
skompilowane w node, dostarczone jako definicja profilu albo zainstalowane jako paczka
operatora. Dystrybucja zmienia postawę zaufania i lifecycle, ale sama nie zmienia
kontraktu runtime.

Referencja modeli dystrybucji jest w [sekcji Modele dystrybucji w Middleware
HOWTO](../howto/middleware-howto.pl.md).
