# Poświadczenie i odzyskiwanie tożsamości w DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-ID-REC-001` |
| `typ` | Ustawa wykonawcza (Poziom 3 hierarchii normatywnej) |
| `wersja` | 0.1.0-draft |
| `podstawa` | Art. III.1-9, VII.4-8, XVI Konstytucji DIA; `ROOT-IDENTITY-AND-NYMS.pl.md` |
| `status mechanizmów` | model przepływu i danych jest normatywny; dobór KDF i parametrów pozostaje wdrożeniowy |

---

## 1. Cel dokumentu

Dokument definiuje:

- pierwsze poświadczenie `root-identity`,
- wytworzenie `anchor-identity`,
- rolę frazy odzyskiwania,
- rolę `salt` i parametrów KDF,
- pamięć wcześniejszego poświadczenia,
- odzyskiwanie i odtwarzanie `anchor-identity`,
- aktualizację danych tożsamościowych,
- klasy kompromitacji, odwoływanie i rotację,
- minimalne profile KDF i politykę migracji parametrów.

Celem jest połączenie trzech własności:

- silnego zakotwiczenia w tożsamości pierwotnej,
- możliwości odzyskania tożsamości pochodnej bez ponownego przechodzenia pełnego
  onboardingu,
- minimalizacji przechowywania danych cywilnych w infrastrukturze roju.

Dokument zakłada, że jedna `anchor-identity` może mieć wiele następujących po
sobie albo współistniejących rekordów poświadczenia, o różnej sile (`weak` /
`strong`), bez zrywania ciągłości tożsamości.

---

## 2. Zasady podstawowe

1. `anchor-identity` MUSI być wywodzona z:

   - znormalizowanych danych tożsamościowych użytych przy pierwszym poświadczeniu,

   - sekretu odzyskiwania wyprowadzanego z frazy słów,

   - losowego `salt`,

   - jawnych parametrów KDF.

2. `salt` **nie jest sekretem**. Ma różnicować wyprowadzenie i chronić przed
   prekomputacją. System POWINIEN przechowywać go samodzielnie, tak aby użytkownik
   nie musiał go pamiętać.

3. Fraza odzyskiwania jest sekretem użytkownika. System NIE MOŻE przechowywać jej
   wprost ani w postaci odwracalnej.

4. Po poprawnym pierwszym poświadczeniu system POWINIEN pamiętać, że dana
   `anchor-identity` została już zakotwiczona metodą o określonym poziomie `IAL`.
   Późniejsze odzyskiwanie NIE MUSI wymagać ponownego użycia `DigitalID`,
   `mObywatel`, podpisu kwalifikowanego ani vouchingu, o ile ciągłość
   kryptograficzna i status poświadczenia pozostają ważne.

5. System NIE POWINIEN przechowywać pełnych danych cywilnych, jeżeli wystarcza:

   - referencja do poświadczenia,

   - `lookup_tag`,

   - `salt`,

   - parametry KDF,

   - status ważności i poziom `IAL`.

6. Upgrade `weak -> strong` POWINIEN podnosić siłę i maksymalny `IAL`
   istniejącej `anchor-identity`, a nie tworzyć nową kotwicę, o ile użytkownik
   udowodni kontrolę nad dotychczasową kotwicą i dostarczy nowe poświadczenie
   mocne.

---

## 3. Model pojęciowy

### 3.1. Przepływ

```text
root-identity claims
  + recovery phrase
  + salt
  + kdf_params
    -> recovery_secret
    -> anchor-identity
      -> node-id
```

### 3.2. Rozróżnienie ról

| Element | Charakter | Kto przechowuje |
| :--- | :--- | :--- |
| `root-identity claims` | dane wejściowe do poświadczenia | użytkownik / urząd poświadczający |
| `recovery phrase` | sekret użytkownika | użytkownik |
| `salt` | parametr różnicujący, niesekretny | system, opcjonalnie użytkownik |
| `kdf_params` | jawny parametr bezpieczeństwa | system |
| `lookup_tag` | znacznik wyszukiwania rekordu | system |
| `anchor-identity` | stabilna tożsamość pochodna | system |

### 3.3. Rola `salt`

`salt`:

- nie jest hasłem ani drugim sekretem,
- nie daje sam w sobie możliwości rekonstrukcji,
- jest potrzebny przy odtwarzaniu `anchor-identity`,
- POWINIEN być przechowywany w rekordzie systemowym,
- MOŻE być również eksportowany użytkownikowi jako element pakietu odzyskiwania.

