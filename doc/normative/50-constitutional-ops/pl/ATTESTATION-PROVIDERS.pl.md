# Metody poświadczenia tożsamości i ich mapowanie w DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-ATTEST-PROVIDERS-001` |
| `typ` | Ustawa wykonawcza / rejestr metod poświadczenia |
| `wersja` | 0.1.0-draft |
| `data` | 2026-03-12 |

---

## 1. Cel dokumentu

Niniejszy dokument mapuje metody poświadczenia tożsamości na:

- klasę siły poświadczenia (`weak` / `strong`),
- maksymalny poziom `IAL`,
- ograniczenia operacyjne,
- wymagania dla upgrade i odświeżenia.

Dokument nie tworzy nowego rodzaju `root-identity`. Określa wyłącznie jakość
poświadczenia źródła tożsamości.

---

## 2. Zasady ogólne

1. `weak` i `strong` są własnościami poświadczenia, nie ontologii osoby.

2. Ta sama `anchor-identity` może mieć w czasie wiele poświadczeń o różnej sile.

3. Upgrade `weak -> strong` POWINIEN zachowywać `anchor-identity`, `node-id` i
   `persistent_nym`, o ile istnieje dowód ciągłości kontroli.

4. Maksymalny `IAL` z danej metody jest sufitem domyślnym; federacja może go
   obniżyć, ale nie powinna go podwyższać bez jawnej procedury walidacyjnej.

---

## 3. Mapa domyślna

| `source_class` | Przykład | Siła | Domyślny max `IAL` | Uwagi |
| :--- | :--- | :--- | :--- | :--- |
| `phone` | numer telefonu z potwierdzeniem OTP | `weak` | `IAL1` | `IAL2` tylko przez jawną politykę federacyjną typu opt-in i dodatkowe zabezpieczenia |
| `multisig-basic` | poręczenie `k-of-n` bez pogłębionego audytu poręczycieli | `weak` | `IAL2` | fallback dla jurysdykcji bez mocnego eID |
| `multisig-audited` | poręczenie `k-of-n` z audytem, różnorodnością i śladem odpowiedzialności poręczycieli | `strong` | `IAL3` | nie odblokowuje `IAL4` bez osobnego toru odpieczętowania |
| `eid` | państwowy lub ponadpaństwowy eID | `strong` | `IAL3` | do `IAL4` po dołączeniu toru odpieczętowania |
| `mobywatel` | kanał urzędowy QR / aplikacja państwowa | `strong` | `IAL3` | lokalna zależność jurysdykcyjna |
| `epuap` | profil zaufany / urząd | `strong` | `IAL3` | zależne od jakości integracji |
| `qualified_signature` | podpis kwalifikowany | `strong` | `IAL4` | preferowana metoda dla ról wysokiej stawki |
| `registry` | formalne dane rejestrowe organizacji | `strong` | `IAL3` | do `IAL4` po spełnieniu wymogów proceduralnych |
| `other` | metoda lokalna / eksperymentalna | zależnie od walidacji | `IAL0-IAL2` | wymaga jawnej dokumentacji federacyjnej |

---

## 4. Reguły szczególne dla numeru telefonu

1. Potwierdzony numer telefonu jest wygodnym wejściem, ale NIE POWINIEN sam z
   siebie odblokowywać ról wysokiej stawki.

2. Dla `source_class = phone` federacja POWINNA co najmniej ograniczyć:

- role governance,
- role panelowe,
- role wyroczni wysokiej stawki,
- operacje wymagające `U2` lub `U3`.

3. Federacja MOŻE dopuścić `phone -> IAL2` wyłącznie przez jawną politykę opt-in
   i tylko wtedy, gdy istnieją dodatkowo:

- dłuższy okres dojrzewania reputacyjnego,
- detekcja anomalii przejęcia,
- limity mnożenia wpływu,
- możliwość szybkiego downgrade po sygnale kompromitacji.

4. Upgrade `phone -> strong` POWINIEN przechodzić przez okres wyczekiwania
   (`phone_upgrade_cooldown`) oraz kontrolę anomalii zgodną z
   `IDENTITY-UPGRADE-ANOMALY-SIGNALS.pl.md`.

Domyślny profil bezpieczny:

- `phone_upgrade_cooldown = 14 dni`,

- brak aktywnego recovery w krótkim oknie poprzedzającym upgrade,

- brak gwałtownej rotacji stacji, nymów albo kluczy węzła,

- brak aktywnego sporu tożsamościowego, sygnału przejęcia albo otwartego incydentu,

- brak świeżej zmiany numeru telefonu lub źródła poświadczenia bez dodatkowego review.

---

## 5. Reguły upgrade

1. Upgrade `weak -> strong` wymaga równocześnie:

- kontroli nad istniejącą kotwicą,
- nowego poświadczenia `strong`,
- braku twardego sporu co do tożsamości.

2. Po upgrade:

- `anchor-identity` pozostaje ta sama,
- `node-id` może pozostać ten sam,
- efemeryczne nymy i certyfikaty stacji mogą zostać odświeżone,
- poprzednie poświadczenie pozostaje w łańcuchu audytowym jako `superseded` albo `expired`.

3. Jeżeli upgrade rozpoczyna się z `source_class = phone`, federacja POWINNA
   uruchomić co najmniej:

- kontrolę wieku poświadczenia telefonu,
- kontrolę churnu urządzeń i stacji,
- kontrolę anomalii geograficznych lub sieciowych, jeśli takie sygnały są dostępne,
- kontrolę niedawnych prób odzyskiwania, resetów kluczy i odwołań,
- manualny review dla ról, które po upgrade miałyby wejść w zakres `IAL3+`.

---

## 6. Relacje do innych dokumentów

- `ROOT-IDENTITY-AND-NYMS.pl.md` definiuje warstwy tożsamości i poziomy `IAL`.
- `IDENTITY-ATTESTATION-AND-RECOVERY.pl.md` definiuje pamięć poświadczeń i upgrade.
- `ROLE-TO-IAL-MATRIX.pl.md` określa, jakie role mogą być odblokowane przy danym `IAL`.
- `IDENTITY-UPGRADE-ANOMALY-SIGNALS.pl.md` definiuje minimalny katalog sygnałów,
  reakcji i review dla upgrade poświadczenia.
