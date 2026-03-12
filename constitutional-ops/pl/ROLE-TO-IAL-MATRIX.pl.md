# Macierz ról i poziomów IAL w DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-ROLE-IAL-001` |
| `typ` | Ustawa wykonawcza / macierz kwalifikacji |
| `wersja` | 0.1.0-draft |
| `data` | 2026-03-12 |

---

## 1. Cel dokumentu

Niniejszy dokument mapuje klasy ról DIA na minimalne poziomy pewności tożsamości
(`IAL`) oraz wskazuje, kiedy `IAL` działa wyłącznie jako bramka, a kiedy może dać
minimalną premię stałą `fixed_power_bonus`.

Dokument nie zmienia zasady nadrzędnej: `IAL` nie zastępuje reputacji
proceduralnej i nie mnoży wpływu dynamicznie.

---

## 2. Zasady ogólne

1. `IAL` działa przede wszystkim jako bramka do klas ról i decyzji.

2. Wyższy `IAL` nie może sam z siebie zastąpić wymaganego progu reputacji,
   doświadczenia ani wyniku screeningu roli.

3. Ewentualny `fixed_power_bonus` MUSI być:

   - jawnie zdefiniowany w polityce federacyjnej,

   - stały dla całego systemu lub danej federacji,

   - ograniczony do `<= 1%`,

   - wyłączalny dla ról najwyższej stawki, jeśli federacja wybierze model bez
     jakiejkolwiek premii za silniejsze zakotwiczenie.

4. Role wysokiej stawki POWINNY wymagać nie tylko `IAL`, ale też okresu próbnego,
   reputacji proceduralnej i kontroli konfliktów interesów.

5. Sufit `IAL` wynika również z klasy poświadczenia źródła tożsamości. Źródła
   `weak` nie powinny same z siebie odblokowywać ról wysokiej stawki, nawet jeśli
   lokalnie spełniono inne warunki.

---

## 3. Minimalna macierz

| Klasa roli | Przykłady | Minimalny `IAL` | `fixed_power_bonus` | Uwagi |
| :--- | :--- | :--- | :--- | :--- |
| Uczestnik podstawowy | zwykły użytkownik, autor treści, obserwator | `IAL0` | `0%` | brak prawa do ról wysokiej stawki |
| Operator węzła | custodiani zwykłych `node-id` | `IAL1` | `0%` | wystarcza trwałość proceduralna |
| Operator stacji / agenta | hostowanie urządzeń i agentów | `IAL1` | `0%` | zależy też od higieny bezpieczeństwa |
| Uczestnik płatności / wymiany | transakcje, płatności, rozrachunek | `IAL1` | `0-0.25%` | federacja może wymagać wyższego progu |
| Wyrocznia niskiej stawki | pomiary i rozstrzygnięcia o niskich skutkach | `IAL2` | `0-0.25%` | tylko przy dodatkowym audycie |
| Opiekun sygnalistów | przyjmowanie zgłoszeń, kanały ochronne | `IAL3` | `0%` | preferowany brak premii |
| Panelista zwykły | panel ad-hoc, apelacja średniej stawki | `IAL3` | `0-0.5%` | obowiązkowy COI-check |
| Panelista wysokiej stawki | sprawy z możliwością `U2` lub ciężkich sankcji | `IAL3` | `0%` | rekomendowany przewodniczący `IAL4` |
| Członek FIP | izba pieczęciowa, quorum odpieczętowania | `IAL4` | `0%` | brak premii, tylko odpowiedzialność |
| Wyrocznia wysokiej stawki | wpływ na zdrowie, wolność, wysokie szkody | `IAL4` | `0%` | wymagana najwyższa kontrola |
| Governance wysokiej stawki | role ustrojowe i konstytucyjne | `IAL4` | `0%` | asymetryczna odpowiedzialność |

---

## 4. Reguły interpretacyjne

1. Federacja MOŻE podnosić progi `IAL` dla własnych ról.

2. Federacja NIE MOŻE obniżać progów dla ról, które wchodzą w zakres `U2`, `U3`,
   ochrony sygnalistów albo wysokostawkowego governance.

3. Jeżeli rola łączy kilka funkcji, obowiązuje najwyższy wymagany `IAL`.

4. Jeżeli sprawa ma charakter międzyfederacyjny, obowiązuje wyższy z progów stron
   uczestniczących.

5. Jeżeli źródło poświadczenia ma klasę `weak`, federacja NIE MOŻE przyznać przez
   samą macierz roli poziomu wyższego niż dopuszczalny sufit z
   `ATTESTATION-PROVIDERS.pl.md`.

---

## 5. Relacje do innych dokumentów

- `ROOT-IDENTITY-AND-NYMS.pl.md` definiuje warstwy tożsamości i `IAL0-IAL4`.

- `PROCEDURAL-REPUTATION-SPEC.pl.md` definiuje warstwę reputacji, która pozostaje
  odrębna od `IAL`.
- `ATTESTATION-PROVIDERS.pl.md` definiuje klasy `weak` / `strong` oraz sufit
  `IAL` dla metod poświadczenia.

- `PANEL-SELECTION-PROTOCOL.pl.md` i `IDENTITY-UNSEALING-BOARD.pl.md` powinny
  korzystać z tej macierzy jako domyślnego minimum dla paneli i izb.
