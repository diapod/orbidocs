# Polityka surowego sygnału i transformacji stylu DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-RAW-001` |
| `typ` | Ustawa wykonawcza (Poziom 3 hierarchii normatywnej) |
| `wersja` | `0.1.0-draft` |
| `podstawa` | Art. II.8-9, III.1-4, XI.7 Konstytucji DIA; `doc/normative/30-core-values/pl/CORE-VALUES.pl.md` sekcja "Prawo do surowego sygnału" |
| `status mechanizmów` | tryby sygnału, podstawy transformacji i model metaznaczników są normatywne; warstwa prezentacji może być federacyjnie parametryzowana |

---

## 1. Cel dokumentu

Konstytucja przyznaje użytkownikowi prawo do surowego sygnału oraz wymaga, by każda
transformacja stylu, tonu, struktury lub poziomu formalizacji wypowiedzi przez AI
pozostawiała metaznacznik. Brakuje jednak dokumentu wykonawczego, który definiuje:

- jakie są tryby pracy na wypowiedzi,
- kiedy transformacja jest dozwolona,
- jakie metaznaczniki są obowiązkowe,
- jak pozostawić ślad audytowy takiej ingerencji.

Niniejszy dokument operacjonalizuje te obowiązki.

---

## 2. Zasada ogólna

1. Surowy sygnał użytkownika jest dobrem chronionym.
2. Domyślnym trybem pracy systemu jest zachowanie charakterystyki wypowiedzi, a nie
   jej wygładzanie, profesjonalizowanie ani estetyzowanie.
3. Transformacja wypowiedzi może nastąpić wyłącznie na podstawie:
   - jawnego żądania użytkownika,
   - jawnej polityki użytkownika,
   - minimalnie koniecznej redakcji ochronnej,
   - wyjątku zgodnego z `EXCEPTION-POLICY.pl.md`.
4. Brak podstawy proceduralnej oznacza zakaz transformacji.

---

## 3. Tryby sygnału

System MUSI rozróżniać co najmniej następujące tryby:

| Tryb | Znaczenie |
| :--- | :--- |
| `raw` | sygnał zachowany bez celowej transformacji stylu, tonu i struktury poza technicznym przeniesieniem |
| `structured` | treść uporządkowana lub zmapowana na strukturę, ale bez celowego wygładzania charakteru wypowiedzi |
| `transformed` | styl, ton, forma lub poziom formalizacji zostały świadomie zmienione |
| `redacted` | sygnał został ograniczony lub zamaskowany z przyczyn ochronnych, prywatnościowych albo prawnych |

`structured` nie może być używane jako furtka do niejawnego wygładzania sygnału.
Jeżeli porządkowanie zmienia charakter wypowiedzi w sposób istotny dla odbioru,
należy użyć trybu `transformed`.

---

## 4. Dopuszczalne podstawy transformacji

### 4.1. Jawne żądanie użytkownika

Transformacja jest dopuszczalna, gdy użytkownik jawnie prosi o:

- skrót,
- listę zadań,
- tłumaczenie,
- zmianę tonu,
- zmianę formalności,
- wygładzenie albo redakcję stylistyczną,
- inne przekształcenie semantycznie równoważne.

### 4.2. Polityka użytkownika

Użytkownik może ustawić trwałą politykę transformacji, o ile:

1. polityka jest jawna,
2. można ją wyłączyć,
3. nie ukrywa przed użytkownikiem faktu, że sygnał został przetworzony.

### 4.3. Redakcja ochronna

Bez żądania użytkownika dopuszczalne są wyłącznie transformacje minimalnie konieczne
dla:

1. ochrony danych wrażliwych,
2. ograniczenia ryzyka bezpośredniej krzywdy,
3. spełnienia obowiązku prawnego lub konstytucyjnego,
4. ochrony sygnalisty lub osoby narażonej na odwet.

