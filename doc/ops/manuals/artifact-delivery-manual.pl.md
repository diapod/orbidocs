# Podręcznik operatorski: Artifact Delivery

Artifact Delivery to należąca do hosta warstwa wysyłania i przyjmowania
artefaktów opisanych schematami danych. Komponent określa, co i komu chce
dostarczyć; host wybiera trasę i adapter, obsługuje ponowienia, przyjmuje dane
przychodzące i udostępnia ich status operatorowi.

Krótkie wyjaśnienie pojęć zawiera
[Artifact Delivery FAQ](../faq/artifact-delivery-faq.pl.md), a przykłady
integracji, konfiguracji i kolejności działań —
[Artifact Delivery HOWTO](../howto/artifact-delivery-howto.pl.md). Ten podręcznik
nie powtarza przykładów z HOWTO. Zbiera limity, kody niepowodzeń, granice
zaufania, stan trwały i wartości domyślne.

## 1. Cel i funkcje

Artifact Delivery istnieje po to, aby **komponenty nie musiały samodzielnie
zarządzać transportem**. Komponent deklaruje artefakt i odbiorców. Host wybiera
trasę i adapter, obsługuje ponowienia i odzyskiwanie, przyjmuje dane
przychodzące oraz pokazuje status operatorowi.

Funkcje:

- przyjęcie koperty `artifact-delivery-envelope.v1` od komponentu i sprowadzenie jej do planu doręczenia,
- rozwiązanie odbiorców przez nazwane selektory, grupy i trasy,
- egzekwowanie autorytetu wychodzącego per komponent, schemat i klasa selektora,
- wybór adaptera transportu i wykonanie planu z trasami zapasowymi,
- trwały zapis doręczeń i decyzji o przyjęciu oraz odzyskiwanie doręczeń
  odroczonych,
- kierowanie danych przychodzących do **dokładnie jednego odbiornika domenowego
  (`acceptor`)** dla danego rodzaju artefaktu,
- udostępnianie operatorowi bieżącego widoku statusu i diagnostyki.

## 2. Zasada działania

W ścieżce wychodzącej komponent wywołuje `artifact.delivery.send` z kopertą.
Host sprawdza kopertę i uprawnienia nadawcy, ustala odbiorców, rozwija plan na
konkretne cele i wykonuje go przez adaptery. Wynik ma postać
`artifact-delivery-result.v1`; stan całego doręczenia i każdego celu jest
zapisywany trwale.

Ścieżka przychodząca ma dwa stopnie, których nie wolno mylić:

1. **Wstępna kontrola (`preflight`)** — opcjonalny, wczesny punkt kontrolny
   należący do właściciela schematu. Może **odrzucić** artefakt albo dołączyć
   wskazówki (`Abstain`, `Continue { hints }`, `Reject { failure_class, message,
   retryable }`). Może też sprawdzić opis artefaktu i mały ładunek umieszczony
   bezpośrednio w kopercie, zanim host pobierze zawartość wskazaną przez
   `artifact/ref`. **Wstępna kontrola nie może przyjąć artefaktu.**
2. **Odbiornik domenowy (`acceptor`)** — zarejestrowany
   `InboundArtifactAcceptor` jest **jedyną ścieżką, która może przyjąć
   artefakt**. Dla każdej pary (schemat, typ treści) istnieje dokładnie jeden
   autorytatywny odbiornik.

Kierowanie jest zamknięte na brak konfiguracji (`fail-closed`): jeżeli dla
danego rodzaju artefaktu nie ma odbiornika, host zwraca `kind-not-supported`
zamiast przyjmować dane domyślnie.

Duży ładunek nie jest umieszczany bezpośrednio w kopercie. Po przekroczeniu tego
progu host używa magazynu obiektów. Adapter `object_store_indirect` wysyła
wskaźnik `artifact-object-pointer.v1`, a odbiorca pobiera właściwe bajty przez
`POST /v1/artifact-delivery/object-store/fetch`, używając tokenu z rejestru.

## 3. Umiejscowienie w architekturze i kanały komunikacji

