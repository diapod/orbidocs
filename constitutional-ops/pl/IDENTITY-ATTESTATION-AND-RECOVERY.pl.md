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
- aktualizację danych tożsamościowych i odwoływanie.

Celem jest połączenie trzech własności:

- silnego zakotwiczenia w tożsamości pierwotnej,
- możliwości odzyskania tożsamości pochodnej bez ponownego przechodzenia pełnego
  onboardingu,
- minimalizacji przechowywania danych cywilnych w infrastrukturze roju.

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
    memory_cost: 65536
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

### 8.1. Procedura

1. Użytkownik inicjuje `identity_update`.

2. System łączy:

   - starą `anchor-identity`,

   - nowy zestaw `normalized_claims`,

   - ważne lub odświeżone poświadczenie.

3. Powstaje:

   - nowy rekord pamięci poświadczenia,

   - ślad migracji,

   - zachowanie ciągłości odpowiedzialności i reputacji.

### 8.2. Zasada

Zmiana danych cywilnych nie może być traktowana ani jako automatyczne wyzerowanie
reputacji, ani jako wystarczająca podstawa do utworzenia nowego, niespowiązanego
`anchor-identity`.

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

---

## 10. Model danych

### 10.1. Parametry KDF

```yaml
kdf_params_record:
  kdf_params_id: "[identyfikator]"
  algorithm: "argon2id"
  memory_cost: 65536
  time_cost: 3
  parallelism: 1
  output_length: 32
  created_at: "[ISO 8601]"
```

### 10.2. Rekord `salt`

```yaml
salt_record:
  salt_id: "[identyfikator]"
  salt_value: "[losowe bajty kodowane]"
  created_at: "[ISO 8601]"
  rotate_at: null
```

### 10.3. Rekord odzyskiwania

```yaml
identity_recovery_record:
  recovery_record_id: "[identyfikator]"
  anchor_identity_ref: "[referencja]"
  lookup_tag: "[znacznik wyszukiwania]"
  salt_ref: "[referencja]"
  kdf_params_ref: "[referencja]"
  attestation_id: "[referencja]"
  recovery_status: "enabled"      # enabled | suspended | revoked
  last_recovered_at: null
  last_recovery_channel: null
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
