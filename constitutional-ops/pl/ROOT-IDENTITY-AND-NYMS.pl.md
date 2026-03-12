# Tożsamość pierwotna i nymy w DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-ROOT-ID-001` |
| `typ` | Ustawa wykonawcza (Poziom 3 hierarchii normatywnej) |
| `wersja` | 0.1.0-draft |
| `podstawa` | Art. III.1-9, VII.4-8, XV, XVI Konstytucji DIA; `PROCEDURAL-REPUTATION-SPEC.pl.md`; `FEDERATION-MEMBERSHIP-AND-QUORUM.pl.md`; `IDENTITY-ATTESTATION-AND-RECOVERY.pl.md` |
| `status mechanizmów` | model danych i poziomy pewności są normatywne; konkretne integracje eID pozostają parametrami wdrożeniowymi |

---

## 1. Cel dokumentu

Konstytucja wymaga jednocześnie:

- ochrony prywatności i minimalnego ujawniania,
- odporności na Sybila i mnożenie wpływu przez tanie tożsamości,
- podwyższonych progów odpowiedzialności dla ról o większej władzy,
- proceduralnej możliwości ujawnienia, gdy stawka jest wysoka.

Brakuje jednak wspólnego modelu, który rozdzielałby:

- **tożsamość pierwotną** osoby lub podmiotu,
- **główną tożsamość pochodną** zakotwiczoną w tożsamości pierwotnej,
- **trwałą tożsamość węzła** jako publiczny pseudonim odpowiedzialności,
- **pseudonimy kryptograficzne** używane w komunikacji i governance,
- **poziom pewności tożsamości**, od którego zależy dopuszczalny wpływ.

W tym modelu słabość lub siła nie jest własnością samej `root-identity`, lecz
własnością poświadczenia źródła tożsamości. Ten sam podmiot może więc przejść od
poświadczenia `weak` do `strong` bez utraty `anchor-identity`, `node-id` i
trwałych nymów.

Niniejszy dokument definiuje taki model.

---

## 2. Zasady podstawowe

1. W komunikacji roju **uczestniczą nymy**, nie cywilna tożsamość pierwotna.

2. Tożsamość pierwotna służy do **zakotwiczenia, poświadczenia i ewentualnego
   odpieczętowania** tożsamości pochodnych, a nie do ciągłej ekspozycji w protokole.

3. **Im większy wpływ na innych, dane wrażliwe, reputację lub decyzje
   governance, tym wyższy wymagany poziom pewności tożsamości i tym większy
   zakres ujawnienia proceduralnego.**

4. Wiele `node-id` lub nymów wywiedzionych z jednej tożsamości pierwotnej **nie
   może samo w sobie mnożyć wpływu**. Anty-Sybil liczy źródło zakotwiczenia, nie
   liczbę masek.

5. Jeden człowiek lub jeden podmiot może działać przez wiele urządzeń i wiele
   agentów, ale nie oznacza to automatycznie wielu niezależnych tożsamości
   reputacyjnych.

6. System preferuje **pseudonimowość operacyjną i jawność proceduralną**, a nie
   anonimowość bez odpowiedzialności ani pełną jawność cywilną jako tryb domyślny.

7. `IAL` służy przede wszystkim jako **bramka kwalifikacyjna** do klas ról,
   decyzji i zakresów działania. Federacja MOŻE przyznać silniej zweryfikowanej
   tożsamości niewielką, stałą dźwignię proceduralną, ale nigdy w formie
   mnożnika reputacji i nigdy powyżej `1%` całkowitej mocy decyzyjnej danego
   mechanizmu.

---

## 3. Model pojęciowy

### 3.1. Warstwy tożsamości

| Warstwa | Znaczenie | Domyślna widoczność |
| :--- | :--- | :--- |
| `root-identity` | Tożsamość pierwotna osoby lub podmiotu | prywatna / ujawnialna tylko proceduralnie |
| `anchor-identity` | Główna tożsamość pochodna: stabilny odcisk kryptograficzny zakotwiczony w `root-identity` | prywatna / selektywnie ujawnialna |
| `node-id` | Trwała, publiczna tożsamość węzła i główny pseudonim odpowiedzialności | publiczny |
| `nym` | Efemeryczny lub kontekstowy pseudonim kryptograficzny używany przez `node-id` | publiczny lub federacyjny |
| `station-id` | Konkretne urządzenie / host działający pod delegacją nymu lub węzła | publiczny lub selektywnie ujawniany |
| `agent-id` | Proces lub instancja wykonawcza działająca w ramach uprawnień stacji | lokalny / techniczny |