Artifact Delivery leży **pomiędzy komponentami a mechanizmami transportu**.
Agora jest publicznym przekaźnikiem tematycznym,
[INAC](inac-manual.pl.md) prywatnym transportem między węzłami, skrzynka Matrix
przechowuje dane do czasu ich odebrania, a magazyn obiektów przechowuje treść
lokalnie. Artifact Delivery nie zastępuje żadnego z tych mechanizmów — wybiera
właściwy z nich dla danego planu.

| Kanał | Kierunek | Uzasadnienie |
| --- | --- | --- |
| `POST /v1/host/capabilities/artifact.delivery.send` | przychodzący, komponent → host | Jedyne wejście intencji doręczenia. Wymaga zezwolenia wychodzącego. |
| `artifact.delivery.status` | odczyt, komponent → host | Komponent pyta o los własnego doręczenia bez dostępu do cudzych. |
| `artifact.delivery.submit` | przychodzący, komponent → host | Złożenie artefaktu do doręczenia w wariancie odroczonym. |
| Adapter `daemon.agora-publish` | wychodzący, host → Agora | Publikacja tematyczna. Ciało błędu adaptera jest przycinane do 16 KiB, żeby zdalna usługa nie mogła zalać loga. |
| Adapter `daemon.inac-direct` | wychodzący, host → zdalny węzeł | Prywatne doręczenie bezpośrednie. Wysyłka strumieniowa dzieli ładunek na porcje po 24 KiB. |
| Adapter `matrix_mailbox` | dwukierunkowy, host ↔ serwer macierzysty Matrix | Przechowuje i przekazuje dane, gdy zdalny węzeł nie jest osiągalny bezpośrednio. |
| Adapter `object-store-indirect` | wychodzący, host → zdalny węzeł (wskaźnik) | Duże ładunki są reprezentowane przez wskaźnik zamiast bajtów w kopercie. |
| `POST /v1/artifact-delivery/admissions` | przychodzący, adapter źródłowy → host | Przyjęcie przez interfejs sterujący. Gdy lista dozwolonych adapterów źródłowych jest pusta, host odmawia wszystkim (`deny-all`). |
| `POST /v1/artifact-delivery/object-store/fetch` | przychodzący, odbiorca → host | Pobranie bajtów doręczenia pośredniego przy użyciu tokenu z rejestru. |
| Odbiorniki modułów nadzorowanych przez HTTP (`supervised-HTTP`) | wychodzący, host → moduł middleware | Host przekazuje artefakt modułowi przez interfejs lokalny; odpowiedź ma ograniczony rozmiar i czas. |
| Odbiorniki JSON-e Flow oraz wbudowane w proces (`in-process`) | wewnętrzny, host → domena | Domena docelowa rozstrzyga o autorytecie; transport go nie nadaje. |
| `GET /v1/artifact-delivery/{deliveries,admissions,routes}` | odczyt, operator → host | Widoki statusu dla operatora; nie nadają autorytetu. |
| `POST /v1/artifact-delivery/recover` | zapis, operator → host | Ręczne uruchomienie odzyskiwania obok pracownika tła. |
| Rejestr SQLite | zapis/odczyt, dysk lokalny | Trwałe doręczenia, cele i decyzje o przyjęciu. |

## 4. Kontrakty danych

| Schemat | Cel użycia | Kanał |
| --- | --- | --- |
| `artifact-delivery-envelope.v1` | Intencja doręczenia deklarowana przez komponent: artefakt, odbiorcy, plan. | `artifact.delivery.send` |
| `artifact-delivery-result.v1` | Wynik doręczenia zwracany komponentowi. | odpowiedź na `send`/`submit` |
| `artifact-delivery-status.v1` | Bieżący widok stanu doręczenia i jego celów. | `GET /v1/artifact-delivery/deliveries/{id}` |
| `artifact-delivery-recovery.v1` | Kontrakt odzyskiwania doręczeń odroczonych. | pracownik tła i `POST …/recover` |
| `artifact-object-pointer.v1` | Wskazanie obiektu, gdy bajty nie są umieszczone bezpośrednio w kopercie. | adapter `object-store-indirect` |
| `artifact-mailbox-sealed.v1` | Zapieczętowany ładunek skrzynki Matrix. | adapter `matrix_mailbox` |
| `artifact-mailbox-chunk.v1` | Porcja ładunku skrzynki powyżej limitu eventu. | adapter `matrix_mailbox` |
| `routing-subject-binding.v1` | Wiązanie podmiotu routingu przy rozwiązywaniu odbiorców. | rozwiązywanie tras |
| `capability-proof-presentation-batch.v1` | Zbiorcza prezentacja dowodów zdolności; obsługiwana przez wbudowany odbiornik. | przyjęcie danych przychodzących |

