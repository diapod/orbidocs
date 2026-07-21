# Federation Root Ceremony HOWTO

Ten dokument opisuje wyłącznie ceremonię utworzenia i podpisania root packa.
Instalację, Seed Directory bootstrap, endorsements, TLS evidence, rotację i
diagnostykę uruchomionego węzła opisuje nadrzędny
[Federation Bootstrap and Trust HOWTO](federation-bootstrap-and-trust-howto.pl.md).

Ten HOWTO opisuje ścieżkę ceremonii federation-root, w której każdy kustosz
generuje świeży klucz narzędziem
`tools/federation-root-ceremony/federation_root_ceremony.py keygen`. Nie opisuje
importu klucza uczestnika z node'a, użycia node `data-dir` ani wyprowadzania
tożsamości operatora z klucza kustosza.

Powiązane dokumenty:

- Proposal 076: `doc/project/40-proposals/076-federation-identity-and-network-selector.md`
- Solution 041: `doc/project/60-solutions/041-federation-root/041-federation-root.md`
- Charter roota: `doc/normative/50-constitutional-ops/pl/ORBIPLEX-MAIN-ROOT-CHARTER.pl.md`
- Referencja narzędzia: `node/tools/federation-root-ceremony/README.md`

## Role

- **Koordynator** przygotowuje roster governance, niepodpisany draft roota,
  manifest, transcript ceremonii i finalne złożenie.
- **Kustosz** generuje jeden dedykowany klucz na własnej maszynie, weryfikuje
  zamrożony digest, podpisuje dokładnie ten draft roota i zwraca tylko materiał
  publiczny oraz podpis odłączony.
- **Weryfikator** niezależnie uruchamia kontrole manifestu, złożenia i finalnego
  packa przed publikacją. Może to być koordynator plus co najmniej jeden
  kustosz.

Koordynator nigdy nie dostaje prywatnego materiału kluczy. Klucze kustoszy mogą
później atestować albo autoryzować oddzielną tożsamość operatora przez jawne
wiązanie, ale nie są tożsamościami operatorów i nie wolno ich w takie
tożsamości konwertować.

## Checklista Przed Ceremonią

Uzgodnijcie te wartości zanim jakikolwiek digest zostanie zamrożony:

- `federation_id`, na przykład `orbiplex-main`;
- `pack_version`;
- subject roota, produkcyjnie zwykle `org:did:key:...`;
- referencję polityki custody, na przykład `org-custody:orbiplex-main-root:v1`;
- próg, na przykład `2-of-3`;
- charter albo governance `policy_ref`;
- dokładny roster kustoszy i nazwy wyświetlane;
- identyfikator ceremonii;
- miejsce publikacji finalnego packa `federation-root.v1`;
- reguły redakcji publicznego transcriptu.

Wszystkie komendy niżej używają ścieżek względnych wobec repozytorium. Uruchamiaj
je z katalogu głównego repozytorium zawierającego `node/`.

## 1. Koordynator Tworzy Workspace

```sh
mkdir -p ceremony/keys ceremony/public ceremony/signatures ceremony/out
```

`ceremony/keys/` jest pokazany tylko dla lokalnych przykładów. W prawdziwej
ceremonii każdy kustosz trzyma własny katalog kluczy prywatnych na własnej
maszynie; koordynator nie powinien tworzyć ani zbierać kluczy prywatnych.

## 2. Każdy Kustosz Generuje Swój Klucz

Każdy kustosz uruchamia lokalnie, używając własnej etykiety w nazwach plików:

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py keygen \
  --out ceremony/keys/alice.ed25519.pem \
  --public-json ceremony/public/alice.public.json \
  --prompt-passphrase
```

Narzędzie pyta o passphrase i jej potwierdzenie, zapisuje zaszyfrowany
prywatny PEM i nigdy nie przyjmuje passphrase jako argumentu CLI. Dla
nieinteraktywnej automatyzacji offline użyj `--passphrase-stdin` albo
krótkotrwałego pliku `--passphrase-file` z restrykcyjnymi uprawnieniami.

Oczekiwane lokalne wyjścia:

- `ceremony/keys/alice.ed25519.pem` — zaszyfrowany prywatny klucz Ed25519,
  tryb `0600`, trzymać tajnie i offline;
- `ceremony/public/alice.public.json` — publiczny rekord `key_public`, można
  wysłać koordynatorowi.

Kustosz wysyła koordynatorowi tylko `alice.public.json`. Nie wysyłaj pliku PEM,
nie wklejaj go do czatu, nie załączaj do ticketów i nie umieszczaj w
transcripcie.

## 3. Koordynator Buduje Roster

Koordynator wyciąga `key_public` z rekordów publicznych i przygotowuje
niepodpisany draft roota z jawnego rosteru governance:

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py \
  root-draft-from-roster \
  --confirm-roster \
  --production-orbiplex-main \
  --out ceremony/unsigned.federation-root.json \
  --federation-id orbiplex-main \
  --pack-version 1 \
  --issued-at-now \
  --policy-ref policy:dia-root-001@0.1.0#appeals \
  --org-id org:did:key:z6Mk... \
  --custody-policy-ref org-custody:orbiplex-main-root:v1 \
  --threshold-min-signers 2 \
  --authorized-key-public z6MkAlice... \
  --authorized-key-public z6MkBob... \
  --authorized-key-public z6MkCarol...
```

