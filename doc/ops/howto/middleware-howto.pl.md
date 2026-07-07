# Middleware HOWTO

Ten HOWTO zachowuje operacyjny materiał referencyjny, szkice konfiguracji, przykłady hooków i wzorce implementacyjne. Krótszy [Middleware FAQ](../faq/middleware-faq.pl.md) jest wejściem koncepcyjnym.

## Jakie są rodzaje middleware'u?

Middleware Orbipleksu nie jest jednym webowym łańcuchem interceptorów. Jest
hostowaną tkaniną rozszerzeń, w której każdy moduł albo deklaratywna definicja
wnosi zachowanie przez jawne kontrakty, a host Node'a pozostaje właścicielem
cyklu życia, dispatchu, walidacji, bram capability, śladów działania i semantyki
awarii.

Główne typy wykonania i specjalizacji to:

- middleware Rust działający w procesie,
- czysty middleware JSON-e,
- middleware JSON-e Flow,
- middleware command/stdio,
- niezarządzany lokalny middleware HTTP JSON,
- supervised HTTP middleware,
- middleware konektora Sensorium,
- middleware-hosted runtime adapter Inquirium.

Dystrybucja jest osobną osią: ten sam typ wykonania może być dostarczany
fabrycznie, instalowany przez operatora albo materializowany z fragmentu profilu
lub konfiguracji. Zobacz [Modele dystrybucji](#modele-dystrybucji).

### Rust w procesie

Middleware Rust działający w procesie jest kompilowany do binarki Node'a albo do
jednej z crate podłączonych do node'a. To najmniej izolowany i najbardziej
uprzywilejowany kształt, więc rezerwujemy go dla zachowań hosta, które należą
blisko granicy daemona. Ten typ ma sens, gdy zachowanie potrzebuje ciasnego
dostępu do struktur runtime hosta, deterministycznego startu, niskiej latencji
albo bardzo małej zaufanej powierzchni implementacyjnej. Nie powinien być
używany tylko dlatego, że wygodnie jest dopisać kod Rust w daemonie. Jeżeli
zachowanie da się wyrazić przez zadeklarowaną capability, szablon JSON-e albo
supervised module, słabsza forma jest zwykle lepsza. Kontrakt nadal powinien
wyglądać jak middleware: jawne wejście, jawne wyjście, śledzalna decyzja i
walidacja należąca do hosta.

#### Kształt rejestracji

- Crate albo moduł Rust kompilowany do workspace Node'a.
- Rejestracja route'a, hooka albo capability należąca do kodu daemona.
- Testy w crate, która jest właścicielem zachowania.

#### Zastosowania

- Mosty dispatchu należące do hosta, które nie powinny zależeć od zewnętrznych
  procesów.
- Małe bramy polityki ciasno powiązane ze stanem runtime daemona.
- Adaptery niskiego poziomu, gdzie nadzór procesu nie dodawałby użytecznej
  granicy.

#### Przykłady

```rust
pub fn register_builtin_middleware(registry: &mut HostRegistry) {
    registry.register("example.builtin", |input| {
        MiddlewareDecision::continue_with(input)
    });
}
```

### Czysty JSON-e

Czysty middleware `json_e` jest deklaratywnym transformatorem danych. Konkretna
zarejestrowana definicja JSON-e jest traktowana operacyjnie jako osobny komponent
middleware, nawet jeżeli daemon wykonuje ją przez współdzielony executor.
Otrzymuje wyprojektowany przez operatora kontekst JSON, renderuje wartość JSON, a
host waliduje tę wartość względem oczekiwanego kontraktu wyjściowego. Nie ma
ambient authority: nie może otwierać plików, wołać sieci, mutować storage,
wywoływać host capabilities ani oglądać danych, które nie zostały
wyprojektowane do jego kontekstu. To właściwy domyślny wybór dla dopasowań,
selekcji pól, małych przepisań, normalizacji, decyzji routingowych i budowania
odpowiedzi wielkości wskaźnika. Jeżeli szablon zaczyna potrzebować efektów,
polityki retry, długotrwałego stanu albo szerokiego rozgałęziania, należy
przejść do JSON-e Flow albo supervised module.

#### Kształt rejestracji

- Wpis konfiguracji JSON deklarujący tożsamość middleware'u, szablon, limity,
  projekcję kontekstu, profil helperów i kontrakt wyjściowy.
- Opcjonalny fragment konfiguracji dostarczony przez pakiet pod
  `middleware-packages/<id>/config/`.
- Rekordy trace generowane przez hosta, zawierające id szablonu, digest,
  podsumowanie wejścia/wyjścia i wynik walidacji.

#### Zastosowania

- Normalizacja przychodzącego payloadu zanim zobaczy go inny komponent.
- Budowa `middleware-decision.v1` z małego wyprojektowanego kontekstu.
- Renderowanie prostego `service-dispatch-response` bez procesu.
- Wybór route'a albo adnotacja żądania na podstawie jawnych danych.

#### Przykłady

```json
{
  "schema": "middleware-json-e.v1",
  "id": "example.normalizer",
  "profile_version": "orbiplex.json_e.v1",
  "limits": { "timeout_ms": 100 },
  "context_projection": {
    "title": "$.request.title"
  },
  "template": {
    "decision": "allow",
    "payload": { "title": "${title}" }
  },
  "output_contract": "middleware-decision.v1"
}
```

### JSON-e Flow

Middleware `json_e_flow` jest flow należącym do hosta, zbudowanym wokół wejść
kroków renderowanych przez JSON-e. Każda definicja flow jest operacyjnie osobnym,
cienkim komponentem middleware z własną tożsamością, bindingami, limitami,
dozwolonymi wywołaniami, rekordami trace, deklaracją raw-signal i statusem dla
operatora. Współdzielony engine wykonuje flow, ale to definicja flow jest
właścicielem granicy middleware. JSON-e renderuje wartości; host wykonuje
zadeklarowane kroki takie jak `render`, `validate`, `call`, `extract`, `respond`
i `fail`. Dzięki temu efekty pozostają poza szablonem, a flow nadal może wołać
jawnie dopuszczone host capabilities. Używaj tego dla małych, ograniczonych
adapterów, które potrzebują jednego lub kilku kontrolowanych efektów. Jeżeli flow
staje się orkiestracją z dynamicznym generowaniem kroków, szerokim stanem
roboczym albo złożoną polityką domenową, lepszy jest supervised HTTP middleware.

#### Kształt rejestracji

- Wpis konfiguracji daemona `middleware_json_e_flow_services`.
- Szablony flow, definicje kroków, limity, dozwolone wywołania i projekcja
  kontekstu.
- Opcjonalne fragmenty konfiguracji pakietu i metadane UI operatora.
- Trace kroków i digests pod powierzchniami trace należącymi do daemona.

#### Zastosowania

- Adaptacja żądania roli Datora do dyrektywy Sensorium.
- Wywołanie `memarium.write` po wyrenderowaniu ograniczonego faktu.
- Publikacja rekordu ukończenia kroku workflow po udanym wywołaniu capability.
- Niskokodowy middleware dla operatorów, którzy nie powinni potrzebować skryptów
  na poziomie systemu operacyjnego.

#### Przykłady

```json
{
  "id": "example.role.summary",
  "module_id": "example.json-e-flow.roles",
  "profile_version": "orbiplex.json_e_flow.v1",
  "limits": { "timeout_ms": 500, "max_steps": 8 },
  "bindings": {
    "role_capability_id": "role/example.summary.execute"
  },
  "allowed_calls": [
    { "capability": "memarium.write", "operation": "write" }
  ],
  "steps": [
    {
      "id": "response",
      "kind": "respond",
      "template": {
        "status": "ok",
        "result": { "summary": "${request.input.text}" }
      }
    }
  ]
}
```

### Command/Stdio

Middleware command/stdio uruchamia ograniczoną komendę jako jednorazowy proces.
Jest silniejszy niż JSON-e, bo może wykonywać kod programu, ale nadal jest
ograniczony timeoutem, wejściem, wyjściem i polityką hosta. Ten typ jest użyteczny
dla małych narzędzi, które naturalnie mają kształt linii poleceń i nie muszą żyć
między żądaniami. Nie powinien być używany dla długotrwałych usług, kolejkowania,
streamingu ani złożonego lokalnego stanu. Host powinien traktować stdout, stderr,
exit code, timeout i rozmiar wyjścia jako część kontraktu. Operatorzy powinni
unikać dawania mu szerokiego dostępu do systemu plików lub sieci, chyba że use
case wyraźnie tego wymaga.

#### Kształt rejestracji

- Konfiguracja ścieżki komendy i argv.
- Limity timeoutu i rozmiaru wyjścia.
- Opcjonalny executable albo skrypt dostarczony przez pakiet.
- Trace wywołania zawierający tożsamość komendy, exit status i ograniczone
  podsumowania wyjść.

#### Zastosowania

- Wywołanie deterministycznego lokalnego konwertera.
- Uruchomienie małego checkera nad ograniczonym payloadem JSON.
- Opakowanie dojrzałego narzędzia CLI bez nadzorowania daemona.

#### Przykłady

```json
{
  "executor": "command_stdio",
  "module_id": "example.slugify",
  "command": ["./bin/slugify"],
  "limits": {
    "timeout_ms": 1000,
    "stdout_max_bytes": 8192,
    "stderr_max_bytes": 4096
  }
}
```

### Niezarządzany lokalny HTTP JSON

Niezarządzany lokalny middleware HTTP JSON używa już działającej lokalnej usługi.
Host Node'a wie, jak wywołać endpoint, ale nie jest właścicielem cyklu życia tej
usługi. Dzięki temu adapter pozostaje cienki i przydatny w developmentcie,
integracji z lokalnymi usługami zarządzanymi przez operatora albo w przypadkach,
gdzie proces ma już własnego supervisora. Jest słabszy operacyjnie niż supervised
HTTP, bo readiness, polityka restartu, logi i shutdown są poza kontrolą Node'a.
Daemon nadal powinien egzekwować kształt żądania, timeout, limit rozmiaru
odpowiedzi, auth modułu i granice host capabilities. Używaj tego typu, gdy
usługa naprawdę należy poza cykl życia Node'a.

#### Kształt rejestracji

- URL endpointu, metoda, nagłówki, timeout i limit rozmiaru odpowiedzi.
- Brak definicji procesu należącej do daemona.
- Opcjonalny lokalny token auth albo polityka bindingu loopback.

#### Zastosowania

- Połączenie z lokalną usługą uruchomioną przez developera podczas prototypowania.
- Most do lokalnej usługi zarządzanej przez systemd, launchd, Dockera albo inny
  supervisor.
- Integracja narzędzia, które ma własny cykl życia i model zdrowia.

#### Przykłady

```json
{
  "executor": "local_http_json",
  "module_id": "example.external-service",
  "endpoint": "http://127.0.0.1:49110/v1/invoke",
  "method": "POST",
  "limits": {
    "timeout_ms": 2000,
    "response_max_bytes": 65536
  }
}
```

### Supervised HTTP

Supervised HTTP middleware jest długotrwałą lokalną usługą HTTP JSON
uruchamianą, obserwowaną i zatrzymywaną przez host Node'a. To normalny kształt
dla silnego middleware'u, który potrzebuje własnego runtime, stanu, kolejek,
logiki domenowej, operatorskiej powierzchni HTML albo kontaktu z sąsiednimi
systemami. Moduł komunikuje się z daemonem przez jawne kontrakty HTTP/JSON i
otrzymuje token auth modułu zamiast ambient daemon privilege. Podczas startu
powinien wystawiać endpointy health i init/report, aby daemon mógł odkryć route'y,
handlery host capabilities, powierzchnie operatorskie i readiness. Ten typ jest
właściwy dla modułów Python, Rust albo innych modułów procesowych, których
zachowanie jest zbyt bogate dla JSON-e Flow. Jest cięższy niż deklaratywny
middleware, więc używaj go tylko wtedy, gdy dodatkowa granica procesu i cykl życia
kupują klarowność albo realną zdolność.

#### Kształt rejestracji

- Kod usługi dostarczony jako moduł wbudowany albo zainstalowany pakiet.
- `GET /healthz`.
- `POST /v1/middleware/init`.
- Raport modułu deklarujący route'y, capabilities i powierzchnie UI.
- Pliki runtime pod `<data-dir>/middleware/<module-id>/`.

#### Zastosowania

- Katalogi ofert i providery dispatchu podobne do Datora.
- Orkiestracja workflow podobna do Arki.
- Powierzchnie operatorskiego UI wymagające żywego server-rendered HTML.
- Konektory wymagające kolejek, cache'y, retry albo dostępu do zewnętrznych
  narzędzi.

#### Przykłady

```python
from http.server import BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

    def do_POST(self):
        if self.path == "/v1/middleware/init":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"module_id":"example.supervised","status":"ready"}')
```

### Jak sprawić, żeby endpoint middleware był widoczny w OpenAPI / Swaggerze?

Nie uruchamiaj osobnego serwera Swaggera wewnątrz middleware'u. Node daemon
posiada jedną opisową projekcję OpenAPI 3.1 pod `GET /v1/openapi.json`;
opcjonalny Swagger UI czyta tę projekcję daemona. Middleware dostarcza dane, a
nie drugi runtime dokumentacyjny.

Dla supervised HTTP middleware dodaj sekcję `api/surface` do raportu modułu
zwracanego przez `POST /v1/middleware/init`. Sekcja musi być zgodna z
`orbiplex.api-descriptor.v1`.

Minimalny fragment raportu modułu:

```json
{
  "schema_version": "v1",
  "module_id": "example.inquirium",
  "module_name": "Example Inquirium Adapter",
  "api/surface": {
    "schema": "orbiplex.api-descriptor.v1",
    "component/id": "example.inquirium",
    "base/path": "/",
    "endpoints": [
      {
        "method": "POST",
        "path": "/v1/inquirium/invoke",
        "summary": "Invoke the adapter through the host-owned Inquirium contract.",
        "tags": ["inquirium", "middleware"],
        "surface": "internal-loopback",
        "path/owner": "middleware-direct",
        "path/exposure": "internal-loopback",
        "loopback/path": "/v1/inquirium/invoke",
        "path/params": [],
        "request": {
          "schema_ref": "urn:orbiplex:schema:inquirium-adapter-invoke:v1"
        },
        "responses": {
          "200": {
            "schema_ref": "urn:orbiplex:schema:inquirium-adapter-response:v1"
          }
        },
        "x-orbiplex-auth": "module-authtok",
        "x-orbiplex-effect": "mutates-state",
        "x-orbiplex-idempotency": "optional",
        "x-orbiplex-authority": "descriptive-only"
      }
    ]
  }
}
```

Dla middleware'u w Pythonie preferuj jedną współdzieloną tabelę route'ów używaną
zarówno przez dispatch, jak i przez generowanie deskryptora:

```python
ROUTES = (
    {
        "method": "POST",
        "path": "/v1/inquirium/invoke",
        "handler": handle_inquirium_invoke,
        "summary": "Invoke the adapter through the host-owned Inquirium contract.",
        "tags": ["inquirium", "middleware"],
        "surface": "internal-loopback",
        "path_owner": "middleware-direct",
        "path_exposure": "internal-loopback",
        "request_schema_ref": "urn:orbiplex:schema:inquirium-adapter-invoke:v1",
        "response_schema_ref": "urn:orbiplex:schema:inquirium-adapter-response:v1",
    },
)

def api_surface_descriptor(module_id):
    return {
        "schema": "orbiplex.api-descriptor.v1",
        "component/id": module_id,
        "base/path": "/",
        "endpoints": [
            {
                "method": route["method"],
                "path": route["path"],
                "summary": route["summary"],
                "tags": route["tags"],
                "surface": route["surface"],
                "path/owner": route["path_owner"],
                "path/exposure": route["path_exposure"],
                "loopback/path": route["path"],
                "path/params": [],
                "request": {"schema_ref": route["request_schema_ref"]},
                "responses": {"200": {"schema_ref": route["response_schema_ref"]}},
                "x-orbiplex-auth": "module-authtok",
                "x-orbiplex-effect": "mutates-state",
                "x-orbiplex-idempotency": "optional",
                "x-orbiplex-authority": "descriptive-only",
            }
            for route in ROUTES
        ],
    }
```

Reguły praktyczne:

- `path` to ścieżka eksponowana przez hosta i widoczna w projekcji daemona.
- `loopback/path` to surowa lokalna ścieżka middleware'u; jest wymagana dla
  ekspozycji `internal-loopback`.
- Parametry ścieżki używają kanonicznych segmentów OpenAPI `{snake_case}`, a
  każdy parametr ścieżki musi też występować w `path/params`.
- Używaj `schema_ref` tylko dla schematów zapisanych w kanonicznym rejestrze.
  Mały schemat `inline` zostaw dla tymczasowych powierzchni kompatybilności.
- Nigdy nie umieszczaj w `api/surface` wartości tokenów auth, sekretów, promptów,
  sealed payloads ani lokalnych ścieżek absolutnych.
- `x-orbiplex-auth` jest opisową etykietą typu `module-authtok`, nie samym
  tokenem.
- `x-orbiplex-authority` ma zawsze wartość `descriptive-only`; OpenAPI opisuje
  kształt, nie autorytet ani pełną politykę bezpieczeństwa.
- Domyślna projekcja OpenAPI obejmuje tylko wpisy z powierzchni `protocol`.
  Inspekcja developerska/operatorska może jawnie dołączyć inne powierzchnie przez
  `?include=operator,developer,internal-loopback`.

Dla zewnętrznie zarządzanych albo instalowanych pakietowo komponentów HTTP,
które nie zwracają raportu modułu, daemon może też ładować zwalidowane sidecary
deskryptorów z `<data-dir>/api-descriptors/`. Preferuj ścieżkę init-report, gdy
komponent jest nadzorowany przez node.

### Konektor Sensorium

Konektor Sensorium jest osobnym modułem middleware, który implementuje akcje za
granicą organu Sensorium. `sensorium-core` jest mediatorem między daemonem a
katalogami akcji konektorów; sam konektor, taki jak `sensorium-os`, nadal jest
middleware'em. Akcja konektora nie jest osobnym modułem middleware: jest operacją
zadeklarowaną przez konektor i mediowaną przez Sensorium Core. Ten kształt jest
właściwy, gdy moduł potrzebuje kontrolowanego kontaktu z systemem operacyjnym,
lokalnymi aplikacjami, sensorami, narzędziami albo innymi enactowanymi
powierzchniami. Konsumenci powinni zależeć od capability Sensorium, klas akcji i
kontraktów katalogu akcji, nie od twardo zakodowanej implementacji konkretnego
konektora. Specjalizowany deployment może sklonować albo zastąpić konektor jako
nowy moduł middleware, ale powinno to być widoczne jako nowa tożsamość modułu i
katalog akcji.

Dla obecnego hard-MVP konektora `sensorium-os` dostępna powierzchnia runtime jest
celowo wąska: skryptowe akcje C1/C2 mogą działać przez podpisany katalog,
natomiast binarne C1 oraz C3-C7 są raportowane jako niedostępne i fail-closed do
czasu istnienia ich enforcement envelopes. Autoryzowany wpis katalogu jest
źródłem prawdy dla wykonania; lokalne wpisy allowlisty albo override'y
`host_policy` z żądania są odrzucane.

#### Kształt rejestracji

- Usługa albo pakiet konektora.
- Katalog akcji Sensorium.
- Raport modułu deklarujący capabilities konektora i powierzchnie operatorskie.
- Opcjonalne skrypty akcji, szablony albo pliki polityki.

#### Zastosowania

- Akcje na poziomie systemu operacyjnego, takie jak ograniczone sprawdzenia Git,
  deterministyczne lokalne skrypty albo wrappery specyficzne dla deploymentu,
  których klasa akcji i kontrakt wyniku są jawne w katalogu.
- Bezpieczna mediacja między deklaratywnym middleware roli a silnymi lokalnymi
  efektami.
- Konektory specyficzne dla deploymentu z ograniczonym katalogiem akcji.

#### Przykłady

```json
{
  "module_id": "sensorium-os",
  "kind": "sensorium-connector",
  "actions": [
    {
      "action_id": "story009.publication.verify",
      "class": "allowlisted-script",
      "input_schema": "sensorium-directive.v1",
      "output_schema": "sensorium-directive-outcome.v1"
    }
  ]
}
```

### Middleware-hosted runtime adapter Inquirium

Adapter runtime Inquirium może być middleware'em w sensie wykonania i hostowania,
ale semantycznie pozostaje adapterem runtime Inquirium. To rozróżnienie jest
celowe: typ wykonania odpowiada na pytanie "jak ten komponent działa?", a rola
adaptera Inquirium odpowiada na pytanie "jakie tłumaczenie wykonania wolno mu
robić?". Taki adapter może działać przez `command_stdio`, niezarządzany
`local_http_json`, supervised `http_local_json`, handler w procesie albo późniejszy
kompatybilny executor, ale nie dostaje przez to ogólnej władzy middleware'u nad
route'ami, hookami, workflow ani polityką modelu.

Inquirium Core pozostaje właścicielem semantyki operacji takich jak `generate`,
`embed`, `classify`, `rerank`, `image.generate` albo `train.adapt`. `model-runtime`
zajmuje się katalogiem runtime'ów, lifecycle, health, supervision i transportem.
Adapter tłumaczy request/result i szczegóły protokołu providera, a worker modelu
wykonuje obliczenie bez authority Orbipleksu. Jeżeli adapter potrzebuje dostępu do
dużych danych lokalnych, powinien dostać jawne lease'y i uchwyty artefaktów, nie
ambient dostęp do filesystemu, sieci ani host capabilities.

Ten sam adapter nie musi oznaczać jednego modelu. Preferowany podział to:
implementacja adaptera dla interfejsu, instancja adaptera dla konfiguracji
lifecycle/trust boundary oraz osobny `runtime/ref` dla każdej routowalnej
konfiguracji modelu. Dzięki temu jeden adapter instance może utrzymywać wspólną
pulę HTTP, kolejkę, supervisor procesu albo cache klienta, a host nadal widzi
każdy model jako osobny runtime candidate z własną polityką, zdrowiem,
conformance i śladem.

To odpowiada częstemu wzorcowi warstw w agentowych orchestratorach: mechanika
providera, tożsamość modelu, backend wykonawczy oraz kanał interakcji są osobnymi
sprawami. Dla klasyfikacji middleware tylko backend wykonawczy może być
middleware-hosted. Mechanika providera pozostaje sprawą adaptera, tożsamość
modelu sprawą model binding, a kanał albo workflow orchestration pozostaje poza
rolą adaptera.

#### Kształt rejestracji

- Manifest adaptera Inquirium z `adapter/ref`, rodziną protokołu, listą operacji,
  modalnościami, limitami, polityką trace/retention i raportem conformance.
- Opcjonalna konfiguracja middleware executora, np. `command_stdio`,
  `local_http_json` albo `http_local_json`.
- Health/status i init/report, jeżeli adapter jest attachable albo supervised.
- Jawne lease'y, egress, sandbox i `effects/allowed` dla operacji z efektami.

#### Zastosowania

- Most do lokalnego serwera modelu zarządzanego przez operatora albo host Node'a.
- Jednorazowe opakowanie narzędzia CLI wykonującego ograniczoną inferencję.
- Adapter zdalnego API wymagający polityki egress, sekretów, limitów i mapowania
  odmów.
- Post-training, batch embedding albo przetwarzanie audio/wizji przez worker, który
  czyta i zapisuje wyłącznie przez scoped leases.

#### Przykłady

```json
{
  "module_id": "inquirium.local-model-runtime",
  "kind": "inquirium-runtime-adapter",
  "executor": "http_local_json",
  "adapter_manifest": {
    "adapter/ref": "adapter:local-model-runtime",
    "hosting/kind": "middleware-hosted",
    "operations": ["generate", "embed", "batch.embed"],
    "modalities/input": ["text"],
    "modalities/output": ["text", "embedding"],
    "effects/allowed": [
      { "kind": "fs/read", "lease/ref": "input-lease" },
      { "kind": "fs/write", "lease/ref": "artifact-output-lease" }
    ]
  }
}
```

## Czym jest Role Middleware?

Role middleware to middleware, który pełni funkcję providera albo dyspozytora dla
nazwanego kontraktu roli/usługi. Nie jest to typ wykonania taki jak supervised
HTTP, JSON-e Flow, command/stdio albo Rust w procesie. To rola funkcjonalna:
komponent otrzymuje ograniczone żądanie w stylu "wykonaj rolę editorial-review"
albo "obsłuż rolę providera offer-catalog", wybiera właściwe zachowanie i zwraca
wynik w stylu `service-dispatch-response` pod zadeklarowanym kontraktem. Ten sam
wzorzec role middleware może być zaimplementowany różnymi typami wykonania,
zależnie od tego, ile authority, stanu i złożoności runtime potrzebuje dana rola.

Praktyczne rozróżnienie jest takie:

- typ wykonania odpowiada na pytanie "jak ten middleware działa?",
- role middleware odpowiada na pytanie "jaką odpowiedzialność dispatchu ten
  middleware pełni?".

Role middleware nie powinien stawać się generycznym runnerem skryptów ani
ukrytym serwerem aplikacyjnym. Powinien reklamować capability roli, którą
udostępnia, walidować przychodzące żądanie roli, produkować śledzalną odpowiedź
i używać host capabilities tylko przez jawne allowlisty. W Story-009 providerzy
ról dla kompozycji szkicu, przygotowania ilustracji, przeglądu redakcyjnego,
publikacji i weryfikacji są przykładami tego kształtu. Część z nich lepiej
pasuje do JSON-e Flow, bo są ograniczonymi adapterami; inne mogą stać się
supervised HTTP modules, jeśli potrzebują stanu, kolejek, bogatszej polityki albo
operatorskiego UI.

### Role middleware przez supervised HTTP

Supervised HTTP role middleware jest użyteczny, gdy provider potrzebuje realnego
procesu: trwałego lokalnego stanu, kolejkowania, nietrywialnej logiki domenowej,
powierzchni HTML dla operatora albo integracji z sąsiednimi narzędziami. Daemon
startuje i monitoruje proces, wysyła handshake init/report modułu i dispatchuje
żądania roli do modułu przez jawny kontrakt HTTP/JSON. Moduł powinien
rozgałęziać się po role capability albo service type w żądaniu, nie po ukrytym
stanie daemona.

```json
{
  "module_id": "story009-roles-http",
  "executor": "http_local_json",
  "capabilities": [
    {
      "capability_id": "role/story009.editorial-review.execute",
      "kind": "service-dispatch-provider"
    }
  ],
  "invoke_path": "/v1/roles/dispatch"
}
```

```python
def dispatch_role(request):
    role = request["role_capability_id"]

    if role == "role/story009.editorial-review.execute":
        return {
            "schema_version": "v1",
            "capability_id": "service_dispatch_execute",
            "status": "completed",
            "dispatch/id": request["dispatch/id"],
            "answer/content": {"decision": "accepted"},
            "answer/format": "json",
            "confidence/signal": 0.82,
            "human-linked-participation": False
        }

    return {
        "schema_version": "v1",
        "capability_id": "service_dispatch_execute",
        "status": "rejected-invalid-request",
        "dispatch/id": request.get("dispatch/id"),
        "reason": "unsupported role capability"
    }
```

Ten kształt pasuje do providerów podobnych do Datora, usług roli sąsiadujących z
Arką albo modułów instalowanych przez operatora, których zachowanie jest zbyt
bogate dla deklaratywnego flow.

### Role middleware przez JSON-e Flow

JSON-e Flow role middleware jest preferowanym niskokodowym kształtem, gdy rola
jest ograniczonym adapterem: wyrenderuj żądanie, opcjonalnie wywołaj dozwoloną
host capability, wyciągnij wynik i odpowiedz. Każda definicja flow jest
operacyjnie osobnym komponentem role middleware, nawet jeżeli działa przez
współdzielony executor JSON-e Flow. Dzięki temu operator może zainstalować albo
sprawdzić providera roli jako dane, bez dawania mu dostępu do systemu
operacyjnego.

```json
{
  "id": "story009.editorial.review",
  "module_id": "story009.editorial.review",
  "executor": "json_e_flow",
  "bindings": {
    "role_capability_id": "role/story009.editorial-review.execute"
  },
  "limits": { "timeout_ms": 500, "max_steps": 6 },
  "steps": [
    {
      "id": "respond",
      "kind": "respond",
      "template": {
        "schema_version": "v1",
        "capability_id": "service_dispatch_execute",
        "status": "completed",
        "dispatch/id": "${request.dispatch/id}",
        "completed-at": "${now}",
        "answer/content": {
          "decision": "accepted",
          "notes": "Rendered by a bounded JSON-e Flow role provider."
        },
        "answer/format": "json",
        "confidence/signal": 1.0,
        "human-linked-participation": false
      }
    }
  ]
}
```

Używaj JSON-e Flow role middleware dla adapterów roli, które da się opisać jako
dane i których efekty są na tyle wąskie, że można je zadeklarować jako kroki
należące do hosta. Przejdź do supervised HTTP, gdy rola zaczyna wymagać bogatszej
granicy runtime.

## Gdzie middleware może wpinać się w ścieżkę danych node'a?

Middleware może wpinać się w różne miejsca ścieżki danych node'a. Hook mówi, w
którym miejscu komunikat staje się widoczny dla komponentu i jakiego rodzaju
decyzję komponent może zwrócić. Jest to osobne od typu wykonania: supervised HTTP
module, definicja JSON-e Flow albo handler Rust w procesie mogą uczestniczyć w
dispatchu, ale każdy robi to przez powierzchnię należącą do hosta, z jawną
walidacją, timeoutami, bramami capability i rekordami trace. Host pozostaje
odpowiedzialny za routing i authority; middleware wnosi ograniczone zachowanie w
zadeklarowanym punkcie podpięcia. Moduł powinien podpinać się do najwęższego
hooka, który odpowiada jego realnej potrzebie, zamiast subskrybować szeroką fazę,
bo jest to wygodne.

Ogólny słownik decyzji middleware jest zależny od hooka, ale obecne nazwy to:

- `allow` - przepuść wejście do następnego etapu hosta albo handlera.
- `annotate` - pozwól wejściu płynąć dalej, dodając metadane widoczne dla hosta
  tam, gdzie hook ma konkretny nośnik adnotacji.
- `rewrite` - zastąp albo spatchuj payload widoczny dla hosta przed kontynuacją.
- `route` - wybierz jawny cel albo następną trasę tam, gdzie hook to wspiera;
  obecne standardowe chain allowlists nie dopuszczają `route` jako samodzielnej
  decyzji, a lokalny routing używa dyrektyw trasy niesionych obok dozwolonych
  decyzji lokalnych.
- `return` - przerwij ścieżkę odpowiedzią albo finalnym payloadem.
- `drop` - zatrzymaj przetwarzanie bez udanej odpowiedzi.
- `defer` - odmów podjęcia decyzji teraz i pozwól działać kolejnemu etapowi
  polityki hosta.
- `reject` - odmów żądaniu z jawnym błędem/statusem.

Nie każdy hook może emitować każdą decyzję. Niektóre punkty podpięcia, takie jak
wywołania host capabilities albo route'y operatorskiego UI, używają własnych
kontraktów odpowiedzi zamiast `middleware-decision.v1`.

### Hook fazy pre-input

`pre-input` jest pierwszym przejściem należącym do hosta, zanim żądanie wejdzie w
konkretną rodzinę dispatchu. Służy do przekrojowego potraktowania przychodzącego
triggera: normalizacji, redakcji, zachowania raw-signal, wczesnej klasyfikacji
albo lokalnych checków polityki, które muszą wydarzyć się zanim daemon zdecyduje,
czy wejście jest lokalnym żądaniem HTTP, wiadomością peer, zdarzeniem broadcast
czy zadaniem workflow. Należy używać go oszczędnie, bo szerokie hooki zwiększają
koszt poznawczy i mogą stać się ukrytym couplingiem. Uczestnik `pre-input`
powinien zwykle adnotować albo przygotować kontekst trace, a nie przejmować
obsługę domenową.

#### Zastosowania

- Zachowanie `raw_signal` dla ścieżek wykonawczych, które go wymagają.
- Inicjalizacja `causality_id` i `component_path[]`.
- Lokalna redakcja albo klasyfikacja zanim zacznie się węższy dispatch.

#### Przykładowe podpięcie

```json
{
  "module_id": "example.pre-input-policy",
  "input_chains": ["pre-input"],
  "decision_contract": "middleware-decision.v1"
}
```

#### Możliwe decyzje

- `allow` - kontynuuj do normalnego wyboru rodziny dispatchu.
- `annotate` - dodaj lokalne metadane i kontynuuj tam, gdzie host może
  reprezentować adnotację. W obecnej peer-message ścieżce `pre-input`
  adnotacja jest przyjmowana przez słownik, ale nie jest jeszcze reprezentowana
  na `PeerMessageEnvelope`, więc efektywnie jest pass-through.
- `rewrite` - znormalizuj albo zredaguj trigger zanim zacznie się węższy
  dispatch.
- `drop` - zatrzymaj przetwarzanie zanim jakakolwiek konkretna rodzina dispatchu
  zobaczy wejście.

#### Szkic implementacji

Konfiguracja deklaruje szeroki hook; implementacja powinna pozostać mała:

```json
{
  "module_id": "example.pre-input-policy",
  "input_chains": ["pre-input"],
  "executor": "json_e",
  "output_contract": "middleware-decision.v1"
}
```

```json
{
  "decision": "annotate",
  "annotations": { "classification": "operator-local" },
  "diagnostics": {}
}
```

#### Znane użycia

- Kontekst dispatchu raw-signal i component-path w daemonie.
- Żaden obecny fabryczny middleware nie powinien polegać na tym jako na szerokim
  punkcie przechwytywania logiki biznesowej.

#### Kompatybilne typy middleware

- Middleware Rust w procesie.
- Czysty middleware JSON-e, dla czystej normalizacji albo renderowania decyzji.
- Middleware JSON-e Flow, gdy faza potrzebuje ograniczonych efektów należących do
  hosta.
- Middleware command/stdio, technicznie możliwy, ale zwykle zbyt ciężki dla tej
  szerokiej fazy.
- Niezarządzany lokalny middleware HTTP JSON, dla lokalnych usług polityki
  należących do operatora.
- Supervised HTTP middleware, dla silnych lokalnych usług polityki, które
  uzasadniają szeroki hook.
- Middleware konektora Sensorium tylko pośrednio, gdy jest też supervised service
  i ma jawny powód uczestnictwa; szerokie podpięcie pre-input nie powinno być
  domyślne dla konektorów.

### Zgłoszone lokalne route'y i inbound local hooks

Lokalny dispatch obejmuje żądania HTTP odbierane przez lokalnego daemona. Moduł
może zgłosić wyłączny lokalny route, zwykle pod `/v1/enact/*`, albo uczestniczyć
w bardziej generycznym łańcuchu `inbound-local`. Zgłoszone route'y są właściwe,
gdy moduł jest właścicielem konkretnej lokalnej powierzchni API. Generyczne hooki
inbound-local są lepsze dla małych adnotacji żądań, lokalnych decyzji polityki
albo helperów routingu. Jeżeli zgłoszony route istnieje, ale jego moduł właściciel
nie jest gotowy, host zwraca lokalną odpowiedź unavailable zamiast po cichu
routować do innego komponentu.

#### Zastosowania

- Udostępnianie lokalnych API należących do modułu.
- Dodawanie operator-local request handling bez zmian w kodzie daemona.
- Adaptacja wywołań lokalnej aplikacji do decyzji middleware.

#### Przykładowe podpięcie

```json
{
  "module_id": "example.local-route",
  "claimed_routes": [
    { "method": "POST", "path": "/v1/enact/example.local-route/run" }
  ]
}
```

#### Możliwe decyzje

- `allow` - pozwól lokalnemu żądaniu przejść do następnego lokalnego handlera.
- `rewrite` - spatchuj albo zastąp payload lokalnego żądania przed kontynuacją.
- `return` - przerwij ścieżkę lokalną odpowiedzią HTTP.
- `reject` - odmów żądaniu z jawnym lokalnym błędem/statusem.

#### Szkic implementacji

Konfiguracja zgłasza route; żywy moduł obsługuje potem żądanie przez swoją
normalną lokalną usługę HTTP:

```json
{
  "module_id": "example.local-route",
  "executor": "http_local_json",
  "claimed_routes": [
    { "method": "POST", "path": "/v1/enact/example.local-route/run" }
  ]
}
```

```python
def handle_run(request):
    return {
        "status": "ok",
        "result": {"echo": request["json"]}
    }
```

#### Znane użycia

- Supervised HTTP middleware publikujący route'y modułu przez
  `middleware-module-report`.
- Pakiety instalowane przez operatora, które wnoszą metadane UI albo lokalnych
  route'ów.

#### Kompatybilne typy middleware

- Middleware Rust w procesie.
- Czysty middleware JSON-e, dla generycznych transformacji `inbound-local`; nie
  powinien samodzielnie posiadać bogatego zachowania HTTP route'a.
- Middleware JSON-e Flow, dla lokalnych adapterów żądań z zadeklarowanymi
  krokami.
- Middleware command/stdio, dla ograniczonych jednorazowych handlerów lokalnych
  żądań.
- Niezarządzany lokalny middleware HTTP JSON, gdy inny supervisor posiada lokalną
  usługę.
- Supervised HTTP middleware, normalny kształt dla zgłoszonych route'ów modułu.
- Middleware konektora Sensorium, gdy konektor wystawia lokalne route'y modułu
  przez supervised service albo metadane pakietu.

### Role and Service Dispatch

Role and service dispatch to rodzina hooków używana wtedy, gdy workflow prosi o
usługę podobną do capability, a nie o surowe wywołanie procesu. Host routuje
`service-dispatch-request` albo żądanie roli do providera, waliduje odpowiedź i
zapisuje materiał trace. To naturalna powierzchnia dla workflow w stylu Datora i
Arki, bo żądanie jest już sformułowane jako "wykonaj tę rolę/usługę pod tym
kontraktem", a nie "obsłuż tę ścieżkę HTTP". Deklaratywne adaptery takie jak
JSON-e Flow pasują tu dobrze, gdy potrzebują tylko przekształcić ograniczone
żądanie roli i wywołać dozwolone host capabilities.

#### Zastosowania

- Routowanie kroków workflow Arki do providerów odkrytych przez Datora.
- Adaptacja żądań roli do dyrektyw Sensorium.
- Zwracanie ograniczonych wartości `service-dispatch-response` ze śledzalną
  semantyką decyzji.

#### Przykładowe podpięcie

```json
{
  "module_id": "story009.editorial.review",
  "role_capability_id": "role/story009.editorial-review.execute",
  "executor": "json_e_flow"
}
```

#### Możliwe decyzje

- `completed` - provider ukończył żądanie i zwraca treść odpowiedzi, format
  odpowiedzi, sygnał pewności i metadane ukończenia.
- `rejected-invalid-request` - provider odmówił żądaniu, bo nie spełniało jego
  kontraktu.
- `failed` - provider podjął albo przyjął pracę, ale nie mógł jej ukończyć.

#### Szkic implementacji

Konfiguracja wiąże tożsamość providera z role capability; implementacją może być
JSON-e Flow albo supervised service:

```json
{
  "module_id": "story009.editorial.review",
  "executor": "json_e_flow",
  "bindings": {
    "role_capability_id": "role/story009.editorial-review.execute"
  },
  "steps": [
    {
      "id": "response",
      "kind": "respond",
      "template": {
        "schema_version": "v1",
        "capability_id": "service_dispatch_execute",
        "status": "completed",
        "dispatch/id": "dispatch:story009.editorial.review:example",
        "completed-at": "${now}",
        "answer/content": { "decision": "accepted" },
        "answer/format": "json",
        "confidence/signal": 1.0,
        "human-linked-participation": false
      }
    }
  ]
}
```

#### Znane użycia

- `arca` - orkiestracja po stronie workflow i emisja żądań roli/usługi.
- `dator` - katalog ofert i provider-side service dispatch.
- Definicje roli JSON-e Flow w Story-009 - ograniczone adaptery między żądaniami
  roli a wywołaniami host capabilities.

#### Kompatybilne typy middleware

- Middleware Rust w procesie, dla providerów roli należących do hosta.
- Czysty middleware JSON-e, dla adapterów roli zwracających tylko odpowiedź i
  niewymagających efektów.
- Middleware JSON-e Flow, preferowany deklaratywny kształt dla ograniczonych
  adapterów roli z dozwolonymi wywołaniami hosta.
- Middleware command/stdio, dla jednorazowych providerów roli ze ścisłymi
  limitami.
- Niezarządzany lokalny middleware HTTP JSON, dla providerów nadzorowanych
  zewnętrznie.
- Supervised HTTP middleware, normalny kształt dla bogatych providerów takich jak
  Dator i usługi sąsiadujące z Arką.
- Middleware konektora Sensorium zwykle uczestniczy za Sensorium Core, a nie jako
  bezpośredni provider roli.

### Most Host Capability

Most host capability jest używany, gdy middleware potrzebuje ograniczonej
operacji należącej do daemona albo organu, takiej jak zapis faktu do Memarium,
emisja notyfikacji, dispatch wiadomości peer, wystawienie capability passport
albo wywołanie akcji Sensorium. Moduł nie otrzymuje ambient daemon authority;
otrzymuje tylko te wywołania hosta, które są zadeklarowane i przyznane przez
lokalną konfigurację, auth modułu, capability passports i dispatch gates. Ten
hook jest właściwym miejscem przejścia z zachowania middleware do efektów
należących do hosta. Nie powinien być używany jako generyczna furtka do dowolnych
wewnętrznych API.

#### Zastosowania

- Zapis ograniczonego faktu do Memarium z kroku JSON-e Flow.
- Emisja notyfikacji operatora po decyzji modułu.
- Wywołanie Sensorium Core w celu mediacji akcji konektora Sensorium.
- Dispatch wiadomości peer przez powierzchnie sieciowe należące do hosta.

#### Przykładowe podpięcie

```json
{
  "module_id": "example.fact-writer",
  "allowed_calls": [
    { "capability": "memarium.write", "operation": "write" }
  ]
}
```

#### Możliwe decyzje

Most host capability nie używa bezpośrednio `middleware-decision.v1`. Konkretne
capabilities mają własne kontrakty odpowiedzi, ale zaimplementowane klasy wyniku
to:

- `success` - host capability zwraca HTTP `200`, `201` albo `202` i w body
  odpowiedzi nie wykryto semantycznego statusu awarii.
- `host_capability_forbidden` - caller/moduł nie ma prawa wywołać tej host
  capability.
- `host_capability_unavailable` - nie ma zarejestrowanego handlera albo moduł
  handlera nie jest gotowy.
- `host_capability_dispatch_error` - host nie mógł zbudować albo zautoryzować
  lokalnego żądania dispatchu.
- `host_capability_dispatch_failed` - wywołanie handlera nie powiodło się albo
  nie dało się odczytać jego odpowiedzi.
- semantyczne statusy awarii takie jak `failed`, `error`, `timed_out`, `timeout`,
  `rejected`, `rejected-invalid-request`, `not_authorized`, `revocation_stale`,
  `passport_expired`, `passport_invalid`, `passport_revoked` i `policy_denied` -
  traktowane przez JSON-e Flow jako nieudane wykonanie host capability.

#### Szkic implementacji

Konfiguracja deklaruje dozwolone wywołanie; implementacja wywołuje capability
przez krok należący do hosta albo endpoint modułu, a nie przez importowanie
wewnętrznych części daemona:

```json
{
  "module_id": "example.fact-writer",
  "executor": "json_e_flow",
  "allowed_calls": [
    { "capability": "memarium.write", "operation": "write" }
  ],
  "steps": [
    {
      "id": "write-fact",
      "kind": "call",
      "capability": "memarium.write",
      "operation": "write"
    }
  ]
}
```

#### Znane użycia

- Definicje ról JSON-e Flow w Story-009 - `memarium.write` i publikacja faktów
  workflow.
- `sensorium-core` i `sensorium-os` - mediacja akcji Sensorium.
- `arca` i `dator` - wywołania hosta związane z workflow, dispatch i publikacją.

#### Kompatybilne typy middleware

- Middleware Rust w procesie.
- Middleware JSON-e Flow, bo efekty są deklarowane jako kroki wykonywane przez
  hosta.
- Middleware command/stdio, tylko przez wrapper hosta przyznający jawne
  wywołania capability; sama komenda nie powinna otrzymywać ambient authority.
- Niezarządzany lokalny middleware HTTP JSON, gdy jest związany auth modułu i
  jawnymi dozwolonymi wywołaniami.
- Supervised HTTP middleware, standardowy kształt procesowy dla konsumentów host
  capabilities.
- Middleware konektora Sensorium, przez mediację capability/akcji należącą do
  Sensorium.
- Czysty middleware JSON-e nie jest kompatybilny z bezpośrednimi wywołaniami host
  capability; użyj JSON-e Flow, gdy szablon potrzebuje efektów.

### Peer Message Dispatch

Peer message dispatch to rodzina hooków dla wiadomości, które docierają po
dekodowaniu sieci/sesji. Jest węższa niż lokalny routing HTTP i niesie kontrakty
zorientowane na peer, takie jak wywołanie peer message, ustanowienie sesji,
wymiana artefaktów albo prezentacja capability. Wbudowane handlery protokołu
powinny posiadać prawdę protokołu, ale middleware może uczestniczyć tam, gdzie
zachowanie rozszerzające jest jawnie zadeklarowane. Hook peer-message musi być
szczególnie uważny na timeouty, semantykę replay, walidację wejścia i diagnostykę
odmów, bo leży na granicy federacyjnej.

#### Zastosowania

- Obsługa rozszerzeniowych wiadomości peer bez zmieniania głównego handlera
  protokołu.
- Routowanie pracy inter-node artifact channel do uczestnika poza procesem.
- Podpinanie katalogu ofert albo prezentacji capability na granicy peer.

#### Przykładowe podpięcie

```json
{
  "module_id": "example.peer-handler",
  "input_chains": ["inbound-peer"],
  "message_kinds": ["example.peer-message.v1"]
}
```

#### Możliwe decyzje

- `allow` - przekaż wiadomość peer do wbudowanych albo późniejszych handlerów
  peer.
- `rewrite` - znormalizuj zdekodowaną wiadomość peer przed kontynuacją.
- `return` - wyprodukuj odpowiedź peer i zatrzymaj dalszy dispatch peer.
- `drop` - zatrzymaj przetwarzanie wiadomości peer bez udanej odpowiedzi.

#### Szkic implementacji

Konfiguracja subskrybuje chain peer i typ wiadomości; implementacja zwraca
ograniczoną decyzję albo odpowiedź peer przez kontrakt hosta:

```json
{
  "module_id": "example.peer-handler",
  "executor": "http_local_json",
  "input_chains": ["inbound-peer"],
  "message_kinds": ["example.peer-message.v1"]
}
```

```json
{
  "decision": "return",
  "annotations": {},
  "diagnostics": {},
  "patch_strategy": "json_merge_patch",
  "patch": { "response": { "status": "ok" } }
}
```

#### Znane użycia

- Wbudowane handlery protokołu peer dla capability, schema, ledger i wymiany
  artefaktów.
- Przyszłe handlery peer poza procesem używające podpięcia `http_local_json` albo
  `local_http_json`.

#### Kompatybilne typy middleware

- Middleware Rust w procesie, dla handlerów sąsiadujących z protokołem.
- Czysty middleware JSON-e, dla wąskiej normalizacji wiadomości peer albo
  renderowania decyzji.
- Middleware JSON-e Flow, dla ograniczonych adapterów wiadomości peer z
  zadeklarowanymi wywołaniami.
- Middleware command/stdio, technicznie możliwy dla ograniczonych handlerów, ale
  zwykle zbyt kosztowny dla gorących ścieżek federacyjnych.
- Niezarządzany lokalny middleware HTTP JSON, dla handlerów peer nadzorowanych
  zewnętrznie.
- Supervised HTTP middleware, dla handlerów peer poza procesem z readiness i
  cyklem życia.
- Middleware konektora Sensorium nie jest naturalnym hookiem peer-message; użyj
  roli, usługi albo mostu host capability, gdy wejście peer ma wywołać lokalne
  enaction.

### Hooki broadcast

Hooki broadcast obserwują albo transformują zdarzenia broadcast zanim staną się
lokalnymi efektami albo materiałem wychodzącego relay. Są użyteczne dla
moderacji, adnotacji, lokalnej polityki i filtrowania, ale nie powinny stać się
ukrytym globalnym porządkiem logiki biznesowej. Obsługa broadcast powinna
zachować rozróżnienie między tym, że zdarzenie zostało zobaczone, lokalnie
przyjęte, przekazane dalej albo zapisane. Jeżeli moduł potrzebuje trwałej
interpretacji, zwykle powinien zapisać jawny fakt przez host capability, zamiast
mutować broadcast w miejscu.

#### Zastosowania

- Adnotacja albo klasyfikacja zdarzeń broadcast.
- Zastosowanie lokalnej polityki moderacji przed forwardowaniem.
- Drop albo kwarantanna materiału broadcast zgodnie z polityką operatora.

#### Przykładowe podpięcie

```json
{
  "module_id": "example.broadcast-policy",
  "input_chains": ["inbound-broadcast"],
  "decision_contract": "middleware-decision.v1"
}
```

#### Możliwe decyzje

- `allow` - przyjmij zdarzenie broadcast do następnego etapu hosta.
- `annotate` - dodaj metadane polityki i kontynuuj.
- `rewrite` - spatchuj payload widoczny dla broadcast przed kontynuacją.
- `drop` - zatrzymaj lokalne przetwarzanie albo forwardowanie tego zdarzenia.
- `defer` - odmów decyzji i pozwól działać kolejnemu etapowi polityki.

#### Szkic implementacji

Konfiguracja subskrybuje chain broadcast; implementacja emituje wąską decyzję
polityki:

```json
{
  "module_id": "example.broadcast-policy",
  "executor": "json_e",
  "input_chains": ["inbound-broadcast"],
  "output_contract": "middleware-decision.v1"
}
```

```json
{
  "decision": "drop",
  "reason": "blocked by local relay policy",
  "annotations": {},
  "diagnostics": { "policy": "example.broadcast-policy" }
}
```

#### Znane użycia

- Żaden produkcyjny fabryczny middleware nie jest obecnie udokumentowany jako
  właściciel dedykowanego hooka broadcast.
- Komponenty skierowane do Agory są prawdopodobnymi przyszłymi użytkownikami
  powierzchni polityki relay i broadcast.

#### Kompatybilne typy middleware

- Middleware Rust w procesie.
- Czysty middleware JSON-e, dla adnotacji, klasyfikacji albo decyzji polityki.
- Middleware JSON-e Flow, gdy obsługa broadcast potrzebuje ograniczonych efektów
  należących do hosta.
- Middleware command/stdio, dla slow-path albo operator-local broadcast checks.
- Niezarządzany lokalny middleware HTTP JSON, dla zewnętrznie nadzorowanych usług
  polityki.
- Supervised HTTP middleware, dla bogatszych usług moderacji, relay albo polityki.
- Middleware konektora Sensorium zwykle nie jest właściwy, chyba że zdarzenie
  broadcast celowo staje się lokalną akcją mediowaną przez Sensorium.

### Hooki pre-send i egress

`pre-send` jest ostatnim punktem mutacji albo decyzji zanim odpowiedź, wiadomość
peer albo zdarzenie broadcast opuści bieżącą ścieżkę dispatchu należącą do hosta.
Nie jest miejscem do ponownego odkrywania znaczenia biznesowego; to finalna
granica dla kształtowania odpowiedzi, metadanych, lokalnej redakcji albo decyzji
deny/drop, które muszą wydarzyć się po tym, gdy główny handler wyprodukował
wyjście. Ponieważ leży późno na ścieżce, powinien być deterministyczny i mały.
Kosztowna praca należy do role/service dispatch, wywołań host capability albo
bogatszego supervised module przed egress.

#### Zastosowania

- Dodanie finalnych lokalnych metadanych przed egress.
- Redakcja albo normalizacja wychodzących payloadów na granicy.
- Drop wychodzącej wiadomości naruszającej lokalną politykę.

#### Przykładowe podpięcie

```json
{
  "module_id": "example.pre-send-policy",
  "input_chains": ["pre-send"],
  "decision_contract": "middleware-decision.v1"
}
```

#### Możliwe decyzje

- `allow` - wyślij bieżące wyjście bez zmian.
- `rewrite` - spatchuj albo zastąp wychodzący payload przed wysłaniem.
- `drop` - zatrzymaj wyjście przed opuszczeniem tej ścieżki dispatchu.

#### Szkic implementacji

Konfiguracja subskrybuje chain egress; implementacja zwraca małą decyzję
brzegową:

```json
{
  "module_id": "example.pre-send-policy",
  "executor": "json_e",
  "input_chains": ["pre-send"],
  "output_contract": "middleware-decision.v1"
}
```

```json
{
  "decision": "rewrite",
  "patch_strategy": "json_merge_patch",
  "patch": { "headers": { "x-orbiplex-local-policy": "applied" } },
  "annotations": {},
  "diagnostics": {}
}
```

#### Znane użycia

- Kształtowanie odpowiedzi, metadane, polityka deny/drop i finalna lokalna
  redakcja.
- Żaden produkcyjny fabryczny middleware nie jest obecnie udokumentowany jako
  właściciel dedykowanego hooka `pre-send`.

#### Kompatybilne typy middleware

- Middleware Rust w procesie.
- Czysty middleware JSON-e, dla finalnych czystych transformacji.
- Middleware JSON-e Flow, tylko gdy egress wymaga ograniczonych efektów
  należących do hosta.
- Middleware command/stdio, technicznie możliwy, ale zwykle zbyt kosztowny dla
  tej późnej granicy.
- Niezarządzany lokalny middleware HTTP JSON, dla usług polityki egress należących
  do operatora.
- Supervised HTTP middleware, dla bogatszych powierzchni polityki egress, gdy
  latencja jest akceptowalna.
- Middleware konektora Sensorium nie jest naturalnym hookiem egress; użyj mediacji
  akcji Sensorium wcześniej na ścieżce.

### Powierzchnie operatorskiego UI

Powierzchnie operatorskiego UI nie są hookami data-plane, ale są ważnym punktem
podpięcia middleware. Moduł albo pakiet może wnieść szablony UI, statyczne assety,
metadane route'ów i workflow operatorskie, aby wbudowane Node UI nie musiało mieć
twardo zakodowanej wiedzy o każdym przyszłym module. Daemon nadal jest
właścicielem montowania route'ów, kontekstu sesji, autoryzacji i bezpiecznych
granic renderowania. To właściwa powierzchnia dla dashboardów lokalnych dla
modułu, ekranów przeglądu akcji, konfiguracji pakietu i czytelnych dla człowieka
eksploratorów trace.

#### Zastosowania

- Udostępnienie historii uruchomień i stron statusu modułu.
- Dodanie stron konfiguracji operatora dla zainstalowanych pakietów.
- Renderowanie specyficznych dla modułu ekranów przeglądu akcji albo workflow
  readiness.

#### Przykładowe podpięcie

```json
{
  "module_id": "example.operator-ui",
  "operator_surfaces": [
    { "path": "/middleware/example/", "template": "ui/index.html" }
  ]
}
```

#### Możliwe decyzje

Powierzchnie operatorskiego UI nie używają `middleware-decision.v1`; ich wybory
na poziomie kodu to tryby własności renderowania i wyniki HTTP/UI:

- `host-mediated` - Node UI posiada renderowany HTML używając metadanych
  pakietu/modułu.
- `server-html` - żywy moduł middleware posiada HTML, a Node UI proxy'uje
  powierzchnię same-origin.
- `unavailable` - Node UI renderuje stronę unavailable/error, gdy nie da się
  rozwiązać pakietu, powierzchni albo modułu backing.
- `redirect-rewrite` - redirecty same-origin z proxy'owanego server HTML mogą
  zostać przepisane pod zamontowaną powierzchnię; redirecty zewnętrzne są
  odrzucane.

#### Szkic implementacji

Konfiguracja deklaruje powierzchnię; implementacją może być statyczne UI pakietu
albo żywy supervised route:

```json
{
  "module_id": "example.operator-ui",
  "operator_surfaces": [
    {
      "path": "/middleware/example/",
      "template": "ui/index.html",
      "requires_operator_session": true
    }
  ]
}
```

```html
<section>
  <h1>Example middleware</h1>
  <p>Status is rendered by the host from module report data.</p>
</section>
```

#### Znane użycia

- `arca` - UI uruchomień workflow.
- Powierzchnie trace JSON-e Flow.
- Przykłady pakietów instalowanych przez operatora z materiałem `ui/` i `ui-op/`.

#### Kompatybilne typy middleware

- Middleware Rust w procesie, gdy UI należy do hosta.
- Czysty middleware JSON-e, przez widoki metadanych i trace/config zamiast żywego
  serwera UI.
- Middleware JSON-e Flow, przez powierzchnie trace, statusu i konfiguracji.
- Middleware command/stdio, przez host-rendered status/config surfaces.
- Niezarządzany lokalny middleware HTTP JSON, jeżeli operator jawnie akceptuje
  zewnętrznie zarządzany endpoint UI.
- Supervised HTTP middleware, normalny kształt dla żywego UI modułu.
- Middleware konektora Sensorium, przez katalogi akcji konektora i powierzchnie
  operatorskie należące do konektora.
- Pakiety instalowane przez operatora i moduły dostarczane fabrycznie mogą wnosić
  assety UI; to kwestia modelu dystrybucji nałożona na typ wykonania.

### Obserwatorzy i hooki audit

Obserwatorzy i hooki audit są powierzchniami widoczności. Mają zapisywać, co się
wydarzyło, a nie stawać się kolejną ukrytą warstwą decyzji. Nowi konsumenci
powinni preferować obserwatorów faz i obserwatorów post-chain dla widoczności;
`audit` pozostaje powierzchnią kompatybilności po dispatchu. Rekordy trace
powinny zachowywać causality, component path, wybrane podsumowania oraz
skonfigurowane raw-signal albo szczegóły component I/O bez wyciekania sekretów
lub niepotrzebnych payloadów. Jeżeli obserwator musi wpływać na zachowanie,
powinien zostać zamodelowany jako prawdziwy hook dispatchu zamiast efektu
ubocznego audytu.

#### Zastosowania

- Zapis podsumowań component I/O trace.
- Emisja rekordów audit dla decyzji autoryzacji albo dispatchu.
- Diagnostyka operatorska bez zmiany zachowania runtime.

#### Przykładowe podpięcie

```json
{
  "module_id": "example.trace-observer",
  "observes": ["pre-input", "inbound-local", "post-chain"],
  "mode": "observer"
}
```

#### Możliwe decyzje

- `allow` - kompatybilnościowa odpowiedź oczekiwana przez legacy handlery audit
  invoke. Obserwacja nie może zmieniać funkcjonalnego wyniku dispatchu, a
  requesty obserwatorów używające `peer-message-observe.v1` nie używają
  `middleware-decision.v1`.

Awarie wywołania obserwatora są polityką hosta, nie decyzjami middleware. Obecna
ścieżka peer audit wywołuje obserwatorów asynchronicznie i loguje awarie bez
zmiany wyniku widocznego dla callera.

#### Szkic implementacji

Konfiguracja deklaruje wyłącznie obserwację; implementacja zapisuje i nie zwraca
decyzji biznesowej:

```json
{
  "module_id": "example.trace-observer",
  "observes": ["pre-input", "inbound-local", "post-chain"],
  "mode": "observer"
}
```

```rust
fn record(event: TraceEvent) {
    tracing::info!(
        event = "middleware_trace_observed",
        component_path = ?event.component_path,
        decision = ?event.decision
    );
}
```

#### Znane użycia

- Powierzchnie trace daemona dla dispatchu middleware.
- Sinki audit autoryzacji i host capability.
- Widoki trace i digest kroków JSON-e Flow.

#### Kompatybilne typy middleware

- Middleware Rust w procesie, dla sinków audit i kolektorów trace należących do
  hosta.
- Czysty middleware JSON-e, dla czystej projekcji podsumowań trace.
- Middleware JSON-e Flow, dla ograniczonych workflow obserwatora.
- Middleware command/stdio, dla ograniczonych zadań eksportu albo diagnostyki.
- Niezarządzany lokalny middleware HTTP JSON, dla usług obserwowalności
  zarządzanych przez operatora.
- Supervised HTTP middleware, dla bogatszych konsumentów audit/trace z własnym
  cyklem życia.
- Middleware konektora Sensorium powinien zwykle emitować obserwacje przez
  Sensorium i powierzchnie audit hosta, a nie podpinać się jako generyczny
  obserwator, chyba że ta rola jest jawnie zadeklarowana.

## Jak jeden HTTP middleware rozróżnia wywołania z wielu hooków?

Supervised HTTP middleware może podpinać się do więcej niż jednego hooka. Na
przykład jeden moduł może obsługiwać input chain i jednocześnie obserwować audit
chain. Host może wołać ten sam endpoint HTTP dla obu hooków, jeżeli raport modułu
albo lokalna konfiguracja używa tego samego `invoke_url` dla obu rejestracji. To
jest legalne, ale ścieżka route'a nie jest semantycznym rozróżnikiem. Kanonicznym
rozróżnikiem jest koperta żądania, zwłaszcza `chain_kind`.

Dla ścieżek handlerów peer-message host wysyła `PeerMessageInvokeRequest`.
Legacy powierzchnia peer-message `audit` również używa tego kształtu invoke, ale
jej wynik jest obserwacyjny: zwrócone decyzje i awarie wywołania nie zmieniają
wyniku dispatchu widocznego dla callera. Ten sam endpoint może otrzymywać
wywołania `inbound-peer` i legacy `audit`:

```json
{
  "schema_version": "v1",
  "envelope_kind": "peer-message",
  "msg": "example.message.v1",
  "chain_kind": "audit",
  "correlation_id": "corr:example",
  "remote_node_id": "node:did:key:z6Mk...",
  "payload": {
    "input_payload": { "example": true },
    "response": null,
    "elapsed_ms": 7
  }
}
```

Dla lokalnego dispatchu HTTP obowiązuje ta sama reguła przez lokalną kopertę
invoke wejścia: moduł powinien rozgałęziać się po `chain_kind`, a nie po
niejawnym założeniu o ścieżce, która została wywołana.

Dla obserwatorów faz i obserwatorów post-chain host wysyła
`peer-message-observe.v1` z `envelope_kind = "peer-message-observe"` oraz
`observation_kind = "phase"` albo `"post-chain"`. Te requesty obserwatorów są
powierzchniami metadanych/trace, a nie punktami decyzyjnymi.

```python
def handle_hook(request):
    chain = request["chain_kind"]

    if chain == "inbound-local":
        return handle_inbound_local(request)

    if chain == "audit":
        record_audit(request)
        return {
            "decision": "allow",
            "annotations": {},
            "diagnostics": {}
        }

    return {
        "decision": "reject",
        "reason": f"unsupported chain_kind {chain}",
        "annotations": {},
        "diagnostics": {}
    }
```

Użycie jednego endpointu jest rozsądne dla małego modułu z jednym wewnętrznym
dispatcherem. Dla większych modułów oddzielne ścieżki HTTP są zwykle
czytelniejsze operacyjnie:

```json
{
  "module_id": "example.multi-hook",
  "hooks": [
    {
      "chain_kind": "inbound-peer",
      "invoke_url": "http://127.0.0.1:49120/hooks/inbound-peer"
    },
    {
      "chain_kind": "audit",
      "invoke_url": "http://127.0.0.1:49120/hooks/audit"
    }
  ]
}
```

Nawet wtedy `chain_kind` pozostaje częścią kontraktu. Ścieżka jest wygodą
diagnostyczną i routingową; koperta jest źródłem prawdy.

## Modele dystrybucji

Typ wykonania mówi, jak middleware działa. Model dystrybucji mówi, jak kod,
definicja, konfiguracja albo pakiet trafia do node'a i jak operator to akceptuje.
Te osie celowo się przecinają: supervised HTTP module może być dostarczany
fabrycznie albo instalowany przez operatora, a definicja JSON-e Flow może być
dostarczana jako profil akceptacyjny bez stawania się samodzielnym modułem
procesowym.

### Middleware dostarczany fabrycznie

Bundled middleware jest dystrybuowany ze źródłami Node'a albo dystrybucją
binarną. Nadal może być supervised HTTP, JSON-e Flow, Rustem w procesie albo
innym typem executora; "bundled" opisuje dystrybucję i postawę zaufania, nie
mechanikę wykonania. Moduły bundled są użyteczne, gdy capability jest częścią
systemu referencyjnego, ale powinna pozostać poza zaufanym rdzeniem daemona. Mogą
otrzymać pierwszoklasowe pokrycie runbookiem, testy, domyślne fragmenty
konfiguracji i integrację UI operatora. Bundling nie usuwa potrzeby raportów
modułu, bram host capability, readiness, trace ani least privilege. Jeżeli moduł
bundled nie jest wymagany przez deployment, operator powinien móc go wyłączyć.

#### Ścieżka dostarczenia

- Kod źródłowy albo executable dostarczony w dystrybucji Node'a.
- Domyślne fragmenty konfiguracji.
- Profile akceptacyjne albo fixtures.
- Testy, runbooki i assety operatorskiego UI, gdy dotyczy.

#### Middleware dostarczany fabrycznie

- `sensorium-core` - bundled in-process Sensorium organ boundary.
- `sensorium-os` - bundled middleware konektora Sensorium.
- `arca` - bundled middleware workflow/orkiestracji.
- `dator` - bundled katalog ofert i middleware dispatchu.
- `recovery-service` - bundled middleware recovery-service.
- `snooper` - bundled middleware obserwacyjny/debug.
- `whisper-intake` - bundled middleware intake Whisper.
- `agora-service` - bundled middleware usługi skierowanej do Agory.
- `agora-verifier` - bundled middleware helpera weryfikacji Agory.
- `agora-demo` - bundled demonstracyjny middleware Agory.

#### Zastosowania

- Referencyjne moduły Arca, Dator, Sensorium OS albo Seed Directory.
- Hard-MVP capabilities, które powinny działać od razu.
- Moduły demonstracyjne używane przez historie akceptacyjne.

#### Przykłady

```json
{
  "module_id": "example.bundled",
  "executor": "http_local_json",
  "bundle": {
    "kind": "python-module",
    "entrypoint": "middleware-modules/example/service.py"
  },
  "enabled": true
}
```

### Definicje dystrybuowane przez profil

Definicje dystrybuowane przez profil są definicjami middleware dostarczanymi jako
część profilu akceptacyjnego, fixture runbooka albo fabrycznego szkieletu
konfiguracji, a nie jako samodzielny pakiet modułu. Ten model dystrybucji jest
użyteczny dla deklaratywnego middleware, zwłaszcza JSON-e Flow, gdzie operacyjnym
komponentem jest sama definicja flow. Profil może materializować fragmenty
konfiguracji do data directory podczas bootstrapu, ale stan runtime nadal należy
do normalnych katalogów runtime zarządzanych przez daemona. Operatorzy powinni
móc sprawdzić i zaakceptować zmaterializowane definicje zanim staną się aktywne w
profilach podobnych do produkcyjnych. Ten model nie powinien ukrywać silnego
zachowania: wywołania host capability, limity, dostęp raw-signal i route'y UI
operatora pozostają jawne w definicji.

#### Ścieżka dostarczenia

- Profil akceptacyjny, szkielet bootstrapu albo fixture runbooka.
- Fabryczne fragmenty konfiguracji materializowane do katalogu danych node'a.
- Deklaratywne definicje middleware takie jak wpisy usług JSON-e Flow.
- Opcjonalnie wygenerowane paszporty, bindingi albo artefakty readiness potrzebne
  profilowi.

#### Middleware dostarczany fabrycznie

- Definicje ról JSON-e Flow w Story-009 - bundled definicje flow profilu
  akceptacyjnego używane do adaptacji żądań roli do ograniczonych wywołań host
  capability.

#### Zastosowania

- Dostarczenie pełnej historii albo profilu akceptacyjnego działającego bez
  dedykowanego modułu procesowego.
- Materializacja niskokodowych adapterów roli jako danych.
- Utrzymanie demonstracyjnego i bootstrapowego middleware'u w sposób
  reprodukowalny bez robienia z każdej definicji osobno wersjonowanego pakietu.

#### Przykłady

```json
{
  "profile": "story-009",
  "materializes": [
    "middleware_json_e_flow_services.story009.editorial.review",
    "middleware_json_e_flow_services.story009.sensorium.prepare"
  ]
}
```

### Pakiet instalowany przez operatora

Pakiet middleware instalowany przez operatora jest artefaktem umieszczanym pod
`<data-dir>/middleware-packages/<package-id>/`. Może wnosić konfigurację modułu,
statyczne fragmenty UI, metadane powierzchni operatorskich, skrypty, szablony i
inne pliki należące do pakietu. Drzewo pakietu jest traktowane jako powierzchnia
artefaktu: semantyczne pliki powinny być podpisane albo inaczej zatwierdzone,
zanim daemon aktywuje wniesioną konfigurację. Stan runtime nie należy do drzewa
pakietu; należy pod `<data-dir>/middleware/<module-id>/`. Ten typ jest użyteczny
dla lokalnej rozszerzalności bez wymagania, aby wbudowane UI albo daemon znały
każdy przyszły moduł. Pakiet może instalować deklaratywne flow, supervised
service albo powierzchnie UI, ale host nadal jest właścicielem aktywacji i
polityki.

#### Ścieżka dostarczenia

- `middleware.package.json`.
- Fragmenty konfiguracji pakietu `config/*.json`.
- Statyczne host-rendered fragmenty UI w `ui/`.
- Deklaracje powierzchni operatorskich w `ui-op/`.
- Opcjonalne sidecary `.signatures/`.

#### Dołączone przykłady

- Żaden produkcyjny pakiet nie jest obecnie traktowany jako fabrycznie
  zainstalowany pakiet operatora. Dokumentacja dostarcza przykłady pakietów takie
  jak `middleware-package-ui`, `middleware-python-package-ui`,
  `role-module-http`, `role-module-json-e`, `json-e-flow-role` i
  `sensorium-connector`.

#### Zastosowania

- Instalacja zewnętrznego albo lokalnego middleware operatora.
- Dodanie powierzchni operatorskiego UI bez zmian w kodzie Node UI.
- Dostarczenie predefiniowanych adapterów JSON-e Flow jako danych.
- Utrzymanie materiału pakietu osobno od stanu runtime.

#### Przykłady

```text
middleware-packages/example-package/
  middleware.package.json
  config/
    50-example-flow.json
  ui/
    index.html
  ui-op/
    operator-surfaces.json
```

```json
{
  "schema": "middleware.package.v1",
  "package_id": "example-package",
  "modules": [
    { "module_id": "example.flow", "config": "config/50-example-flow.json" }
  ]
}
```