Artefakty **przenoszone** przez tę warstwę (`agora-record.v1`,
`memarium-blob.v1`, `contact-request.v1`, `corpus-*`,
`capability-passport-present.v1`, `federation-service-endorsement.v1`) należą do
swoich domen, nie do Artifact Delivery. Warstwa zna ich schematy tylko po to,
aby wybrać właściwy odbiornik.

## 5. Limity i zachowanie po ich przekroczeniu

| Pułap | Wartość domyślna | Zachowanie po przekroczeniu | Konfigurowalny |
| --- | --- | --- | --- |
| Rozwiązany artefakt | 64 MiB | niepowodzenie `runtime-limit` | nie |
| Próg danych umieszczanych bezpośrednio w kopercie | 64 KiB | powyżej — ładunek trafia do magazynu obiektów | nie |
| Próg doręczenia pośredniego | 1 MiB | powyżej — wysyłany wskaźnik zamiast bajtów | tak — `object_store_indirect.threshold_bytes` |
| Obiekt w magazynie | 256 MiB | odrzucenie zapisu | tak — `object_store.max_object_bytes` |
| Retencja magazynu obiektów | 7 dni | obiekt usuwany | tak — `object_store.retention_seconds` |
| Porcja strumienia INAC przy wysyłce | 24 KiB | wartość stała, nie pułap | nie |
| Pamięć podręczna artefaktów zdalnych węzłów | 4096 wpisów / 256 MiB | usunięcie najstarszych wpisów; sprzątanie co 64 zapisy | tak — konfiguracja `matrix_mailbox` |
| Odpowiedź odbiornika `supervised-HTTP` | 64 KiB | niepowodzenie `adapter-permanent` | tak — `…acceptor_response_limit_bytes` |
| Czas odpowiedzi odbiornika | 5000 ms | `admission-timeout` | tak — `…acceptor_request_timeout_ms` |
| Ciało błędu adaptera Agora | 16 KiB | przycięcie w diagnostyce | nie |
| Sufiks referencji magazynu artefaktów | 1024 B | odrzucenie | nie |
| Partia odzyskiwania | 32 doręczenia | reszta w następnym przebiegu | tak — `artifact_delivery_recovery.batch_limit` |
| Budżet jednego przebiegu odzyskiwania | 4000 ms | przebieg kończy się, reszta czeka | tak — `…pass_deadline_ms` |
| Próg „dużego ładunku" w profilowaniu | 1 MiB | oznaczenie w diagnostyce | tak — `artifact_delivery_profiling…` |

## 6. Słowniki niepowodzeń i statusów

Niepowodzenie jest **klasą**, nie tekstem. Dwanaście klas:

| Klasa | Znaczenie | Ponawialne? |
| --- | --- | --- |
| `envelope-malformed` | Koperta niezgodna ze schematem. | Nie. |
| `envelope-invalid` | Koperta poprawna składniowo, ale niespójna semantycznie. | Nie. |
| `route-unresolved` | Nie dało się rozwiązać trasy ani odbiorców. | Nie, dopóki trasy się nie zmienią. |
| `admission-conflict` | Konflikt podczas przyjmowania artefaktu po stronie odbiorcy. | Nie. |
| `kind-not-supported` | Brak odbiornika dla rodzaju artefaktu. | Nie, dopóki nie zarejestrujesz odbiornika. |
| `outbound-denied` | Brak autorytetu wychodzącego dla tego komponentu, schematu lub selektora. | Nie, dopóki polityka się nie zmieni. |
| `adapter-transient` | Adapter zawiódł przejściowo. | **Tak.** |
| `adapter-permanent` | Adapter zawiódł trwale. | Nie. |
| `stage-timeout` | Etap planu przekroczył czas. | **Tak.** |
| `admission-timeout` | Odbiornik nie odpowiedział w czasie. | **Tak.** |
| `ledger-error` | Nie udało się odczytać lub zapisać trwałego rejestru. | **Tak.** |
| `runtime-limit` | Przekroczony pułap wykonania. | Nie w tym kształcie. |

