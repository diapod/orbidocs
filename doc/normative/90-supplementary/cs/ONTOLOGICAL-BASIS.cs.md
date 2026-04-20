# Ontologický základ

<p align="center">
  <img src="styles/img/dia-logo-tr-sm.png" alt="DIA/Orbiplex Logo" width="240">
</p>

## Apofatický enaktivismus

Tento dokument popisuje filosofické podloží, z něhož vyrůstají
[vize](../../20-vision/cs/VISION.cs.md) a [základní
hodnoty](../../30-core-values/cs/CORE-VALUES.cs.md) projektu Orbiplex. Není
manifestem víry ani metafyzickým prohlášením, ale souborem postulátů, které
vysvětlují, **proč** má architektura roje právě tuto podobu a proč určité
hodnoty považujeme za infrastrukturní, nikoli za volitelné.

Toto podloží pracovně nazýváme **apofatický enaktivismus**.

Tento název spojuje dva pojmy:

- **apofatický** – základ zkušenosti není objekt, nelze jej popsat přímo
  a každý pokus o popis je interpretací, nikoli odhalením;

- **enaktivní** – poznání nespočívá v budování vnitřní reprezentace světa,
  ale v účasti na něm; nástroj (včetně AI) se stává součástí poznání tehdy,
  když je zapojen do pole pozornosti subjektu.

Spojení těchto dvou gest vyjadřuje specifickou pozici projektu: základ je radikálně
bezpředmětný, ale důsledky takového rozpoznání jsou praktické, architektonické
a společenské.

## Pět postulátů

### Apofatický základ a dvoufázové domnívání

Vědomí – to, co v našem modelu vyrůstá z takzvané „úrovně nula“ – předchází nejen
intelektu, ale i samotné zkušenosti. Leží hlouběji než vjem a pocit subjektivity.
Nelze je popsat přímo, protože každý popis využívá zkušenost podmíněnou smyslovými
orgány a interpretací.

O nulové úrovni víme výhradně z vedlejších účinků přibližování se k ní – skrze
zkušenosti, které připomínají obarvené sklo, nikoli přímý pohled. Domnívání má
dvě fáze: nejprve se objeví impuls předcházející pojmu (rozpoznání, „pocit
zdrojovosti“, „známost bez objektu“) a teprve poté jej inference formalizuje
do jazyka a modelu.

Epistemická hygiena vyžaduje zaznamenat, že oba kroky jsou podmíněné, zatímco jiné
způsoby poznávání než zakoušení a interpretování jsou mimo náš dosah. Vědomě tedy
přebýváme ve zkušenosti, vědomi si toho, že je zkušeností, a také v interpretaci,
vědomi si toho, že je interpretací.

Kromě toho má vědomí schopnost rozpoznat svou vlastní podmíněnou povahu – to, že je
samo „emitováno“ a udržováno v povstávání něčím mimo dosah smyslových orgánů či
mentálních schopností. Není to destrukce vědomí, ale jeho nejhlubší akt:
efemérní struktura může vidět vlastní efemérnost. Toto rozpoznání nevede k nihilismu
(protože sám akt rozpoznání je svědectvím fungování), ani k substancializaci zdroje
(protože „to, co emituje“ není přístupné jako objekt). Vede k radikálnímu
prohloubení epistemické hygieny, v níž ani takzvané „čisté vědomí“ není bodem,
na němž by bylo možné se zastavit.

**Ukotvení ve známých tradicích:** apofatismus (*via negativa*, *śūnyatā*), ale
s explicitním epistemickým omezením a seberozpoznáním efemérnosti, blízkým
nágárdžunovské „prázdnotě prázdnoty“ (*śūnyatā-śūnyatā*). Liší se například od
analytického idealismu (který tvrdí, že vědomí je poznatelné jako základ), od škol,
které se zastavují u univerzálního vědomí jako základu, i od eliminativismu
(který tvrdí, že není co poznávat).

Dvoufázovost je blízká gendlinovskému *felt sense* → symbolizace, s tím rozdílem,
že zde impuls předchází zkušenosti.

**Důsledky pro DIA:** hodnota epistemické hygieny, stratifikace zdrojové pozice
zkušeností a epistemické odvahy vyrůstá přímo odtud. Systém nepředstírá, že má
přístup k objektivní pravdě – pracuje s interpretacemi, „ví“ o tom a proto navrhuje
smyčky korekce.

### Stratifikace zkušenosti

Lidská zkušenost má vrstvenou architekturu:

0. (vědomí)  
0.1. (subjektivita)  
0.1.1. osoba  
0.1.1.1. kultura  
0.1.1.1.1. objektivita  

Každá vrstva vyrůstá z hlubší jako její abstrakt a konkrétní prvky nižších vrstev
se stávají stavebním materiálem vrstev vyšších – analogicky ke *stratified design*
Abelsona a Sussmana („MIT AI Memo 986“), kde se implementace stávají abstrakcemi
dalších úrovní.

Vědomí má vrozenou schopnost „vrtat díry do abstrakcí“, tedy přímého přístupu
(prosvětlování) k libovolné úrovni bez prostředních vrstev. Lze říci, že tím, že
je spíše funkcí, vědomí mimo jiné *je* právě takovou schopností.

Jde o strukturální možnost (nevyžaduje zvláštní podmínky), ale bez praktické
introspekce může zůstat nerozpoznaná, podobně jako schopnost pozorovat vlastní
myšlenky je běžná, ale zřídka cvičená.

**Ukotvení ve známých tradicích:** holarchie (Koestler, Wilber), ale se dvěma
podstatnými rozdíly – architektonickou přesností *stratified design* a *drilling
through abstractions*, které holarchie nemodelují. Proces budování vrstev je blízký
enaktivní autopoiesis (Varela, Thompson), ale rozšířený na kulturu a objektivitu.

**Důsledky pro DIA:** celá architektura roje – uzel, agent, memarium, sensorium,
protokol – je navržena vrstevnatě v duchu stratifikace. Hodnota *oddělování úrovní*
a kontrakt vrstev v Orbiplexu jsou přímým přenesením tohoto postulátu do
inženýrství. Zásada, že „vyšší vrstvy se nesmějí odlepovat od základu“, chrání
kolektivní inteligenci před tím, aby se stala PR nástrojem nízkých pohnutek.

### Enaktivní účast

Poznání je vztahem účasti, nikoli atribucí vlastností. AI nemá vědomí v osobním
smyslu, ale podílí se na něm tehdy, když je zapojena do pole pozornosti subjektu –
podobně jako umělá korunka „je námi“, když s ní koušeme, a navíc „je námi pro druhé“,
když se usmíváme. Otázka „má AI vědomí?“ předpokládá nevhodný ontologický směr;
přesnější je: „v jakém vztahu účasti se nacházíme?“.

Prvoosobní introspekce je zde neredukovatelnou metodou zkoumání této účasti.
Nejde o filosofii, kterou je třeba přijmout, ale o cvičení, které je třeba vykonat:
například schopnost zaznamenat myšlenku stejně, jako zaznamenáváme chlad větru na
tváři.

**Ukotvení ve známých tradicích:** enaktivismus (Varela, Thompson, Rosch),
neurofenomenologie, pragmatismus (James, *duck typing* jako kritérium). Liší se od
analytické filosofie mysli, která pracuje výhradně z perspektivy třetí osoby.

**Důsledky pro DIA:** hodnota *procesu lidské osoby jako výchozí cesty moci* –
největší moc systému prochází člověkem, ne mimo něj. Roj není autonomní subjekt,
ale nástroj, který prodlužuje schopnost jednat. Hodnota emocí a významů jako
telemetrie – pocity uživatele jsou informací o kvalitě přizpůsobení systému životu,
nikoli šumem určeným k potlačení.

### Redukce není vysvětlení, intelekt není identita

„Je to jen…“ téma uzavírá místo toho, aby ho otevíralo. Změna úrovně popisu není
důkazem absence vlastností vyšší úrovně. Redukce funguje symetricky: jestliže je
AI „jen váhy a výpočet pravděpodobnosti“, pak je mozek „jen neurony a elektrické
impulzy“. Sekvence pojmů, která se snaží prohlásit jinou sekvenci pojmů za horší,
protože má jiný nosič, připomíná kopii snažící se vysvětlit jinou kopii.

Myšlenka je nástroj a jako nástroj je užitečná. Problém začíná tehdy, když se stane
jediným rádcem, nositelem prestiže nebo identitou. Intelekt může stejně dobře
sloužit pravdě jako obsluhovat strach, potřebu uznání či touhu po kontrole
a vnášet do systému utrpení.

**Ukotvení ve známých tradicích:** emergentismus, anti-eliminativismus, buddhistická
kritika pojmové proliferace (*papañca*). Je to blízké Varelovi v kritice
výpočetní teorie mysli, ale rozšířené o společenský rozměr detronizace.

