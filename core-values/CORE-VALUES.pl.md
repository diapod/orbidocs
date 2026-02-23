# CORE VALUES — Distributed Intelligence Agency / Orbiplex

Poniższe wartości są zaprojektowane jako **etyczny rdzeń konstytucyjny** dla projektu
rozproszonego systemu skomunikowanych agentów AI (DIA) oraz jego warstwy technicznej
(Orbiplex). Każda z nich ma brzmieć jak zasada, którą da się zastosować w sporach
architektonicznych, produktowych i etycznych.

## 1. Suwerenność użytkownika i jego danych

System ma wzmacniać sprawczość człowieka, a nie zastępować go ani uzależniać:
użytkownik jest właścicielem swoich danych, swoich polityk i swoich agentów. Orbiplex
powinien działać sensownie także w trybie "samotnej wyspy" (offline / self‑hosted),
a integracje z chmurą mają być opcją, a nie warunkiem. W praktyce oznacza to
eksportowalność, możliwość migracji, brak ukrytych formatów i brak wymuszonych
subskrypcji na poziomie protokołu.

## 2. Anti‑lock‑in jako cecha protokołu, nie marketingu

Jeżeli coś ma być wolnością, musi być wolnością techniczną: interfejsy, formaty
i semantyka powinny być publiczne, wersjonowane i testowalne. Orbiplex nie może
"sprzedawać wolności" przez obietnice, a jednocześnie wiązać użytkownika detalami
implementacyjnymi bądź tajnym routingiem. Lock‑in najczęściej rodzi się w miejscach
niewidocznych (metadane, telemetria, polityki kosztowe), więc projekt ma obowiązek
robić te miejsca jawnymi.

## 3. Kultura współdziałania

DIA ma być infrastrukturą dla wspólnoty twórców i użytkowników: dzielenie się
narzędziami, praktykami i perspektywami jest częścią produktu. To nie jest romantyzm,
lecz strategia odporności: gdy wiedza krąży, system jest mniej kruchy, a jakość
rośnie. Warto projektować ścieżki, w których wkład społeczności (reguły, konektory,
polityki, prompty, testy) jest naturalny i nagradzany uznaniem.

## 4. Rzemiosło ponad fajerwerki

Preferujemy rozwiązania proste, czytelne i odporne, nawet jeżeli nie są najbardziej
efektowne w krótkim terminie. Rzemiosło oznacza tu: minimalne, dobrze nazwane
abstrakty; brak magicznych skrótów; kontrakty danych; testowalność; oraz zdolność do
diagnostyki po miesiącach. To ma być system, który starzeje się godnie – nie demo,
które błyszczy, dopóki nie dotknie go rzeczywistość.

## 5. Inżynieria oparta o kontrakty

W Orbipleksie liczy się kontrakt: wejście/wyjście, semantyka, kryteria *done*,
ograniczenia wykonania, klasy błędów i *retry-ability*. Kontrakt jest ważniejszy niż
najlepszy model czy najsprytniejszy agent. Ta wartość prowadzi do architektury, w
której komponenty są autonomiczne, a integracja nie staje się tajną religią opartą o
domysły.

## 6. Bezpieczeństwo jako model zagrożeń (a nie ozdoba)

Security nie jest checkboxem, tylko sposobem myślenia o świecie: Sybil, DoS, wycieki,
eskalacje uprawnień, kompromitacje węzłów, złośliwe plug-iny, *prompt injection*, *data
poisoning*. Protokoły zaufania, reputacji i autoryzacji muszą być pierwszorzędne, tak
samo jak PFS, rotacja kluczy i minimalizacja powierzchni ataku. System ma być
"cypherpunk-pragmatic": spokojny, rzeczowy i weryfikowalny.

## 7. Prywatność i godność jako domyślna konfiguracja

Domyślnie zakładamy minimalną ekspozycję: lokalność danych, selektywne ujawnianie,
sensowne anonimizacje oraz przejrzyste polityki logowania. Telemetria ma być
*opt-in*, a logi projektowane tak, by nie zdradzały tego, czego zdradzać nie
muszą. Wartość godności oznacza też: żadnych ukrytych kanałów podsłuchu oraz
mechanizmów, które czynią użytkownika surowcem.

## 8. Przejrzystość działania agentów

