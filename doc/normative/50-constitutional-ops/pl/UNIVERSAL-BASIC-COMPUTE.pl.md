# Specyfikacja uniwersalnego minimum obliczeniowego DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-UBC-001` |
| `typ` | Ustawa wykonawcza (Poziom 3 hierarchii normatywnej) |
| `wersja` | `0.1.0-draft` |
| `podstawa` | Art. XII.12-14 Konstytucji DIA; `SWARM-ECONOMY-SUFFICIENCY.pl.md`; `ROOT-IDENTITY-AND-NYMS.pl.md`; `IDENTITY-UNSEALING-BOARD.pl.md`; `FIP-MEMBERSHIP-AND-QUORUM.pl.md` |
| `status mechanizmów` | minimalny model PoP, alokacji UBC i rozliczeń jest normatywny; profile limitów konkretyzuje `UBC-LIMIT-PROFILES.pl.md`; uznawanie trans-federacyjne może przebiegać przez federacje albo minimalny most/rejestr `FIP` |

---

## 1. Cel dokumentu

Konstytucja przyznaje zweryfikowanej obecności człowieka w sieci prawo do
nieodbieralnego minimum zasobów obliczeniowych potrzebnych do komunikacji,
orientacji oraz dostępu do trybów ratunkowych i opiekuńczych. Brakuje jednak
dokumentu wykonawczego, który definiuje:

- minimalny model Proof-of-Personhood bez domyślnej deanonimizacji,
- zasady przyznawania `universal_basic_compute`,
- ograniczoną przenośność między federacjami, także przez minimalny most/rejestr `FIP`,
- minimalny ślad finansowania i rozliczania tego minimum.

Niniejszy dokument operacjonalizuje te obowiązki.

---

## 2. Zasada ogólna

1. `Universal Basic Compute` (`UBC`) jest progiem uczestnictwa i ochrony, a nie
   nagrodą za status, reputację ani kapitał.
2. Brak bieżącego wkładu reputacyjnego lub ekonomicznego NIE MOŻE sam przez się
   odcinać człowieka od podstawowej zdolności do komunikacji z rojem, orientacji
   w sytuacji oraz korzystania z trybów ratunkowych i opiekuńczych.
3. Dostęp do `UBC` i jego trybów ochronnych NIE MOŻE być warunkowany upokorzeniem,
   uniżeniem, zależnością emocjonalną ani arbitralną łaską operatora.
4. Kwalifikacja do `UBC` opiera się na konstytucyjnie dopuszczalnym
   `Proof-of-Personhood`, domyślnie bez pełnej deanonimizacji.
5. Federacja lokalna MOŻE przyznawać szerszy zakres `UBC`, ale nie może zejść
   poniżej minimum określonego w tym dokumencie.
6. Uznawanie `Proof-of-Personhood` między federacjami jest domyślnie ograniczone i
   może odbywać się przez federacje albo minimalny most/rejestr `FIP`:
   - tryby ratunkowe MUSZĄ być dostępne bez limitu,
   - komunikacja MUSI być dostępna w profilu limitowanym,
   - tryby pomocowe MUSZĄ być dostępne w profilu limitowanym.
7. Federacje MOGĄ rozszerzać uznawanie trans-federacyjne i podnosić limity, a most
   `FIP` MOŻE gwarantować wyłącznie minimalny profil przenośności; żadna z tych
   ścieżek nie może zejść poniżej powyższego minimum.
8. `UBC` nie może być używane jako ukryta ścieżka do przewagi ustrojowej,
   priorytetowego routingu wysokiej stawki ani obejścia wymagań reputacyjnych.

---

## 3. Pojęcia podstawowe

| Pojęcie | Znaczenie |
| :--- | :--- |
| `proof_of_personhood_attestation` | poświadczenie, że dany podmiot odpowiada jednej zweryfikowanej osobie, bez konieczności publicznego ujawnienia tożsamości pierwotnej |
| `ubc_allocation` | przydział minimalnych zasobów obliczeniowych i odpowiadających im trybów dostępu |
| `ubc_settlement` | okresowy rekord finansowania i rozliczenia `UBC` w federacji |
| `portability_profile` | profil określający, jaki zakres `UBC` jest honorowany lokalnie i trans-federacyjnie |
| `limited_communication` | profil komunikacyjny z jawnymi limitami wolumenu, częstotliwości lub przepływu |
| `limited_care` | profil trybów pomocowych z jawnymi limitami wolumenu lub częstotliwości |
| `emergency_unlimited` | brak limitu dla trybów ratunkowych przy ważnym `proof_of_personhood_attestation` |
| `fip_pop_bridge` | minimalny rejestr/most `FIP` uznający trans-federacyjne PoP dla potrzeb minimalnego profilu `UBC` |

