# Karta Korzenia Orbiplex-Main DIA

> **Projekt zmiany.** Zob. [tryb przyjęcia i przepisy przejściowe](../../40-constitution/pl/COMMUNITY-SELF-GOVERNMENT-AMENDMENT.pl.md).

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-ROOT-001` |
| `type` | Akt wykonawczy (poziom 3 hierarchii normatywnej) |
| `version` | 0.1.0 |
| `status` | Przyjęto wersję 0.1.0; przedstawione zmiany są projektem; aktywacja produkcyjna oczekuje |
| `basis` | Konstytucja DIA (zasady korzenia zaufania i odwołań); `ENTRENCHMENT-CLAUSE.pl.md`; `PANEL-SELECTION-PROTOCOL.pl.md`; `FEDERATION-MEMBERSHIP-AND-QUORUM.pl.md`; `doc/project/40-proposals/076-federation-identity-and-network-selector.md` (§4, §6, P076-004/013/014/026) |

---

## 1. Cel dokumentu

Proposal 076 definiuje *kształt* korzenia federacji `orbiplex-main`
(org-kind threshold root niesiony przez `federation-root.v1`) i jawnie
wyłącza ze swojego zakresu dostarczalne governance, które czynią ten korzeń
produkcyjnie wiarygodnym: konkretny skład kluczników, konkretne klucze
podpisujące, finalny próg custody, procedurę rotacji oraz organ odwoławczy.
Ta karta jest przyjętym domem governance dla tych dostarczalnych. Jej
przyjęcie czyni reguły realnymi, ale samo w sobie nie aktywuje produkcyjnego
autorytetu korzenia. Dopóki tabela składu i kluczy nie zostanie wypełniona,
produkcyjny pack `federation-root.v1` nie zostanie podpisany, a produkcyjne
pakowanie nie wyłączy bundled fixture, `orbiplex-main` pozostaje deweloperskim
fixture bootstrapowym i NIE WOLNO traktować go jako produkcyjnego autorytetu
korzenia (P076-004).

## 2. Zakres i granica autorytetu

Strażnicy kluczy (klucznicy lub klucznicy federacji) to osoby sprawujące pieczę nad kluczami
podpisującymi root pack federacji. Ich podpisy wykonują określone poniżej uprawnienia.
Założyciel, członek rady i arbiter mają odrębne mandaty, również gdy funkcje łączy jedna
osoba. Karta reguluje techniczną domenę zaufania wybieraną przez `orbiplex-main`. Nie
ustanawia konstytucji Emergatu ani ustroju społeczności korzystających z korzenia. Tożsamość
`root-identity` uczestnika podlega odrębnemu kontraktowi.

Karta reguluje: kwalifikowalność i skład kluczników, klucze custody, próg,
przebieg ceremonii root-packa, rotację i sukcesję, awaryjne usunięcie
klucznika, wystawianie endorsementów oficjalnych usług oraz ścieżkę
odwoławczą. Nie definiuje mechaniki schematów (Proposal 076), weryfikacji
runtime (loader Node i `capability-binding`) ani członkostwa w federacji w
ogólności (`FEDERATION-MEMBERSHIP-AND-QUORUM.pl.md`).

Nic w tej karcie nie może nadpisać weryfikacji kryptograficznej: pack lub
endorsement, który nie przechodzi kontroli podpisu bądź custody, pozostaje
odrzucony na czas trwania odwołania. Odwołania zmieniają to, *kto decyduje
dalej* — nigdy to, *co weryfikuje się teraz*.

## 3. Kształt korzenia i próg

- Korzeń `orbiplex-main` jest **org-kind threshold root**
  (`org:did:key:...`), którego polityka custody niesie purpose
  `federation-root`.
- Próg custody wynosi **co najmniej `2-z-3`**. Poprawka może go podnieść;
  żadna poprawka nie może go obniżyć poniżej `2-z-3`. Semantyka progu za
  Proposal 076: M-z-N unikalnych autoryzowanych kluczy podpisujących, nie
  M-z-N osób.
- Skład MUSI liczyć co najmniej 3 klucze kluczników w każdym momencie.

<a id="4-skad-kustoszy"></a>

## 4. Skład kluczników

| Miejsce | Tożsamość klucznika (`participant:did:key:...`) | Odcisk klucza (`z...`) | Od |
| :--- | :--- | :--- | :--- |
| 1 | *TBD — nominacja governance w toku* | *TBD* | — |
| 2 | *TBD — nominacja governance w toku* | *TBD* | — |
| 3 | *TBD — nominacja governance w toku* | *TBD* | — |

Kwalifikowalność (za P076-013):

- tożsamość klucznika to **dedykowana tożsamość operacyjna**, używana
  wyłącznie do zatwierdzania root-packów, rotacji i ceremonii odzyskiwania,
- NIE MOŻE być nymem, zwykłą tożsamością operatora ani kluczem codziennego
  uczestnika; żyje w **osobnym `data-dir` klucznika**,
- klucz klucznika MOŻE atestować lub autoryzować oddzielną tożsamość operatora
  przez jawny artefakt wiązania, ale NIE MOŻE być konwertowany, promowany ani
  wyprowadzany do pełnej tożsamości operatora,
- żadna pojedyncza osoba fizyczna ani organizacja nie może kontrolować
  liczby kluczy kluczników wystarczającej do samodzielnego spełnienia progu,
- miejsce klucznika zwalnia się przez rezygnację, potwierdzoną kompromitację
  klucza albo usunięcie w trybie §7.

## 5. Klucze

- Klucze kluczników to dedykowane klucze Ed25519 generowane podczas ceremonii
  narzędziami P076-014; nigdy nie są reużywane w żadnej innej roli klucza.
- Materiał prywatny przechowywany jest wyłącznie jako zaszyfrowany sekret
  kontrolowany przez klucznika: zaszyfrowany ceremony PEM wygenerowany
  narzędziami P076-014 albo zaszyfrowany przepływ `data-dir` klucznika.
  Passphrase jest podawana przez prompt albo stdin, nigdy jako argument
  powłoki, a każdy plik passphrase użyty do automatyzacji offline musi być
  prywatny, krótkotrwały i obsługiwany oddzielnie od zaszyfrowanego klucza.
- Podejrzenie kompromitacji dowolnego klucza klucznika uruchamia §7 bez
  czekania na dowód nadużycia — rotacja jest tania, trwająca kompromitacja
  nie.

## 6. Ceremonia

Wydania root-packa podążają za zamrożonym kształtem ceremonii (P076-026):
autorstwo packa → digest manifestu → niezależna weryfikacja digestu przez
każdego sygnatariusza → odłączone podpisy zbierane offline → deterministyczne
złożenie → weryfikacja → publikacja. `pack_version` rośnie monotonicznie;
loadery odrzucają rollback i podmianę digestu przy tej samej wersji. Każdy
sygnatariusz weryfikuje dokładnie te bajty, które podpisuje; żaden klucznik
nie podpisuje digestu, którego sam nie wyprowadził.

## 7. Rotacja, sukcesja i awaryjne usunięcie

- **Rotacja planowa**: skład ustępujący i wchodzący współpodpisują pack
  przejściowy w oknie nakładania, po czym skład wchodzący podpisuje kolejny
  pack samodzielnie. Długość okna ustala się per rotacja i zapisuje w
  dokumencie `policy_ref` packa.
- **Usunięcie awaryjne** (kompromitacja lub niezdolność): pozostali
  klucznicy, spełniając próg bez dotkniętego klucza, podpisują nowy pack
  usuwający go. Jeżeli progu nie da się spełnić bez dotkniętego klucza,
  organ odwoławczy (§9) zwołuje nadzwyczajne obsadzenie składu.
- Rotacja wygasza autorytet pochodny za darmo: endorsementy i inne artefakty
  weryfikowane względem aktywnego packa przestają się rozwiązywać, gdy ich
  sygnatariusze opuszczają skład (Proposal 076 §6).

## 8. Endorsementy oficjalnych usług

Skład działa jako suwerenny org-subject `orbiplex-main` dla wystawiania
`federation-service-endorsement.v1` (Proposal 076 §6): wystawienie wymaga
progu custody (ceremonia per P076-018); **rewokacja jest celowo
asymetryczna** — dowolny pojedynczy autoryzowany klucz klucznika może
odwołać, ponieważ jednostronne wycofanie zawęża zaufanie i jest fail-safe.

## 9. Ścieżka odwoławcza

- Organ odwoławczy wyłaniany jest wg `PANEL-SELECTION-PROTOCOL.pl.md`, z
  regułami konfliktu interesów stosowanymi względem bieżącego składu (żaden
  urzędujący klucznik, ani tożsamość operacyjnie z nim związana, nie może
  zasiadać w panelu oceniającym decyzję tego składu).
- Sprawy odwoławcze: kwestionowana rotacja lub usunięcie, odmowa
  wystawienia bądź odwołania endorsementu oficjalnej usługi oraz
  kwestionowane poprawki polityki custody.
- Rozstrzygnięcie odwołania wiąże skład do ponownego przeprowadzenia
  zakwestionowanej decyzji zgodnie z ustaleniem panelu; nigdy nie zastępuje
  progu custody podpisem panelu.

## 10. Poprawki

Poprawki tej karty wymagają obowiązującego progu custody i MUSZĄ respektować
`ENTRENCHMENT-CLAUSE.pl.md`. Wersja karty rośnie przy każdej poprawce;
`policy_ref` root-packa POWINIEN wskazywać wersję karty, pod którą pack
został podpisany. Profil ceremonii produkcyjnej hard-MVP egzekwuje
maszynowo-czytelną konwencję `policy:dia-root-001@<charter-version>`, na
przykład `policy:dia-root-001@0.1.0#appeals`.

## 11. Status przyjęcia

Przyjęcie karty 0.1.0 obejmowało samą kartę. Konstytucja wskazana w jej podstawie
była wówczas projektem i nadal ma ten status.

Przyjęto **pierwotny akt wykonawczy** (0.1.0). Jego zmiana wymaga trybu z §10. Tabela
składu i kluczy jest celowo niewypełniona do czasu ceremonii aktywacyjnej.
Aktywacja produkcyjna wymaga: trzech nazwanych tożsamości kluczników z
wygenerowanymi kluczami, podpisanego produkcyjnego packa
`federation-root.v1` zastępującego bundled fixture oraz produkcyjnego pakowania
wyłączającego `federation.allow_bundled_fixture_root` (Proposal 076, Next
Actions 1–2). Do tego czasu każdy konsument MUSI traktować zaufanie
`orbiplex-main` jako deweloperskie.