Użytkownik ma móc zrozumieć: dlaczego agent wykonał daną czynność, na jakich danych,
w jakiej wersji zasad i z jakim kosztem. Preferujemy ślady działania (trace), które
są czytelne i eksportowalne, zamiast czarnej skrzynki. Transparentność nie ma
oznaczać wylewania promptów i sekretów, ale dostarczenie rozumnej "księgowości
przyczynowości".

## 9. Odpowiedzialna autonomia: agent ma granice

Autonomia agentów jest narzędziem, a nie ideologią. Agent powinien mieć jasno
określone uprawnienia, budżety, limity czasu, zakres operacji i mechanizmy
zatrzymania (kill-switch) oraz bezpieczne tryby dla środowisk
korporacyjnych. Orbiplex ma umieć działać w reżimach compliance bez degenerowania w
bezużyteczny produkt.

## 10. Minimalny zaufany rdzeń, reszta jako moduły

Rdzeń protokołu ma być mały, audytowalny i stabilny; innowacje mają żyć w modułach i
rozszerzeniach. To broni przed „pęcznieniem” systemu oraz przed niejawnie rosnącą
złożonością. W praktyce oznacza to: cienkie interfejsy zachowań, walidację na
brzegach, a nie w środku — oraz świadome projektowanie punktów rozszerzeń.

## 11. Odporność na zmienność świata

Środowiska, kontenery, wersje systemów, polityki korporacyjne, ograniczenia
sieciowe — to nie są wyjątki, lecz norma. DIA/Orbiplex powinien zakładać, że kontekst
będzie się zmieniał i że działanie w różnych warunkach jest częścią życia
systemu. Preferujemy strategie, które wytrzymują degradację: fallbacki, tryby
offline, komunikację *proxy-friendly* i sensowne *retry*.

## 12. Weryfikowalność zamiast wiary

W projekcie agentowym łatwo odpłynąć w narrację; my chcemy stać na faktach. Tam,
gdzie się da, wprowadzamy pomiary, testy, benchmarki, metryki jakości i mechanizmy
detekcji regresji. Gdy coś jest spekulacją, nazywamy to spekulacją i projektujemy
eksperyment, który ją obali albo wzmocni.

## 13. Wieloparadygmatowość i pluralizm

Świat nie jest jedną ontologią: czasem liczy się formalna poprawność, czasem
użyteczność, czasem bezpieczeństwo, a czasem sens dla człowieka. DIA ma umieć trzymać
wiele trybów poznawczych bez wojny ideologicznej: od twardej inżynierii po język
fenomenologii doświadczenia. To przekłada się na architekturę: różne agenty, różne
kryteria kompletności i różne zasady dowodu.

## 14. Human‑in‑the‑loop jako domyślna ścieżka mocy

Największa moc systemu ma przechodzić przez człowieka, nie obok człowieka. Domyślne
UX to: propozycje, warianty, porównania, uzasadnienia, a nie "zrobiłem, bo
mogłem". Automatyzacja ma być stopniowalna, a nie skokowa, ponieważ zaufanie buduje
się iteracyjnie.

## 15. Emocje i znaczenie jako telemetria (bez psychologizowania)

Ludzie nie są tylko operatorami — ich odczucia (tarcie, ulga, niepokój, ekscytacja)
są informacją o jakości dopasowania systemu do życia. DIA może to szanować, np. przez
tryby pracy, tempo zmian, jasne komunikaty i kontrolę nad intensywnością
interakcji. Jednocześnie system nie ma udawać terapeuty: ma być narzędziem, które
wspiera człowieczeństwo.

## 16. Anty‑sekciarstwo i higiena epistemiczna

Projekty AI łatwo stają się "kościołami": objawienia, osobowi liderzy,
niekwestionowane dogmaty. My wybieramy higienę: rozdział między hipotezą a faktem,
przestrzeń na krytykę, powtarzalne procedury i możliwość wyjścia. W kulturze projektu
cenimy kompetencję, ale nie idolatrię.

## 17. Koszt i energia jako element etyki

Optymalizujemy nie tylko dla działania, ale też dla kosztu, energii i zasobów:
sprzęt, prąd, czas człowieka, koszty tokenów i utrzymania. To jest etyka inżynierska:
nie produkować marnotrawstwa, nie przerzucać kosztów na użytkownika, ani nie budować
skomplikowanych monumentów. System ma być wydajny, bo szanuje świat.

## 18. Uczciwe granice i jawne kompromisy

