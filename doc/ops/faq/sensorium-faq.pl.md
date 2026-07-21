# FAQ Sensorium

## Czym jest Sensorium?

Sensorium jest organem węzła odpowiedzialnym za lokalny kontakt sensomotoryczny ze
światem. Dopuszcza obserwacje, pośredniczy w ograniczonych dyrektywach, zapisuje ich
wyniki i ukrywa mechanikę konektorów za capabilities należącymi do hosta. To granica,
na której lokalny sygnał staje się dopuszczonym faktem węzła, a zamierzony efekt -
działaniem sprawdzonym przez politykę.

Sensorium nie jest całym systemem middleware, runtime'em LLM ani ogólną magistralą
zdalnych wywołań. Zapytania do modeli należą do Inquirium. Dystrybucja należy do
Artifact Delivery. Konektor integruje jedną klasę zewnętrznej rzeczywistości, lecz nie
staje się autorytetem rozstrzygającym, kto może z niego korzystać.

Praktyczną ścieżkę od konfiguracji do wywołania opisuje [HOWTO
Sensorium](../howto/sensorium-howto.pl.md).

## Dlaczego Sensorium jest organem, a nie tylko kolejnym API konektora?

Organ stanowi stabilną granicę semantyczną; konektory są wymiennymi mechanizmami.
Wołający prosi Sensorium o dopuszczenie sygnału albo wykonanie działania z allowlisty.
Host stosuje politykę tożsamości, capability, wrażliwości, czasu, zgody i audytu,
zanim wybierze konektor. Dzięki temu każde urządzenie, adapter systemu operacyjnego
czy backend Workbench nie wymyśla własnego modelu władzy.

Termin **konektor** nazywa hostowany komponent. **Adapter** jest techniką
implementacyjną wewnątrz konektora lub runtime'u hosta. W dokumentacji nie należy
używać tych słów jako wymiennych ról architektonicznych.

## Czym są Observation, Directive, Action i Outcome?

**Observation** jest dopuszczoną i ograniczoną w czasie reprezentacją sygnału.
Konektor proponuje kandydata; Sensorium nadaje metadane dopuszczenia należące do hosta
i umieszcza wynik w lokalnym modelu odczytowym.

**Directive** jest związaną z wystawcą prośbą o wykonanie jednego `action_id` z
typowanymi parametrami i ograniczoną polityką czasu. Wyraża intencję, nie uprawnienie.

**Action** jest zachowaniem z operatorskiej allowlisty, nazwanym przez `action_id`.
Wpis katalogowy określa kształt parametrów, limity, dostępność, kontrakt wyniku i trasę
do konektora ukrytą pod Sensorium Core.

**Outcome** jest faktem audytowym powstałym dla dyrektywy. Zapisuje ukończenie,
odmowę, błąd albo timeout i może wskazywać dopuszczone obserwacje lub artefakty. Nie
staje się automatycznie kolejną obserwacją ani publicznym strumieniem zdarzeń.

## Czym jest Sensorium Interface?

Sensorium Interface jest jawnie opublikowaną, ograniczoną projekcją reprezentacji
enaktywnej albo powierzchni efektu. To zasób z odrębnymi grantami, cyklem życia,
klasyfikacją, kursorem i semantyką odwołania. Może udostępniać na przykład paczkę
pomiarów temperatury, ekran terminala Workbench albo ograniczoną metodę sterowania.

Interfejs nie jest konektorem i nie ujawnia jego poświadczeń. Lokalne dopuszczenie w
Sensorium pozostaje domyślnie lokalne; publikacja przez Sensorium Interfaces jest
odrębną, widoczną dla operatora decyzją. Zobacz [Solution 046: Sensorium
Interfaces](../../project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md).

## Jakie rodzaje konektorów istnieją?

Kształt konektora wynika z zachowania, a nie z jednego zamkniętego podziału:

- konektory obserwacyjne produkują kandydatów na sygnały;
- konektory działań skończonych wykonują ograniczone operacje i zwracają wyniki;
- Sensorium OS jest konektorem referencyjnym dla jawnych wpisów katalogu działań
  systemu operacyjnego;
- Sensorium Workbench zarządza stanowymi operacjami przestrzeni roboczej, terminala,
  patchy i środowisk, chronionymi silniejszymi grantami i regułami recovery;
- adaptery źródeł mogą projektować wybrany stan konektora do Sensorium Interfaces.

Ta lista służy wyjaśnieniu, nie jest enumem, który muszą kopiować implementacje
zewnętrzne. Każdy konektor nadal deklaruje konkretne działania, kontrakty, limity i
status.

## Czym różnią się `action_id` i `connector_id`?

`action_id` jest publicznym adresem semantycznym, na przykład
`sensorium.workbench.file.read` albo `whisper.redaction.prepare`. Konsument może
umieścić go w `sensorium-directive.v1`, jeżeli otrzymał uprawnienie do wywołania
Sensorium.

`connector_id` jest prywatnym detalem routingu hosta. Zwykłe middleware, JSON-e Flows,
Agenty i zdalne peery nie mogą go wybierać. Zależność konsumenta od id konektora
zmieniałaby wymianę providera w złamanie API i odbierałaby hostowi jedną wspólną
granicę polityki.

## Czym Sensorium OS różni się od Sensorium Workbench?

Sensorium OS wykonuje skończone działania katalogowe, na przykład dopuszczony skrypt
o zamkniętym kontrakcie parametrów i wyniku. Katalog działania, digest skryptu,
katalog roboczy, środowisko, timeout i limity wyjścia należą do operatora. Wołający
przekazuje parametry, a nie plik wykonywalny ani tekst powłoki.

Sensorium Workbench zarządza zasobami żyjącymi dłużej: korzeniami workspace, snapshotami
plików, sesjami terminala, ustrukturyzowanymi komendami, artefaktami, patchami i
zarządzanymi środowiskami. Operacje mają tożsamość zasobu, kursory zdarzeń,
idempotency, recovery i często sterowanie dostępne tylko operatorowi. Workbench jest
więc specjalizacją wyższego ryzyka pod Sensorium Core, a nie zamiennikiem Sensorium OS.

## Czy zachowania Workbench można nazywać "Sensorium Workbench Actions"?

Na granicy `sensorium-directive.v1` są działaniami identyfikowanymi przez `action_id`.
Wewnątrz Workbench precyzyjniejszym terminem jest **operation**, ponieważ wiele
zachowań tworzy lub zmienia stanowy zasób: sesję terminala, komendę, przechwycony
artefakt albo zarządzane środowisko. W opisie domenowym używaj "operacji Workbench",
a "action id" podczas omawiania dispatchu Sensorium.

## Czy Inquirium albo Agent mogą bezpośrednio wykonać komendę?

Nie. Inquirium może zaproponować ustrukturyzowaną intencję; Agent albo JSON-e Flow może
przekształcić propozycję w dyrektywę. Sensorium i Workbench nadal walidują wołającego,
granty, `action_id`, parametry, profil komendy, workspace, czas, idempotency i bieżący
stan runtime'u. Wynik modelu jest dowodem albo poradą, nigdy uprawnieniem wykonawczym.

Agent, runda Corpus albo workflow Room może użyć
`sensorium-workbench-tool-request.v1` do przeniesienia zweryfikowanej proweniencji.
Wrapper nie tworzy dodatkowej władzy; daemon rozpakowuje go do zwykłej ścieżki
Sensorium.

## Czy JSON-e albo JSON-e Flow mogą używać Sensorium?

Tak. JSON-e Flow może wyrenderować `sensorium-directive.v1` i wywołać literalne
capability `sensorium.directive.invoke`. `allowed_calls` dopuszcza tylko taki statyczny
kształt wywołania. Host nadal sprawdza passport lub grant komponentu, a Sensorium -
katalog działań i politykę właściwą dla konektora.