`Proof-of-Personhood` może być realizowany między innymi przez:

- kryptograficzne poręczenia multisig bez deanonimizacji,
- poświadczenia federacyjne,
- mechanizmy uznawane przez Federację Izb Pieczęciowych,
- hybrydy funkcjonalnie równoważne.

---

## 4. Minimalny model danych

### 4.1. `proof_of_personhood_attestation`

```yaml
proof_of_personhood_attestation:
  attestation_id: "[unikalny identyfikator]"
  subject_ref: "[stabilny anonimowy uchwyt osoby]"
  issuer_scope: "federation" # federation | fip_bridge | hybrid
  issuer_ref: "[federacja lub most FIP]"
  issuer_federation_id: "[federacja wystawiająca lub uznająca]"
  bridge_ref: "[opcjonalna referencja do mostu FIP]"
  attestation_method: "cryptographic_vouching" # cryptographic_vouching | federation_attestation | sealed_chambers_recognition | fip_bridge_recognition | hybrid
  assurance_scope: "proof_of_personhood"
  deanon_not_required: true
  uniqueness_scope: "federation" # federation | trans_federation_limited | trans_federation_extended
  valid_from: "[timestamp]"
  valid_until: "[timestamp]"
  portability_profile:
    trans_federation_default:
      emergency: "unlimited"
      communication: "limited"
      care: "limited"
    bridge_minimum_supported: true
    federation_extension_allowed: true
  evidence_ref: "[referencja do pakietu dowodowego lub procedury]"
  revocation_ref: "[opcjonalna referencja do procedury cofnięcia]"
```

### 4.2. `ubc_allocation`

```yaml
ubc_allocation:
  allocation_id: "[unikalny identyfikator]"
  subject_ref: "[stabilny anonimowy uchwyt osoby]"
  federation_id: "[federacja przydzielająca]"
  attestation_ref: "[proof_of_personhood_attestation]"
  recognition_source: "federation_local" # federation_local | federation_cross_recognition | fip_bridge
  recognition_ref: "[federacja uznająca albo most FIP]"
  measurement_period: "P30D"
  valid_from: "[timestamp]"
  valid_until: "[timestamp]"
  compute_unit: "[compute_credit / second / tokenized_quota / inna jednostka]"
  portability_scope: "trans_federation_limited" # local | trans_federation_limited | trans_federation_extended
  guaranteed_modes:
    emergency:
      access: true
      limit_profile: "unlimited"
    communication:
      access: true
      limit_profile: "limited"
      limit_ref: "[profil limitów]"
    care:
      access: true
      limit_profile: "limited"
      limit_ref: "[profil limitów]"
  funding_policy_ref: "DIA-UBC-001"
  limit_policy_ref: "DIA-UBC-LIMITS-001"
  policy_annotations: {}
  created_at: "[timestamp]"
```

### 4.3. `ubc_settlement`

```yaml
ubc_settlement:
  settlement_id: "[unikalny identyfikator]"
  federation_id: "[federacja]"
  period_start: "[timestamp]"
  period_end: "[timestamp]"
  compute_unit: "[jednostka]"
  beneficiary_count: 0
  total_allocated_compute: 0
  funding_sources:
    - source_class: "business_nodes" # business_nodes | high_margin_instances | surplus_recirculation | voluntary_operator_surplus | federation_reserve
      amount: 0
    - source_class: "surplus_recirculation"
      amount: 0
  emergency_usage: 0
  communication_usage: 0
  care_usage: 0
  policy_ref: "DIA-UBC-001"
  created_at: "[timestamp]"
```

---

## 5. Kwalifikacja do `UBC`

1. Minimalnym warunkiem kwalifikacji jest ważne `proof_of_personhood_attestation`.
2. Federacja NIE MOŻE wymagać pełnej deanonimizacji jako warunku zwykłego wejścia do
   `UBC`, chyba że zachodzi konstytucyjny wyjątek zgodny z odpowiednią procedurą.