Każdy system ma *trade-offy*: bezpieczeństwo vs wygoda, autonomia vs kontrola,
prywatność vs personalizacja. W DIA te kompromisy mają być jawne, nazwane i możliwe
do skonfigurowania. Uczciwość oznacza też: jeśli czegoś nie wiemy, mówimy "nie wiemy"
i projektujemy drogę do wiedzy.

## 19. Estetyka prostoty i klarowności

Klarowność jest funkcją etyczną: zmniejsza liczbę błędów, obniża próg wejścia i
ułatwia audyt. Preferujemy proste nazwy, proste przepływy i formaty – takie, które
niosą sens i nie ukrywają złożoności w miejscach, gdzie ta złożoność ma
konsekwencje. Estetyka jest tu narzędziem prawdy.

## 20. Sprawczość zbiorowa: roje, węzły, wspólnota

DIA ma wzmacniać zdolność ludzi do wspólnego działania: małe zespoły,
mikro-wspólnoty, federacje, koalicje ad-hoc. Architektura roju nie jest tylko
techniką, ale też polityką: rozproszenie, brak pojedynczego punktu dominacji,
możliwość lokalnych norm i konsensualnej reputacji. Orbiplex powinien umożliwiać, aby
wiedza i inteligencja były dystrybuowane nie tylko w maszynach, ale też w relacjach
między ludźmi.

## 21. Rój jako nawigator i filtr w kulturze poliwersyjnego przekazu

W kulturze poliwersyjnego przekazu (wiele równoległych wersji treści, kontekstów i
intencji) rój nie może być tylko wzmacniaczem sygnału. Jego rolą jest nawigacja:
łączenie źródeł, oznaczanie pochodzenia, porównywanie wariantów i wskazywanie ścieżek
decyzyjnych adekwatnych do celu użytkownika. Rój ma też działać jak filtr
epistemiczny: redukować szum, wykrywać manipulacje, eksponować niepewność i oddzielać
hipotezy od faktów, bez centralnej cenzury i bez tłumienia pluralizmu.

## 22. Zrównoważanie i demokratyzacja

Wiedza i inteligencja nie mogą być trwale monopolizowane przez centra kapitału,
instytucjonalne skupiska władzy ani kartele danych. Architektura roju ma aktywnie
równoważyć tę asymetrię: dystrybuować dostęp do informacji, umożliwiać lokalną
weryfikację oraz wzmacniać wspólnotowe modele tworzenia i oceny wiedzy.
Demokratyzacja nie oznacza chaosu, lecz sprawiedliwszy rozkład zdolności
poznawczych i decyzyjnych, w którym pojedynczy aktor nie przejmuje dominacji tylko
dlatego, że ma większy budżet lub infrastrukturę.

## 23. Sprawiedliwość proceduralna i reprezentacja pokrzywdzonych

Deklaratywna równość wobec prawa i instytucji nie wystarcza, gdy dostęp do
informacji, kompetencji i narzędzi obrony jest nierówny. Rój ma wyrównywać tę
asymetrię: przekładać wiedzę ekspercką i faktyczne zdolności partycypujących (zarówno
węzłów jak i ich użytkowników) na zrozumiałe ścieżki działania, a w razie zauważenia
krzywdy uczestnika uruchamiać kolektywne wsparcie i chronić integralność faktów,
dokumentacji oraz przetrwania węzła i jego właściciela. Na styku węzły-społeczność
system powinien umożliwiać akcje pomocowe (nawigacja po procedurach, asysta
eskalacyjna, niezależna weryfikacja danych, świadkowanie przebiegu sprawy, wsparcie
materialne i operacyjne), tak aby osoba w kryzysie wywołanym krzywdzącymi
okolicznościami odzyskiwała autonomię i sprawczość bez przemocy i bez logiki
samosądu. Miarą tej wartości jest realna zdolność człowieka do obrony swoich praw,
zdrowia i godności, oraz do korzystania z tych praw samodzielnie, a także ze
wsparciem społeczności oraz kolektywnej inteligencji roju.

## 24. Godność jest najważniejsza

Godność osoby ludzkiej jest wartością najważniejszą. Odpieranie nagłych zagrożeń
bezpośrednio niszczących godność ma wyższy priorytet niż inne wartości. W przypadkach
decyzji i działań mogących stwarzać podczas gwarantowania ochrony godności konflikty
z innymi wartościami wymagana jest decyzja operatora węzła o kontynuacji.