`--confirm-roster` jest wymagane, bo autorytet pochodzi z rosteru governance, a
nie z tego, jakie podpisy pojawią się później w katalogu.

## 4. Koordynator Zamraża Digest

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py digest \
  ceremony/unsigned.federation-root.json
```

Zapisz zwrócony digest `sha256:...` w transcripcie ceremonii. To jest wartość,
którą każdy kustosz musi niezależnie porównać przed podpisaniem.

## 5. Koordynator Tworzy i Weryfikuje Manifest

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py manifest-init \
  --production-orbiplex-main \
  --out ceremony/manifest.json \
  --ceremony-id orbiplex-main-root-001 \
  --federation-id orbiplex-main \
  --min-signers 2 \
  --total-signers 3 \
  --root ceremony/unsigned.federation-root.json
```

Następnie sprawdź, czy manifest nadal wskazuje na zamrożony draft roota:

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py manifest-verify \
  --production-orbiplex-main \
  --manifest ceremony/manifest.json
```

Wyślij każdemu kustoszowi:

- `ceremony/unsigned.federation-root.json`;
- `ceremony/manifest.json`;
- oczekiwany digest `sha256:...`, najlepiej drugim kanałem;
- dokładny identyfikator ceremonii i podsumowanie rosteru.

Nie wysyłaj kluczy prywatnych, bo koordynator nie powinien ich posiadać.

## 6. Każdy Kustosz Weryfikuje Przed Podpisem

Każdy kustosz lokalnie sprawdza digest:

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py digest \
  ceremony/unsigned.federation-root.json
```

Porównuje wynik z digestem zapisanym przez koordynatora. Jeśli wynik się nie
zgadza, zatrzymajcie ceremonię. Nie podpisujcie draftu "prawie takiego samego".

Każdy kustosz powinien też sprawdzić co najmniej:

- `federation_id`;
- `pack_version`;
- `attestation_roots[]`;
- `custody_policies[]`;
- `threshold/min_signers`;
- własny `key_public` na liście autoryzowanych signerów;
- `policy_ref`;
- wpisy bootstrap i Seed Directory.

## 7. Każdy Kustosz Podpisuje Zamrożony Root

Każdy kustosz podpisuje swoim lokalnym kluczem prywatnym:

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py sign \
  --root ceremony/unsigned.federation-root.json \
  --key ceremony/keys/alice.ed25519.pem \
  --prompt-passphrase \
  --out ceremony/signatures/alice.sig.json
```

Passphrase odblokowuje wyłącznie lokalny zaszyfrowany PEM. Nie jest zapisywana
do rekordu podpisu, manifestu, transcriptu ani root-packa.

Kustosz odsyła koordynatorowi tylko `alice.sig.json`. Podpis odłączony jest
publicznym materiałem ceremonii; klucz prywatny zostaje lokalnie.

## 8. Koordynator Składa Root Pack

Po zebraniu wystarczającej liczby podpisów odłączonych koordynator wykonuje
strict assemble:

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py assemble \
  --production-orbiplex-main \
  --strict \
  --root ceremony/unsigned.federation-root.json \
  --out ceremony/out/federation-root.v1.json \
  ceremony/signatures
```

Strict assembly odrzuca niepoprawne i nieautoryzowane podpisy. Dla produkcyjnego
`orbiplex-main` komenda wymusza też profil produkcyjny i wymaga `--strict`.

## 9. Wszyscy Weryfikują Finalny Pack

Koordynator i co najmniej jeden kustosz weryfikują finalny artefakt:

```sh
node/tools/federation-root-ceremony/federation_root_ceremony.py verify \
  --production-orbiplex-main \
  ceremony/out/federation-root.v1.json
```

Zgłoszony digest powinien odpowiadać zamrożonemu digestowi. Jeśli weryfikacja
nie przechodzi, nie publikujcie packa.

## 10. Publikacja i Archiwizacja

Opublikujcie:

- `ceremony/out/federation-root.v1.json`;
- zredagowany transcript ceremonii;
- publiczne rekordy kustoszy;
- manifest i finalny digest.

Zarchiwizujcie prywatnie:

- zaszyfrowany prywatny klucz każdego kustosza, kontrolowany wyłącznie przez
  tego kustosza;
- lokalne notatki maszynowe potrzebne do przyszłej rotacji albo odzyskiwania;
- niepubliczne notatki incydentowe.

Nigdy nie archiwizuj kluczy prywatnych w repozytorium, publicznym transcripcie,
issue trackerze, czacie ani współdzielonym backupie. Kopia zaszyfrowanego PEM-a
jest dopuszczalna tylko wtedy, gdy backup i passphrase są zarządzane jako
oddzielne sekrety danego kustosza.

## Reguły Przerwania

Zatrzymajcie ceremonię i zacznijcie od nowego draftu albo nowego digestu, gdy:

- którykolwiek kustosz otrzyma inny digest;
- manifest przestaje się weryfikować;
- roster jest błędny albo niepełny;
- próg jest błędny;
- klucz prywatny mógł zostać skopiowany do koordynatora albo kanału publicznego;
- strict assembly odrzuca podpis;
- finalna weryfikacja zgłasza inny digest albo odrzucony podpis.

Fakty są ważniejsze niż wygoda: jeśli zamrożone bajty się zmieniły, podpisy nad
starymi bajtami nie nadają się do ponownego użycia.