3. Federacja MOŻE wymagać okresowego odświeżania poświadczenia, ale nie może używać
   tej procedury jako ukrytego narzędzia wykluczania ubogich, słabszych lub
   czasowo nieaktywnych operatorów.
4. Procedura wejścia, odświeżania lub review NIE MOŻE wymagać upokorzenia,
   uniżenia, zależności emocjonalnej ani osobistego zadowolenia gatekeepera jako
   warunku dostępu.
5. `UBC` nie zależy od salda nagród, pozycji reputacyjnej ani aktywności
   komercyjnej, choć federacja może warunkować rozszerzone limity dodatkowymi
   kryteriami.

---

## 6. Ograniczona trans-federacyjność

### 6.1. Minimum obowiązkowe

Jeżeli federacja albo most/rejestr `FIP` uznaje trans-federacyjne
`proof_of_personhood_attestation`, musi zapewnić co najmniej:

1. nieograniczony dostęp do trybów ratunkowych,
2. limitowany dostęp do komunikacji,
3. limitowany dostęp do trybów pomocowych.

### 6.2. Zakaz degradacji ratunku

Tryb ratunkowy NIE MOŻE być objęty limitem wolumenu, który praktycznie uniemożliwia
wezwanie pomocy, zgłoszenie przemocy, zagrożenia życia, ciężkiego nadużycia albo
utraty bezpieczeństwa podstawowego.

### 6.3. Rozszerzenia federacyjne

Federacja może:

1. podnosić limity komunikacyjne,
2. podnosić limity pomocowe,
3. uznawać szerszą klasę poświadczeń trans-federacyjnych,
4. dodawać lokalne tryby opiekuńcze,

o ile pozostawia ślad polityki i nie osłabia minimum z punktów 6.1-6.2.

Most/rejestr `FIP`:

1. MOŻE uznawać trans-federacyjne `Proof-of-Personhood` dla celów minimalnego profilu,
2. NIE MOŻE samodzielnie obniżać limitów poniżej minimum,
3. NIE POWINIEN przyznawać profilu szerszego niż `bridge_minimum`, chyba że działa
   na podstawie jawnego rozszerzenia federacyjnego.

---

## 7. Finansowanie

1. `UBC` MUSI mieć jawny model składkowy.
2. Minimalny katalog źródeł finansowania obejmuje:
   - `business_nodes`,
   - `high_margin_instances`,
   - `surplus_recirculation`,
   - `voluntary_operator_surplus`.
3. Federacja MOŻE dodać inne źródła, ale nie może ukrywać ich poza audytem.
4. Finansowanie `UBC` nie może być uzależnione wyłącznie od dobrowolnych darów,
   jeżeli federacja deklaruje konstytucyjne minimum.

---

## 8. Testy zgodności

System nie spełnia tej polityki, jeżeli:

1. wymaga pełnej deanonimizacji jako zwykłego warunku wejścia do `UBC`,
2. odcina osobę z ważnym `Proof-of-Personhood` od trybów ratunkowych,
3. nie pozostawia śladu `ubc_allocation` albo `ubc_settlement`,
4. warunkuje dostęp upokorzeniem, uniżeniem, zależnością emocjonalną albo
   arbitralną łaską operatora,
5. uzależnia podstawowy przydział od reputacji, salda lub pozycji kapitałowej,
6. używa `UBC` jako ukrytego kanału kupowania przewagi proceduralnej,
7. uznaje trans-federacyjne PoP tylko deklaratywnie, bez realnego minimum
   komunikacyjnego i pomocowego.

---

## 9. Relacja do innych dokumentów

- **Konstytucja Art. XII.12-14**: PoP, nieodbieralne minimum compute i zakaz ukrytej przewagi.
- **`SWARM-ECONOMY-SUFFICIENCY.pl.md`**: wspólny model finansowania, nadwyżek i hamulców koncentracji.
- **`ROOT-IDENTITY-AND-NYMS.pl.md`**: warstwa zakotwiczenia tożsamości bez domyślnej jawności.
- **`IDENTITY-UNSEALING-BOARD.pl.md`**: federacyjnie uznawane mechanizmy silnego potwierdzenia bez pełnej publikacji tożsamości.
- **`FIP-MEMBERSHIP-AND-QUORUM.pl.md`**: minimalna struktura i odpowiedzialność wyspecjalizowanej federacji `FIP`.
- **`UBC-LIMIT-PROFILES.pl.md`**: kanoniczne profile limitów i przenośności dla `UBC`.
