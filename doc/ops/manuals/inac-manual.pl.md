# Podręcznik operatorski: INAC (Inter-Node Artifact Channel)

INAC jest adapterem bezpośredniego transportu między węzłami. Przenosi artefakty
Orbiplex bez zmiany ich bajtów i bez publikowania ich w publicznej warstwie
komunikacyjnej.

Pojęcia wprowadzające wyjaśnia
[Artifact Delivery FAQ](../faq/artifact-delivery-faq.pl.md), a procedury i
przykłady zawiera
[Artifact Delivery HOWTO](../howto/artifact-delivery-howto.pl.md).

## 1. Cel i funkcje

INAC pozwala węzłom wymieniać artefakty **prywatnie i bezpośrednio**, bez
publikowania ich w przekaźniku tematycznym. Agora obsługuje publiczny lub
półpubliczny obieg tematyczny. Artifact Delivery przyjmuje od komponentów
zlecenia doręczenia i wybiera transport, a INAC wykonuje prywatny transport
między węzłami. Memarium pozostaje lokalnym magazynem powierzonych danych.

Funkcje:

- wymiana ofert, żądań, przesłań (`push`) i odmów artefaktów przez
  uwierzytelnione sesje z węzłami partnerskimi (`peer`),
- utrzymanie bajtowej identyczności koperty artefaktu przez cały transfer i zapis,
- korzystanie z istniejących mechanizmów autoryzacji — paszportów zdolności,
  zaproszeń i opieki nad danymi (`custody`) — zamiast tworzenia własnego źródła
  autorytetu,
- przekazywanie odebranych artefaktów do wspólnej ścieżki przyjmowania Artifact
  Delivery, która ma dokładnie jeden autorytatywny odbiornik domenowy
  (`acceptor`) dla danego rodzaju,
- przenoszenie dużych ładunków poza główną ramką kontrolną JSON, w porcjach
  strumienia związanych z konkretną sesją i treścią.

## 2. Zasada działania

Węzły wymieniają ramki `inac-control.v1` przez kanał wiadomości
`msg = "inac.v1"` w uwierzytelnionej sesji WSS. Ramka zawiera operację,
opcjonalny identyfikator korelacji, opis artefaktu i transferu, dane autoryzacji
oraz odpowiedź.

Operacje inicjujące: `offer`, `request`, `push`.
Operacje odpowiedzi: `accept`, `decline`, `defer`, `ingested`, `already-present`, `refused`, `partial`.

Ładunek może znajdować się dokładnie w jednym miejscu: bezpośrednio w ramce
(`inline`) albo w strumieniu. Host sprawdza tę rozłączność. Małe ładunki mieszczą
się w ramce; większe są przesyłane porcjami. Preferowany kontrakt to
`inac.stream.chunk.binary.v1`, ze sprawdzaniem skrótu kryptograficznego
(`digest`), przesunięcia i rozmiaru każdej porcji. Wariant JSON/base64url
pozostaje zapasową ścieżką zgodności. Zdekodowana porcja większa niż 8 MiB jest
odrzucana **przed** dopisaniem do pliku.

Odebrane ramki `push` nie mają osobnej tablicy kierowania. Trafiają do wspólnego
rejestru odbiorników Artifact Delivery. Brak zarejestrowanej obsługi rodzaju
artefaktu (`handler`) oznacza odmowę; dane nie są przyjmowane domyślnie.

Lokalne zezwolenia wychodzące (`outbound/allows`) domyślnie odmawiają dostępu.
Pusty zbiór `operations` albo `schemas` oznacza brak autorytetu, a nie zgodę na
wszystkie wartości.

## 3. Umiejscowienie w architekturze i kanały komunikacji

INAC działa nad uwierzytelnionymi sesjami z węzłami partnerskimi i równolegle do
Agory. Komponenty zlecają jednak doręczenie przez Artifact Delivery. Nie
zarządzają gniazdami WSS, sesjami, rejestrem zaproszeń ani znaczeniem operacji
`offer` i `push`; odpowiadają za nie warstwa sesji węzłów i host INAC.

Kanały i ich uzasadnienia:

| Kanał | Kierunek | Uzasadnienie |
| --- | --- | --- |
| `msg = "inac.v1"` w łańcuchu wiadomości węzłów (WSS) | dwukierunkowy, węzeł ↔ węzeł | Jedyny kanał sieciowy INAC. Korzysta z istniejącej uwierzytelnionej sesji, więc nie wprowadza własnego uwierzytelniania transportu. |
| Porcje strumienia (`inac.stream.chunk.binary.v1`, zapasowy JSON/base64url) | dwukierunkowy, węzeł ↔ węzeł | Przenoszą duże dane poza ramką kontrolną. Są związane z sesją i adresem treści, dlatego nie można ich użyć poza właściwym transferem. |
| `PeerSender` z `ad-host` | wychodzący, komponent → INAC | Konsumencka strona Artifact Delivery prosi o doręczenie przez INAC bez posiadania wiedzy o transporcie. |
| `InacAdmissionBridge` → rejestr odbiorników Artifact Delivery | przychodzący, INAC → host | Odebrane ramki wchodzą we wspólną ścieżkę przyjmowania zamiast do osobnej dyspozycji INAC. Dzięki temu dla danego rodzaju artefaktu istnieje dokładnie jeden autorytatywny odbiornik. |
| `POST /v1/host/capabilities/inac.offer`, `…/inac.request`, `…/inac.push` | przychodzący, lokalny komponent → daemon | Hostowe zdolności dla komponentów nadzorowanych; wymagają jawnego zezwolenia wychodzącego. |
| `GET /v1/inac/status` | odczyt, operator → daemon | Widok statusu dla operatora; nie nadaje autorytetu. |
| Rejestr transferów SQLite | zapis/odczyt, lokalny dysk | Trwałe decyzje o transferach, oczekujące oferty i kontakty. |
| Magazyn strumieni na dysku | zapis/odczyt, lokalny dysk | Składanie porcji przed przekazaniem artefaktu do odbiornika. |
| Dowód adresu z Seed Directory (`node-address-attestation.v1`) | odczyt, wykrywanie węzłów → nadzorca połączeń | Odcisk certyfikatu adresu trafia do danych kandydata połączenia. Świeży dowód ma pierwszeństwo przed statycznie przypiętym odciskiem; przeterminowany nie może zostać użyty do połączenia. |
| Powiadomienia operatorskie (przepływ zaproszeń) | wychodzący, daemon → operator | Zatwierdzenie oferty zaproszenia jest decyzją człowieka, nie automatu. |

## 4. Kontrakty danych

| Schemat | Cel użycia | Kanał |
| --- | --- | --- |
| `inac-control.v1` | Niezależna od transportu ramka kontrolna dla `offer`, `request`, `push` oraz wszystkich odpowiedzi i odmów. | `msg = "inac.v1"` w sesji ze zdalnym węzłem |
| `agora-record.v1` | Przenoszony podpisany rekord Agory; obsługiwany przez jeden z dwóch bazowych odbiorników Artifact Delivery. | ładunek transferu → przyjęcie przez AD |
| `memarium-blob.v1` | Przenoszona podpisana koperta artefaktu Memarium; obsługiwana przez drugi bazowy odbiornik. | ładunek transferu → przyjęcie przez AD |
| `artifact-object-pointer.v1` | Wskazanie obiektu, gdy bajty nie są umieszczone bezpośrednio w ramce; ich późniejsze pobranie ma własny limit. | opis artefaktu w ramce kontrolnej |
| `contact-request.v1` | Artefakt prośby o kontakt o niskich uprawnieniach; przyjęcie przez transport **nie** nadaje prawa do wysyłania wiadomości. | ramka `push` → wstępna kontrola i odbiornik AD |
| `node-address-attestation.v1` | Dowód adresu z mechanizmu wykrywania węzłów; źródło odcisku certyfikatu dla kandydata połączenia. | Seed Directory → nadzorca połączeń |
| `inac-status.v1` | Bieżący widok statusu dla operatora. | `GET /v1/inac/status` |

## 5. Limity i zachowanie po ich przekroczeniu

