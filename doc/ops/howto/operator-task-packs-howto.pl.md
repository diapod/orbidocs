# HOWTO pakietów zadań operatora

Pełny przewodnik po zaimplementowanej ścieżce znajduje się przy właścicielach Node:
[HOWTO po polsku](https://github.com/diapod/node/blob/master/docs/operations/TASK-PACKS.pl.md)
i [HOWTO po angielsku](https://github.com/diapod/node/blob/master/docs/operations/TASK-PACKS.en.md).
Przykłady komend w obu językach sprawdza faktyczny parser CLI; taka walidacja
nie uprawnia do wykonania efektów.

Procedura obejmuje inspekcję pakietu, przygotowanie przypiętego obrazu qmail,
conformance i aktywację, restrykcyjny lokalny binding i diff profilu, readiness,
zatwierdzenie dokładnej oferty, zadanie lokalne lub z kolejki zdalnej, HIL dla
każdej mutacji, dowody weryfikacji/destrukcji, pause/resume, recovery, withdrawal
i revokację. Używa istniejących API, bez przedstawiania planowanych komend jako gotowych.

Checkpoint developerski kontynuacji komunikacji dodaje do strony uczestników
dokładny podgląd epoki, zatwierdzenie i recovery przerwanego przygotowania Roomu.
Zachowuje pierwotny łączny budżet i termin pętli, ale nie dziedziczy członkostwa
ani zgód na efekty. Adopcja historycznego kandydata i routing zadania między
epokami nie są jeszcze zaimplementowane; nie jest to pełna kwalifikacja
prowadzonej kontynuacji. HOWTO Node opisuje wynikającą z tego odmowę pozycji.

Pochodzenie pakietu, lokalne zaufanie i bieżący autorytet wykonania są odrębne.
[Proposal 094](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)
jest właścicielem ograniczeń i decyzji; [Story 013](../../project/30-stories/story-013-qmail-task-pack.md)
definiuje przykład qmail. Bramka odmów zachowuje historyczne klasy dowodów
natywnych/fizycznych, nie przyjmuje proposala ani nie ogłasza gotowości alfy.
Limit historii bindingów i brak recovery po migracji relaya są jawne w HOWTO,
nie ukryte pod automatycznym retry.