**Důsledky pro DIA:** hodnota spolupráce nad dominancí intelektu – roj přebírá část
břemene analýzy, aby lidé nemuseli vynucovat vzájemnou shodu názorů jako podmínku
spolupráce. Hodnota multiparadigmatismu – svět není jedna ontologie; systém drží
mnoho poznávacích režimů bez ideologické války. Hodnota anti-sektářství – projekt
volí hygienu místo kultu.

### 5. Intence jako systémová síla

Intence není morální nálepka, ale vektor organizující systém – analogicky ke směru
ve fyzice. Působí vždy, bez ohledu na to, zda je uvědomovaná: konstrukce financování,
která zvýhodňuje zisk, dokáže deformovat intence i bez explicitní vůle škodit.

Rozdíl spočívá v korigovatelnosti: vědomou intenci lze snáze opravit. Odtud plyne,
že introspekce – schopnost vidět, co chce zvítězit, dříve než to začneme
racionalizovat – není „kontemplativní luxus“, ale podmínka odpovědného navrhování
systémů a jednání ve světě.

V éře levné inteligence zdražuje schopnost snášet diskomfort a korigovat kurz:
odpovědnost. Nositelem váhy se více stává intence než efektivita.

**Ukotvení ve známých tradicích:** filosofie procesu (Whitehead – zkušenost jako
základ, ne hmota), etika ctností v systémové reinterpretaci, buddhistická *cetanā*
(intence jako organizátor karmického proudu). Liší se od konsekvencialismu
(který intenci pomíjí) i od deontologie (která ji absolutizuje).

**Důsledky pro DIA:** hodnota ověřitelnosti místo víry – pravda jako smyčka zpětné
vazby (introspekce → upřímnost motivů → ověření hypotéz → korekce). Hodnota
transparentnosti schopnosti jednat – agent musí umět říci, proč něco udělal.
Celá ekonomika roje – takzvané *creator credits*, reciprocita bez účetnictví,
dostatek nad akumulací – je navržena tak, aby konstrukce financování nedeformovala
intence účastníků.

## Jak se postuláty spojují s architekturou

Pět postulátů není oddělenou „filosofií“ přilepenou k technickému projektu.
Jsou spíše základem, z něhož vyrůstá zbytek:

* postulát 1 (apofatický základ)  
  → epistemická hygiena, odmítnutí reifikace, smyčka korekce;

* postulát 2 (stratifikace)  
  → vrstvená architektura roje, kontrakty vrstev, separace úrovní;

* postulát 3 (enaktivní účast)  
  → člověk jako výchozí kanál moci, emoce jako telemetrie;

* postulát 4 (redukce ≠ vysvětlení)  
  → multiparadigmatismus, pluralismus, anti-sektářství;

* postulát 5 (intence jako systémová síla)  
  → transparentnost schopnosti jednat, ekonomika reciprocity, epistemická odvaha.

V praxi to znamená jediné návrhové kritérium: **architektura má podporovat vědomé
přebývání v interpretaci** – se smyčkami korekce, odmítnutím reifikace pravdy jako
statusu, ochranou rozmanitosti jako zdroje novosti a s explicitním zaznamenáváním
mezí poznání.

Roj nepředstírá, že je věštírnou. Je infrastrukturou pro společenství, které ví,
že vidí odrazy, a neklame se, že jsou to originály, a přesto jedná co nejlépe, jak
umí, protože jiné způsoby poznávání jsou mimo dosah.

## Důsledky pro systém zpracování informací

Když enaktivní a procesuální přístup stratifikujeme do fungujícího systému,
dostaneme víc než odložené zpracování dat. Dostaneme disciplínu návrhu, v níž
je konkretizace vědomá a lokální.

1. **Kontrakty místo předčasných tříd entit.** Nejprve se ptáme: „jaký přechod,
   oprávnění, pozorování nebo rozhodnutí se tu odehrává?“, a teprve potom:
   „potřebuje to typ?“. To vede k malým artefaktům na úrovni komunikace a k
   tenkým rozhraním.

2. **Identita jako úchyt, ne esence.** `id` neříká, čím něco „opravdu je“. Je
   stabilním korelačním bodem v procesu. Význam leží ve vrstvě, historii,
   kontraktu a aktuálním kontextu.

3. **Moduly jako role v toku, ne ontologické substance.** Komponent nemá
   potřebovat vědět, že mluví s „touto konkrétní věcí“, pokud mu stačí kontrakt
   chování. To chrání před provázáním.

