# Polityka członkostwa i sponsoringu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-MEMBERSHIP-SPONSORSHIP-001` |
| `type` | Akt wykonawczy / polityka wejścia i sponsoringu |
| `version` | `0.2.0-draft` |
| `date` | `2026-05-27` |
| `basis` | Konstytucja art. VII, XV, XVI; Wartości podstawowe; Proposal 051; Specyfikacja reputacji proceduralnej |

## Cel

Ta polityka definiuje, jak uczestnicy wchodzą na wspólne powierzchnie wpływu Orbipleksu bez zamieniania członkostwa w test moralnej czystości.
Pytanie nie brzmi "czy ta osoba jest dobra?", lecz "na które wspólne powierzchnie ten podmiot może wpływać, z jakimi limitami, na podstawie jakich dowodów, z czyim ograniczonym poręczeniem i z jaką ścieżką apelacji?".

Orbiplex utrzymuje otwartość lokalnego czytania i lokalnego uruchamiania węzła, ale stawia śluzy wokół wpływu.
Śluzy chronią komunikację, pamięć publiczną, wymianę rynkową, governance, routing, custody i powierzchnie zaufania publicznego przed Sybil pressure, spamem, oszustwem, przejęciem frakcyjnym i lekkomyślnym poręczeniem.

## Kanoniczne słownictwo

Schematy membership i surface-access używają `doc/schemas/_shared/membership-enums.v1.schema.json` jako wspólnego źródła słownictwa.
Proza normatywna może te pojęcia objaśniać, ale implementacje nie powinny ręcznie kopiować enumów.

Klasy wejścia:

- `guest`
- `contactable-participant`
- `sponsored-candidate`
- `probationary-member`
- `full-participant`
- `public-trust-role`

Powierzchnie wpływu:

- `local-read`
- `contactability`
- `public-comment`
- `public-publishing`
- `unsolicited-dm`
- `broadcast`
- `marketplace`
- `custody`
- `routing`
- `moderation`
- `arbitration`
- `governance`
- `public-trust`

`public-trust-role` jest klasą wejścia.
`public-trust` jest powierzchnią, na której wykonywana jest władza roli wysokiego zaufania.

## Kanoniczna macierz dostępu

Nie istnieje jeden globalny stan `accepted`, który odblokowuje wszystkie wspólne możliwości.
Polityka wejścia działa przez macierz `(entry-class, surface) -> decision`, zapisaną jako `surface-access-policy.v1`.

| Klasa wejścia | Powierzchnia | Domyślna decyzja | Dodatkowa bramka |
|---|---|---|---|
| `guest` | `local-read` | `allow` | lokalne oprogramowanie i publiczne czytanie |
| `guest` | dowolna wspólna powierzchnia wpływu | `deny` | brak wspólnego wpływu domyślnie |
| `contactable-participant` | `contactability` | `probation+attestation` | atestacja kanału kontaktu; limity antyspamowe |
| `contactable-participant` | `public-comment` | `review` | polityka społeczności może dopuścić komentarze low-rate |
| `sponsored-candidate` | `public-comment` | `n-sponsors` | domyślnie jeden sponsor zakresowy; limity slow-start |
| `sponsored-candidate` | `public-publishing` | `review` | zakres sponsora i polityka powierzchni publikacji |
| `probationary-member` | `public-comment` | `allow` | limity low-rate albo normalne według polityki lokalnej |
| `probationary-member` | `unsolicited-dm` | `deny` | wymagana relacja albo opt-in |
| `probationary-member` | `broadcast` | `deny` | domyślnie brak wysokiego fan-out |
| `probationary-member` | `marketplace` | `review` | niski limit wartości, escrow/procurement contract |
| `full-participant` | `broadcast` | `review` | reputacja, rate limits i kontrole antykoluzyjne |
| `full-participant` | `routing` | `review` | capability passport i historia niezawodności |
| `full-participant` | `custody` | `review` | capability passport, polityka storage, audyt |
| `full-participant` | `governance` | `review` | reputacja proceduralna i kontrole COI |
| `public-trust-role` | `public-trust` | `review` | IAL, reputacja proceduralna, COI, audyt, odwoływalność |

Macierz jest celowo konserwatywna.
Federacje mogą ją zaostrzać lub rozluźniać, ale powinny publikować wynik jako `surface-access-policy.v1`, zamiast ukrywać go w gałęziach runtime.

## Sponsoring

Sponsoring jest zakresową relacją odpowiedzialności, a nie gwarancją moralnej jakości.
Sponsor stwierdza:

> Znam ten podmiot wystarczająco, aby wprowadzić go na tę powierzchnię Orbipleksu, w tym zakresie i limicie ryzyka, oraz przyjmuję ograniczoną ekspozycję reputacyjną, jeżeli sponsoring okaże się rażąco lekkomyślny albo koluzyjny.

Sponsoring daje kandydaturę, nie władzę.
Sponsorowany podmiot nadal potrzebuje wymaganych atestacji, probation, kontroli polityki i limitów runtime dla powierzchni docelowej.

Domyślne templates sponsoringu:

| Template | Znaczenie | Domyślne użycie |
|---|---|---|
| `light-vouch` | słabe wprowadzenie, niska ekspozycja | contactability albo bardzo niskoryzykowne wejście lokalne |
| `standard-introduction` | zwykły sponsoring zakresowy | podstawowe wejście do społeczności i public comment low-rate |
| `strong-vouch` | sponsoring wysokiego zaufania | szersza publikacja albo marketplace probation |
| `mentor-with-liability` | aktywna relacja mentorska z większą odpowiedzialnością | intensywne probation albo wrażliwe wejście do społeczności |

