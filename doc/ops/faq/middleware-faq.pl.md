# Middleware FAQ

## Jakie są rodzaje middleware'u?

Middleware to hostowane zachowanie rozszerzające, opisane jawnymi kontraktami. Główne
typy wykonania to Rust w procesie, czysty JSON-e, JSON-e Flow, command/stdio,
niezarządzany lokalny HTTP JSON, nadzorowany `channel_json`, konektory Sensorium oraz
middleware-hosted adaptery runtime Inquirium. Stary nadzorowany executor
`http_local_json` pozostaje wyłącznie na czas przyjętej migracji wycofującej z P080.
Dystrybucja jest osobną osią: middleware
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
Nie rejestruj tej samej semantycznej route'y w obu transportach jako niejawnego
fallbacku. Nowe nadzorowane moduły i paczki muszą używać `channel_json`; zachowany
listener produktowy HTTP jest osobną powierzchnią domenową, a nie executorem
middleware.

Obecne siedem modułów fabrycznych nadal wybiera `http_local_json` podczas migracji
opisanej przez P080-024..P080-033. Jest to stan przejściowy, a nie zalecenie dla
autorów paczek. Po wycofaniu konfiguracje daemona i manifesty paczek nazywające
`http_local_json` będą odrzucane z jawną diagnostyką migracyjną; Node nigdy nie
przekształca ich po cichu.

Moduły Pythonowe powinny używać wspólnego adaptera zamiast implementować framing
WebSocket. Zobacz [Tworzenie middleware channel_json](../howto/middleware-howto.pl.md#tworzenie-middleware-channel-json).

Dla Inquirium katalog model-runtime może wybrać `channel_json`, podając identyfikator
modułu, zadeklarowaną ścieżkę invoke i timeout. Zmienia to wyłącznie transport:
`runtime/ref`, model binding, polityka i walidacja odpowiedzi pozostają własnością hosta.

## Co się dzieje, gdy znika wymagany middleware?

Node nie kieruje dalej wywołań do konsumenta, którego wymagany provider zniknął.
Rozwiązuje dokładne zależności capability-digest kontraktu, usuwa dotkniętych
konsumentów z routingu, wygasza i zatrzymuje ich w kolejności od zależnych do
providerów oraz raportuje `dependency_unavailable`. Dedykowana pętla rekoncyliacji
wznawia konsumentów w kolejności od providerów dopiero po zaobserwowaniu gotowości
dokładnie tych samych wymagań; odczyt health/status nigdy nie uruchamia ani nie
zatrzymuje komponentu. Provider o tej samej nazwie, lecz niezgodnym kontrakcie albo
niespełnionym pinie nie oznacza odzyskania.

To przejście cyklu życia uprząta typowane zasoby lokalne hosta. Efekty trwałe,
zewnętrzne i federacyjne zachowują własną semantykę transakcji, dziennika,
kompensacji, zastąpienia lub zatwierdzania. Zatrzymanie procesu nigdy nie jest
przedstawiane jako cofnięcie takiego efektu. Zobacz [Deklarowanie zależności
komponentów i odzyskiwania po efektach](../howto/middleware-howto.pl.md).

## Czym jest Role Middleware?

Role Middleware nie jest typem wykonania. To wzorzec specjalizacji: komponent middleware
przyjmuje request ukształtowany rolą i rozdziela go do zachowania wybranego po roli,
capability albo tożsamości usługi. Może być zaimplementowany jako nadzorowany channel JSON,
JSON-e Flow albo inna zarejestrowana forma middleware.

Konkretne przykłady dla nadzorowanego channel JSON i JSON-e Flow są w [sekcji Role Middleware w
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

## Jak jeden nadzorowany middleware rozróżnia wywołania z wielu hooków?

Nadzorowany middleware channel może używać jednej zadeklarowanej ścieżki invoke dla
wielu rejestracji, ale ścieżka nie jest semantycznym rozróżnikiem. Middleware powinien
sprawdzać kopertę requestu, zwłaszcza `chain_kind`, `envelope_kind` i schema-specific
kształt payloadu. Oddzielne ścieżki są często czytelniejsze operacyjnie, lecz nawet
wtedy źródłem prawdy pozostaje koperta.

Przykłady requestów i szkice rozgałęziania są w [sekcji multiple-hook dispatch w
Middleware HOWTO](../howto/middleware-howto.pl.md).

## Gdzie opisane są zasady dystrybucji i paczkowania?

Typ wykonania i model dystrybucji są osobne. To samo zachowanie middleware może być
skompilowane w node, dostarczone jako definicja profilu albo zainstalowane jako paczka
operatora. Dystrybucja zmienia postawę zaufania i lifecycle, ale sama nie zmienia
kontraktu runtime.

Referencja modeli dystrybucji jest w [sekcji Modele dystrybucji w Middleware
HOWTO](../howto/middleware-howto.pl.md).
