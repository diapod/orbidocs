# Memarium FAQ

Memarium jest lokalnym organem pamięci węzła, a nie ogólnym interfejsem do
bazy danych. Poniższe odpowiedzi wyjaśniają przede wszystkim granice:
co jest faktem, co projekcją, kto może wywołać skutek oraz kiedy brak
autorytetu musi zakończyć się odmową.

Procedury operatorskie znajdują się w [Memarium HOWTO](../howto/memarium-howto.pl.md).

## Czym Memarium różni się od zwykłego magazynu dokumentów?

Magazyn odpowiada przede wszystkim na pytanie "gdzie zapisać bajty?". Memarium
odpowiada na trudniejsze pytanie: "w jakiej przestrzeni pamięci wolno utrwalić
ten fakt, pod jaką klasyfikacją, z jaką retencją, możliwością zapomnienia i
ścieżką audytu?".

Dlatego Memarium nie udostępnia ambient authority wynikającego z samego faktu,
że kod działa w procesie węzła. Zapis, odczyt, promocja, zapomnienie i
deklasyfikacja przechodzą przez jawne kontrakty oraz policy gates.

## Jak wybrać przestrzeń pamięci?

- **Personal** przechowuje pamięć właściciela węzła. Jest szyfrowana i nie
  opuszcza węzła bez jawnego eksportu.
- **Community** przechowuje wiedzę wspólnoty. Wymaga `community_id`, klucza
  wspólnoty i procedur zarządczych właściwych tej wspólnocie.
- **Public** przechowuje treści przeznaczone do jawnego wykorzystania lub
  publikacji. Publiczna przestrzeń nie znosi wymogu klasyfikacji ani
  pochodzenia danych.
- **Crisis** przechowuje materiały potrzebne w sytuacjach awaryjnych. Ma
  konstytucyjne minimum retencji i odrębne reguły rozwiązania aktywnego alarmu.

Przestrzeń jest policy envelope, nie osobną bazą. Przeniesienie treści między
przestrzeniami jest nowym, audytowalnym przejściem, a nie zmianą etykiety na
istniejącym rekordzie.

## Dlaczego Memarium wymaga passportu?

Passport jest zewnętrzną, podpisaną i odwoływalną reprezentacją autorytetu.
Wiąże wywołującego z capability, przestrzenią, klasą artefaktu i – tam, gdzie
to potrzebne – identyfikatorem wspólnoty albo powierzchnią egress.

Bez passportu daemon musiałby uznawać, że kod uruchomiony "wewnątrz" jest
zaufany, albo powielać rozpoznawanie operatora, modułu i delegata w każdym
silniku domenowym. Pierwsza możliwość tworzy ambient authority, druga splątuje
warstwy. Memarium stosuje trzeci wariant: bramka autoryzuje, silnik wykonuje.