| Pułap | Wartość domyślna | Zachowanie po przekroczeniu | Konfigurowalny |
| --- | --- | --- | --- |
| Ładunek bezpośrednio w ramce (`inline`) | 64 KiB | odmowa `payload-too-large` | tak — `inac.inline_max_bytes` |
| Rozmiar artefaktu | 1 GiB | odmowa `payload-too-large` | tak — `inac.max_artifact_size_bytes` |
| Pojedyncza porcja strumienia | 8 MiB (po zdekodowaniu) | odrzucenie **przed** dopisaniem do pliku | nie |
| Bezczynność strumienia | 15 minut | strumień uznany za nieświeży | nie |
| Pobranie danych obiektu pośredniego | 256 MiB | odmowa | nie |
| Oferty oczekujące na zdalny węzeł | 128 | nowe oferty odrzucane | nie |
| Token kontrolny | 256 znaków | odmowa `malformed` | nie |
| Właściwości metadanych | 16 pozycji, klucz 64 B, wartość 512 B | odmowa `malformed` | nie |
| Bufor ostatnich odmów w statusie | 16 | najstarsze wypadają (okno diagnostyczne, nie utrata faktu) | tak — `inac.recent_refusals_limit` |
| Budżet przychodzący dla węzła | brak domyślnego | odmowa `rate-limited` lub `quota-exceeded` | tak — `inac_peer_transport.inbound_budgets` |

## 6. Słownik odmów

Odmowa jest wartością w ramce, nie wyjątkiem. Kody:

| Kod | Znaczenie | Ponawialne? |
| --- | --- | --- |
| `kind-not-supported` | Brak obsługi dla tego rodzaju artefaktu. | Nie, dopóki nie zarejestrujesz odpowiedniego odbiornika. |
| `kind-conflict` | Rodzaj artefaktu koliduje z deklaracją transferu. | Nie — błąd nadawcy. |
| `not-authorized` | Brak autorytetu dla tej operacji. | Nie, dopóki autorytet się nie zmieni. |
| `invitation-unknown` | Zaproszenie nieznane odbiorcy. | Nie. |
| `invitation-expired` | Zaproszenie po TTL. | Po odnowieniu zaproszenia. |
| `invitation-revoked` | Zaproszenie cofnięte. | Nie. |
| `invitation-scope-mismatch` | Zaproszenie nie pokrywa tej operacji lub tego rodzaju. | Nie. |
| `payload-too-large` | Przekroczony limit danych w ramce albo całego artefaktu. | Nie w tym kształcie — użyj strumienia lub zmniejsz artefakt. |
| `digest-mismatch` | Bajty nie odpowiadają zadeklarowanemu skrótowi kryptograficznemu. | Nie — integralność została naruszona. |
| `malformed` | Ramka niezgodna z kontraktem. | Nie. |
| `handler-unavailable` | Odbiornik istnieje, ale jest chwilowo niedostępny. | **Tak.** |
| `already-present` | Artefakt jest już lokalnie obecny. | Nie — to sukces idempotentny, nie błąd. |
| `operation-not-supported` | Operacja nieobsługiwana na tej ścieżce. | Nie. |
| `policy-denied` | Polityka lokalna odmawia. | Nie, dopóki polityka się nie zmieni. |
| `transport-unavailable` | Transport niedostępny. | **Tak.** |
| `rate-limited` | Przekroczony budżet częstotliwości. | **Tak, po odczekaniu.** |
| `quota-exceeded` | Przekroczony budżet rozmiaru lub wolumenu. | **Tak, po odnowieniu okna.** |

Kody `handler-unavailable`, `transport-unavailable`, `rate-limited` i `quota-exceeded` opisują stan przejściowy — ponowienie ma sens. Pozostałe są terminalne dla danej ramki.

## 7. Autorytet i jego cofnięcie

Zdolności hosta (dla komponentów nadzorowanych):

- `inac.offer` — `host/inac.offer`
- `inac.request` — `host/inac.request`
- `inac.push` — `host/inac.push`

Zdolność aplikacyjna: `inac.invitation` (`app/inac.invitation`), należąca do domeny paszportów zdolności. Paszporty zaproszeń wystawiane przez odbiorcę mają TTL (domyślnie 3600 s) i są tworzone w przepływie zatwierdzenia przez operatora.

Autorytet wychodzący komponentu wynika z `outbound/allows` i domyślnie jest
odmawiany. Wpis wiąże `component/id` z konkretnymi operacjami, schematami i
opcjonalnym limitem bajtów. Wstępną zgodę na ruch od zdalnego węzła określa
`inbound_allowed_peers`; **pusta lista odmawia wszystkim (`deny-all`)**, a nie
zezwala wszystkim.