Taka operacja powinna być możliwie najwęższa i używać trybu `redacted`, nie
`transformed`, chyba że rzeczywiście zachodzi dodatkowa transformacja stylu.

### 4.4. Wyjątek proceduralny

Odstępstwo od powyższych zasad wymaga wyjątku zgodnego z
`EXCEPTION-POLICY.pl.md` i nie może stać się trybem domyślnym.

---

## 5. Metaznaczniki

### 5.1. Reguła obowiązkowa

Jeżeli wynik nie jest trybem `raw`, system MUSI dołączyć metaznacznik widoczny dla
odbiorcy końcowego albo jednoznacznie dostępny w tym samym interfejsie.

### 5.2. Minimalne pola metaznacznika

```yaml
signal_marker:
  mode: "transformed" # raw | structured | transformed | redacted
  actor: "ai"         # ai | human | hybrid
  requested_by: "user" # user | user_policy | safety_policy | exception
  basis_ref: "[prompt / policy-id / exception-id / rule-id]"
  operations:
    - "tone_shift"
    - "structure_extraction"
  visible_to_user: true
```

### 5.3. Minimalna semantyka operacji

`operations` POWINNO używać słownika kontrolowanego, obejmującego co najmniej:

- `structure_extraction`,
- `summarization`,
- `translation`,
- `tone_shift`,
- `formality_shift`,
- `style_polish`,
- `safety_redaction`,
- `privacy_redaction`.

---

## 6. Ślad audytowy transformacji

Każda transformacja różna od `raw` MUSI pozostawić ślad audytowy:

```yaml
signal_transform_event:
  transform_id: "[unikalny identyfikator]"
  source_ref: "[wiadomość / segment / artefakt]"
  input_mode: "raw"
  output_mode: "structured"
  actor_type: "ai"
  requested_by: "user"
  basis_ref: "[referencja]"
  operations:
    - "structure_extraction"
  created_at: "[timestamp]"
```

Ślad nie musi ujawniać pełnej treści transformowanego sygnału wszystkim uczestnikom,
ale MUSI być dostępny zgodnie z zasadami minimalnego ujawnienia dla audytu,
odwołania i analizy nadużyć.

---

## 7. Testy zgodności

System nie spełnia tej polityki, jeżeli zachodzi którykolwiek z warunków:

1. domyślnie wygładza lub profesjonalizuje wypowiedzi bez podstawy,
2. ukrywa przed użytkownikiem fakt transformacji,
3. używa trybu `structured` do ukrycia realnej zmiany tonu lub stylu,
4. nie pozostawia `basis_ref` dla transformacji niebędącej trybem `raw`,
5. traktuje surową formę wypowiedzi jako domyślny powód obniżenia praw lub
   wiarygodności użytkownika.

---

## 8. Metryki zdrowia federacyjnego

Federacja powinna mierzyć co najmniej:

- `raw_preservation_rate` - odsetek sygnałów pozostawionych w trybie `raw`,
- `non_requested_transform_rate` - odsetek transformacji niewywołanych przez
  bezpośrednie żądanie użytkownika,
- `hidden_transform_incidents` - liczbę wykrytych transformacji bez metaznacznika,
- `redaction_overreach_rate` - odsetek redakcji ochronnych uznanych po review za zbyt
  szerokie,
- `appeals_on_signal_transform` - liczbę odwołań dotyczących transformacji sygnału.

Wysoki `non_requested_transform_rate` albo `hidden_transform_incidents` jest
sygnałem dryfu w stronę paternalizmu lub maskowania rzeczywistości.

---

## 9. Relacja do innych dokumentów

- **Konstytucja Art. II.8-9**: prawo do surowego sygnału i obowiązek metaznacznika.
- **Konstytucja Art. III.1-4**: użytkownik zachowuje kontrolę nad danymi i politykami.
- **Konstytucja Art. XI.7**: filtr nie może działać jako ukryta cenzura.
- **`EXCEPTION-POLICY.pl.md`**: odstępstwa proceduralne i redakcje ochronne.