### 3.2. Relacje

```text
root-identity
  -> poświadcza jedną lub wiele anchor-identity
anchor-identity
  -> wyprowadza lub poświadcza jeden lub wiele node-id
node-id
  -> może wystawiać jeden lub wiele nymów
  -> może delegować jeden lub wiele station-id
nym
  -> może delegować jeden lub wiele station-id
station-id
  -> może uruchamiać jeden lub wiele agent-id
```

### 3.3. Zasada źródła wpływu

Wpływ reputacyjny, kwalifikowalność do ról i ograniczenia anty-Sybil odnoszą się
domyślnie do **`node-id` zakotwiczonego w `anchor-identity`**, a nie do samej
liczby nymów, stacji ani procesów.

---

## 4. Root identity

`root-identity` oznacza źródłową, pozaprotokołową tożsamość osoby fizycznej,
osoby prawnej albo innego uznawanego podmiotu odpowiedzialności.

`root-identity` może być poświadczana przez źródła o różnej sile dowodowej:

- `weak` - źródła o niskim koszcie wejścia i ograniczonej mocy dowodowej,
  np. potwierdzony numer telefonu,

- `strong` - źródła o wysokiej mocy dowodowej i silniejszym zakotwiczeniu
  prawnym lub organizacyjnym, np. eID, podpis kwalifikowany albo formalny rejestr.

Może być poświadczona przez:

- potwierdzony numer telefonu albo równoważny kanał telekomunikacyjny,

- państwowy lub ponadpaństwowy system eID,
- podpis kwalifikowany,
- profil zaufany / ePUAP,
- aplikację mObywatel i mechanizm kodów QR lub równoważny kanał urzędowy,
- kontrolowany multisig poręczeń węzłów o niezerowej reputacji proceduralnej,
- inną metodę zaakceptowaną federacyjnie, o ile zapewnia audytowalność i
  odwoływalność.

`root-identity` nie jest domyślnie publikowana. Jej rola to:

- wystawianie poświadczeń dla `anchor-identity`,
- umożliwienie ograniczonego odpieczętowania przy wysokiej stawce,
- ograniczanie mnożenia wpływu przez tanie tworzenie tożsamości.

Mapowanie konkretnych metod do klas `weak` / `strong` oraz do maksymalnego
poziomu `IAL` definiuje `ATTESTATION-PROVIDERS.pl.md`.

---

## 5. Tożsamość kotwicząca, tożsamość węzła i nymy

### 5.1. Tożsamość kotwicząca (`anchor-identity`)

`anchor-identity` jest główną tożsamością pochodną wywiedzioną z
`root-identity`. Ma charakter stabilnego odcisku kryptograficznego albo
poświadczenia, które:

- nie jest domyślnie ujawniane innym uczestnikom,
- pozwala rozpoznać wspólne źródło zakotwiczenia wielu `node-id` lub nymów,
- umożliwia utrzymanie ciągłości odpowiedzialności mimo rotacji publicznych masek,
- stanowi podstawę do wyliczania `IAL` i kontroli anty-Sybil.

Jeżeli implementacja techniczna pozwala bezpiecznie wywodzić `node-id`
bezpośrednio z `root-identity`, federacja MOŻE pominąć osobny artefakt
`anchor-identity`, ale semantycznie nadal musi zachować tę warstwę jako
rozróżnienie między tożsamością pierwotną a publicznym identyfikatorem węzła.

Szczegółowy sposób pierwszego poświadczenia, użycia frazy odzyskiwania, roli
`salt` oraz pamięci wcześniejszego poświadczenia definiuje
`IDENTITY-ATTESTATION-AND-RECOVERY.pl.md`.

### 5.2. Tożsamość węzła (`node-id`)

`node-id` jest trwałą, publiczną tożsamością węzła i głównym pseudonimem
odpowiedzialności w roju. To `node-id`:

- gromadzi główną reputację proceduralną i operacyjną,
- jest podstawową jednostką trasowania zaufania i kontroli anty-Sybil,
- może delegować stacje i wystawiać nymy kontekstowe,
- ma swojego **dysponenta** (`custodian`), identyfikowanego proceduralnie przez
  trwały nym, rekord zakotwiczenia albo - przy wysokiej stawce - przez tor
  odpieczętowania do `root-identity`.

`node-id` powinien być wyprowadzany z klucza lub certyfikatu kontrolowanego przez
`anchor-identity`, ale nie musi zdradzać samej `anchor-identity`.

`custodian_ref` należy rozumieć jako trwały identyfikator proceduralny dysponenta
`node-id`: stabilniejszy niż zwykły efemeryczny nym, ale słabszy i bardziej
osłonowy niż `root-identity`. Domyślnie nie jest on równy `anchor-identity`, choć
tor audytowy może powiązać go z rekordem zakotwiczenia albo - przy najwyższej
stawce - z `root-identity`.

### 5.3. Nymy

`nym` jest efemerycznym lub kontekstowym pseudonimem kryptograficznym
delegowanym przez `node-id` na potrzeby komunikacji, transakcji, płatności,
sporu, akcji albo innego działania. To nym:

- podpisuje komunikację lub wskazuje klucz podpisujący,
- może gromadzić reputację lokalną lub czasową,
- pełni role kontekstowe,
- podlega sankcjom proceduralnym,
- jest widoczny dla innych uczestników.

Emitentem kryptograficznym nymu jest `node-id`, a emitentem odpowiedzialnościowym
jest dysponent (`custodian`) tego `node-id`. Oznacza to, że protokół widzi nym
jako maskę wystawioną przez `node-id`, a tor audytowy może - jeśli wymaga tego
stawka sprawy - powiązać ten akt emisji z `custodian_ref`, a wyjątkowo także z
`root-identity`.

`nym` nie jest domyślnie główną jednostką wpływu w systemie. Wpływ trwały,
anti-Sybil i główna odpowiedzialność pozostają przypisane do `node-id` oraz,
pośrednio, do wspólnego źródła zakotwiczenia.

### 5.4. Typy nymów

| Typ | Zastosowanie | Własność |
| :--- | :--- | :--- |
| `persistent_nym` | dłuższa relacja komunikacyjna lub operacyjna | długowieczny, ale wtórny wobec `node-id` |
| `federation_nym` | działanie w konkretnej federacji | ograniczony kontekstem federacji |
| `role_nym` | rola o specjalnym ciężarze (np. panel, wyrocznia) | ograniczony do roli |
| `case_nym` | sprawa, zgłoszenie, panel ad-hoc | jednorazowy / krótkowieczny |
| `transaction_nym` | transakcja, płatność, krótki akt wymiany | efemeryczny |

### 5.5. Reguły

1. `node-id` MUSI mieć jawny rekord pochodzenia: czy jest wywiedziony z
   `anchor-identity`, poświadczony federacyjnie, czy delegowany z innego
   podmiotu odpowiedzialności.

2. Nym MUSI mieć jawny rekord pochodzenia: czy jest wystawiony przez `node-id`,
   delegowany z innego nymu, czy poświadczony federacyjnie.

3. Federacja MOŻE ograniczyć liczbę aktywnych `node-id` lub nymów jednego źródła
   zakotwiczenia w danych klasach ról.

4. `node-id` używany do ról o podwyższonej stawce MUSI mieć poziom pewności
   odpowiedni dla tej roli (sekcja 7).

5. Nym używany do roli o podwyższonej stawce MUSI być delegowany z `node-id`,
   który spełnia próg `IAL` odpowiedni dla tej roli.

6. Reset nymu nie resetuje automatycznie historii odpowiedzialności, jeśli
   zachodzą przesłanki wspólnego źródła zakotwiczenia lub obejścia sankcji.

---

## 6. Stacje, urządzenia i delegacja

Jeden `node-id` może działać przez wiele stacji
sieciowych.

### 6.1. Delegacja stacji

Każda stacja POWINNA mieć:

- własny `station-key`,
- własny `station-id`,
- certyfikat delegacji podpisany przez klucz `node-id` albo uprawniony nym
  delegowany przez `node-id`,
