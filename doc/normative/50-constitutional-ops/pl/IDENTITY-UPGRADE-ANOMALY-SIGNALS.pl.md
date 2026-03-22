# Sygnały anomalii przy upgrade tożsamości w DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-ID-UPGRADE-ANOM-001` |
| `typ` | Ustawa wykonawcza / sygnały i review |
| `wersja` | 0.1.0-draft |
| `data` | 2026-03-12 |

---

## 1. Cel dokumentu

Niniejszy dokument definiuje minimalny katalog sygnałów anomalii dla upgrade
poświadczenia, w szczególności `phone -> strong`, tak aby federacje mogły
wykrywać przejęcie, pranie tożsamości i obejście progów odpowiedzialności.

---

## 2. Zasada ogólna

Upgrade tożsamości nie jest tylko zmianą pola w rekordzie. Jest zmianą jakości
zakotwiczenia, która może odblokować role i uprawnienia o wyższej stawce.
Dlatego upgrade musi być traktowany jako operacja ryzykowna i objęta kontrolą
anomalii.

---

## 3. Klasy sygnałów

| Kod | Klasa | Przykład | Minimalna reakcja |
| :--- | :--- | :--- | :--- |
| `A1` | churn urządzeń / stacji | nagła rotacja wielu `station-id` lub nymów | wzmożony monitoring |
| `A2` | świeże recovery | niedawne użycie toru odzyskiwania przed upgradem | soft hold albo manual review |
| `A3` | reset kluczy | świeża zmiana `node-key` lub kluczy stacji | manual review |
| `A4` | anomalia geograficzna | wzorzec aktywności z odległych lokalizacji w krótkim czasie | soft hold albo manual review |
| `A5` | anomalia sieciowa | nietypowa zmiana ASN, sieci, proxy lub kanału | wzmożony monitoring |
| `A6` | spór tożsamościowy | aktywna sprawa, odwołanie albo sygnał przejęcia | blokada upgrade do wyjaśnienia |
| `A7` | churn źródła poświadczenia | świeża zmiana numeru telefonu albo źródła `weak` | cooldown restart lub manual review |
| `A8` | sygnał nadużycia | otwarty incydent, obejście sankcji, fałszywe poręczenie | blokada upgrade |

---

## 4. Poziomy reakcji

- `monitor` - zapis sygnału bez blokady,
- `soft_hold` - czasowe zatrzymanie upgrade do dodatkowej weryfikacji,
- `manual_review` - wymagana decyzja człowieka lub panelu proceduralnego,
- `hard_block` - zakaz upgrade do czasu zamknięcia sprawy.

---

## 5. Minimalny profil dla `phone -> strong`

Domyślny profil federacyjny powinien wymagać:

- `phone_upgrade_cooldown = 14 dni`,
- braku `A6` i `A8`,
- `manual_review` przy `A2`, `A3` albo `A7`,
- co najmniej `soft_hold` przy `A4`,
- agregacji sygnałów `A1-A5` w jednym oknie czasu.

---

## 6. Relacje do innych dokumentów

- `ATTESTATION-PROVIDERS.pl.md` - określa, kiedy sygnały anomalii są wymagane.
- `IDENTITY-ATTESTATION-AND-RECOVERY.pl.md` - określa upgrade i łańcuch poświadczeń.
- `UNSEAL-CASE-MODEL.pl.md` - może służyć jako wspólny model sprawy, jeśli upgrade przechodzi w spór proceduralny.