Zasada praktyczna jest prosta: użytkownik **nie musi** przechowywać `salt`, ale
**może** to zrobić dla niezależnego backupu.

---

## 4. Pierwsze poświadczenie

### 4.1. Wejście

Przy pierwszym poświadczeniu użytkownik dostarcza:

- dane wymagane przez wybraną metodę poświadczenia,
- materiał potrzebny do normalizacji claimów tożsamości,
- lokalnie wygenerowaną frazę odzyskiwania albo zgodę na jej wygenerowanie przez
  klienta,
- opcjonalne dane pomocnicze do eksportu pakietu odzyskiwania.

### 4.2. Kroki

1. System lub klient normalizuje dane wejściowe do postaci `normalized_claims`.

2. Generowany jest losowy `salt`.

3. Z frazy odzyskiwania wyprowadzany jest `recovery_secret`.

4. Wyliczana jest `anchor-identity`:

   - przez KDF odporny na zgadywanie i kosztowny obliczeniowo,

   - z wejścia `normalized_claims + recovery_secret + salt + kdf_params`.

5. Tworzony jest rekord poświadczenia i rekord `anchor-identity`.

6. Użytkownik dostaje opcjonalny pakiet odzyskiwania.

### 4.3. Efekt

Po sukcesie system pamięta:

- że dla tej `anchor-identity` wykonano już poświadczenie,
- jaką metodą,
- z jakim poziomem `IAL`,
- do kiedy poświadczenie jest ważne,
- czy wymaga ponowienia.

---

## 5. Pamięć poświadczenia

System utrzymuje pamięć wcześniejszego poświadczenia w postaci rekordu
odwołującego się do `anchor-identity`, a nie do samych danych cywilnych.

### 5.1. Rekord pamięci poświadczenia

```yaml
identity_attestation_memory:
  attestation_id: "[unikalny identyfikator]"
  anchor_identity_ref: "[referencja]"
  lookup_tag: "[znacznik wyszukiwania]"
  lookup_domain: "person:v1"
  pepper_id: "[identyfikator lub null]"
  attestation_strength: "strong" # weak | strong
  source_class: "mobywatel"      # phone | eid | qualified_signature | registry | multisig | other
  assurance_level: "IAL3"
  method: "mobywatel"        # mobywatel | epuap | qualified_signature | multisig | other
  status: "valid"            # valid | expired | revoked | superseded
  issued_at: "[ISO 8601]"
  valid_until: "[ISO 8601]"
  evidence_ref: "[referencja do dowodu]"
  salt_ref: "[referencja do salt]"
  kdf_params_ref: "[referencja do parametrów]"
```

### 5.2. `lookup_tag`

`lookup_tag` służy do odnajdywania właściwego rekordu bez przechowywania pełnych
danych cywilnych jako klucza wyszukiwania.

Powinien być wyliczany z:

- `normalized_claims`,
- opcjonalnego lokalnego `pepper` federacji albo domeny,
- jawnego algorytmu haszującego.

`lookup_tag` nie powinien sam z siebie umożliwiać łatwej korelacji między
federacjami.

### 5.3. Kontrakt `lookup_tag`

`lookup_tag` POWINIEN być liczony według kontraktu:

```text
lookup_tag = H(
  lookup_domain
  || canonical(normalized_lookup_claims)
  || pepper_or_empty
)
```

Gdzie:

- `lookup_domain` odróżnia klasy rekordów i zastosowania,
- `normalized_lookup_claims` to tylko minimalny podzbiór claimów potrzebnych do
  odnalezienia rekordu,
- `pepper_or_empty` to federacyjny lub domenowy `pepper`, jeśli jest używany.

`normalized_lookup_claims` NIE POWINNY obejmować nadmiarowych danych
cywilnych. W szczególności:

- dla osoby fizycznej powinny obejmować wyłącznie minimalny stabilny zestaw
  claimów użyty przy pierwszym poświadczeniu,
- dla organizacji powinny obejmować minimalny zestaw danych rejestrowych lub
  organizacyjnych.

### 5.4. `pepper`

Federacja MOŻE stosować `pepper`, aby ograniczyć korelację `lookup_tag` między
federacjami albo domenami. Jeżeli `pepper` jest stosowany:

1. MUSI być przechowywany jako sekret systemowy poza rekordem użytkownika.

2. MUSI mieć własny `pepper_id` i okres ważności.

3. NIE MOŻE być eksportowany razem z pakietem odzyskiwania.