- zakres uprawnień (`scope`),
- czas ważności (`valid_from`, `valid_until`),
- możliwość odwołania.

### 6.2. Zasady

1. Wiele stacji pod jednym `node-id` **nie tworzy wielu niezależnych głosów ani wielu
   niezależnych reputacji**, chyba że odrębna procedura nada im rozdzielną
   podmiotowość.

2. Kompromitacja jednej stacji POWINNA domyślnie prowadzić do odwołania certyfikatu
   tej stacji, a nie do rotacji całego `node-id`, `anchor-identity` ani
   `root-identity`, chyba że istnieją przesłanki szerszego naruszenia.

3. Ślady operacyjne i analiza incydentów MOGĄ być prowadzone na poziomie
   `station-id`, nawet jeśli reputacja główna liczona jest na poziomie `node-id`.

---

## 7. Poziomy pewności tożsamości

### 7.1. Poziomy

| Poziom | Nazwa | Źródło pewności | Dopuszczalny wpływ domyślny |
| :--- | :--- | :--- | :--- |
| `IAL0` | pseudonim niezakotwiczony | brak zewnętrznego poświadczenia | niski; brak ról wysokiego zaufania |
| `IAL1` | pseudonim wspólnotowo zakotwiczony | sponsor / zaproszenie / podstawowe poręczenie | ograniczony udział operacyjny |
| `IAL2` | pseudonim multisig | poręczenie progu `k-of-n` przez węzły z reputacją proceduralną | średni wpływ, role niższego ryzyka |
| `IAL3` | pseudonim silnie zakotwiczony | eID, podpis kwalifikowany, ePUAP, mObywatel lub odpowiednik | wysoki wpływ, większość ról zaufania |
| `IAL4` | pseudonim odpieczętowalny prawnie / konstytucyjnie | silne zakotwiczenie + procedura kontrolowanego ujawnienia | najwyższe role i sprawy najwyższej stawki |

### 7.2. Jurysdykcje i przykłady

W praktyce `IAL3` i `IAL4` mogą być osiągane różnymi drogami:

- **UE / Polska**:
  - mObywatel,
  - ePUAP,
  - podpis kwalifikowany,
  - w przyszłości również europejski Digital ID.

- **Jurysdykcje bez dojrzałej infrastruktury eID**:
  - multisig poświadczeń,
  - federacyjne ceremonie identyfikacyjne,
  - poświadczenia organizacyjne lub zawodowe.

Federacja MUSI dokumentować, jakie mechanizmy mapują się na który poziom `IAL`.

### 7.2.a. Sufit `IAL` zależny od siły poświadczenia

1. Poświadczenie `weak` POWINNO domyślnie kończyć się na `IAL1`, a wyjątkowo na
   `IAL2`, jeśli federacja wprowadzi dodatkowe zabezpieczenia przeciw przejęciu i
   mnożeniu wpływu.

2. Poświadczenie `strong` może odblokowywać `IAL3` i `IAL4`, zgodnie z polityką
   federacyjną i wymogami roli.

3. Upgrade `weak -> strong` NIE POWINIEN tworzyć nowej `anchor-identity`, jeżeli
   użytkownik potrafi jednocześnie:

   - udowodnić kontrolę nad istniejącą kotwicą,

   - dostarczyć nowe mocne poświadczenie.

### 7.3. IAL jako bramka, nie mnożnik

1. `IAL` służy do odblokowywania klas ról, decyzji i uprawnień, a nie do
   liniowego wzmacniania reputacji.

2. Federacja NIE MOŻE używać `IAL` jako mnożnika wyniku reputacyjnego ani jako
   otwartego wzmacniacza siły głosu.

3. Federacja MOŻE przyznać tożsamościom o wyższym `IAL` niewielką, stałą premię
   proceduralną (`fixed_power_bonus`), ale tylko wtedy, gdy:

   - premia jest jawnie opisana,

   - nie przekracza `0.01` (`1%`) całkowitej mocy danego mechanizmu,

   - nie omija progów reputacyjnych ani progów domenowych,

   - może być audytowana i cofnięta.

---

## 8. Zasada: większy wpływ -> większe wymagania

### 8.1. Reguła ogólna

Im większy wpływ danego `node-id` lub nymu na:

- bezpieczeństwo ludzi,
- dane wrażliwe,
- reputację innych,
- decyzje governance,
- środki tymczasowe,
- procedury ujawnienia i odwołań,

tym wyższe MUSZĄ być:

- poziom pewności tożsamości,
- wymóg utrzymywania aktualnego zakotwiczenia,
- możliwość proceduralnego odpieczętowania,
- jakość śladów działania.

### 8.2. Minimalna matryca

| Klasa działania / roli | Minimalny poziom domyślny |
| :--- | :--- |
| zwykła komunikacja i uczestnictwo lokalne | `IAL0` |
| sponsorowanie nowych nymów lub wejść | `IAL1` |
| głos o wadze proceduralnej, operator federacji lokalnej, rola screeningu | `IAL2` |
| panel ad-hoc, wyrocznia, audytor, opiekun sygnalistów, operator danych wrażliwych | `IAL3` |
| role najwyższej stawki z możliwością nieodwracalnej szkody albo z kontrolowanym ujawnieniem tożsamości innych | `IAL4` |

Federacje mogą zaostrzać tę matrycę, ale nie mogą jej rozluźniać dla ról o wysokiej
stawce.

---

## 9. Multisig poręczeń

W środowiskach, gdzie silne państwowe eID nie istnieje albo nie jest bezpieczne,
system MOŻE używać modelu poręczeń.

### 9.1. Minimalny model

Pseudonim osiąga `IAL2`, gdy:

- został poświadczony przez co najmniej `k` z `n` węzłów,
- poręczające węzły mają niezerową reputację proceduralną,
- poręczenia pozostawiają ślad, czas ważności i zakres,
- poręczyciele nie są w oczywistym konflikcie interesów ani w jednej zwartej
  grupie kontrolnej.

### 9.2. Skutek dla poręczycieli

Fałszywe lub rażąco niedbałe poręczenie jest sygnałem proceduralnym obciążającym
poręczycieli. System nie traktuje poręczenia jako gestu symbolicznego, lecz jako
delegację zaufania z konsekwencjami.

---

## 10. Odpieczętowanie i ujawnienie

Tożsamość pierwotna może zostać ujawniona wyłącznie:

- zgodnie z Art. III.9 i Art. X Konstytucji,
- przy wysokiej stawce,
- przez zdefiniowaną procedurę wielo-rolową,
- w zakresie minimalnie koniecznym.

### 10.1. Reguły

1. Sam fakt posiadania root-identity nie oznacza prawa do jej automatycznego
   żądania przez innych uczestników.

2. Ujawnienie root-identity poza torem wewnętrznym wymaga tego samego lub wyższego
   rygoru co ujawnienie odpowiedzialności za ciężkie nadużycie.

3. Panel, audyt albo tryb prawny mogą uzyskać dostęp do tożsamości pierwotnej tylko
   wtedy, gdy bez tego nie da się ochronić ludzi, rozstrzygnąć odpowiedzialności albo
   wykonać obowiązku prawnego.

4. Odpieczętowanie pozostawia osobny ślad audytowy z:
   `reason`, `scope`, `owner`, `legal_basis`, `expiry`.

---

## 11. Model danych

### 11.1. Root identity attestation

```yaml
root_identity_attestation:
  root_attestation_id: "[unikalny identyfikator]"
  subject_type: "human"          # human | organization
  attestation_strength: "strong" # weak | strong
  source_class: "qualified_signature"  # phone | eid | qualified_signature | registry | multisig | other
  assurance_level: "IAL3"
  method: "qualified_signature"  # eidas | mobywatel | epuap | multisig | other
  issuer: "[podmiot lub procedura]"
  issued_at: "[ISO 8601]"
  valid_until: "[ISO 8601]"
  revoke_at: null
  evidence_ref: "[referencja do dowodu lub procedury]"
```

### 11.2. Anchor identity

```yaml
anchor_identity_record:
  anchor_identity_id: "[stabilny identyfikator pochodny]"
  root_attestation_ref: "[referencja]"
  derivation_method: "hash_binding"   # hash_binding | certificate | other
  recovery_record_ref: "[referencja]"
  valid_from: "[ISO 8601]"
  valid_until: "[ISO 8601]"
  revoke_at: null
```

### 11.3. Node identity

