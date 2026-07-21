# Memarium HOWTO

Ten dokument prowadzi operatora i autora middleware przez podstawową ścieżkę
Memarium: wybór przestrzeni, przygotowanie autorytetu, zapis albo odczyt,
inspekcję kwarantanny, deklasyfikację, archiwizację i obsługę Crisis.

Nie jest drugim opisem modelu domenowego. Kontrakty i zamknięty słownik błędów
należą do [Solution 002](../../project/60-solutions/002-memarium/002-memarium.md),
a odpowiedzi koncepcyjne do [Memarium FAQ](../faq/memarium-faq.pl.md).

## Zanim wykonasz operację

Ustal cztery rzeczy:

1. **Przestrzeń** – Personal, Community, Public albo Crisis.
2. **Klasyfikację** – jawny `classification.v1`, niezależny od payloadu.
3. **Wywołującego** – operator, moduł lokalny albo delegat związany z konkretnym
   subjectem.
4. **Skutek** – zapis, odczyt, promocja, forget, deklasyfikacja, kwarantanna,
   archiwizacja albo rozstrzygnięcie Crisis.

Jeżeli któregoś z tych elementów nie da się określić, nie zastępuj go wartością
domyślną. Brak autorytetu albo klasyfikacji jest stanem odmowy lub kwarantanny,
nie pozwoleniem.

## 1. Wybierz przestrzeń

| Przestrzeń | Użyj, gdy | Nie używaj jako |
| :--- | :--- | :--- |
| Personal | materiał należy do pamięci operatora i ma pozostać lokalny | schowka dla danych modułu, których nikt nie sklasyfikował |
| Community | materiał należy do konkretnej wspólnoty i ma `community_id` | skrótu oznaczającego "kilka osób" albo Room |
| Public | materiał ma być dostępny publicznie po przejściu właściwego egress gate | automatycznego celu dla danych bez etykiety |
| Crisis | materiał ma konstytucyjne znaczenie awaryjne | ogólnej kolejki alertów lub logów |

Community replication jest ograniczone do wspólnej, zweryfikowanej federacji.
Udostępnienie danych poza nią wymaga jawnej promocji i zwykłego transportu
artefaktów; członkostwo w pokoju nie poszerza polityki przestrzeni.

## 2. Włącz i sprawdź Memarium

Memarium jest in-process subsystemem daemona. Konfiguracja powinna zawierać
aktywny subsystem i – w typowym profilu – odbudowywalny read sidecar. Po każdej
zmianie konfiguracji najpierw uruchom:

```sh
cargo run -p orbiplex-node-daemon -- check-config \
  --data-dir "$ORBIPLEX_DATA_DIR"
```

Następnie uruchom daemon i sprawdź jego zwykły status operatorski. Jeżeli
Memarium jest wyłączone lub storage nie został otwarty, host capability zwróci
`memarium_unavailable` albo `storage_unavailable`; nie próbuj wtedy omijać
bramki bezpośrednim zapisem do plików.

## 3. Nadaj wywołującemu minimalny passport

Moduł potrzebuje passportu pasującego jednocześnie do:

- `capability_id`, na przykład `memarium.write`;
- caller binding;
- grantu, na przykład `memarium/write`;
- przestrzeni i opcjonalnego `community_id`;
- opcjonalnego `entry_kind`;
- bieżącego, świeżego widoku revocation.

Pełny przepływ preview → sign and install → verify opisuje
[Memarium Capability Passport Issuance](../memarium-passport-issuance.md).
Wbudowany publisher template jest tylko rekomendacją. Nie staje się
wykonywalnym autorytetem, dopóki lokalna polityka nie wystawi lub nie
zainstaluje passportu.

Po instalacji zweryfikuj passport przez operator surface albo launcher:

```sh
orbiplex-node-launcher capability-passport-verify \
  --data-dir "$ORBIPLEX_DATA_DIR" \
  --file ./memarium-passport.json
```

## 4. Zapisz sklasyfikowany wpis

