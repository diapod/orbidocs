# Federation Bootstrap and Trust HOWTO

Ten dokument prowadzi od materiału ceremonii do działającego, diagnozowalnego
bootstrapu federacji. Składa Federation Root, official-service endorsements,
Seed Directory, TLS evidence, capability passports i peer handshake, lecz nie
zlewa ich w jedno pojęcie "zaufania".

Szczegółowa ceremonia kluczy ma osobny
[Federation Root Ceremony HOWTO](federation-root-ceremony-howto.pl.md).
Granice pojęciowe wyjaśnia
[Federation Bootstrap and Trust FAQ](../faq/federation-bootstrap-and-trust-faq.pl.md).

Jeżeli polecenie nie stanowi inaczej, wszystkie poniższe komendy `cargo` i
`tools/...` uruchamiaj z katalogu głównego workspace'u `node/`.

## Zanim zaczniesz: rozdziel dowody

| Warstwa | Pytanie, na które odpowiada |
| :--- | :--- |
| `federation-root.v1` | czyj autorytet i jaka polityka konstytuują federację? |
| official-service endorsement | czy konkretna usługa jest oficjalna w tej federacji? |
| capability passport | jaki zakres capability posiada konkretny subject? |
| Seed Directory | jakie zaakceptowane fakty discovery są obecnie projektowane? |
| TLS pin/CA/evidence | czy zaszyfrowany kanał prowadzi do oczekiwanego endpointu? |
| peer handshake | czy peer posiada klucz deklarowanej tożsamości węzła? |
| local policy | czy ten węzeł dopuszcza skutek w bieżącym kontekście? |

Nie zastępuj brakującego dowodu innym. W szczególności certificate nie jest
passportem, bootstrap nie jest endorsementem, a odpowiedź katalogu nie jest
peer handshake.

## 1. Wybierz profil ceremonii

Do disposable acceptance użyj jawnego lokalnego fixture profile. Do produkcji
użyj org/threshold custody zgodnego z charterem federacji. Produkcyjny klucz
custodiana powinien być passphrase-encrypted; plaintext PEM jest dozwolony
wyłącznie jako jawny, krótkotrwały fixture.

Przed podpisaniem ustal:

- `federation/id`;
- roster custodianów i threshold;
- sovereign/attestation subjects;
- endorsement policy;
- bootstrap Seed Directory;
- opcjonalne TLS pins;
- początkowy `pack_version` i policy refs.

## 2. Przeprowadź ceremonię root

Wykonaj kroki z dokumentu ceremonii: workspace, klucze, roster, frozen digest,
manifest, verify-before-sign, detached signatures, assembly i final verify.

Końcowym artefaktem jest zweryfikowany `federation-root.v1.json`. Opublikowany
digest i manifest należy archiwizować niezależnie od samego pliku. Transport
artefaktu nie staje się jego authority.

## 3. Zainstaluj root pack w data-dir

Umieść zweryfikowany plik pod:

```text
<data-dir>/federation-root.v1.json
```

W profilu produkcyjnym wyłącz fixture fallback:

```json
{
  "federation": {
    "allow_bundled_fixture_root": false
  }
}
```

Następnie sprawdź konfigurację przed uruchomieniem:

```sh
cargo run -p orbiplex-node-daemon -- check-config \
  --config-dir "$ORBIPLEX_CONFIG_DIR"
```

Loader ma odrzucić nieważny podpis, niespełniony threshold, nieznaną politykę
custody, rollback `pack_version`, ten sam numer z innym digestem oraz konflikt
z aktywnym `federation/id` zapisanym w data-dir.

## 4. Uruchom daemon i sprawdź aktywację

Pierwsza aktywacja i każda zmiana root fingerprint wymagają pełnego restartu.
SIGHUP albo hot reload może zgłosić, że kandydat wymaga restartu, lecz nie może
zmienić aktywnej federacji procesu.

Po starcie sprawdź:

```http
GET /v1/seed-directory
GET /v1/operator/network/peer-supervisor/status
GET /v1/operator/federation-service-endorsements
```

Oczekuj spójnego `federation/id`, root digest i `pack_version`. Brak usable Seed
Directory powinien być widoczny jako isolated/bootstrap albo degraded, a nie
zamaskowany pustą listą.

## 5. Zweryfikuj bootstrap Seed Directory

Każdy aktywny wpis bootstrap powinien mieć:

- jawne `enabled`;
- `node/id` i endpoint zgodny z rootem;
- ważny official-service endorsement, jeżeli ma być
  `federation-endorsed`;
- HTTPS i poprawny `tls_certificate_sha256`, jeżeli root używa pinningu;
- capability passport albo registration wymagane przez konsumenta.

Wpis bez aktywnego endorsementu może pozostać advisory. Nie naprawiaj tego
przez lokalne przepisanie trust level na `official`.

## 6. Skonfiguruj dodatkowe trusted directories

`network.seed_directory_trust[]` opisuje lokalnie zaakceptowane źródła i ich
poziomy zaufania. Wybierz jedną jawną politykę zapytań:

- `preferred-directory` dla deterministycznego primary z kontrolowanym fallback;
- `quorum`, gdy wymagane jest zgodne minimum niezależnych katalogów;
- `weighted-trust`, gdy źródła mają jawne, różne wagi.

Wagi, policy refs i federation ids są wejściami lokalnej polityki. Embedded
directory nie powinno głosować na siebie bez jawnego opt-in. Każdy wynik nadal
przechodzi weryfikację artefaktu u konsumenta.