Cofnięte lub przeterminowane zaproszenie daje przy następnym użyciu odpowiednio
`invitation-revoked` albo `invitation-expired`. Przeterminowany dowód adresu nie
może zostać użyty do przypięcia certyfikatu połączenia. Przyjęcie oferty
zaproszenia może utworzyć trwały wpis kontaktu, lecz **kontakt nie jest
autorytetem**.

## 8. Granice zaufania

| Co | Kto weryfikuje |
| --- | --- |
| Tożsamość zdalnego węzła | Uwierzytelniona sesja WSS, nie INAC. |
| Skrót kryptograficzny i rozmiar artefaktu | INAC przed przyjęciem, także dla każdej porcji strumienia. |
| Bajtowa identyczność koperty | INAC, przez cały transfer i zapis. |
| Zgodność ramki z kontraktem | Schema Gate + walidacja `inac-core`. |
| Uprawnienie do rodzaju artefaktu | Rejestr odbiorników; brak wpisu oznacza odmowę. |
| Autorytet domenowy artefaktu | **Nie INAC.** Rozstrzygają o nim odbiornik Artifact Delivery i domena docelowa. Pomyślne przyjęcie przez transport nie nadaje autorytetu domenowego. |
| Odcisk certyfikatu adresu | Nadzorca połączeń na podstawie dowodu z mechanizmu wykrywania węzłów; świeżość jest sprawdzana przed użyciem. |

Najważniejsza zasada brzmi: **przyjęcie przez transport nigdy nie oznacza zgody
domenowej**. W przypadku `contact-request.v1` pozwala jedynie uruchomić wstępną
kontrolę i odbiornik prośby o kontakt; samo nie nadaje prawa do wysyłania
wiadomości.

## 9. Zależności i tryby zdegradowane

Wymaga uwierzytelnionej sesji ze zdalnym węzłem, rejestru odbiorników Artifact
Delivery, magazynu obiektów, rejestru transferów oraz — dla przepływu zaproszeń
— powiadomień operatorskich.

Dostarcza: transport `inac-direct` dla celów zdalnych Artifact Delivery.

Tryby zdegradowane:

- **Transport niedostępny** — nie ma aktywnej sesji ze zdalnym węzłem; operacja
  wychodząca kończy się `transport-unavailable`, a stan transferu pozostaje w
  rejestrze.
- **Odbiornik niedostępny** — `handler-unavailable`; artefakt nie jest
  przyjmowany, a licznik odmów rośnie.
- **Rejestr niedostępny** — odczyt statusu nadal działa, lecz zwraca puste listy
  i zapisuje `inac_status_ledger_read_failed` w logu.
- **Uszkodzony stan współdzielony** — gdy wewnętrzna blokada stanu została
  zatruta po panice, status zwraca jedną syntetyczną odmowę
  `handler-unavailable` z opisem przyczyny.

## 10. Stan trwały i restart

| Magazyn | Ścieżka | Trwałość | Po restarcie |
| --- | --- | --- | --- |
| Rejestr transferów | `<data-dir>/storage/inac.sqlite` | trwały | odtwarzany z bazy; decyzje, oferty oczekujące i kontakty przeżywają restart |
| Magazyn strumieni | `<data-dir>/storage/artifact-delivery/streams` | trwały (pliki) | niedokończone strumienie starsze niż 15 minut są nieświeże |
| Liczniki i ostatnie odmowy | pamięć procesu | ulotne | zerowane przy starcie — to okno diagnostyczne, nie księga |

To rozróżnienie jest ważne: **liczniki statusu nie są historią**. Trwała historia
decyzji o transferach znajduje się w rejestrze SQLite.

## 11. Konfiguracja

### Składanie warstw

Efektywna konfiguracja daemona powstaje w tej kolejności, każda kolejna warstwa nadpisuje poprzednią przez głębokie scalanie:

1. **Wbudowane wartości domyślne** — `InacRuntimeConfig::default()` i
   `DaemonInacPeerTransportAdapterConfig::default()` skompilowane w daemonie.
2. **Konfiguracja fabryczna modułów** — fragmenty wbudowanych modułów middleware. Klucze INAC nie pochodzą z tej warstwy, ale warstwa jest częścią wspólnego składania.
3. **`<data-dir>/config/*.json`** — wszystkie pliki `.json` w katalogu, czytane w **kolejności alfabetycznej nazw** i głęboko scalane. To jest właściwe miejsce na konfigurację INAC.
4. **`<data-dir>/control/middleware-settings.json`** — ustawienia zastosowane w czasie działania przez operatora; scalane ponad warstwą 3.