Artefakt sponsoringu zapisuje template, zakresy, czas wystawienia i wygaśnięcia, okno probation, strukturalne referencje due diligence, odwoływalność, czas ogona po odwołaniu i politykę dowodową.
Nie niesie ad-hoc numerycznych pól ekspozycji; te są projekcjami polityki z template'u i dowodów.

## Odpowiedzialność sponsora

Pochodna odpowiedzialność sponsora jest domyślnie bezpośrednia.
Może dotknąć sponsora, gdy dowody wskazują na zaniedbujący, lekkomyślny albo koluzyjny sponsoring w świeżym oknie sponsoringu.

Odpowiedzialność jest klasyfikowana porządkowo, a nie przez mnożenie lokalnych współczynników:

| Klasa | Znaczenie | Typowe triggery |
|---|---|---|
| `negligible` | brak istotnej odpowiedzialności pochodnej | szkoda była nieprzewidywalna albo poza zakresem sponsoringu |
| `mitigated` | obniżona odpowiedzialność po konstruktywnej reakcji | sponsor szybko odwołał, zgłosił flagi albo ograniczył szkodę |
| `moderate` | zwykła ograniczona odpowiedzialność | sponsor pominął słabe sygnały albo sponsorował zbyt szeroko |
| `serious` | silna odpowiedzialność | sponsor ignorował powtarzalne czerwone flagi, sponsorował masowo albo poza kompetencją |
| `collusive` | sponsor był częścią wzorca nadużycia | sweep antykoluzyjny wykrył sponsor-ring albo skoordynowane przejęcie |

Każda klasyfikacja musi wskazywać triggery i referencje dowodowe.
Dzięki temu decyzję można podważyć bez udawania, że pięć lokalnych współczynników liczbowych jest przenośną prawdą.

Odpowiedzialność nie propaguje dalej niż jeden poziom, chyba że proces antykoluzyjny wykaże zorganizowany sponsor-ring.

## Hamulce przeciw klanowości

Sponsoring nie może stać się prywatną arystokracją.
Federacje i społeczności powinny wymagać:

- sponsorowania tylko w zakresie własnej reputacji i uprawnień sponsora,
- niezależnych sponsorów dla powierzchni wyższego ryzyka,
- wymogów odległości grafowej albo zróżnicowania klastrów,
- limitów aktywnych sponsoringów w okresie,
- automatycznego przeglądu przy nietypowej prędkości sponsorowania,
- domyślnej odpowiedzialności jednego poziomu,
- wykrywania sponsor-ring,
- oraz prawa apelacji sponsora i sponsorowanego.

Bazowy detektor MVP dla nadużyć sponsoringu to **abnormal sponsorship velocity**: zbyt wiele aktywnych sponsoringów od jednego sponsora w oknie polityki, z progami strojonymi lokalnie.

## Slow-start newcomerów

Nowi uczestnicy powinni zaczynać z wąskimi limitami capability.
Kanoniczne domyślne postawy są wyrażone przez:

- `default.surface-access-policy.json`
- `newcomer.participant-entry-profile.json`
- `newcomer.participant-effective-limits.json`

Te przykłady są sprawdzane schemami i powinny być traktowane jako kanoniczny fixture profilu newcomera.
Dokumenty powinny linkować do nich zamiast powielać bloki YAML.

To są domyślne limity, nie trwałe wykluczenie.
Konstruktywne, niezależnie udokumentowane działanie powinno czynić awans tańszym niż destrukcję.

## Sankcje i ścieżka powrotu

Sankcje są wyrażane jako `(surface x intensity)`, a nie jedna mieszana drabina nieporównywalnych akcji.

| Grupa powierzchni | `soft` | `hold` | `hard` | `block` |
|---|---|---|---|---|
| `communication` | rate-limit | DM restriction | routing cut-off | federation block |
| `marketplace` | rate-limit | marketplace hold | escrow-only | marketplace block |
| `reputation` | downweight | quarantine | freeze | revoke projection |
| `role` | warning | review | suspension | revocation |
| `relationship` | warn | sponsor review | sponsor revoke | sponsor-ring action |
| `routing` | deprioritize | require fresh proof | cut-off | federation block |
| `custody` | require review | hold writes | suspend custody | revoke custody eligibility |
| `governance` | reduce weight | recusal | suspend voting/panel eligibility | governance block |

Kanoniczny porządek intensywności to `soft < hold < hard < block`.
Sankcje muszą zachowywać ślad audytowy, ścieżkę apelacji i ścieżkę naprawy, chyba że istnieje bezpośrednie zagrożenie bezpieczeństwa.
Powinny ograniczać powierzchnie wpływu, a nie wymazywać człowieczeństwo.

## Bazowe detektory antykoluzyjne

Pierwsza implementacja nie powinna próbować wykryć wszystkich form koluzji naraz.
Bazowe detektory MVP to:

- sponsoring: abnormal sponsorship velocity,
- public adjudication: co-flagging coherence, np. podobieństwo Jaccarda zbiorów flagujących między obiektami,
- marketplace: closed-loop receipt detection, np. cykle settlement `A -> B -> C -> A`.

Dalsze detektory powinny być dokładane jawnie, gdy istnieją dane operacyjne pokazujące, że baseline nie wystarcza.

## Powiązane kontrakty

Tę politykę wspierają:

- `membership-invitation.v1`
- `membership-sponsorship.v1`
- `membership-acceptance.v1`
- `participant-entry-profile.v1`
- `participant-effective-limits.v1`
- `surface-access-policy.v1`
- `participant-capability-limits.v1`
- `reputation-signal.v1`