Pełne uzasadnienie architektoniczne, obejmujące rozdzielenie A0/A1/A2,
odwoływalną delegację, audyt przyczynowy i authority Crisis, zachowuje
[Solution 002](../../project/60-solutions/002-memarium/002-memarium.md#why-the-passport-gate-is-architectural).

## Czy token HTTP zastępuje passport?

Nie. Token uwierzytelnia kanał i pozwala hostowi rozpoznać wywołującego.
Passport odpowiada na inne pytanie: czy ten wywołujący może wykonać konkretną
operację na konkretnym zakresie. Poprawne uwierzytelnienie bez pasującego
passportu kończy się `passport_lookup_failed` albo inną dokładniejszą odmową.

## Czy klasyfikacja jest częścią payloadu?

Klasyfikacja jest osobnym, pierwszoklasowym kontraktem `classification.v1`.
Nie należy ukrywać jej w `attributes`, `fields` ani tekście dokumentu. Dzięki
temu adapter egress może wyliczyć dopuszczalną projekcję dla dokładnej
powierzchni, tematu i chwili, nie zgadując intencji producenta.

Brak wymaganej klasyfikacji nie oznacza "publiczne". W trybie ścisłym oznacza
odmowę. W kontrolowanym trybie migracyjnym może oznaczać oznaczenie jako
Personal oraz kwarantannę, lecz ten wyjątek jest mierzony i ma warunki
wygaszenia.

## Czy deklasyfikacja zmienia zapisany fakt?

Nie. `memarium.declassify` dopisuje osobny fakt polityki. Źródłowy tier,
payload i historia pozostają niezmienne. Deklasyfikacja jest związana z
powierzchnią, klasą tematu, trybem użycia, czasem oraz aktualnym widokiem
odwołań.

Dlatego "można opublikować ten fakt w Agora" nie znaczy "fakt stał się
publiczny wszędzie". Jednorazowa zgoda jest konsumowana przed skutkiem, a
brak świeżego widoku revocation czyni wyjątek nieaktywnym.

## Czym różnią się `forget`, kwarantanna i deklasyfikacja?

- **Forget** usuwa dostępność danych zgodnie z polityką przestrzeni. Personal
  może dopuścić natychmiastowe zapomnienie, Community wymaga governance ref,
  Public pozostawia tombstone, a Crisis jest restrykcyjne.
- **Kwarantanna** zatrzymuje wykorzystanie rekordu do czasu decyzji operatora.
  Akceptacja albo odrzucenie są osobnymi faktami i nie przepisują historii.
- **Deklasyfikacja** dopuszcza węższe użycie danych na określonej powierzchni.
  Nie jest usunięciem ani ogólnym obniżeniem tieru źródłowego.

## Czy obserwator Memarium może zablokować wiadomość?

Nie. Post-chain i phase observers są ścieżką obserwacyjną: widzą efektywny
payload i wynik dispatchu, lecz nie mogą zmienić decyzji, payloadu ani wyniku.
Awaria zapisu obserwacyjnego może pogorszyć diagnostykę, ale nie staje się
ukrytym drugim systemem admission.

Jeżeli dana operacja wymaga autorytatywnego zapisu przed skutkiem, wywołujący
powinien użyć jawnego `memarium.write`, a nie polegać na obserwatorze.

## Czy SQLite sidecar jest źródłem prawdy?

Nie. Źródłem prawdy pozostają append-only streams wpisów i faktów. SQLite
sidecar jest odbudowywalną projekcją przyspieszającą point reads i odczyty
polityki. Startup wykonuje catch-up, a skan strumieni pozostaje ścieżką
poprawności, gdy sidecar jest wyłączony lub wymaga odbudowy.

Nie należy naprawiać Memarium przez ręczną edycję sidecaru. Taka zmiana nie
tworzy faktu, nie przechodzi policy gate i zniknie przy odbudowie.

## Czy Memarium replikuje się automatycznie między węzłami?

Nie jako ogólny mechanizm. Publiczne artefakty mogą być przekazywane przez
Agora, a materiały archiwalne przez Artifact Delivery, lecz są to jawne
handoffs z klasyfikacją i provenance. Community nie przekracza granicy
federacji przez samo członkostwo w Roomie lub grupie.

Pełna, automatyczna federacyjna replikacja Memarium pozostaje poza kontraktem
v1. Carrier nie staje się przez to właścicielem polityki pamięci.

## Kto może rozwiązać alarm w przestrzeni Crisis?

Detektor może dopisać `crisis-detected` i automatyczne `crisis-resolved`, gdy
warunek faktycznie ustąpi. Wymuszone rozwiązanie przez
`memarium.crisis_resolve` jest operacją operatorską, wymaga reason i nie usuwa
historii alarmu.

Samo kliknięcie "resolved" nie naprawia źródła problemu. Operator powinien
najpierw sprawdzić warunek opisany w
[runbooku detektorów](../runbooks/crisis-detectors.md), a dopiero potem dopisać
jawny fakt rozstrzygnięcia.

## Gdzie szukać przyczyny odmowy?

Klient powinien interpretować stabilne pole `status`, nie tekst `reason`.
Najczęstsze klasy to brak lub nieważność passportu, nieświeży revocation view,
naruszenie polityki przestrzeni, kwarantanna, brak deklasyfikacji oraz awaria
storage. Odpowiedź i audit decision mają wspólną przyczynę oraz correlation id;
diagnostyka nie powinna być rekonstruowana z luźnych logów.

Pełny zamknięty słownik statusów należy do
[Solution 002](../../project/60-solutions/002-memarium/002-memarium.md).