## 7. Włącz trusted Agora replay, jeżeli jest potrzebny

`network.seed_directory_agora_replay` jest opt-in. Po włączeniu musi wskazywać
jawny executor/provider i bounded page limit. Runtime replayuje lane'y `adv`,
`cap` i `revocations` tylko dla skonfigurowanych federation ids.

Po pierwszym przebiegu sprawdź w `/v1/seed-directory`:

- cursor per `(federation_id, lane)`;
- accepted i rejected counts;
- last run i last error;
- skip reason, jeżeli źródło nie kwalifikuje się do replayu.

Pojedynczy malformed record ma zostać odrzucony i odnotowany, nie zatrzymać
całego daemona ani wejść do projekcji jako wartość domyślna.

## 8. Wystaw albo zainstaluj endorsement usługi

Operator surface udostępnia:

```http
POST /v1/operator/federation-service-endorsements/issue
POST /v1/operator/federation-service-endorsements/install
GET  /v1/operator/federation-service-endorsements
```

Issuance musi odpowiadać custody policy aktywnego root. Dla org/threshold nie
udawaj, że jeden lokalny podpis zastępuje ceremonię. Install zapisuje
ingress-enforced source; body może nieść tylko dodatkowe `source/detail`, nie
może zmienić pochodzenia audytowego.

Po instalacji zweryfikuj node id, capability id, validity window, signer
authority i revocation status. Dopiero wtedy konsument może projektować
official status.

## 9. Zarejestruj capability i sprawdź discovery

Capability registration w Seed Directory jest passport-backed i monotoniczne
po dodatnim `sequence/no`. Identyczny republish jest idempotentny; starszy
sequence nie może nadpisać nowszego. Wygasłe albo odwołane registration nie
powinno pojawić się w aktywnym lookup.

Sprawdź osobno:

1. registration i passport;
2. official endorsement, jeżeli wymagany;
3. endpoint projection;
4. TLS evidence;
5. peer handshake przy realnym połączeniu.

Zielony lookup bez ostatnich dwóch punktów jest kandydatem discovery, nie
dowodem działającej sesji.

## 10. Poproś o query attestation tylko tam, gdzie ma sens

Krytyczne odczyty `/adv`, `/cap` i `/revocations` mogą żądać:

```text
attest=seed-directory-query.v1
```

Zweryfikuj digest kanonicznej odpowiedzi, normalized query, projection
high-water, validity window i signer id. Brak signer'a przy jawnym żądaniu
atestacji powinien zwrócić `503 attestation_unavailable`; bez parametru response
shape pozostaje zwykłą projekcją katalogu.

## 11. Sprawdź TLS i peer identity jako osobne warstwy

Jeżeli bootstrap zawiera pin, porównaj `sha256:<base64url>` z raw leaf
certificate DER. Połączenie musi używać HTTPS/WSS. Dla node endpoint evidence
dopuszczalne są aktywne `sha256-leaf-der` albo `sha256-spki` zgodnie z polityką.

Po zestawieniu TLS wykonaj Orbiplex peer handshake i sprawdź deklarowany
`node:did:key`. Opaque `route:` w certificate subject ogranicza wyciek stabilnej
tożsamości do skanerów TLS; nie jest substytutem handshake.

## 12. Rotuj bez split-brain

Przy zmianie root packa:

1. przygotuj wyższy `pack_version`;
2. wykonaj pełną ceremonię i final verify;
3. rozprowadź pack poza kanałem, którego ważność właśnie zmieniasz;
4. zatrzymaj daemon;
5. atomowo zastąp `federation-root.v1.json`;
6. uruchom `check-config`;
7. uruchom daemon i sprawdź status wszystkich warstw.

Nigdy nie używaj tego samego `pack_version` dla innego digestu. Przy rotacji
TLS pinu skoordynuj dostępność nowego certificate z restartem konsumentów;
MVP nie utrzymuje równolegle dwóch aktywnych pinów na endpoint.

## 13. Uruchom acceptance

Kontrakty helperów root i acceptance seeders sprawdza:

```sh
python3 tools/acceptance/test_federation_root_acceptance.py
```

Story-010 i Story-011 budują runtime root po poznaniu rzeczywistych node ids,
dołączają bounded endorsements i sprawdzają `/v1/seed-directory` przed
uruchomieniem wyższych przepływów. Dla warstwy komponentowej uruchom:

```sh
cargo test -p orbiplex-node-seed-directory
cargo test -p orbiplex-node-daemon seed_directory
cargo test -p orbiplex-node-daemon federation_root
```

Acceptance fixture dowodzi poprawności ścieżki lokalnej. Nie dowodzi, że
produkcyjny roster, zewnętrzna dystrybucja packa ani publiczne endpointy są już
operacyjnie gotowe.

## 14. Diagnozuj od korzenia do skutku

Gdy discovery nie działa, sprawdzaj w tej kolejności:

1. root signature, threshold, digest i `pack_version`;
2. bootstrap endorsement i jego revocation;
3. Seed Directory source status i replay;
4. capability passport/registration;
5. TLS pin albo endpoint evidence;
6. peer handshake;
7. consumer-local policy.

Ta kolejność rozplątuje przyczynę. Próba naprawy od końca – na przykład przez
dodanie peer allowlisty – może ukryć brak autorytetu, lecz go nie tworzy.