Status doręczenia (7): `accepted`, `running`, `succeeded`, `partial`, `failed-retryable`, `failed-permanent`, `expired`.
Status pojedynczego celu (4): `pending`, `succeeded`, `failed-retryable`, `failed-permanent`.
Status przyjęcia danych przychodzących (4): `accepted`, `already-present`,
`rejected`, `retryable`.

`partial` jest stanem pierwszej klasy, nie awarią: część celów mogła się powieść. `already-present` to sukces idempotentny.

## 7. Autorytet i jego cofnięcie

Zdolności hostowe: `artifact.delivery.send`, `artifact.delivery.status`, `artifact.delivery.submit` (`host/*`).

Autorytet wychodzący pochodzi z `artifact_delivery.outbound/allows`. Każdy wpis
wiąże komponent z dozwolonymi schematami artefaktów, klasami wyboru odbiorców,
trasami, docelowymi węzłami, maksymalną liczbą odbiorców, liczbą tras zapasowych
i limitem bajtów. Brak odpowiedniego wpisu daje `outbound-denied`.

Autorytet przychodzący ma dwie osobne bramki:

- `artifact_delivery_acceptors.http_admission_allowed_source_adapters` — **pusta
  lista odmawia wszystkim (`deny-all`)** na wejściu HTTP. Adaptery transportowe
  działające w procesie mogą nadal wywoływać warstwę wykonawczą bezpośrednio.
- rejestracja odbiornika — brak wpisu dla rodzaju artefaktu oznacza
  `kind-not-supported`.

Cofnięcie działa od następnego użycia. Zmiana `outbound/allows` może zablokować
kolejne wysyłki, a wyrejestrowanie odbiornika — kolejne próby przyjęcia.
Doręczenia już zapisane w rejestrze zachowują swój stan: cofnięcie autorytetu
nie zmienia historii.

## 8. Granice zaufania

| Co | Kto weryfikuje |
| --- | --- |
| Zgodność koperty ze schematem | Artifact Delivery, przed jakimkolwiek efektem. |
| Autorytet wychodzący komponentu | Artifact Delivery, z `outbound/allows`. |
| Tożsamość zdalnego węzła | Uwierzytelniona sesja transportu INAC/WSS, nie Artifact Delivery. |
| Digest i rozmiar ładunku | Adapter transportu (dla INAC — per porcja) oraz host przy rozwiązywaniu. |
| Uprawnienie do rodzaju artefaktu | Rejestr odbiorników; brak wpisu oznacza odmowę. |
| **Autorytet domenowy artefaktu** | **Nie Artifact Delivery.** Rozstrzygają o nim odbiornik i domena docelowa. Pomyślne przyjęcie przez transport nie nadaje autorytetu domenowego. |
| Docelowa przestrzeń przechowywania (`custody`) dla `memarium-blob.v1` | **Polityka lokalna demona**, nigdy nadawca. Domyślnie `public`, dozwolone `["public"]`; `crisis` jest odrzucane przez walidację konfiguracji. |
| Wynik wstępnej kontroli (`preflight`) | Kontrola może odrzucić artefakt lub dodać wskazówki; **nie może go przyjąć**. |

Dwie zasady są szczególnie ważne. Po pierwsze, **przyjęcie przez transport nigdy
nie oznacza zgody domenowej**. W przypadku `contact-request.v1` pozwala jedynie
uruchomić wstępną kontrolę i odbiornik prośby. Po drugie, **nadawca nie wybiera
przestrzeni przechowywania**. Jest to decyzja lokalna, ponieważ przestrzenie
Memarium nakładają lokalną politykę na przechowywane dane.

