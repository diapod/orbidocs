# Kontakty i wiadomości: HOWTO

Ten dokument prowadzi przez pełną ścieżkę: od atestacji kanału kontaktowego, przez
publikację trasy i zaakceptowanie relacji, po prywatne dostarczenie wiadomości.
Odpowiedzi pojęciowe i granice odpowiedzialności znajdują się w
[FAQ kontaktów i wiadomości](../faq/contacts-and-messaging-faq.pl.md).

## Rozdziel źródła prawdy

| Warstwa | Odpowiedzialność | Nie jest źródłem prawdy dla |
|---|---|---|
| Contact Attestation | kontrola e-maila lub telefonu w określonym czasie | tożsamości cywilnej i relacji |
| Contact Catalog | atestowane claims i lookup-safe trasy zaproszeń | lokalnej książki adresowej |
| Local contacts | etykiety i owner-scoped projekcja UX | capability authority |
| Local Relationship Layer | klasy, członkostwa, predykaty i grupy właściciela | transportu i passportów |
| Pseudonym Vault | routing subject, pairwise nym i materiał odzyskania | publicznego katalogu osób |
| Messaging | outbox, inbox, treść, flagi i temporalny ślad dostarczenia | odkrywania providerów |
| AD + INAC | prywatny transport i admission artefaktów | zgody na relację |

## Sprawdź konfigurację i gotowość

Najpierw uruchom daemonowe `check-config`, a następnie sprawdź warstwy osobno:

```http
GET /v1/contact-catalog/status
GET /v1/messaging/status
GET /v1/local-relationships/status
GET /v1/messaging/contactability/options
```

Status `ready` jednego komponentu nie implikuje gotowości całego przepływu. Opcje
contactability powinny wskazywać lokalnego uczestnika oraz odkrytego, zaufanego i
świeżego providera atestacji. Kontakt zdalny wymaga ponadto działającej ścieżki AD/INAC.

## Przygotuj uczestnika i routing subject

Kontaktowalność publikuje się dla konkretnego lokalnego uczestnika, ale katalog nie
powinien ujawniać jego root identity. Utwórz lub zaimportuj uczestnika, odblokuj jego
klucz podpisujący i utwórz osobny routing subject. Zachowaj rozdział:

```text
participant/id       -> lokalna authority i podpis
routing-subject/id   -> publiczna trasa zaproszenia
pairwise nym         -> relacja po zaakceptowaniu prośby
```

## Zapisz draft contactability

Draft deklaruje handle oraz przeznaczenie trasy. Nie publikuje jeszcze claimu:

```http
POST /v1/messaging/contactability/draft
Content-Type: application/json
```

```json
{
  "handles": [
    {"handle/kind": "email", "handle/value": "marcin@example.org"}
  ],
  "routes": [
    {"participant/id": "participant:LOCAL", "purpose": "messaging"}
  ]
}
```

Wartość handle jest transientnym wejściem operatora. Trwały indeks katalogowy powinien
być lookup-safe; nie kopiuj surowego e-maila do publicznych diagnostyk ani audytu.

## Uzyskaj contact attestation

Rozpocznij challenge przez daemonowy bridge, a następnie redeem zgodnie z adapterem
dostawy providera:

```http
POST /v1/messaging/contactability/attestation/challenges
POST /v1/messaging/contactability/attestation/challenges/{challenge_id}/redeem
```

Request `contact-attestation-request.v1` określa `contact/kind`, `contact/value`,
subject, żądany profil i czas ważności. Wynikiem jest passport kontroli kanału. Profil
Story-010 może używać jawnego developmentowego `always_accept`; nie przenoś tego
ustawienia do środowiska produkcyjnego.

## Zwiąż atestację i opublikuj claim

Najpierw zwiąż passport z handlem w draftcie, potem opublikuj podpisany claim:

```http
POST /v1/messaging/contactability/attest
POST /v1/messaging/contactability/publish
```

```json
{
  "handle/kind": "email",
  "handle/value": "marcin@example.org",
  "passport": {"schema": "capability-passport.v1"}
}
```

Wartość `passport` powyżej skraca pełny passport zwrócony przez `redeem`; pokazany
obiekt nie jest samodzielnie poprawnym passportem.

Publikacja przechodzi przez nadzorowany Contact Catalog. Claim bez poprawnej atestacji,
z wygasłym passportem albo bez zgodnego subjectu powinien zostać odrzucony.

## Zweryfikuj lookup bez ujawnienia identity

Provider Contact Catalog przyjmuje `POST /v1/contact-catalog/lookups`. Produkcyjny
klient powinien korzystać z providera odkrytego przez Seed Directory, nie z
zakodowanego endpointu. Minimalna semantyka requestu jest następująca:

```json
{
  "schema": "contact-lookup-request.local.v1",
  "contact_index_value": "sha256:LOOKUP_SAFE_VALUE",
  "purpose": "messaging",
  "lookup_mode": "invitation-only"
}
```

Oczekiwany `contact-lookup-result.v1` ma `match/class = invitation-available` i
`result/routes`. Nie powinien zawierać root `participant/id` ani surowego handle'a.

## Wyślij pierwszą wiadomość

Nadawca może podać zewnętrzny handle. Messaging zapisze wiadomość w outboxie, lecz
nie wyśle jej jako treści do nieznanego odbiorcy przed zakończeniem contact request:

```http
POST /v1/messaging/outbound
Content-Type: application/json
```

