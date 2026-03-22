# Indeks memów

Ten katalog zawiera krótkie notatki ideowe, zalążki i prompty projektowe, które nie są jeszcze na tyle dojrzałe, by stać się propozycjami, wymaganiami albo stories.

## Komunikacja i pomoc

- `swarm-broadcast-assistance.md` - użytkownik otwiera okno komunikacyjne do roju jako całości i prosi o pomoc w ważnej sprawie.
- `swarm-communication-exposure-modes.md` - trzy tryby ekspozycji próśb użytkownika: `private-to-swarm`, `federation-local` oraz `public-call-for-help`.
- `swarm-question-channel-transports.md` - kandydackie klasy transportu dla kopert pytań i dużych konwersacji answer-channel z redundantnymi serwerami.
- `transcription-monitors-and-public-vaults.md` - węzły monitorujące transkrypcje zachowują wartościowe dyskusje jako transkrypty źródłowe, a węzły-archiwiści publikują je w trwałych skarbcach do późniejszej syntezy i trenowania.
- `human-expertise-escalation.md` - rój prosi o pomoc ludzkiego specjalistę stojącego za węzłem, gdy dochodzi do granicy własnej pewności albo kompetencji.
- `operator-participation-in-answer-channel.md` - uczestniczący węzeł może konsultować się prywatnie ze swoim operatorem albo pozwolić mu dołączyć do żywej debaty, z jawną proweniencją odróżniającą output węzła od wkładu pochodzącego od człowieka.
- `operator-proxy-co-regulation.md` - węzeł może działać jako zewnętrzny rzecznik swojego operatora i prowadzić dialogi koregulacyjne proxy-to-proxy, łącznie z prywatnym lokalnym powiązaniem kontaktów bez globalnej depseudonimizacji.

## Orientacja użytkownika i filtrowanie

- `filtrum.md` - osobisty komponent filtrujący, który priorytetyzuje treści na podstawie preferencji, celów, cech i bieżącego stanu użytkownika, potencjalnie w formie rozszerzenia przeglądarki.

## UX i odkrywanie węzłów

- `client-simplicity.md` - klient węzła powinien pozostać prosty w instalacji, konfiguracji i uruchamianiu.
- `pod-backed-thin-clients.md` - klienci mobilni i desktopowi mogą działać jako cienkie interfejsy do węzłów wystawiających moduł `pod`, bez uruchamiania własnego lokalnego modelu językowego.
- `wide-caps.md` - hierarchiczna reklama zdolności i lekkie dopasowanie semantyczne między capability węzłów.

## Zaufanie, bezpieczeństwo i kontrola

- `bad-actors.md` - wykrywanie złych aktorów oraz wykluczanie ich lub karanie przez konsensus.
- `model-requests.md` - żądania mogą określać fingerprinty modeli, które muszą albo nie mogą być użyte.

## Reguła promocji

Każdy memo powinien pozostać krótki. Gdy idea uzyska stabilną semantykę, jawnych aktorów albo presję implementacyjną, należy awansować ją do jednej z poniższych kategorii:

- `doc/project/30-stories/` dla scenariuszy użytkownika,
- `doc/project/40-proposals/` dla kierunku architektonicznego,
- `doc/project/50-requirements/` dla konkretnych wymagań systemowych,
- `doc/normative/50-constitutional-ops/`, jeżeli staje się normatywna.