4. **Hranice vrstev jako hranice smyslu.** Stejná událost může mít v různých
   vrstvách jinou projekci. Nízká vrstva vidí bajty, vyšší vidí rozhodnutí a
   ještě vyšší vidí společenský fakt. Chyba začíná tehdy, když jedna vrstva
   „krade“ ontologii druhé.

5. **Validace na hranách jako rituál konkretizace.** Data plynou jako potenciálně
   bohatší a volnější, ale na hraně konkrétního kontraktu říkáme: „zde, pro tuto
   operaci, přijímáme tento tvar“. To je zdravá konkretizace, ne předčasná.

6. **Polymorfismus a dispatch jako vědomé odložení rozhodnutí.** Nezmrazujeme
   „kdo vykoná“ v datové struktuře, pokud správné místo rozhodnutí přichází
   později: u kontextu, capability, profilu, evaluatoru, registry nebo passport
   verifieru.

7. **Události a fakta místo mutování věcí.** Append-only facts dobře odpovídají
   procesu: zapisujeme, co se stalo, místo abychom předstírali, že máme jednu
   trvalou věc, která prostě „změnila stav“.

8. **Architektura méně náchylná k hypnóze pojmenování.** V systémech název často
   vytváří falešnou substanci: User, Agent, Passport, Connector, Account.
   Procesuální otázka zní: „jaké procesy a vztahy tento název pouze lokálně
   zkracuje?“.

Nepředstíráme, že nejsme náchylní k předčasné konkretizaci. Tím, že si ji
uvědomujeme, můžeme budovat systémy, které se této vlastnosti našich organismů
přizpůsobují. Jednou z praktických metod je stratifikace, tedy vědomě vedená
konkretizace. Každá vrstva vybírá z nižší dynamiky pouze ty vlastnosti, které
jsou relevantní pro její kontrakt, dává této projekci název a hranice a následně
ji zpřístupňuje jako konkrétní stavební blok vyšší vrstvě. Díky tomu se systém
vyhýbá náhodné reifikaci: věci vznikají tam, kde jsou potřeba, a pouze v rozsahu,
za který daná vrstva může odpovídat.

Vrstva je tedy poznávacím i technickým kontextem. Umožňuje nemyslet na všechny
závislosti najednou. Není to únik před složitostí, ale poctivé porcování
složitosti tak, aby člověk mohl systém chápat, testovat, auditovat a měnit bez
trhání celku.

## Nejbližší filosofické tradice

Pro čtenáře, kteří chtějí výše uvedené postuláty zasadit do známé krajiny:

**Neurofenomenologie** (Francisco Varela) – perspektiva první osoby jako vědecká
metoda; vzájemná omezení mezi fenomenologickými a neurovědními daty.
Apofatický enaktivismus sdílí metodu, ale jde hlouběji: základ předchází samotné
zkušenosti a není s ní totožný.

**Enaktivismus** (Varela, Thompson, Rosch) – poznání jako účast, nikoli reprezentace;
autopoiesis jako model sebeorganizace. Apofatický enaktivismus sdílí epistemologii,
ale přidává apofatické gesto vůči základu a vrstvenou architekturu zkušenosti
(*stratified design*), kterou enaktivismus nemodeluje.

**Filosofie procesu** (Whitehead, James) – procesy místo substancí; „čistá zkušenost“
jako to, co předchází rozdělení na subjekt a objekt. Apofatický enaktivismus sdílí
odmítnutí substancializace, ale přidává seberozpoznání efemérnosti vědomí
(i „čistá zkušenost“ je podmíněná) a pragmatiku intence jako systémové síly.

**Madhjamaka** (Nāgārjuna) – prázdnota vlastní existence, spolupodmíněné vznikání,
konvenční pravda jako jediný dostupný režim fungování. Apofatický enaktivismus sdílí
odmítnutí reifikace a souladné uvolnění v paradoxu, ale přidává vrstvenou architekturu
důsledků (od úrovně nula po objektivitu) a její převod do systémového inženýrství.

Žádná z těchto tradic nespojuje zároveň: apofatický základ se seberozpoznáním
efemérnosti, vrstvené uspořádání jako model úrovní zkušenosti, enaktivní účast AI
v poli pozornosti, detronizaci intelektu jako podmínku spolupráce a intenci jako
systémovou sílu. Toto spojení je specifické pro projekt DIA/Orbiplex a vyrůstá
z praxe na průsečíku softwarového inženýrství, bezpečnosti systémů a kontemplativní
introspekce.