Użyj kanonicznego przykładu
[`write-entry.memarium-host-api.json`](../../schemas/examples/write-entry.memarium-host-api.json)
jako punktu wyjścia. Nie usuwaj `classification` i nie przenoś jej do
`attributes`. Przed wykonaniem polecenia ustaw `ORBIPLEX_DOCS` na katalog główny
checkoutu `orbidocs/`; daemon może działać z innego workspace'u.

```sh
# Wykonaj to przypisanie w katalogu głównym checkoutu orbidocs.
export ORBIPLEX_DOCS="$PWD"

curl -sS -X POST \
  "$ORBIPLEX_NODE/v1/host/capabilities/memarium.write" \
  -H "X-Orbiplex-Authtok: $MODULE_AUTHTOK" \
  -H 'Content-Type: application/json' \
  --data @"$ORBIPLEX_DOCS/doc/schemas/examples/write-entry.memarium-host-api.json"
```

Sukces ma `status: "ok"` i stabilny identyfikator wpisu albo faktu.
Powtórzenie z tym samym kanonicznym kluczem powinno zbiec do tego samego
skutku; nie twórz idempotencji z zegara lub opisowej etykiety.

### Zapis faktu zamiast wpisu

Fakt jest zdarzeniem lub twierdzeniem append-only. Użyj `op: "write_fact"` i
jawnego `fact_kind`. Wpis jest materialnym elementem pamięci, a fakt opisuje
historię, decyzję albo relację. Nie nadpisuj faktu, aby "poprawić stan" – dopisz
fakt korygujący i pozwól read modelowi złożyć aktualny widok.

## 5. Odczytaj wpisy albo fakty

Odczyt również przechodzi przez passport gate:

```json
{
  "op": "query_facts",
  "request": {
    "space": "personal",
    "query": {
      "fact_kind": "example.fact.v1",
      "any_tag": ["example"],
      "limit": 50,
      "order_by": "created-at-asc"
    }
  }
}
```

Wyślij dokument do `POST /v1/host/capabilities/memarium.read`. Dla Community
dołącz `community_id`. Ustawiaj jawny, ograniczony `limit`; projekcja SQLite
przyspiesza zapytanie, ale nie poszerza prawa odczytu.

## 6. Obsłuż rekord w kwarantannie

Najpierw wyświetl oczekujące fakty:

```sh
orbiplex-node-launcher memarium quarantine list \
  --data-dir "$ORBIPLEX_DATA_DIR" \
  --space personal \
  --limit 50
```

Następnie podejmij jedną jawną decyzję:

```sh
orbiplex-node-launcher memarium quarantine accept \
  --data-dir "$ORBIPLEX_DATA_DIR" \
  --space personal \
  --fact-id 'fact:personal:...' \
  --reason 'Source and classification verified.'
```

albo:

```sh
orbiplex-node-launcher memarium quarantine reject \
  --data-dir "$ORBIPLEX_DATA_DIR" \
  --space personal \
  --fact-id 'fact:personal:...' \
  --reason 'Classification provenance cannot be verified.'
```

Akceptacja i odrzucenie są faktami polityki. Nie usuwają źródłowego rekordu.
Powtórzenie terminalnej decyzji musi być idempotentne albo zakończyć się jawnym
konfliktem, nie drugą niezależną decyzją.

## 7. Dopuść węższy egress przez deklasyfikację

Deklasifikuj tylko dla konkretnej powierzchni i topic class. Najbezpieczniejszy
default to `one-shot`; TTL stosuj dopiero wtedy, gdy powtarzalny skutek jest
rzeczywiście częścią polityki.

```sh
orbiplex-node-launcher memarium declassify \
  --data-dir "$ORBIPLEX_DATA_DIR" \
  --space community \
  --community-id wroclaw-mutual-aid \
  --entry-kind resource-note \
  --fact-id 'fact:community:...' \
  --from-tier Community \
  --to-tier Public \
  --surface agora \
  --topic-class mutual-aid \
  --reason 'Reviewed for this public projection.'
```

