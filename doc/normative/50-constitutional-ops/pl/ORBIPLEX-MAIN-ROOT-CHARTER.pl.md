# Karta Korzenia Orbiplex-Main DIA

## Status dokumentu

| Pole | Wartość |
| :--- | :--- |
| `policy-id` | `DIA-ROOT-001` |
| `type` | Akt wykonawczy (poziom 3 hierarchii normatywnej) |
| `version` | 0.1.0-draft |
| `basis` | Konstytucja DIA (zasady korzenia zaufania i odwołań); `ENTRENCHMENT-CLAUSE.pl.md`; `PANEL-SELECTION-PROTOCOL.pl.md`; `FEDERATION-MEMBERSHIP-AND-QUORUM.pl.md`; `doc/project/40-proposals/076-federation-identity-and-network-selector.md` (§4, §6, P076-004/013/014/026) |

---

## 1. Cel dokumentu

Proposal 076 definiuje *kształt* korzenia federacji `orbiplex-main`
(org-kind threshold root niesiony przez `federation-root.v1`) i jawnie
wyłącza ze swojego zakresu dostarczalne governance, które czynią ten korzeń
produkcyjnie wiarygodnym: konkretny skład kustoszy, konkretne klucze
podpisujące, finalny próg custody, procedurę rotacji oraz organ odwoławczy.
Ta karta jest domem dla tych dostarczalnych. Dopóki nie zostanie przyjęta w
wersji `1.0.0` lub wyższej z wypełnionym składem, `orbiplex-main` pozostaje
deweloperskim fixture bootstrapowym i NIE WOLNO traktować go jako
produkcyjnego autorytetu korzenia (P076-004).

## 2. Zakres i granica autorytetu

Karta reguluje: kwalifikowalność i skład kustoszy, klucze custody, próg,
przebieg ceremonii root-packa, rotację i sukcesję, awaryjne usunięcie
kustosza, wystawianie endorsementów oficjalnych usług oraz ścieżkę
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
- Skład MUSI liczyć co najmniej 3 klucze kustoszy w każdym momencie.

## 4. Skład kustoszy

| Miejsce | Tożsamość kustosza (`participant:did:key:...`) | Odcisk klucza (`z...`) | Od |
| :--- | :--- | :--- | :--- |
| 1 | *TBD — nominacja governance w toku* | *TBD* | — |
| 2 | *TBD — nominacja governance w toku* | *TBD* | — |
| 3 | *TBD — nominacja governance w toku* | *TBD* | — |

Kwalifikowalność (za P076-013):

- tożsamość kustosza to **dedykowana tożsamość operacyjna**, używana
  wyłącznie do zatwierdzania root-packów, rotacji i ceremonii odzyskiwania,
- NIE MOŻE być nymem, zwykłą tożsamością operatora ani kluczem codziennego
  uczestnika; żyje w **osobnym `data-dir` kustosza**,
- żadna pojedyncza osoba fizyczna ani organizacja nie może kontrolować
  liczby kluczy kustoszy wystarczającej do samodzielnego spełnienia progu,
- miejsce kustosza zwalnia się przez rezygnację, potwierdzoną kompromitację
  klucza albo usunięcie w trybie §7.

## 5. Klucze

- Klucze kustoszy to dedykowane klucze Ed25519 generowane podczas ceremonii
  narzędziami P076-014; nigdy nie są reużywane w żadnej innej roli klucza.
- Materiał prywatny przechowywany jest w zaszyfrowanym przepływie `data-dir`
  kustosza (passphrase wyłącznie przez stdin; nigdy w argumentach powłoki
  ani plikach jawnych).
- Podejrzenie kompromitacji dowolnego klucza kustosza uruchamia §7 bez
  czekania na dowód nadużycia — rotacja jest tania, trwająca kompromitacja
  nie.

## 6. Ceremonia

Wydania root-packa podążają za zamrożonym kształtem ceremonii (P076-026):
autorstwo packa → digest manifestu → niezależna weryfikacja digestu przez
każdego sygnatariusza → odłączone podpisy zbierane offline → deterministyczne
złożenie → weryfikacja → publikacja. `pack_version` rośnie monotonicznie;
loadery odrzucają rollback i podmianę digestu przy tej samej wersji. Każdy
sygnatariusz weryfikuje dokładnie te bajty, które podpisuje; żaden kustosz
nie podpisuje digestu, którego sam nie wyprowadził.

## 7. Rotacja, sukcesja i awaryjne usunięcie

- **Rotacja planowa**: skład ustępujący i wchodzący współpodpisują pack
  przejściowy w oknie nakładania, po czym skład wchodzący podpisuje kolejny
  pack samodzielnie. Długość okna ustala się per rotacja i zapisuje w
  dokumencie `policy_ref` packa.
- **Usunięcie awaryjne** (kompromitacja lub niezdolność): pozostali
  kustosze, spełniając próg bez dotkniętego klucza, podpisują nowy pack
  usuwający go. Jeżeli progu nie da się spełnić bez dotkniętego klucza,
  organ odwoławczy (§9) zwołuje nadzwyczajne obsadzenie składu.
- Rotacja wygasza autorytet pochodny za darmo: endorsementy i inne artefakty
  weryfikowane względem aktywnego packa przestają się rozwiązywać, gdy ich
  sygnatariusze opuszczają skład (Proposal 076 §6).

## 8. Endorsementy oficjalnych usług

Skład działa jako suwerenny org-subject `orbiplex-main` dla wystawiania
`federation-service-endorsement.v1` (Proposal 076 §6): wystawienie wymaga
progu custody (ceremonia per P076-018); **rewokacja jest celowo
asymetryczna** — dowolny pojedynczy autoryzowany klucz kustosza może
odwołać, ponieważ jednostronne wycofanie zawęża zaufanie i jest fail-safe.

## 9. Ścieżka odwoławcza

- Organ odwoławczy wyłaniany jest wg `PANEL-SELECTION-PROTOCOL.pl.md`, z
  regułami konfliktu interesów stosowanymi względem bieżącego składu (żaden
  urzędujący kustosz, ani tożsamość operacyjnie z nim związana, nie może
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
przykład `policy:dia-root-001@1.0.0#appeals`.

## 11. Status przyjęcia

Ten dokument jest **szkicem szkieletowym** (0.1.0-draft): tabela składu i
kluczy jest celowo niewypełniona. Przyjęcie w `1.0.0` wymaga: trzech
nazwanych tożsamości kustoszy z wygenerowanymi kluczami, podpisanego
produkcyjnego packa `federation-root.v1` zastępującego bundled fixture oraz
produkcyjnego pakowania wyłączającego
`federation.allow_bundled_fixture_root` (Proposal 076, Next Actions 1–2).
Do tego czasu każdy konsument MUSI traktować zaufanie `orbiplex-main` jako
deweloperskie.