```json
{
  "recipient/handle": {"kind": "email", "value": "marcin@example.org"},
  "subject": "Próba kontaktu",
  "body": "Cześć, czy możemy porozmawiać?",
  "content-type": "text/plain"
}
```

Uruchom przetwarzanie kolejki:

```http
POST /v1/messaging/outbox/process

{"batch/limit": 10}
```

## Obsłuż zgodę transportową i contact request

Jeżeli węzły nie mają jeszcze relacji transportowej, odbiorca zobaczy notyfikację
`inac/invitation-request`. Po jej zaakceptowaniu ponów przetwarzanie outboxu. Następnie
pojawi się osobna notyfikacja `contact-request/received`:

```http
GET /v1/operator/notifications?limit=50
POST /v1/operator/notifications/{notification_id}/actions/accept

{"version": 1}
```

Użyj wersji zwróconej przez konkretną notyfikację; przykład `1` nie jest stałą.
Akceptacja contact request tworzy lub aktualizuje lokalny kontakt, członkostwo
`contacts`, pairwise mapping i wąski receive passport. Po decyzji ponownie przetwórz
outbox nadawcy.

## Sprawdź outbox, inbox i body

Warstwy odczytu są rozdzielone:

```http
GET /v1/messaging/outbox
GET /v1/messaging/outbox/{envelope_id}/body
GET /v1/messaging/mailboxes
GET /v1/messaging/mailboxes/{mailbox_id}/messages
GET /v1/messaging/mailboxes/{mailbox_id}/messages/{envelope_id}/body
GET /v1/messaging/messages/{message_id}
```

Body endpointy są osobnymi, ograniczonymi powierzchniami. Lista wiadomości nie powinna
przypadkowo przenosić pełnej treści ani sekretów diagnostycznych.

## Zmieniaj flagi jako fakty

Read/unread i pokrewne flagi zapisuj przez endpoint flag wiadomości. Runtime utrwala
`messaging.flag.v1`, a read model składa aktualny stan:

```http
POST /v1/messaging/messages/{message_id}/flags
```

Nie edytuj SQLite ani plików Maildir ręcznie. Gdy projekcja wymaga odbudowy, użyj
`POST /v1/messaging/reindex`; dla zaległych faktów użyj
`POST /v1/messaging/pending-facts/replay`.

## Klasyfikuj kontakty bez nadawania authority

LRL pozwala dodać członkostwo i rozwiązać grupę:

```http
POST /v1/local-relationships/memberships
POST /v1/local-relationships/group.resolve
```

```json
{
  "owner/ref": "participant:LOCAL",
  "contact/ref": "contact:EXAMPLE",
  "class/id": "friends",
  "status": "active",
  "actor/ref": "participant:LOCAL",
  "reason/code": "operator-classification"
}
```

Rozwiązanie grupy jest owner-scoped i respektuje blokady. Wynik jest kandydaturą do
routingu, nie passportem i nie zgodą na broadcast.

## Wycofaj kontakt albo capability

Przy zakończeniu relacji wykonaj jawnie właściwe operacje: zmień lub usuń lokalny
kontakt, ustaw członkostwo LRL na `blocked` albo nieaktywne oraz odwołaj receive
passport. Następnie sprawdź revocation view i ponów reindex, jeżeli operator naprawiał
projekcję. Nie usuwaj faktów historycznych po to, aby „wyczyścić” widok.

## Uruchom Story-010

Z katalogu `node/` przygotuj profile i uruchom pełny, samowystarczalny smoke:

```sh
python3 tools/acceptance/story-010-operator/story-010-local-profiles.py init
python3 tools/acceptance/story-010-operator/story-010-local-profiles.py \
  ad-smoke --strict
```

Dla bramki LRL uruchom:

```sh
python3 tools/acceptance/story-010-operator/story-010-relationship-acceptance.py
```

Acceptance działa na dwóch profilach węzła na jednym hoście. Potwierdza kontrakty,
restarty, provider discovery, prywatne dostarczenie i owner-scope, lecz nie zastępuje
testu przez publiczną sieć ani produkcyjnego adaptera dostawy OTP.

## Diagnozuj od granicy, na której powstała odmowa

| Objaw | Najpierw sprawdź |
|---|---|
| brak providera atestacji | Seed Directory trust, freshness i capability profile |
| publish claim odrzucony | passport, subject, expiry i podpis claimu |
| lookup zwraca `no-match` | lookup-safe canonicalization, purpose i aktywność claimu |
| outbox czeka na permission | notyfikację INAC, contact request i retry schedule |
| contact istnieje, lecz message jest odrzucona | membership `contacts`, receive passport i revocation view |
| inbox ma rekord bez body | bounded body surface, Maildir i projection diagnostics |
| grupa różni się między operatorami | `owner/ref`, status membership i lokalne predykaty |

Naprawiaj najniższą niespełnioną granicę. Ręczne dopisywanie rekordów do dalszej
warstwy maskuje przyczynę i tworzy stan, którego nie da się odtworzyć.

## Dokumenty źródłowe

- [Solution 025: Contact Catalog](../../project/60-solutions/025-contact-catalog/025-contact-catalog.md)
- [Solution 026: Pseudonym Vault and Key Roles](../../project/60-solutions/026-pseudonym-vault-and-key-roles/026-pseudonym-vault-and-key-roles.md)
- [Solution 027: Messaging Middleware](../../project/60-solutions/027-messaging-middleware/027-messaging-middleware.md)
- [Solution 032: Local Relationship Layer](../../project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md)
- [Story-010](../../project/30-stories/story-010-message-to-a-friend.md)