4. Zmiana `pepper` MUSI uruchamiać reindeksację `lookup_tag` albo okres
   przejściowy, w którym uznawane są co najmniej dwie wersje `pepper`.

5. Surowy `lookup_tag` NIE POWINIEN być przenoszony między federacjami jako
   artefakt interoperacyjny.

---

## 6. Odzyskiwanie

### 6.1. Minimalne wejście użytkownika

Do odzyskania `anchor-identity` użytkownik podaje:

- te same lub semantycznie równoważne dane tożsamościowe, które były użyte przy
  pierwszym poświadczeniu,
- frazę odzyskiwania.

Użytkownik nie musi podawać `salt`, jeśli system zachował rekord pamięci
poświadczenia.

### 6.2. Kroki odzyskiwania

1. System normalizuje wejście do `normalized_claims`.

2. System wylicza `lookup_tag` i znajduje rekord pamięci.

3. System pobiera `salt` i `kdf_params`.

4. Z frazy użytkownika wyliczany jest `recovery_secret`.

5. Odtwarzana jest `anchor-identity`.

6. System porównuje wynik z zapisanym rekordem.

7. Jeżeli rekord poświadczenia pozostaje ważny, użytkownik odzyskuje ciągłość
   bez ponownego pełnego poświadczenia `root-identity`.

### 6.3. Kiedy wymagane jest ponowne poświadczenie

Ponowne poświadczenie jest wymagane, gdy:

- rekord ma status `expired` albo `revoked`,
- istnieje spór co do integralności wcześniejszego poświadczenia,
- polityka federacji wymaga odświeżenia `IAL3` lub `IAL4`,
- odzyskiwanie dotyczy roli, dla której wymagany jest świeży dowód zakotwiczenia.

---

## 7. Pakiet odzyskiwania

System POWINIEN umożliwiać użytkownikowi eksport pakietu odzyskiwania, ale nie
może go wymagać jako jedynego sposobu odtworzenia.

### 7.1. Minimalna zawartość

```yaml
recovery_bundle:
  anchor_hint: "[krótka wskazówka identyfikująca rekord]"
  salt: "[salt]"
  kdf_params:
    algorithm: "argon2id"
    memory_cost: 262144
    time_cost: 3
    parallelism: 1
  attestation_id: "[referencja]"
  issued_at: "[ISO 8601]"
```

### 7.2. Zasady

1. Pakiet odzyskiwania NIE zawiera frazy odzyskiwania.

2. Utrata pakietu nie może sama z siebie uniemożliwiać odzyskania, jeśli system
   zachował rekord pamięci.

3. Posiadanie pakietu bez frazy i bez poprawnych claimów tożsamościowych nie daje
   prawa do przejęcia tożsamości.

---

## 8. Aktualizacja danych tożsamościowych

Zmiana danych cywilnych, takich jak nazwisko, nazwa organizacji albo numer
rejestrowy, nie powinna automatycznie niszczyć ciągłości tożsamości.

### 8.0. Upgrade siły poświadczenia

System POWINIEN dopuszczać przejście z poświadczenia `weak` do `strong` bez
rotacji `anchor-identity`, `node-id` i `persistent_nym`, jeśli spełnione są
jednocześnie:

- kontrola nad istniejącą kotwicą albo nad `node-id` wywiedzionym z tej kotwicy,

- nowe poświadczenie `strong`,

- brak twardych sygnałów przejęcia lub sporu co do tożsamości.

Jeżeli upgrade zaczyna się z `source_class = phone`, federacja POWINNA dodatkowo
wymagać:

- upływu `phone_upgrade_cooldown` od pierwszego poświadczenia albo ostatniej
  istotnej zmiany tożsamościowej,

- braku aktywnego recovery albo świeżego resetu kluczy,

- kontroli churnu stacji, nymów i urządzeń,

- kontroli anomalii geograficznych, sieciowych albo behawioralnych, jeśli takie
  sygnały są dostępne,

- manualnego review, gdy wynik upgrade miałby odblokować role `IAL3+`.

### 8.1. Procedura

1. Użytkownik inicjuje `identity_update`.

2. System łączy:

   - starą `anchor-identity`,

   - nowy zestaw `normalized_claims`,

   - ważne lub odświeżone poświadczenie.

3. Powstaje:

   - nowy rekord pamięci poświadczenia,

   - ewentualne oznaczenie poprzedniego poświadczenia jako `superseded`,

   - ślad migracji,

   - zachowanie ciągłości odpowiedzialności i reputacji.

