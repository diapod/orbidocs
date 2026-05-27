# Polityka antyfraudowa marketplace

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-MARKETPLACE-ANTI-FRAUD-001` |
| `type` | Akt wykonawczy / polityka ryzyka marketplace |
| `version` | `0.1.0-draft` |
| `date` | `2026-05-27` |
| `basis` | Konstytucja art. XV, XVI; Matryca ról do IAL; Proposal 021; Proposal 051 |

## Cel

Powierzchnie marketplace tworzą ryzyko finansowe i operacyjne.
Orbiplex powinien ułatwiać zwykłą współpracę, a jednocześnie czynić scam, self-dealing i nadużycia wysokiej wartości wolnymi, widocznymi i kosztownymi.

## Reguły bazowe

Domyślna polityka marketplace:

- brak niezamówionych ofert finansowych przez DM,
- wszystkie oferty finansowe powinny używać jawnych powierzchni service albo marketplace,
- nowi uczestnicy zaczynają z bardzo niskimi limitami wartości,
- escrow albo kontrakty procurement są wymagane tam, gdzie ryzyko nie jest trywialne,
- zewnętrzne linki płatnicze są ograniczone dla nowych albo niskodowodowych uczestników,
- self-dealing nie tworzy przenośnej reputacji,
- powierzchnie wysokiej wartości wymagają silniejszego IAL, reputacji proceduralnej, cooling-off i ścieżek sporu.

## Progi ryzyka

```yaml
marketplace:
  new_participant:
    max_contract_value: low
    escrow_required: true
    external_payment_links: denied
    unsolicited_offers: denied
  elevated:
    min_IAL: IAL1_or_higher
    min_contract_reputation: threshold
    independent_receipts_required: true
  high_value:
    min_IAL: strong
    cooldown: required
    dispute_path: required
    legal_notice_policy: required
```

## Dowody

Reputacja marketplace powinna wynikać z first-hand settled receipts powiązanych z kontraktami, zamówieniami, settlementami albo wynikami sporów.
Gossip-only score updates i zamknięte pętle wzmacniania nie powinny odblokowywać limitów wartości.

## Egzekwowanie

Wzorce takie jak ukryta akwizycja, niezamówiona perswazja finansowa, podejrzany fan-out, powtarzalne nadużycia zwrotów, fałszywe pętle receiptów i asymetryczne targetowanie mogą uruchamiać:

- hold marketplace,
- obniżenie limitu wartości,
- tryb tylko-escrow,
- sygnały reputacji proceduralnej,
- przegląd sponsora,
- routing cut-off z powierzchni marketplace,
- albo formalną eskalację sporu.

