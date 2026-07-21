# Federation Bootstrap and Trust FAQ

Federacja Orbipleksu nie jest listą adresów ani wspólnym CA. Jest lokalnie
przyjętym ładem technicznym, którego korzenie, role i dowody są jawne, podpisane
i używane przez niezależne policy gates.

Procedura uruchomienia znajduje się w
[Federation Bootstrap and Trust HOWTO](../howto/federation-bootstrap-and-trust-howto.pl.md).

## Co właściwie ustanawia `federation-root.v1`?

Root pack wiąże w jednym podpisanym kontrakcie `federation/id`, sovereign
subjects, politykę official-service endorsements, bootstrap Seed Directory,
domyślne selektory sieciowe oraz metadane ceremonii i odwołań.

Nie dowodzi prawdziwości każdego rekordu, który pojawi się później. Określa,
czyje podpisy i jakie policy material mogą uczestniczyć w lokalnej ewaluacji.
Każdy konsument nadal weryfikuje używany artefakt w swoim punkcie decyzji.

## Czy wpis bootstrap jest dowodem, że usługa jest oficjalna?

Nie. Wpis mówi, gdzie spróbować połączenia. Official status wynika wyłącznie z
aktywnego `federation-service-endorsement.v1`, zweryfikowanego względem
bieżącego root packa i widoku odwołań.

Bootstrap bez poprawnego endorsementu może pozostać advisory albo community
source, lecz nie powinien zostać po cichu podniesiony do official service.

## Czym endorsement różni się od capability passportu?

Passport odpowiada: "czy ten subject może świadczyć lub wywołać capability w
tym zakresie?". Endorsement odpowiada: "czy ta usługa ma status oficjalny w
tej federacji?".

Usługa może mieć ważny passport i nie być oficjalna. Może też być oficjalnie
endorsowana, lecz nadal nie pasować do capability, recipienta albo lokalnej
polityki wywołania. Te dowody są koniunkcją, nie zamiennikami.

## Czy TLS certificate dowodzi tożsamości węzła?

Nie. TLS dowodzi, że kanał spełnił politykę transportową dla endpointu. Peer
handshake dowodzi posiadania klucza tożsamości węzła. Passport i endorsement
dotyczą autorytetu usługowego, a lokalna polityka podejmuje końcową decyzję.

Publiczne WebPKI może ułatwić HTTPS/WSS na porcie 443, lecz samo nie ustanawia
członkostwa w federacji ani prawa do świadczenia capability.

## Po co Seed Directory, skoro root pack zawiera bootstrap?

Root pack powinien być mały i zmieniać się rzadko. Seed Directory utrzymuje
czasową projekcję reachability, capability registrations, revocations,
subject routing i endpoint evidence. Bootstrap wskazuje pierwszą drogę do tej
projekcji; nie zastępuje jej.

To rozdzielenie ogranicza blast radius: codzienna zmiana endpointu albo
capability nie wymaga nowej ceremonii root, natomiast zmiana źródeł suwerennego
autorytetu wymaga nowego root packa.

## Czy atestowana odpowiedź Seed Directory jest prawdą o sieci?

Nie. `seed-directory-query-attestation.v1` dowodzi, że konkretny katalog
zwrócił określony kanoniczny widok przy danym projection high-water. Nie
dowodzi, że katalog zna wszystkie fakty ani że świat odpowiada jego projekcji.

Konsument powinien nadal stosować multi-directory policy, odwołania, TTL,
handshake i domain verification.

## Co daje trusted Agora replay?

Replay pozwala lokalnemu Seed Directory odtworzyć zaakceptowane fakty z
zaufanych lane'ów Agora bez uznawania Agora za authority domenowe. Agora
przenosi envelope i egzekwuje własne publish ACL; Seed Directory ponownie
waliduje record kind, schema, podpis i semantykę.

Cursor jest stanem technicznym replayu. Nie zastępuje projection high-water ani
monotonicznych sequence numbers rekordów domenowych.

## Dlaczego zmiana root packa wymaga restartu?

Aktywny root wyznacza federacyjną tożsamość procesu. Hot reload mógłby sprawić,
że część subsystemów wykona pracę pod starym ładem, a część pod nowym. Dlatego
daemon może zweryfikować kandydata, lecz zmiana aktywnego fingerprintu jest
restart-only.

Data-dir guard odrzuca rollback `pack_version`, ten sam numer z innym digestem
oraz niezgodne `federation/id`. Restart jest kontrolowanym punktem przejścia,
nie sposobem na obejście tych reguł.

## Jak rotować TLS pin Seed Directory?

MVP utrzymuje jeden aktywny leaf-DER pin na endpoint. Rotacja wymaga root packa
z wyższym `pack_version`, nowego podpisu oraz restartu. Pin wymaga HTTPS i
chroni kanał do katalogu; nie nadaje mu official status.

Nie dodawaj drugiego, sprzecznego pinu dla tego samego endpointu w manual trust
config. Konfiguracja ma odmówić, zamiast losowo wybrać jedną wartość.

## Co się dzieje, gdy wszystkie Seed Directory są niedostępne?

Węzeł przechodzi w isolated/bootstrap lub degraded posture zależnie od
aktywnej konfiguracji. Nie powinien zastępować brakującego katalogu pierwszym
napotkanym endpointem ani wyłączać weryfikacji passportów.

Istniejące, świeże i lokalnie zweryfikowane dane mogą pozostać użyteczne w
granicach swojej retencji, lecz nowe krytyczne decyzje zależne od revocation
freshness powinny fail closed.

## Czy federacja uniemożliwia współpracę między federacjami?

Nie. Federation Root wybiera jeden aktywny `federation/id` i jej wewnętrzny
ład. Współpraca przekraczająca tę granicę należy do wyższych kontraktów, na
przykład alliance policy, Room, Corpus, Whisper albo jawnego Artifact Delivery.

Cross-federation carrier nie przepisuje lokalnego root i nie rozszerza
automatycznie Community Memarium, capability passports ani official status.

## Jakie dowody powinien zobaczyć operator?

Operator powinien móc rozdzielić:

- aktywny root digest, `pack_version` i `federation/id`;
- zaakceptowane oraz odrzucone official-service endorsements;
- Seed Directory source, trust tier, replay cursor i ostatni błąd;
- TLS pin/evidence oraz wynik peer handshake;
- capability passport i jego revocation status;
- końcową decyzję konsumenta wraz z policy ref.

Jedno zielone pole "trusted" ukryłoby zbyt wiele różnych przyczyn.