### 8.2. Zasada

Zmiana danych cywilnych nie może być traktowana ani jako automatyczne wyzerowanie
reputacji, ani jako wystarczająca podstawa do utworzenia nowego, niespowiązanego
`anchor-identity`.

### 8.3. Skutek upgrade `weak -> strong`

1. `anchor-identity` pozostaje ta sama.

2. `node-id` i `persistent_nym` mogą pozostać bez zmian.

3. Efemeryczne nymy, certyfikaty stacji i materiały sesyjne MOGĄ zostać
   odświeżone tak, aby dalsza komunikacja odwoływała się już do mocniejszego
   zakotwiczenia.

4. Historia wcześniejszego poświadczenia `weak` pozostaje w łańcuchu audytowym.

---

## 9. Odwołanie i kompromitacja

### 9.1. Odwołanie

Rekord poświadczenia albo rekord `anchor-identity` może zostać odwołany, gdy:

- stwierdzono fałszywe poświadczenie,
- stwierdzono kradzież lub przejęcie frazy odzyskiwania,
- istnieje twardy dowód nadużycia toru odzyskiwania,
- wymaga tego prawomocna procedura konstytucyjna lub prawna.

### 9.2. Skutek

Odwołanie może powodować:

- obniżenie `IAL`,
- czasowe zawieszenie `node-id`,
- wymóg świeżego poświadczenia,
- rotację nymów i stacji,
- uruchomienie procedury incydentowej.

### 9.3. Klasy kompromitacji

| Klasa | Opis | Minimalna reakcja |
| :--- | :--- | :--- |
| `C1` | Podejrzenie utraty poufności frazy odzyskiwania bez twardego dowodu | zawieszenie toru odzyskiwania, wzmożony monitoring, dodatkowa weryfikacja |
| `C2` | Twardy dowód przejęcia frazy odzyskiwania lub `recovery_secret` | odwołanie toru odzyskiwania, rotacja `anchor-identity`, przegląd powiązanych `node-id` |
| `C3` | Kompromitacja tylko `node-key` lub głównego klucza `node-id` | rotacja `node-id`, nymów i stacji; `anchor-identity` może pozostać |
| `C4` | Kompromitacja jednej lub wielu stacji bez oznak naruszenia wyżej | odwołanie `station_delegation`, analiza szkody, brak automatycznej rotacji `anchor-identity` |
| `C5` | Fałszywe poświadczenie `root-identity` albo błąd w kanale poświadczającym | odwołanie poświadczenia, obniżenie `IAL`, możliwe unieważnienie `anchor-identity` |
| `C6` | Nadużycie procedury odzyskiwania albo obejście progów odpieczętowania | zawieszenie toru odzyskiwania, audyt, możliwe sankcje proceduralne i prawne |

### 9.4. Macierz rotacji

1. Kompromitacja stacji (`C4`) nie powinna sama z siebie wymuszać rotacji
   `node-id` ani `anchor-identity`.

2. Kompromitacja `node-key` (`C3`) POWINNA prowadzić do:

   - nowego `node-id`,

   - rotacji aktywnych nymów,

   - odnowienia certyfikatów stacji,

   - zachowania ciągłości odpowiedzialności przez wspólną `anchor-identity`.

3. Kompromitacja frazy odzyskiwania (`C2`) POWINNA prowadzić do:

   - odwołania starego toru odzyskiwania,

   - wygenerowania nowej frazy,

   - nowego `salt`,

   - nowej `anchor-identity`,

   - kontrolowanego przepięcia aktywnych `node-id` albo ich rotacji zgodnie z
     polityką federacji.

4. Fałszywe poświadczenie albo kompromitacja kanału poświadczającego (`C5`)
   POWINNY być traktowane jak naruszenie warstwy zakotwiczenia i mogą wymagać:

   - pełnego ponownego poświadczenia,

   - zamrożenia ról wysokiej stawki,

   - unieważnienia pochodnych `node-id`.

5. Każda rotacja MUSI zostawić ślad łączący starą i nową warstwę tożsamości na
   torze audytowym, ale NIE MUSI tworzyć publicznej korelacji między starą i nową
   maską operacyjną.

---

## 10. Model danych

### 10.1. Minimalne profile KDF

Domyślnym algorytmem POWINIEN być `argon2id`.