## 9. Zależności i tryby zdegradowane

Wymaga rejestru SQLite, magazynu obiektów artefaktów oraz co najmniej jednego
skonfigurowanego adaptera transportu. Odbiorniki `supervised-HTTP` wymagają
nadzorcy middleware, a odbiorniki JSON-e Flow — środowiska wykonawczego Flow.

Dostarcza jeden interfejs doręczania dla wszystkich komponentów i jedną ścieżkę
przyjmowania danych ze wszystkich transportów, w tym
[INAC](inac-manual.pl.md).

Tryby zdegradowane:

- **Adapter niedostępny** — `adapter-transient`; doręczenie otrzymuje stan
  `failed-retryable` i czeka na zadanie odzyskiwania działające w tle.
- **Odbiornik nie odpowiada** — `admission-timeout`; próbę przyjęcia można
  ponowić (`retryable`), nie jest to trwałe odrzucenie.
- **Rejestr niedostępny** — `ledger-error`; operację można ponowić, ponieważ
  błąd rejestru nie jest rozstrzygnięciem o samym artefakcie.
- **Odzyskiwanie wyłączone** (`artifact_delivery_recovery.enabled = false`) — doręczenia odroczone czekają na ręczne `POST /v1/artifact-delivery/recover`.
- **Częściowe doręczenie do wielu odbiorców** — status `partial`; część celów ma
  stan `succeeded`, a część `failed-*`. Jest to pełnoprawny wynik, nie błąd
  mechanizmu wykonawczego.

## 10. Stan trwały i restart

| Magazyn | Ścieżka | Trwałość | Po restarcie |
| --- | --- | --- | --- |
| Rejestr doręczeń i decyzji o przyjęciu | `<data-dir>/storage/artifact-delivery.sqlite` | trwały (schemat v2) | odtwarzany z bazy; doręczenia odroczone wracają do kolejki odzyskiwania |
| Rejestr tokenów pobrania obiektów | `<data-dir>/storage/artifact-delivery/object-fetch-tokens.v1.json` | trwały | odtwarzany; tokeny przeżywają restart |
| Pamięć podręczna artefaktów zdalnych węzłów | `<data-dir>/storage/artifact-delivery/peer-artifacts` | trwały (pliki) | zachowana; wpisy są usuwane zgodnie z limitami |
| Składanie strumieni | `<data-dir>/storage/artifact-delivery/streams` | trwały (pliki) | patrz [manual INAC](inac-manual.pl.md) |
| Magazyn obiektów | katalog z `object_store.root` | trwały | retencja domyślnie 7 dni |
| Liczniki profilowania | pamięć procesu | ulotne | zerowane przy starcie |

Odzyskiwanie po restarcie wykonuje osobne zadanie działające w tle, a nie odczyt
statusu. Zadanie uruchamia przebieg co `interval_ms`, przetwarza najwyżej
`batch_limit` doręczeń i kończy go po upływie `pass_deadline_ms`.

## 11. Konfiguracja

HOWTO pokazuje na przykładach, jak przygotować konfigurację hosta, pakietu i
koperty. Ta sekcja uzupełnia je o kolejność scalania warstw i wartości domyślne.

### Składanie warstw

Efektywna konfiguracja daemona powstaje w tej kolejności, każda kolejna warstwa nadpisuje poprzednią przez głębokie scalanie:

1. **Wbudowane wartości domyślne** — skompilowane w daemonie, łącznie z czterema
   odbiornikami działającymi w jego procesie (patrz niżej).
2. **Konfiguracja fabryczna modułów** — fragmenty wbudowanych modułów middleware.
3. **`<data-dir>/config/*.json`** — wszystkie pliki `.json` w katalogu, czytane w **kolejności alfabetycznej nazw** i głęboko scalane.
4. **`<data-dir>/control/middleware-settings.json`** — ustawienia zastosowane w czasie działania przez operatora.