```yaml
node_record:
  node_id: "[publiczny identyfikator węzła]"
  node_pubkey: "[klucz publiczny węzła]"
  anchor_identity_ref: "[referencja]"
  assurance_level: "IAL2"
  custodian_ref: "[persistent_nym | procedural_ref]"
  valid_from: "[ISO 8601]"
  valid_until: "[ISO 8601]"
  revoke_at: null
```

### 11.4. Nym

```yaml
nym_record:
  nym_id: "[publiczny identyfikator]"
  nym_pubkey: "[klucz publiczny]"
  node_ref: "[node_id]"
  anchor_identity_ref: "[referencja lub null]"
  assurance_level: "IAL2"
  nym_type: "persistent_nym"
  federation_scope: null
  role_scope: []
  valid_from: "[ISO 8601]"
  valid_until: "[ISO 8601]"
  revoke_at: null
```

### 11.5. Station delegation

```yaml
station_delegation:
  station_id: "[identyfikator stacji]"
  station_pubkey: "[klucz publiczny]"
  delegated_from_node: "[node_id]"
  delegated_from_nym: "[nym_id | null]"
  scope: []
  valid_from: "[ISO 8601]"
  valid_until: "[ISO 8601]"
  revoke_at: null
  delegation_sig: "[podpis nymu lub węzła]"
```

---

## 12. Tryby awarii i środki zaradcze

| Tryb awarii | Środek zaradczy |
| :--- | :--- |
| Mnożenie `node-id` lub nymów z jednego źródła dla zwiększenia wpływu | wpływ i progi liczone względem źródła zakotwiczenia; limity aktywnych `node-id` i nymów dla ról wrażliwych |
| Kradzież jednego urządzenia | odwołanie `station_delegation`; analiza szkody na poziomie `station-id` |
| Fałszywe poręczenia multisig | negatywne sygnały proceduralne dla poręczycieli; cofnięcie poświadczenia |
| Nadużycie żądania ujawnienia | osobny ślad odpieczętowania, wymóg multisig i podstawa prawna / konstytucyjna |
| Brak interoperacyjnego eID | fallback do modelu multisig i federacyjnych poziomów `IAL` |
| Whitewashing przez rotację `node-id` lub nymu | powiązanie przez `anchor-identity` lub wspólne źródło zakotwiczenia; utrzymanie ciągłości odpowiedzialności |

---

## 13. Relacja do innych dokumentów

- **Konstytucja Art. III.1-9**: dokument konkretyzuje ochronę prywatności,
  minimalne ujawnianie i warunki proceduralnego odpieczętowania.
- **Konstytucja Art. VII.4-8**: dokument doprecyzowuje, jak poziom pewności
  tożsamości ogranicza dopuszczalny wpływ i role wysokiej stawki.
- **`PROCEDURAL-REPUTATION-SPEC.pl.md`**: reputacja jest przypisywana głównie do
  `node-id`, lokalnie także do nymów; anty-Sybil może agregować wpływ do poziomu
  wspólnego zakotwiczenia.
- **`FEDERATION-MEMBERSHIP-AND-QUORUM.pl.md`**: wspólna kontrola federacji jest
  analogiczna do wspólnego źródła zakotwiczenia wielu nymów - oba mechanizmy
  ograniczają mnożenie wpływu przez rozszczepienie formalne.
- **`PANEL-SELECTION-PROTOCOL.pl.md`**: kwalifikowalność panelowa dla ról o
  podwyższonej stawce POWINNA opierać się na poziomie `IAL` odpowiednim dla panelu.
- **`ABUSE-DISCLOSURE-PROTOCOL.pl.md`**: procedury ujawnienia i odpieczętowania
  root-identity muszą być zgodne z progami i zasadą minimalnego ujawniania.
- **`IDENTITY-ATTESTATION-AND-RECOVERY.pl.md`**: dokument określa pierwsze
  poświadczenie, pamięć wcześniejszego poświadczenia, frazę odzyskiwania oraz
  zasady rekonstrukcji `anchor-identity`.
- **`IDENTITY-UNSEALING-BOARD.pl.md`**: dokument definiuje Federację Izb
  Pieczęciowych, progi `nym -> node-id` i `node-id -> root-identity` oraz
  wieloizbowe quorum dla pełnego odpieczętowania.