Nieprawidłowy JSON w którymkolwiek pliku warstwy 3 zatrzymuje start i wskazuje
plik zawierający błąd; konfiguracja nie jest stosowana częściowo.

### Opcje: `inac`

| Opcja | Typ | Domyślnie | Działanie |
| --- | --- | --- | --- |
| `inline_max_bytes` | liczba | 65536 | Największy ładunek umieszczany bezpośrednio w ramce kontrolnej. Powyżej wymagany jest strumień. |
| `max_artifact_size_bytes` | liczba | 1073741824 | Bezwzględny pułap rozmiaru artefaktu, niezależnie od lokalizacji ładunku. |
| `recent_refusals_limit` | liczba | 16 | Ile ostatnich odmów zachowuje widok statusu. Jest to okno diagnostyczne. |
| `outbound/allows` | lista | `[]` | Zezwolenia wychodzące dla komponentów lokalnych. **Pusta lista oznacza brak autorytetu wychodzącego.** |

Wpis `outbound/allows`:

| Pole | Typ | Działanie |
| --- | --- | --- |
| `component/id` | tekst | Komponent, którego dotyczy zezwolenie. |
| `operations` | zbiór | Dozwolone operacje. **Pusty zbiór to brak autorytetu, nie wieloznacznik.** |
| `schemas` | zbiór | Dozwolone schematy artefaktów. Ta sama zasada. |
| `max/bytes` | liczba lub brak | Opcjonalny pułap bajtów węższy niż globalny. |

### Opcje: `inac_peer_transport`

| Opcja | Typ | Domyślnie | Działanie |
| --- | --- | --- | --- |
| `enabled` | bool | `true` | Włącza adapter transportu między węzłami dla INAC. |
| `inbound_allowed_peers` | lista tekstów | `[]` | Węzły uprawnione do wysyłania przychodzących ramek `offer` i `push`. **Pusta lista oznacza odmowę dla wszystkich (`deny-all`).** |
| `inbound_budgets` | lista | `[]` | Budżety odbiorcze dla ramek przychodzących. |
| `invitation_passport_ttl_seconds` | liczba | 3600 | TTL paszportu zaproszenia wystawianego przez odbiorcę w przepływie zatwierdzenia przez operatora. |
| `contact_creation_after_accept` | bool | `true` | Czy przyjęcie oferty zaproszenia tworzy trwały wpis kontaktu. Kontakt nie jest autorytetem. |
| `response_timeout_ms` | liczba | 5000 | Czas oczekiwania na odpowiedź zdalnego węzła. |
| `contact_requests.enabled` | bool | `false` | Czy przyjmować nisko-uprzywilejowane artefakty `contact-request.v1`. |
| `contact_requests.unknown_peer_mode` | `auto-admit` / `operator-approval` / `deny` | `deny` | Postępowanie z prośbą od nieznanego węzła. |
| `contact_requests.deny_blocked` | bool | `true` | Czy odrzucać prośby od zablokowanych węzłów. |

Wpis `inbound_budgets`:

| Pole | Typ | Działanie |
| --- | --- | --- |
| `remote_node_ids` | lista | Zdalne węzły objęte regułą. **Pusta lista działa jak wieloznacznik.** |
| `operations` | lista | Operacje objęte regułą. Pusta — wieloznacznik. |
| `artifact_schemas` | lista | Schematy objęte regułą. Pusta — wieloznacznik. |
| `content_types` | lista | Typy treści objęte regułą. Pusta — wieloznacznik. |
| `max_size_bytes` | liczba lub brak | Pułap rozmiaru dla dopasowanych ramek. |
| `max_per_minute` | liczba lub brak | Pułap częstotliwości dla dopasowanych ramek. |

Te dwa miejsca mają celowo różną semantykę. W `outbound/allows` pusty zbiór
oznacza **brak autorytetu**, natomiast w `inbound_budgets` pusta lista kryteriów
oznacza **dopasowanie wszystkich wartości**. Pierwsze pole przyznaje
uprawnienia, a drugie wybiera ruch objęty regułą.

## 12. Obserwowalność

