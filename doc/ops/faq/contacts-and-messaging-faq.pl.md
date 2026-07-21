# Kontakty i wiadomości: FAQ

## Gdzie użytkownik przechowuje swoją książkę adresową?

Książka adresowa jest lokalnym, owner-scoped read-modelem węzła. Rekordy
`local-contact.v1` przechowują etykiety i metadane potrzebne interfejsowi, natomiast
kanoniczna zgoda na odbieranie wiadomości wynika z aktywnego członkostwa w klasie
relacji `contacts`. Contact Catalog nie zastępuje tej warstwy.

Praktyczną ścieżkę od publikacji kontaktowalności do lokalnego kontaktu opisuje
[HOWTO kontaktów i wiadomości](../howto/contacts-and-messaging-howto.pl.md).

## Czym Contact Catalog różni się od lokalnych kontaktów?

Contact Catalog odpowiada na pytanie: „czy dla tego lookup-safe indeksu istnieje
atestowana trasa zaproszenia?”. Lokalny kontakt odpowiada natomiast na pytanie:
„jak właściciel tego węzła klasyfikuje daną relację i czy zgodził się odbierać nią
wiadomości?”. Pierwsza warstwa służy odkrywaniu, druga lokalnej polityce i UX.

Katalog nie powinien ujawniać surowego e-maila, numeru telefonu ani głównego
`participant/id`. Wynik lookupu niesie trasę zaproszenia, nie globalną książkę osób.

## Co dowodzi contact attestation?

`email-control@v1` albo `phone-control@v1` dowodzi, że podmiot kontrolował wskazany
kanał podczas procedury atestacyjnej. Nie dowodzi nazwiska, tożsamości cywilnej ani
tego, że kanał pozostanie pod jego kontrolą bezterminowo. Dlatego atestacja otwiera
contactability i ograniczenia antyspamowe, lecz nie role wysokiego zaufania.

## Dlaczego publikowana trasa nie wskazuje bezpośrednio uczestnika?

Publiczna odpowiedź katalogu prowadzi do `routing-subject/id` albo innego
ograniczonego celu routowalnego. Pseudonym Vault wiąże następnie lokalne i pairwise
nymy z trasą potrzebną konkretnej relacji. Dzięki temu publiczny handle nie staje się
uniwersalnym identyfikatorem korelującym wszystkie działania uczestnika.

## Dlaczego pierwsza wiadomość zaczyna się od contact request?

Nieznany nadawca nie otrzymuje od razu prawa do wysyłania treści. Messaging najpierw
rozwiązuje handle w Contact Catalog i dostarcza `contact-request.v1`. Dopiero decyzja
odbiorcy tworzy lokalną relację `contacts`, pairwise mapping oraz wąski passport
`messaging-receive@v1`. Odmowa nie jest błędem transportu, lecz prawidłowym wynikiem
polityki odbiorcy.

## Dlaczego operator może zobaczyć dwa pytania o zgodę?

Pierwsze pytanie może dotyczyć wpuszczenia zdalnego węzła przez INAC dla określonej
klasy artefaktu. Drugie dotyczy samej prośby kontaktowej użytkownika. Są to różne
akty władzy: autoryzacja transportu nie tworzy relacji, a relacja nie może po cichu
otworzyć dowolnego transportu.

## Czy klasa relacji nadaje capability?

Nie. `contacts`, `friends` albo inna klasa LRL jest lokalnym wejściem polityki i
selektorem grupy. Samo przypisanie klasy nie wydaje passportu ani nie omija
autoryzacji hosta. Capability powstaje wyłącznie przez jawny mechanizm wydawania i
pozostaje ograniczone profilem, podmiotem, trasą, czasem oraz revocation view.

## Gdzie przechowywana jest wiadomość?

Messaging utrzymuje trwały outbox i inbox, indeks rozmów oraz temporalny ślad prób i
zmian stanu. Natywny outbound body jest przechowywany jako EML, a canonical inbound
record jako JSON Maildir z odtwarzalną projekcją EML. `messaging.flag.v1` utrwala
między innymi read/unread jako fakty, zamiast bezśladowo nadpisywać widok.

## Czy treść wiadomości trafia do Contact Catalog albo Seed Directory?

Nie. Katalog i Seed Directory służą odkrywaniu zaufanych providerów oraz tras, nie
przechowywaniu treści wiadomości. Sama wiadomość jest dostarczana prywatnie przez
Artifact Delivery i INAC. Publiczne lub utrwalone kopie wymagają osobnego, jawnego
kontraktu, na przykład recorded-message policy i Agora Vault.

## Jak zablokować albo odwołać relację?

Operator lub właściciel zmienia stan członkostwa LRL, odwołuje właściwy passport i
aktualizuje lokalny kontakt. Każda z tych czynności ma inny skutek: LRL wpływa na
lokalną selekcję, revocation zatrzymuje authority, a rekord kontaktu aktualizuje UX.
Nie należy zastępować trzech jawnych zmian jednym ukrytym polem `blocked`.

## Czy Messaging obsługuje grupy?

LRL potrafi deterministycznie rozwiązać klasę, taką jak `friends`, do lokalnej listy
kandydatów z zachowaniem scope właściciela. Jest to gotowy prymityw selekcji, lecz nie
pełny protokół wieloosobowej rozmowy. Długotrwała komunikacja grupowa i wspólna
historia należą do Room/Corpus, nie do udawanej pętli prywatnych wiadomości.

## Jaki jest najkrótszy test całego przepływu?

Story-010 uruchamia dwa lokalne węzły, Seed Directory, Attestation Service, Contact
Catalog i dwa serwisy Messaging. Test publikuje atestowaną contactability, wykonuje
lookup, obsługuje zgodę INAC, akceptuje contact request i sprawdza prywatne
dostarczenie oraz inbox/outbox. Jest to acceptance wielowęzłowe na jednym hoście, a
nie dowód działania przez publiczny Internet.