| Profil | Zastosowanie minimalne | `memory_cost` | `time_cost` | `parallelism` |
| :--- | :--- | :--- | :--- | :--- |
| `KDF-S` | niski koszt, urządzenia ograniczone, brak ról wysokiej stawki | `65536` | `3` | `1` |
| `KDF-M` | profil domyślny dla większości użytkowników i `IAL2-IAL3` | `262144` | `3` | `1` |
| `KDF-H` | role wysokiej stawki, `IAL4`, odzyskiwanie uprzywilejowane | `524288` | `4` | `1` |

Federacja MOŻE podnosić te minima, ale nie może schodzić poniżej nich dla
danego profilu.

### 10.2. Polityka migracji parametrów KDF

1. Rekord KDF MUSI być wersjonowany.

2. System MUSI umieć zweryfikować starszy profil przez okres migracyjny.

3. Podniesienie profilu KDF POWINNO następować:

   - przy udanym odzyskaniu,

   - przy istotnej zmianie roli lub poziomu `IAL`,

   - przy planowej migracji bezpieczeństwa federacji.

4. System NIE MOŻE automatycznie obniżać profilu KDF dla już istniejącej
   tożsamości.

5. Jeżeli rekord ma profil słabszy niż wymagany dla aktualnej roli, federacja
   POWINNA wymusić migrację przed dopuszczeniem do tej roli.

6. Migracja KDF NIE POWINNA sama z siebie zmieniać `anchor-identity`, o ile nie
   zmieniają się `normalized_claims`, fraza odzyskiwania albo `salt`.

### 10.3. Parametry KDF

```yaml
kdf_params_record:
  kdf_params_id: "[identyfikator]"
  profile: "KDF-M"
  version: 1
  algorithm: "argon2id"
  memory_cost: 262144
  time_cost: 3
  parallelism: 1
  output_length: 32
  created_at: "[ISO 8601]"
```

### 10.4. Rekord `pepper`

```yaml
pepper_record:
  pepper_id: "[identyfikator]"
  scope: "federation"        # federation | domain
  status: "active"           # active | grace | retired
  valid_from: "[ISO 8601]"
  valid_until: null
```

### 10.5. Rekord `salt`

```yaml
salt_record:
  salt_id: "[identyfikator]"
  salt_value: "[losowe bajty kodowane]"
  created_at: "[ISO 8601]"
  rotate_at: null
```

### 10.6. Rekord odzyskiwania

```yaml
identity_recovery_record:
  recovery_record_id: "[identyfikator]"
  anchor_identity_ref: "[referencja]"
  lookup_tag: "[znacznik wyszukiwania]"
  lookup_domain: "person:v1"
  pepper_id: "[identyfikator lub null]"
  salt_ref: "[referencja]"
  kdf_params_ref: "[referencja]"
  attestation_id: "[referencja]"
  recovery_status: "enabled"      # enabled | suspended | revoked
  last_recovered_at: null
  last_recovery_channel: null
```

### 10.7. Rekord łańcucha poświadczeń

```yaml
attestation_chain_record:
  chain_id: "[identyfikator]"
  anchor_identity_ref: "[referencja]"
  current_attestation_id: "[referencja]"
  prior_attestation_ids:
    - "[referencja]"
  strongest_attestation_strength: "strong" # weak | strong
  current_max_ial: "IAL3"
  continuity_proof_ref: "[dowód kontroli nad dotychczasową kotwicą]"
  upgrade_cooldown_profile: "phone-default-14d"
  anomaly_check_ref: "[referencja lub null]"
  updated_at: "[ISO 8601]"
```

---

## 11. Relacja do innych dokumentów

- **`ROOT-IDENTITY-AND-NYMS.pl.md`**: dokument definiuje warstwy tożsamości; ten
  akt doprecyzowuje, jak powstaje i jak jest odzyskiwana `anchor-identity`.
- **`PANEL-SELECTION-PROTOCOL.pl.md`**: audyt i panel mogą korzystać z
  `custodian_ref`, a zejście do `root-identity` wymaga toru odpieczętowania.
- **`ABUSE-DISCLOSURE-PROTOCOL.pl.md`**: ujawnienie tożsamości pierwotnej musi
  respektować zasadę minimalnego ujawniania i wysokiej stawki.
- **`PROCEDURAL-REPUTATION-SPEC.pl.md`**: kwalifikowalność wysokiej stawki zależy
  od ważności pamięci poświadczenia i bieżącego `IAL`.
- **`ATTESTATION-PROVIDERS.pl.md`**: dokument mapuje metody poświadczenia na
  klasy `weak` / `strong`, maksymalne `IAL` i ograniczenia operacyjne.