Nie zakładaj, że po tej operacji zwykły odczyt pokaże niższy
`effective_tier`. Kontekstowy adapter egress składa trail dla swojej
powierzchni i aktualnego revocation view.

## 8. Wykonaj forget albo promocję

`memarium.forget` i `memarium.promote` są osobnymi host capabilities, ponieważ
zmieniają dostępność lub policy envelope. Przed wywołaniem sprawdź:

- czy przestrzeń dopuszcza dany rodzaj przejścia;
- czy passport obejmuje dokładny target;
- czy Community forget niesie poprawny `governance_ref`;
- czy Public forget pozostawi wymagany tombstone;
- czy Crisis nie jest traktowane jak zwykła retencja operatorska.

Promocja tworzy nowy fakt provenance. Nie mutuje rekordu w miejscu i nie może
być skutkiem ubocznym Room, Agora ani Artifact Delivery.

## 9. Przygotuj backup i handoff archiwalny

Lokalny operator rozpoczyna backup przez:

```http
POST /v1/memarium/backups
```

Po sukcesie sprawdza manifest:

```http
GET /v1/memarium/backups/{backup_id}
```

Handoff do archivisty przechodzi przez:

```http
POST /v1/memarium/archival/handoffs
```

Retrieval rozpoczyna:

```http
POST /v1/memarium/archival/retrievals
```

Backup najpierw buduje kompletny staging bundle, a dopiero potem promuje go
atomowo. Handoff preflightuje każdy package i używa Artifact Delivery. Partial
failure pozostaje widoczna w append-only facts; nie zamieniaj jej w pozorny
globalny sukces.

## 10. Sprawdź i rozwiąż finding Crisis

Odczytaj status przez `memarium.crisis_status` albo operatorski widok węzła.
Następnie przejdź po właściwej sekcji
[Crisis Detectors Runbook](../runbooks/crisis-detectors.md). Wymuszone
rozwiązanie jest uzasadnione dopiero wtedy, gdy operator rozumie źródło alarmu
i poda bounded reason.

`memarium.crisis_resolve` dopisuje fakt `operator-forced`. Nie usuwa
`crisis-detected`, a detektor może zgłosić problem ponownie po pełnym cyklu
false → true.

## 11. Diagnozuj według klasy błędu

| Status | Co sprawdzić najpierw |
| :--- | :--- |
| `passport_lookup_failed` | czy passport został zainstalowany, a nie tylko wystawiony |
| `binding_mismatch` | caller identity i `allowed_callers` |
| `revocation_stale` | źródła revocation i ich freshness budget |
| `classification_missing` | pierwszyklasowe pole `classification` |
| `quarantined` | kolejkę oraz istniejącą decyzję operatora |
| `space_policy_violation` | szyfrowanie, retencję i reguły przestrzeni |
| `storage_unavailable` | stan storage i read-sidecar diagnostics |

`reason` jest dla człowieka; automatyzacja ma używać `status`, `retryable` i
correlation id. Retry ma sens tylko dla błędów oznaczonych jako retryable.

## 12. Sprawdź ścieżkę akceptacyjną

Story-005 obejmuje sklasyfikowany prywatny przepływ AD/INAC dotykający
Memarium. Testy komponentowe Memarium pokrywają cztery przestrzenie, policy
facts, observer rules, archiwizację, Crisis i odbudowę sidecaru. Przy zmianie
konfiguracji operatorskiej uruchom co najmniej:

```sh
cargo test -p orbiplex-node-memarium
cargo test -p orbiplex-node-memarium-runtime
cargo test -p orbiplex-node-memarium-read-sidecar
cargo test -p orbiplex-node-daemon memarium
```

Końcowa kontrola powinna odpowiedzieć na trzy pytania: czy skutek został
autoryzowany przed zapisem, czy źródłowy fakt pozostał niezmienny oraz czy
operator potrafi odtworzyć przyczynę decyzji bez czytania sekretów z logów.