`GET /v1/inac/status` zwraca dokument `inac-status.v1`:

- `runtime.handlers` — zarejestrowane odbiorniki i opisy obsługiwanych danych,
- `runtime.counters` — `accepted`, `ingested`, `refused`, `malformed` (ulotne, od startu procesu),
- `runtime.recent_refusals` — ostatnie odmowy z kodem i komunikatem (okno o rozmiarze `recent_refusals_limit`),
- `transfers.diagnostics` — diagnostyka trwałego rejestru transferów,
- `transfers.recent_decisions` — do 25 ostatnich decyzji transferu,
- `contacts.recent_contacts` — do 25 ostatnich kontaktów.

Bieżący widok nie zawiera ładunków: nie ujawnia bajtów artefaktów ani sekretów.
Odczyt statusu nie nadaje autorytetu.

Daemon udostępnia także diagnostykę dowodów adresów używanych przez nadzorcę
połączeń. Świeży dowód może wskazać cel bezpośredniego doręczenia INAC. Dowód
nieświeży lub martwy pozostaje jedynie wskazówką dla wykrywania węzłów i
diagnostyki; **bez ponownej weryfikacji nie staje się celem doręczenia**.

## 13. Koszt i zasoby

INAC nie obciąża budżetów wnioskowania. Koszty są materialne:

- **dysk** — rejestr transferów SQLite oraz pliki strumieni; niedokończone strumienie zajmują miejsce do momentu uznania ich za nieświeże (15 minut),
- **sieć** — ruch wychodzący i przychodzący równy rozmiarowi artefaktów; pułap artefaktu 1 GiB jest jedynym twardym ogranicznikiem pojedynczego transferu,
- **pamięć** — ładunki do 64 KiB umieszczane bezpośrednio w ramce oraz okno
  ostatnich odmów.

## 14. Wersje kontraktów i kompatybilność

Ramka kontrolna ma wersję `inac-control.v1`. Dla porcji strumienia preferowany
jest `inac.stream.chunk.binary.v1`; wariant JSON/base64url pozostaje świadomie
utrzymywaną ścieżką zgodności. Dwa bazowe odbiorniki Artifact Delivery obsługują
`agora-record.v1` i `memarium-blob.v1`.

## 15. Znane ograniczenia

Wpis `INAC Local Operator MVP` w rejestrze implementacji nadal ma status
**`partial`**. Działa już transport WSS i Matrix, strumieniowanie, paszportowe
bramki odbiorcze, rejestr decyzji, UI operatora i dwa bazowe odbiorniki. Nadal
obowiązują następujące ograniczenia:

- Bazowy rejestr obejmuje dwa konkretne rodzaje artefaktów (`agora-record.v1`,
  `memarium-blob.v1`). Rodzaje należące do middleware są dokładane przez jawne
  punkty kompozycji, a nie przez zamkniętą listę w INAC.
- `inbound_allowed_peers` pozostaje płaską, wstępną listą dozwolonych węzłów.
  Dokładniejsze uprawnienia dla konkretnego przesłania są już osobno sprawdzane
  przez paszporty zaproszeń, zdolności, wiadomości i opieki nad danymi; lista
  ich nie zastępuje.
- Statycznie przypięte odciski z węzłów startowych pozostają skrótem
  bootstrapowym. Świeży dowód adresu z atestacji ma przed nimi pierwszeństwo.
- Liczniki statusu są ulotne — do korelacji zdarzeń w czasie służy rejestr transferów, nie status.

## 16. Powiązanie z implementacją

| Pole | Wartość |
| --- | --- |
| Komponent | INAC (Inter-Node Artifact Channel) |
| Wpis w rejestrze implementacji | `INAC Local Operator MVP` |
| Skrzynie Rust | `inac-core`, `inac-runtime`, `inac-handlers`, `inac-host`, `daemon`, `node-ui` |
| Schematy | `inac-control.v1`, `memarium-blob.v1`, `agora-record.v1` |
| Zdolności | `inac.offer`, `inac.request`, `inac.push`, `inac.invitation` |
| Trasy | `POST /v1/host/capabilities/inac.{offer,request,push}`, `GET /v1/inac/status` |
| Źródła | [Propozycja 042](../../project/40-proposals/042-inter-node-artifact-channel.md), [Rozwiązanie 017](../../project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md) |
| Status komponentu | `partial` |