Czyste JSON-e powinno wyłącznie budować albo normalizować dane. Nie może samodzielnie
wykonać efektu. Zobacz [HOWTO JSON-e i JSON-e
Flows](../howto/json-e-and-json-e-flows-howto.pl.md).

## Czy włączenie konektora autoryzuje jego działania?

Nie. Aktywacja procesu, rejestracja capability, autoryzacja katalogu działań,
uprawnienie wołającego i dopuszczenie wywołania są osobnymi bramkami. Działający
konektor może nie udostępniać żadnego efektywnego działania. Wpis katalogowy może być
autoryzowany, lecz chwilowo niedostępny, gdy brakuje wymaganego runtime'u albo izolacji.

To rozdzielenie jest celowe: instalacja nie jest władzą, a gotowość nie jest zgodą.

## Jak działa interaktywna zgoda operatora?

Daemon jest właścicielem maszyny stanów zgody i przedstawia pytanie przez powierzchnie
operator-question oraz notification. Uczestnik z aktywnym powiązaniem operatora węzła
może zezwolić jednorazowo, zapamiętać dokładną komendę, zapamiętać ograniczony prefiks
argv, zatwierdzić wpis katalogu Sensorium OS, odmówić albo później odwołać trwały grant.

Host projektuje udzieloną zgodę do sidecaru właściwego dla adaptera. Workbench otrzymuje
delty profili komend, a Sensorium OS - delty katalogu działań. Konektor scala sidecar z
główną konfiguracją tym samym walidatorem, którego używa przy starcie. Zgoda nie może
poszerzyć sieci, środowiska z poświadczeniami, timeoutu, limitu wyjścia, workspace ani
innych ograniczeń poza politykę operatora.

Trwałe decyzje można przeglądać i odwoływać pod `/operator/consents`. Autoryzacja
katalogu Sensorium OS ma osobny widok `/operator/sensorium-os`.

## Czy Sensorium wspiera operacje odroczone?

Tak. Wpis katalogu działania deklaruje tryb `sync-only`, `async-only` albo oba.
Asynchroniczna dyrektywa zwraca `deferred-operation.v1`; wspólny rejestr hosta jest
właścicielem pollingu, wygaśnięcia, anulowania i widoczności operatorskiej. Konektor
jest właścicielem stanu operacji domenowej, lecz nie może zmuszać wołającego do
wymyślenia prywatnej pętli pollingu.

Używaj `sensorium.operation.status` oraz, jeżeli operacja wystawia prawidłową ścieżkę
anulowania, `sensorium.operation.cancel`. Envelope odroczenia jest danymi control
plane, nie wynikiem domenowym działania.

## Gdzie trafiają duże wyniki i pliki?

Zwykłe wyniki powinny pozostać ograniczone. Konektor może zwrócić mały typowany wynik
oraz referencje do artefaktów. Duże lub trwałe bajty powinny przejść przez właściwy
magazyn artefaktów i Artifact Delivery, zamiast być kopiowane do obserwacji, faktów
audytowych, zdarzeń terminala lub śladów JSON-e.

Workbench ponownie sprawdza digest i rozmiar artefaktu przed użyciem. Jego publikacja
lub dostarczenie pozostają osobną decyzją. Zobacz [HOWTO dostarczania
artefaktów](../howto/artifact-delivery-howto.pl.md).

## Czy Sensorium publikuje każdą obserwację do innych węzłów?

Nie. Dopuszczenie obserwacji buduje lokalny model odczytowy. Lokalna projekcja do
Agory jest opcjonalna i nie jest ogólnym kontraktem zdalnego odczytu. Jawny zdalny
dostęp należy do Sensorium Interfaces, gdzie operator publikuje dokładną projekcję
źródła i nadaje ograniczone metody odczytu, subskrypcji albo sterowania.

