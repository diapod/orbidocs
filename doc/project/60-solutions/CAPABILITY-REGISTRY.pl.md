# Rejestr capability IDs

Ten dokument jest ludzkoczytelnym rejestrem capability IDs używanych na granicy
Node <-> Node oraz Node <-> Seed Directory.

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

Nie obejmuje host-local capabilities typu `recovery.sign` czy
`catalog.local.query`. Te należą do lokalnej powierzchni hosta, nie do
federacyjnego rejestru capability IDs.

## Źródła prawdy

Ten dokument ma pozostać zsynchronizowany co najmniej z:

- `node:capability/src/lib.rs`
- `orbidocs:doc/project/60-solutions/node.md`
- `orbidocs:doc/project/60-solutions/CAPABILITY-MATRIX.pl.md`
- odpowiednimi proposalami capability lub attached roles

Jeżeli zmienia się:

- `capability_id`,
- wire name,
- semantyka capability,
- albo jej główny owner runtime,

to ten rejestr również powinien zostać zaktualizowany.

## Capability Registry

| capability_id | Wire name | Klasa | Rola semantyczna | Typowy owner runtime | Passport w MVP | Uwagi |
|---|---|---|---|---|---|---|
| `network-ledger` | `core/network-ledger` | infrastrukturalna | zdalny autorytet settlement ledger dla innych node'ów | settlement-capable Node | tak | Capability oznacza autorytet księgi, nie tylko pojedynczy hold czy politykę. |
| `seed-directory` | `role/seed-directory` | infrastrukturalna | katalog capability passports, revocations i advertisementów używany do bootstrapu i discovery | Seed Directory service lub embedded Node service | tak | Capability dotyczy katalogu i zaufanego publikowania/odczytu wpisów katalogowych. |
| `offer-catalog` | `role/offer-catalog` | rola domenowa | federacyjna powierzchnia ofertowa używana do responder-side fetch i discovery | Dator jako strona podaży, Arca jako strona popytu/discovery | tak, jeśli capability jest delegowane przez passport | Capability jest domenowa; konkretna implementacja może rozdzielać supply i observed/discovery na różne moduły. |
| `escrow` | `role/escrow` | attached supervisory role | nadzorca hold, release, refund, freeze i dispute path dla settlement kontraktów | escrow supervisor node lub attached service | tak | Capability oznacza nadzór nad losem środków zarezerwowanych dla kontraktu, nie pełny autorytet całej księgi. |
| `oracle` | `plugin/oracle` | attached role / plugin | bounded external judgment, verification lub adjudication surface | przyszły oracle service | planowane | Na obecnym etapie to zarezerwowany identyfikator i kierunek rozszerzenia, nie pełny hard-MVP runtime slice. |

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

## Następne kroki

- Rozszerzyć ten rejestr, gdy pojawią się kolejne capability IDs o stabilnym
  znaczeniu między-node.
- Dopisać bardziej precyzyjną tabelę `issuer -> consumer -> scope`, jeżeli
  attached-role passports zaczną mieć bogatsze zakresy (`scope`) niż obecne MVP.