Pakiet może dostarczyć proponowany fragment konfiguracji, lecz **obowiązujące
uprawnienia wynikają z konfiguracji demona zaakceptowanej przez operatora**.
Nieprawidłowy JSON w warstwie 3 zatrzymuje start i wskazuje plik zawierający
błąd; host nie stosuje takiej konfiguracji częściowo.

### Klucze najwyższego poziomu

| Klucz | Zakres |
| --- | --- |
| `artifact_delivery` | Polityka doręczania: `defaults`, `groups`, `routes`, `outbound/allows`. |
| `artifact_delivery_adapters` | Zachowanie adapterów: `agora_publish`, `matrix_mailbox`, `object_store`, `object_store_indirect`. |
| `artifact_delivery_acceptors` | Przyjmowanie danych i rejestracja odbiorników. |
| `artifact_delivery_recovery` | Zadanie odzyskiwania doręczeń odroczonych. |
| `artifact_delivery_profiling` | Widoczność liczników profilowania w statusie. |
| `artifact_delivery_observers` | Zdarzenia obserwacyjne, które nie zmieniają stanu. |
| `inac_peer_transport` | Polityka odbiorcza transportu INAC — opisana w [manualu INAC](inac-manual.pl.md). |

### Wartości domyślne

| Opcja | Domyślnie | Uwaga |
| --- | --- | --- |
| `artifact_delivery_recovery.enabled` | `true` | |
| `artifact_delivery_recovery.interval_ms` | 5000 | odstęp bezczynności między przebiegami |
| `artifact_delivery_recovery.batch_limit` | 32 | doręczeń na przebieg |
| `artifact_delivery_recovery.pass_deadline_ms` | 4000 | budżet jednego przebiegu |
| `artifact_delivery_profiling.enabled` | `true` | |
| `artifact_delivery_profiling.large_payload_threshold_bytes` | 1 MiB | |
| `artifact_delivery_observers.tracing_enabled` | `false` | zdarzenia tylko-metadanowe |
| `artifact_delivery_acceptors.http_admission_allowed_source_adapters` | `[]` | odmowa dla wszystkich (`deny-all`) |
| `…acceptor_request_timeout_ms` | 5000 | |
| `…acceptor_response_limit_bytes` | 64 KiB | |
| `object_store.max_object_bytes` | 256 MiB | |
| `object_store.retention_seconds` | 604800 (7 dni) | |
| `object_store_indirect.enabled` | `false` | |
| `object_store_indirect.threshold_bytes` | 1 MiB | |
| `object_store_indirect.control_adapter` | wartość wbudowana | |
| `memarium_blob_custody.default_target_space` | `"public"` | |
| `memarium_blob_custody.allowed_target_spaces` | `["public"]` | `crisis` odrzucane przez walidację |

### Odbiorniki wbudowane w proces

Nowa konfiguracja ma cztery zarejestrowane odbiorniki. Nadpisanie
`artifact_delivery_acceptors.in_process` **zastępuje całą listę**. Dodając
własny odbiornik, trzeba więc ponownie wymienić także te, które mają pozostać.

| `acceptor_id` | Schemat | `invoke` |
| --- | --- | --- |
| `contact-request.local` | `contact-request.v1` | `contact.request` |
| `federation-service-endorsement.install` | `federation-service-endorsement.v1` | `federation-service-endorsement.install` |
| `capability-passport-present.accept` | `capability-passport-present.v1` | `capability-passport-present.accept` |
| `capability-proof-presentation-batch.accept` | `capability-proof-presentation-batch.v1` | `capability-proof-presentation-batch.accept` |

Pozostałe wartości `invoke` dostępne dla odbiorników: `inac.push`,
`agora.record.ingest`, `memarium.inac.accept`, `corpus.query`, `corpus.answer`,
`corpus.room-invite`.

## 12. Obserwowalność