Obecność na carrierze, członkostwo w Room ani znajomość id interfejsu nigdy nie
zastępują aktualnego grantu interfejsu.

## Jak komunikowane jest ryzyko żywego środowiska?

Workbench i inne odpowiednie źródła publikują `sensorium-operational-context.v1` z
klasą wpływu, taką jak `research`, `experimental`, `test`, `production` albo `critical`,
oraz ograniczonym opisem. Sensorium Interfaces propaguje ten niemutowalny kontekst
publikacji, aby konsumenci Agent, Corpus, Room i Inquirium mogli wybrać ostrożniejszą
politykę przed odczytem lub działaniem.

Kontekst jest dowodem, nie uprawnieniem. Konsument może podnieść efektywną klasę
ryzyka, ale nie może jej obniżyć. Zmiana generacji źródła albo zastąpienie publikacji
czyni stary kontekst nieaktualnym i zamyka odpowiednią ścieżkę odmową.

## Jak diagnozować odmowę działania?

Idź od zewnętrznej władzy do wewnętrznego mechanizmu:

1. potwierdź, że wołający może użyć `sensorium.directive.invoke`;
2. sprawdź `sensorium.directive.list` i efektywny katalog działań;
3. sprawdź gotowość konektora i dostępność konkretnego działania;
4. zweryfikuj parametry, timeout, klucz idempotency, workspace i profil komendy;
5. sprawdź diagnostykę zgody operatora lub sidecaru katalogu;
6. odczytaj outcome dyrektywy przez `sensorium.audit.read`;
7. dla pracy odroczonej sprawdź wspólny rekord deferred operation.

Nie zaczynaj od bezpośredniego wywołania prywatnego endpointu loopback konektora.
Omijałoby to tę samą granicę, której odmowę próbujesz wyjaśnić.

## Co jest zaimplementowane dzisiaj, a co pozostaje celowo niepełne?

Zaimplementowano dopuszczanie obserwacji i lokalny read model Sensorium Core, dispatch
dyrektyw, audyt outcome, wykonywanie działań C1/C2 Sensorium OS, autoryzację katalogu,
zgodę operatora i operacje odroczone. Sensorium Interfaces ma działające ścieżki
carrierów: lokalną host capability, uwierzytelnioną direct-peer, lokalną SSE oraz WSS
Room. Ich pokrycie jest celowo asymetryczne: SSE jest lokalnym adapterem
obserwacyjnym, Room przenosi obserwacyjny `latest-state` i zamknięte klasy aktuacji
P083, a ścieżki host-local i direct-peer udostępniają osobno autoryzowaną aktuację.

Workbench ma zaimplementowany fundament lokalny i zarządzany fixture, ustrukturyzowany
PTY, pliki, patche, artefakty, brokera, zgody, interfejsy i recovery. Przypięty obraz
pełnego systemu, produkcyjne dowody wdrożenia vfkit, w pełni zwirtualizowany adapter
Workbench i późniejsze backendy linuksowe pozostają pracą post-MVP. Dokumentacja i
polityka operatora nie mogą opisywać przyszłych backendów jako obecnych gwarancji
izolacji.

## Gdzie są kontrakty kanoniczne?

Zacznij od [Solution 030: Sensorium](../../project/60-solutions/030-sensorium/030-sensorium.md),
[Solution 042: Sensorium Workbench](../../project/60-solutions/042-sensorium-workbench/042-sensorium-workbench.md)
i [Solution 046: Sensorium Interfaces](../../project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md).
Główne uzasadnienia projektowe pozostają w Proposalach
[045](../../project/40-proposals/045-sensorium-local-enaction-stratum.md),
[048](../../project/40-proposals/048-sensorium-os-connector-action-classes.md),
[071](../../project/40-proposals/071-sensorium-workbench.md),
[082](../../project/40-proposals/082-sensorium-interfaces.md) i
[083](../../project/40-proposals/083-sensorium-interactive-interfaces.md).