| Trasa | Zawartość |
| --- | --- |
| `GET /v1/artifact-delivery/deliveries?limit={n}` | lista doręczeń |
| `GET /v1/artifact-delivery/deliveries/{delivery_id}` | stan doręczenia i wszystkich celów |
| `GET /v1/artifact-delivery/deliveries/{delivery_id}/operation-status` | status operacji dla wywołującego |
| `GET /v1/artifact-delivery/admissions?limit={n}` | lista decyzji o przyjęciu danych przychodzących |
| `GET /v1/artifact-delivery/admissions/{admission_id}` | szczegóły jednej decyzji o przyjęciu |
| `GET /v1/artifact-delivery/routes` | rozwiązane trasy i selektory |

Gdy `artifact_delivery_profiling.enabled` jest włączone, widoki statusu zawierają
liczniki przygotowania ładunku i transportu. Ładunki przekraczające ustalony próg
są wyróżniane w diagnostyce. Obserwator (`observers.tracing_enabled`) emituje
zdarzenia zakończenia doręczenia i przyjęcia zawierające **wyłącznie metadane**,
bez bajtów artefaktów.

## 13. Koszt i zasoby

Artifact Delivery nie obciąża budżetów wnioskowania. Koszty materialne:

- **dysk** — rejestr SQLite, magazyn obiektów (do 256 MiB na obiekt,
  przechowywanie przez 7 dni), pamięć podręczna artefaktów zdalnych węzłów (do
  256 MiB) i pliki strumieni,
- **sieć** — ruch zależny od rozmiaru artefaktów i liczby odbiorców; przy
  doręczeniu do wielu węzłów liczba odbiorców jest głównym mnożnikiem kosztu,
- **pamięć** — ładunki do 64 KiB umieszczane bezpośrednio w kopercie oraz
  odpowiedzi odbiorników do 64 KiB.

Doręczenie pośrednie ogranicza powielanie dużego ładunku przy wielu odbiorcach:
w planie przesyłany jest mały wskaźnik, a właściwe bajty pobiera odbiorca, który
ich potrzebuje.

## 14. Wersje kontraktów i kompatybilność

Koperta: `artifact-delivery-envelope.v1`. Wynik: `artifact-delivery-result.v1`. Rejestr SQLite ma własną wersję schematu (obecnie 2) niezależną od wersji kontraktów — migracja rejestru nie jest zmianą kontraktu i nie wymaga zmiany po stronie komponentów.

## 15. Znane ograniczenia

Wpis `Artifact Delivery MVP` w rejestrze implementacji ma status `done`.
Szersze rozwiązanie 023 pozostaje `partial`, ponieważ dwa kierunki są świadomie
otwarte:

- decyzja o niżejpoziomowym podziale ramek WebSocket bez kopiowania ma zapaść **na podstawie liczników profilowania**, a nie z góry — dlatego profilowanie jest domyślnie włączone,
- Matrix media pozostaje wariantem transportu po-MVP do czasu, aż dowody z wdrożeń tego wymuszą.

Ponadto nadpisanie `in_process` zastępuje całą listę wbudowanych odbiorników.
Jest to najczęstsza pułapka w konfiguracji tego komponentu.

## 16. Powiązanie z implementacją

| Pole | Wartość |
| --- | --- |
| Komponent | Artifact Delivery |
| Wpis w rejestrze implementacji | `Artifact Delivery MVP` (status `done`) |
| Skrzynie Rust | `artifact-delivery-core`, `artifact-delivery`, `ad-host`, `memarium-host`, `daemon`, `node-ui` |
| Schematy | `artifact-delivery-envelope.v1`, `artifact-delivery-result.v1`, `artifact-delivery-status.v1`, `artifact-delivery-recovery.v1`, `artifact-object-pointer.v1`, `artifact-mailbox-sealed.v1`, `artifact-mailbox-chunk.v1`, `routing-subject-binding.v1`, `capability-proof-presentation-batch.v1` |
| Zdolności | `artifact.delivery.send`, `artifact.delivery.status`, `artifact.delivery.submit` |
| Trasy | `/v1/artifact-delivery/{deliveries,admissions,routes,recover,object-store/fetch}` |
| Źródła | [Rozwiązanie 023](../../project/60-solutions/023-artifact-delivery/023-artifact-delivery.md), [Artifact Delivery HOWTO](../howto/artifact-delivery-howto.pl.md) |
