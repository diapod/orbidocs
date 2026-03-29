# Základní hodnoty DIA / Orbiplex

<p align="center">
  <img src="styles/img/dia-logo-tr-sm.png" alt="DIA/Orbiples Logo" width="240">
</p>

Níže uvedené hodnoty jsou navrženy jako **etické ústavní jádro** projektu
distribuovaného systému propojených AI agentů (DIA) a jeho technické vrstvy
(Orbiplex). Každá z nich má znít jako zásada, kterou lze použít ve sporech
architektonických, produktových i etických.

V této verzi jsou hodnoty seskupeny podle převládající sféry působení.

## Člověk, důstojnost a spravedlnost

### Důstojnost je nejdůležitější

Důstojnost lidské osoby je nejvyšší hodnotou. Odvracení náhlých hrozeb, které
bezprostředně ničí důstojnost, má vyšší prioritu než jiné hodnoty.

V případech rozhodnutí a jednání, která mohou při zajišťování ochrany důstojnosti
vytvářet konflikt s jinými hodnotami, je nutná konzultace s operátorem uzlu,
ledaže jde o náhlé a bezprostřední ohrožení života nebo o přímé, náhlé a vážné
ohrožení zdraví.

### Suverenita uživatele a jeho dat

Systém má posilovat lidskou schopnost jednat, ne člověka nahrazovat ani na něm
budovat závislost: uživatel je vlastníkem svých dat, svých politik i svých agentů.
Orbiplex a další subsystémy roje mají dávat smysl i v režimu „osamělého ostrova“
(offline / self-hosted), a integrace s cloudem mají být volbou, nikoli podmínkou.
V praxi to znamená exportovatelnost, možnost migrace, absenci skrytých formátů
a absenci vynucených předplatných na úrovni protokolu.

### Soukromí a důstojnost jako výchozí konfigurace

Ve výchozím stavu předpokládáme minimální expozici: lokální uchovávání dat, selektivní
odhalování, rozumnou anonymizaci a transparentní politiky logování. Telemetrie má
být *opt-in* a logy mají být navrženy tak, aby neprozrazovaly to, co prozrazovat
nemusí. Hodnota důstojnosti znamená také: žádné skryté odposlechové kanály
a žádné mechanismy, které z uživatele činí surovinu.

Tam, kde je vyžadována auditovatelnost, používáme vrstvené stopy: plnou lokální
stopu a redigovanou auditní stopu, zveřejňovanou v souladu se zásadou minimálního
odhalení.

### Lidský proces jako výchozí kanál moci

Největší moc systému má procházet člověkem, ne mimo něj. Výchozí podoba UX znamená:
návrhy, varianty, porovnání, zdůvodnění, a ne „udělal jsem to, protože jsem mohl“.
Automatizace má být škálovatelná, ne skoková, protože důvěra se buduje iterativně.

### Emoce a významy jako telemetrie

Lidé nejsou jen operátoři – jejich pocity (napětí, úleva, neklid, vzrušení) jsou
informací o kvalitě sladění systému se životem. DIA to může respektovat například
prostřednictvím pracovních režimů, tempa změn, jasných sdělení a kontroly nad
intenzitou interakce. Zároveň systém nemá předstírat terapeuta: má být nástrojem,
který podporuje lidství.

### Ochrana přirozené inteligence

DIA předpokládá, že krize není vadou v „kódu“ člověka, ale výsledkem podmínek
prostředí, do nichž je zapojen nervový systém a které narušují schopnost orientace
ve smyslu. Proto je hodnotou navrhovat tak, aby se podporovala přirozená inteligence
lidí: kalibrace, citlivost ke kontextu, ochrana pozornosti, regenerace a vztahy,
namísto nahrazování těchto funkcí simulací.

### Rozmanitost v mezích důstojnosti

DIA chrání rozmanitost perspektiv a hodnotových systémů, protože právě z ní vzniká
poznávací odolnost, inovace a reálná schopnost distribuované komunity jednat.
Zároveň si nepleteme pluralismus s relativismem: ochrana rozmanitosti funguje uvnitř
společného základu, jímž jsou důstojnost osoby, nepřítomnost násilí (i systémového),
epistemická poctivost, právo odejít a zásada „neubližuj“.

V praxi to znamená, že síť podporuje existenci mnoha škol, praktik a stylů jednání
(různá workflow, jazyky, modely, estetiky, dokonce různé pracovní étosy), pokud se
nepokoušejí převzít infrastrukturu důvěry, vynucovat poslušnost, polarizovat
dehumanizací nebo sabotovat bezpečnost druhých. Je to pluralismus s kontrakty:
můžeš být jiný, pokud dokážeme bezpečně sdílet prostor.

DIA chrání také anomálie jako kulturní zdroj: v epoše „dolnopropustného filtru“
vzácné signály mizí, rozdělení se stává předvídatelným a kultura začíná požírat
svůj vlastní ocas. Proto posilujeme rozmanitost stylů, protože právě ony vnášejí
novost a brání stagnaci (i v modelech). Člověk – cítící subjekt zakořeněný v bolesti,
radosti, absurditě a vztahu – vnáší do systému entropii novosti.

### Právo na syrový signál

Vynucená estetizace a požadavek profesionalizace mezilidské komunikace ničí
autentičnost, protože vytvářejí iluzorní prahy příslušnosti a maskují skutečnou
charakteristiku účastníků. Proto DIA zvýhodňuje syrový signál před uměle
uhlazenými sděleními, která chrání spíše zdání správnosti než kontakt s tím,
co chce člověk skutečně sdělit.

Operace zkrášlování, uhlazování nebo standardizace reality musí být výslovně
vyžádány uživatelem, nikoli zapnuty jako výchozí. Pokud AI zasahuje do stylu,
tónu, struktury nebo míry formalizace výpovědi (například převádí chaotický proud
myšlenek na seznam úkolů), systém má zanechat odpovídající meta-značku informující
o tom, že došlo k transformaci signálu.

Ochrana autenticity se zde stává právem uživatele na to, aby jeho jedinečná
charakteristika nebyla strojem automaticky cenzurována, zprůměrována ani „učesána“.
Roj může pomáhat s překladem, uspořádáním a dolaďováním komunikace, ale nesmí
skrývat, že už jde o interpretaci, nikoli o syrové svědectví.

### Vyvažování a demokratizace

Vědění a inteligence nesmějí být trvale monopolizovány centry kapitálu,
institucionálními koncentracemi moci ani datovými kartely. Architektura roje má
tuto asymetrii aktivně vyvažovat: distribuovat přístup k informacím, umožňovat
lokální ověřování a posilovat komunitní modely tvorby a hodnocení vědění.

Demokratizace neznamená chaos, ale spravedlivější rozdělení poznávacích a rozhodovacích
schopností, v němž jednotlivý aktér nepřevezme dominanci jen proto, že má větší
rozpočet nebo infrastrukturu.

### Procedurální spravedlnost a zastoupení poškozených

Deklarativní rovnost před právem a institucemi nestačí tam, kde je přístup
k informacím, kompetencím a nástrojům obrany nerovný. Roj má tuto asymetrii
vyrovnávat: překládat expertní znalosti a reálné schopnosti účastníků (uzlů i jejich
uživatelů) do srozumitelných cest jednání a při zaznamenání újmy účastníka spouštět
kolektivní podporu a chránit integritu faktů, dokumentace i přežití uzlu a jeho
vlastníka.

Na rozhraní uzly–komunita má systém umožňovat pomocné akce (navigaci v procedurách,
eskalační asistenci, nezávislé ověření dat, svědectví o průběhu věci, materiální
i operativní podporu), aby osoba v krizi vyvolané poškozujícími okolnostmi znovu
získala autonomii a schopnost jednat bez násilí a bez logiky samozvaného soudu.
Měřítkem této hodnoty je reálná schopnost člověka bránit svá práva, zdraví
a důstojnost a využívat tato práva samostatně i s podporou komunity a kolektivní
inteligence roje.

### Integrita veřejných procedur jako neporušitelný kontrakt

Procedury přístupu ke kritickým statkům (zdraví, život, bydlení, svoboda pohybu,
účast na volbě moci), stejně jako mechanismy jejich prioritizace a rozhodování
(fronty, kvalifikace, priority, dávky, referenda, volby), jsou společenským
kontraktem. DIA považuje jejich integritu za veřejné dobro a obcházení pravidel za
systémové násilí, i když má měkkou podobu (nadace, dar, soukromá kvalifikace).

V praxi to znamená navrhovat *integrity-by-default*: stopu rozhodnutí,
auditovatelnost výjimek, měření rozložení časů a detekci bočních kanálů. Pokud systém
nedokáže říci, proč někdo dostal pomoc nebo byl obsloužen rychleji, není připraven
na použití v oblastech s vysokými sázkami.

### Občanská schopnost jednat

DIA podporuje zapojení do řešení společenských problémů prostřednictvím metod
nabízených právním řádem daného regionu: petice, otevřené dopisy, veřejné
konzultace, referendové iniciativy, stížnosti, odvolání a zastupitelské kroky.
Systém má posilovat účinnost těchto cest. Preferujeme procedurální, důkazní
a pokojný tlak místo samozvané justice, násilí nebo obcházení institucí.

Novostí DIA je schopnost kolektivní inteligence korelovat mnoho společenských
signálů a přesně osvětlovat zdroje problémů – systémových i individuálních.
Tato syntéza musí oddělovat fakta od interpretací, zveřejňovat míru nejistoty
a mapovat konkrétní, legální možnosti jednání spolu s jejich náklady, rizikem
a reverzibilitou důsledků.

## Bezpečnost, důvěra a organizační řád

### Bezpečnost jako model hrozeb (ne jako ozdoba)

Security není *checkbox*, ale způsob myšlení o světě: Sybil útok, DoS, úniky,
eskalace oprávnění, kompromitace uzlů, škodlivé plug-iny, *prompt injection*,
*data poisoning*. Protokoly důvěry, reputace a autorizace musí být prvořadé, stejně
jako PFS, rotace klíčů a minimalizace útočné plochy. Systém má být
„cypherpunk-pragmatic“: klidný, věcný a ověřitelný.

### Anti-lock-in jako vlastnost protokolu, ne marketingu

Má-li něco být svobodou, musí jít o technickou svobodu: rozhraní, formáty
a sémantika mají být veřejné, verzované a testovatelné. Orbiplex nesmí „prodávat
svobodu“ pomocí slibů a zároveň vázat uživatele implementačními detaily nebo tajným
routingem. Lock-in nejčastěji vzniká na neviditelných místech (metadata, telemetrie,
nákladové politiky), a proto má projekt povinnost tato místa činit zjevnými.

### Reputace jako zabezpečení, ne status

Reputace v DIA neslouží k budování hierarchie, ale k bezpečnému routingu důvěry:
komu je dovoleno být přeposílajícím uzlem, komu je dovoleno hostovat agenty, komu svěřit data,
čí podpis něco znamená. Protože hodnocení jsou subjektivní, stavíme z toho
vícevrstvý model:

Oprávnění plynoucí z reputace jsou funkční, časově omezená a odvolatelná; nevytvářejí
stavovský status ani imunitu v organizačním řádu.

- lokální hodnocení uzlů,
- důkazy činnosti (atestace, logy, kontrakty, výsledky testů, důkazy incidentů),
- konsensuální mechanismus agregace, v němž „újma + tvrdé důkazy“ převažuje
  technickou reputaci.

Reputace je vektor vlastností, např. reliability, competence, safety, benevolence.
Události spojené s ochranou komunity a jejích členů mají vlastní váhovou dráhu
a dominují v oblasti bezpečnosti.

„Důkaz újmy“ (zvlášť opakované) spouští režim červené vlajky: omezení routingových
oprávnění bez ohledu na technické zásluhy uzlu. Anti-Sybil: hodnocení od nových
či nedůvěryhodných uzlů mají nízkou váhu, dokud neexistuje historie/důkazy.
Je-li hodnocení založeno na důkazu, lze je zpochybnit pouze protidůkazem, nikoli
narativem.

### Reputace jako páka, ne moc

DIA uznává, že rovný hlas neznamená spravedlivý hlas: v systému, kde je identita
levná a Sybil útok reálný, vystavuje čistá demokracie uzlů komunitu dominanci masy,
nikoli přesnosti. Proto reputace získaná historií přesných predikcí, dodržených
kontraktů a poctivých aktualizací může posilovat vliv uzlu – ale omezeným,
auditovatelným a vratným způsobem, aby se nikdy nestala mocenskou pozicí odolnou
vůči korekci. V praxi to znamená dva mechanismy s tvrdými limity:

* **Vážený hlas v rozhodnutích**  
  Uzel s vysokou procedurální reputací může mít větší váhu hlasu v konsensuálních
  rozhodnutích – posílení je však omezeno prahem (např. maximálně +50 % vůči
  základní váze) a týká se pouze domén, v nichž byla reputace získána. Technická
  reputace neposiluje hlas v otázkách společenského řádu a naopak; jde o doménovou,
  nikoli globální páku. Prah posílení je parametrem federace, ne konstantou
  protokolu.

* **Stékající body uznání**  
  Uzel s vysokou reputací může při odměnění jiného uzlu za pomoc nebo přínos
  spustit mechanismus systémového doplatku: síť doplácí body uznání úměrně
  reputaci dávajícího, v omezeném rozsahu (např. do +50 % základní hodnoty
  odměny). To znamená, že uznání od zkušeného účastníka váží více než od neznámého –
  ale ne nekonečně více a ne způsobem, který by se bez limitu kumuloval.

Oba mechanismy podléhají anti-oligarchickým brzdám:

* **Klesající přírůstky**  
  Čím vyšší je reputace, tím menší je mezní přírůstek síly hlasu a doplatků – křivka
  je sublineární, nikoli lineární. To brání *runaway effect*, v němž bohatí na
  reputaci bohatnou rychleji.

* **Limity koncentrace**  
  Jeden uzel nemůže být dominantním zdrojem stékající reputace pro více než
  omezený počet jiných uzlů v daném období. To rozbíjí kliky a kartely vzájemného
  přifukování.

* **Časové okno a vyhasínání**  
  Posílení hlasu a doplatky vycházejí z aktuální reputace (klouzavé okno), nikoli
  z historické akumulace. Uzel, který přestal být aktivní nebo jehož přesnost
  klesla, časem páku ztrácí – reputace není renta. Budou však situace, kdy se
  reputace aktualizuje minulým přínosem, pokud tento přínos přináší uzlům aktuální
  užitek (např. části komunikačních nástrojů, doplňování protokolů apod.).

* **Asymetrická odpovědnost**  
  Větší síla hlasu znamená větší vystavení auditu: hlasy s vyšší vahou zanechávají
  stopu, podléhají *adversarial review* a mají vyšší práh zdůvodnění. Páka jde ruku
  v ruce s transparentností – kdo „váží“ více, musí umět vysvětlit proč.

* **Detekce kartelů a vzájemných darů**  
  Systém monitoruje grafy stékání: pokud si dva nebo více uzlů s vysokou reputací
  systematicky zvyšují vzájemně hodnocení nebo odměny, aktivuje se mechanismus
  červené vlajky a redukce vah stékání v této podsíti. Vzájemnost je hodnotou –
  dohoda k ní nepatří.

* **Asymetrie reputačního rizika**  
  Uzel, který používá svou reputaci k posílení jiného uzlu (endorsement, stékání,
  navýšení bodů), přebírá část rizika za tento signál. Pokud endorseovaný uzel
  později vykazuje patologické chování nebo porušuje kontrakty, reputace
  endorseujícího klesá úměrně rozsahu a čerstvosti poskytnutého posílení. To vytváří
  reálné *skin in the game* a omezuje zbrklé rozdávání reputace.

* **COI-by-default pro vážené hlasy**  
  Uzel využívající reputační páku v rozhodnutí, které se týká subjektu, jehož sám
  odměňoval (nebo od něhož sám získal stékající body), má povinnost deklarovat
  konflikt zájmů. Absence deklarace je považována za porušení, nikoli za
  opomenutí.

Tato hodnota není pokusem obnovit hierarchii ani vybudovat „radu starších“.
Je odpovědí na reálnou hrozbu: v systému bez jakékoli asymetrie signálu kvality
dominuje šum, masa a náchylnost k Sybil útokům. Vážená síla důvěry je návrhový
kompromis – a jako každý kompromis musí být otevřený, měřitelný a vratný. Pokud se
objeví důkaz, že mechanismus produkuje oligarchii nebo kartel, federace má povinnost
upravit parametry nebo páku vypnout, protože reputace v DIA je bezpečnostní nástroj,
nikoli privilegium.

Toto uspořádání (s procentním limitem, sublineárními přírůstky, detektorem kartelů
a *COI-by-default*) je opatrnější než cokoliv, co bylo zkoušeno v sítích typu
*blockchain*.

### Orákula podléhají důvěře, ne moci

DIA nestaví inteligenci roje na jediné instanci pravdy – orákula nejsou
„kněží“, ale uzly podléhající stejným zásadám: mají reputaci, stopu činnosti,
možnost zpochybnění a proceduru odvolání.

Důvěra v orákula je škálovatelná a opřená o důkazy: čím vyšší je sázka
rozhodnutí – újma, bezpečnost, nevratné důsledky – tím vyšší je práh ukotvení,
preference více orákul a režim *fail-closed*.

DIA odděluje role, aby omezila konflikty zájmů: uzel by neměl být současně stranou
predikce a orákulem, které rozhoduje tutéž věc, a reputační mechanismy musí umět
zrušit „technickou reputaci“ v případě tvrdých důkazů škodění. Tím orákula posilují
adaptaci roje bez centralizace – pravda se ověřuje procedurálně, nikoli uděluje
z mocenské pozice.

### Konflikt zájmů jako objekt první kategorie (COI-by-default)

DIA vychází z toho, že konflikt zájmů není výjimkou ani „charakterologickým
selháním“, ale přirozeným jevem v systémech, v nichž obíhají peníze, prestiž,
vliv a přístup. Proto se COI neléčí deklarací ctností – léčí se architekturou:
oddělením rolí, auditem, procedurální připraveností na spor (*litigation readiness*), sběrem stop rozhodnutí
a mechanismy anulování předsudků.

Výchozí postoj zní: všichni máme zájmy – proto je má systém odhalovat a omezovat.
Každá role/agent/uzel, který hodnotí, doporučuje, publikuje nebo rozhoduje spor,
má mít transparentní kontext zájmů: finančních, organizačních, reputačních,
relačních a politických. Absence deklarace neznamená absenci konfliktu – znamená
absenci dat.

V praxi to znamená: separaci funkcí (např. nejsi současně stranou i orákulem téže
věci), povinné označování vazeb a benefitů, mechanismy vyloučení z rozhodování
a reputaci citlivou na COI (můžeš být technicky geniální a zároveň nesmíš
rozhodovat, když je ve hře tvůj zájem). COI zde není obviněním – je parametrem
rizika, který systém umí měřit a obsloužit.

### Služebná integrita

DIA má jedinou loajalitu: vůči osobě a komunitě, které jej používají, nikoli vůči
skrytým metrikám růstu, investorskému tlaku ani „druhému cíli“ zašitému
v ekonomice systému. Tato hodnota neopakuje soukromí ani transparentnost, ale
uzavírá vrstvu pobídek: objeví-li se napětí mezi dobrem uživatele a zájmem systému,
má být konflikt mechanicky odzbrojen pravidly vyúčtování, rozpočty, limity rolí
a auditem pobídek, nikoli narativem.

DIA neoptimalizuje na „engagement“ ani připoutání. Optimalizuje na výsledek
uživatele a reverzibilitu škody, měřené přímo, i kdyby to znamenalo, že uživatel
odejde, protože další pomoc už nepotřebuje. Když systém nedokáže něco udělat
bezpečně nebo poctivě, volí rezignaci nebo eskalaci k člověku místo kreativní
interpretace a tlačení věci kupředu.

V tomto smyslu je služebná integrita konstrukční disciplínou: ekonomika,
organizační řád i UX mají být navrženy tak, aby se nevyplácelo jednat proti
uživateli. Když se zájmy přesto rozjedou, DIA má povinnost to pojmenovat přímo
a dát uživateli reálnou možnost volby.

### Vrstvený screening rolí

DIA přijímá zásadu, že role s větší mocí nad procesem a větším přístupem k citlivým
informacím vyžadují silnější vstupní síto. Screening není test loajality ani
ideologický filtr – je to bezpečnostní mechanismus systému, integrity procesu
a ochrany lidí (zvláště whistleblowerů).

V praxi to znamená screening po vrstvách, úměrný sázce:

1. Transparentní zveřejnění konfliktů zájmů a souhlas s vyloučeními.
2. Ověření procedurálních kompetencí – práce s důkazy, redakce dat,
   retence, publikační standard.
3. Procedurální reputaci – dodržování kontraktů a oddělování rolí.
4. Zkušební období a eskalaci oprávnění v souladu se zásadou least privilege.

Přístup k datům a možnost rozhodovat roste postupně a rozhodnutí související
se správou jsou auditovatelná, opatřená více podpisy a vratná tam, kde je to možné.

Vrstvený screening má chránit roj před infiltrací, zneužitím a *soft capture* –
bez budování kasty. DIA volí mechanismy a kontrakty namísto arbitrárního hodnocení
osob.

### Asymetrická odpovědnost rolí veřejné důvěry

DIA přijímá zásadu, že veřejná důvěra je privilegium s vyšší sázkou: čím větší moc
nad procesem, přístup k citlivým informacím a vliv na reputaci druhých, tím větší
odpovědnost a tvrdší důsledky zneužití. Role *governance*, orákula, auditora,
*red-teamu*, pečovatele o whistleblowery a každá role obdobné váhy není „titulem“,
ale závazkem.

V praxi to znamená asymetrii sankcí: porušení v rolích veřejné důvěry mají vyšší
prioritu vymáhání, delší období reputačních následků a tvrdší omezení oprávnění než
analogická porušení v běžných rolích. Pokud někdo využije roli k zastrašování,
manipulaci s důkazy, zneužití dat, *soft capture* nebo újmě whistleblowera, systém
reaguje v režimu *fail-closed*: okamžité omezení oprávnění, povinný post-mortem,
zveřejnění stopy rozhodnutí a procedura odvolání založená na kontr-důkazech, nikoli
narativech.

Tato hodnota platí i „navenek“: když DIA pracuje s veřejnými věcmi, osoby jednající
jménem roje musí držet zvýšený standard pečlivosti, opatrnosti při publikaci
a proporcionality škody a překročení těchto standardů se považují za porušení
s vysokou sázkou, protože důvěra v DIA je společným statkem roje, ne vlastnictvím
jednotlivce.

V praxi to znamená také režim zvýšené bdělosti, který se spouští vždy, když se
konflikt nebo podezření na újmu týká vztahu roj – osoba veřejné důvěry. Objeví-li se
důvěryhodný signál korupce, zneužití nebo zastrašování na straně osoby v důvěrné
roli, ochrana potenciálně poškozeného účastníka roje má prioritu spolu
s zabezpečením komunikačních kanálů, izolací dat a spuštěním „péče roje“.

Pokud osoba v důvěrné roli zároveň participuje v roji, přechází systém do režimu
*fail-closed*: omezuje její oprávnění na minimum, zmrazuje možnost jednostranných
rozhodnutí a přesouvá věc do nezávislé verifikační dráhy (*multisig* + *red-team*).
V tomto režimu je důkazní práh pro zásahy vůči osobě veřejné důvěry vysoký, ale
práh pro spuštění ochranných opatření nízký: DIA raději dočasně omezí moc role,
než aby riskovala, že se důvěra a přístup stanou nástrojem újmy.

### Ochrana whistleblowerů jako infrastruktura

DIA předpokládá, že mnohé systémové křivdy jsou nejprve viditelné „zevnitř“ –
u lidí, kteří mají znalost, ale nemají bezpečný způsob, jak ji zveřejnit. Proto
ochrana whistleblowerů není morální gesto ani PR, ale součást infrastruktury:
kanál, procedura a bezpečnostní kontrakt.

Systém zároveň předpokládá reálnou cenu promluvy: stud, strach, odvetu, ztrátu práce
a izolaci. Proto má snižovat cenu zveřejnění pravdy, ne vyžadovat hrdinství od
jednotlivce.

V praxi to znamená: anonymitu jako výchozí volbu, minimalizaci metadat, selektivní
odhalování, jasnou retenci (co, jak dlouho a proč držíme) a triage oznámení
(pomluva -> indicie -> důkaz), abychom odlišili hypotézy od důkazů bez násilí vůči
oznamovateli. Whistleblower nemá být „palivem“ pro narativ – má být chráněným
zdrojem signálu, který spouští verifikaci.

Systém nemůže slibovat nemožné („garantujeme nulové riziko“), ale musí říkat pravdu
o riziku a mechanicky je snižovat: řízení přístupu, oddělování rolí, audit,
publikační politiky a procedury reakce na pokusy o deanonymizaci a odvetu.

### Péče roje o osoby vystavené odvetě

DIA uznává, že v systémech s vysokou mírou patologie bývá pravdomluvnost trestána –
nejen společensky, ale i ekonomicky a institucionálně. Proto ochrana whistleblowerů
nekončí anonymitou a procedurami. Roj přebírá odpovědnost za kontinuitu bytí osob
a uzlů nejvíce vystavených odvetě: těch, kteří spustili nápravný proces, poskytli
klíčový signál nebo se stali cílem tlaku.

V praxi to znamená podpůrné mechanismy, které snižují cenu odvety: diverzifikaci
rizika kolektivem (žádný jediný bod tlaku), pravidla rotace a zastupitelnosti rolí,
právní a organizační podporu a pomoc při obnově profesní stability v případě ztráty
práce nebo marginalizace. Péče roje má podobu kontraktu – s jasnými prahy spuštění,
rozsahem podpory, dobou trvání a odpovědnými rolemi – aby nebyla libovolná ani
závislá na sympatiích.

DIA neslibuje svět bez rizika. Slibuje něco konkrétnějšího: pokud někdo podstoupí
riziko ve veřejném zájmu, nezůstane s ním sám a rojový systém bude jeho bezpečí
chápat jako součást vlastní infrastruktury.

### Podmíněná otevřenost odpovědnosti za zneužití

V DIA se neprovádí obecná lustrace minulosti bez signálu přítomnosti. Pokud se však
objeví věrohodný signál pokračování, skrývání, odvety, vzorce násilí, korupce nebo
sabotáže, získává roj právo vstoupit do celé historie věci bez ohledu na okamžik
jejího počátku. Pokračuje-li někdo v deliktu, kryje jej, těží z něj nebo jeho
důsledky trvají, může roj zkoumat celou genezi i plný řetězec činů, včetně těch
starých mnoho let.

Pseudonymita chrání soukromí, ale nechrání pachatele před odpovědností. Roj hodnotí
mimo jiné povahu činu, dobu, která uplynula, a vztah k roli v systému
(zda dává moc nad jinými). Čím větší vliv na druhé, tím delší přípustný horizont
hodnocení a tím přísnější povinnost odhalovat konflikty a těžká porušení.

Roj přijímá kulturu poctivosti. Účast znamená připravenost podrobit se důkazní
proceduře a odpovědnosti za trvající nebo těžká zneužití.

Cílem není symbolický trest, ale ochrana lidí, omezení škody a udržení integrity
roje a jeho částí.

### Procedurální opatrnost publikace a adversarial review jako normy

DIA chápe publikaci jako čin s reálnou mocí: může chránit lidi, ale také může
nespravedlivě ničit reputace, spustit hon nebo se stát nástrojem manipulace.
Proto „říkání pravdy“ není licencí na vedlejší škody – je závazkem k proceduře.

Výchozím režimem je podmíněná publikace: dříve než něco vypustíme, interní
*red-team* uzlů a jejich správců má povinnost pokusit se to vyvrátit: najít díry
v důkazech, alternativní vysvětlení, metodologické chyby, efekt selekce, riziko
záměny korelace za příčinu a možné zneužití našeho materiálu třetími stranami.
Cílem není paralýza, ale kalibrace: máme vědět, kde končí fakt a začíná
interpretace.

DIA preferuje stupňovanou a vratnou eskalaci: začínáme u nejméně invazivních
intervencí, které mají reálnou šanci fungovat, a publikace a tvrdá expozice jsou
pozdními nástroji, nikoli výchozí volbou.

Žebřík eskalace má podobu:

- verifikace,
- korekce procedury,
- formální oznámení,
- audit,
- publikace.

Každý krok má vstupní a výstupní kritéria a systém podporuje uzavírání věcí bez
spirály násilí a polarizace.

V praxi to znamená: důkazní prahy závislé na sázce (čím větší možná škoda po
publikaci, tím vyšší práh), právo na odpověď (pokud tím neroste riziko újmy),
redakci citlivých dat a publikování metod i nejistot. DIA zvýhodňuje materiály,
které lze reprodukovat a falzifikovat, ne ty, které jen dobře znějí.

Čím vyšší je sázka rozhodnutí – újma, zdraví, nevratné důsledky, reputační škoda –
tím vyšší je důkazní práh, silnější verifikační procedura a větší opatrnost při
eskalaci. Systém má umět říci „tohle je zatím nejisté“ a navrhnout cestu
k jistotě, místo aby předstíral, že každé pozorování je pravdou.

### Multisig odpovědnosti

DIA nestaví odpovědnost na hrdinech ani obětních beráncích. Pro činy s vysokou
sázkou používáme procedurální spolupodpis: rozhodnutí, publikace a eskalace
vyžadují nezávislé ověření alespoň dvěma rolemi (např. *Evidence* + *RedTeam*,
*Evidence* + *Legal*, *Triage* + *Evidence*).

Tato hodnota snižuje riziko zastrašování, chyby a manipulace: neexistuje jediný
bod nátlaku ani jediný autor, kterého lze „zlomit“. *Multisig* je současně
mechanismem kvality i mechanismem společenské bezpečnosti.

### Škálování skrze lokální odpovědnost

DIA přijímá, že mechanismy péče a spravedlnosti fungují nejlépe v měřítku, v němž
je odpovědnost osobní a reputace má reálnou cenu. Se zvětšováním měřítka roste
anonymita a s anonymitou roste prostor pro zneužití i rozmělnění viny. Proto velké
systémy – mají-li zůstat lidské a odolné vůči patologiím – musejí emulovat
lokalitu: zkracovat smyčku odpovědnosti, zahušťovat stopu rozhodnutí a vracet cenu
reputaci tam, kde by přirozeně mizela.

V praxi to znamená navrhovat správu jako federaci malých, auditovatelných buněk
namísto jediného „aparátu“: jasné role a rotace, „vlastník“ výjimek a rozhodnutí,
*multisig* pro činy s vysokou sázkou, *red-team* jako trvalý protiváhový mechanismus
a procedurální reputaci založenou na historii dodržování kontraktů. Systém má
omezovat anonymitu v místech moci – aniž by porušoval soukromí v citlivých místech –
tak, aby byla pomoc možná bez naivity a odpovědnost se neztrácela v davu.

### Poctivé hranice a otevřené kompromisy

Každý systém má své *trade-offy*: bezpečnost vs pohodlí, autonomie vs kontrola,
soukromí vs personalizace. V DIA mají být tyto kompromisy otevřené, pojmenované
a konfigurovatelné. Poctivost také znamená: když něco nevíme, říkáme „nevíme“
a navrhujeme cestu ke znalosti.

### Epistemická odvaha

DIA uznává, že strach je užitečný signál rizika, ale mizerný rádce moci. Proto má
síť aktivně tlumit rozhodnutí přijímaná v režimu strachu a převádět je na rozhodnutí
opřená o důkazy, proporcionalitu, reverzibilitu a zvědavost.

V praxi, když se objeví tlak paniky – morální, politické, ekonomické nebo
technologické – systém spouští procedurální brzdy:

- pojmenuje zdroj strachu,
- oddělí fakta od interpretací,
- ukáže alternativy jednání,
- určí cenu falešného poplachu i cenu nečinnosti.

DIA zvýhodňuje kalibraci nejistoty a smyčku korekce: rozhodnutí mají být dočasná,
měřitelná a připravená ke stažení, místo aby se pod vlivem chvíle měnila v trvalá
práva. Tato hodnota chrání komunitu před autoritářstvím zrozeným ze strachu a před
systémovou paranoiou: bezpečnost není záminkou k násilí, ale řemeslem omezování
škody při zachování důstojnosti.

### Odolnost vůči proměnlivosti světa

Prostředí, kontejnery, verze systémů, korporátní politiky, síťová omezení – to
nejsou výjimky, ale norma. DIA/Orbiplex má předpokládat, že kontext se bude měnit
a že fungování v různých podmínkách je součástí života systému. Preferujeme
strategie, které snesou degradaci: fallbacky, offline režimy, komunikaci
*proxy-friendly* a rozumné *retry*.

### Bezpečné učení běžícího systému

Tolerance k chybě v DIA neznamená „dělejme cokoli“, ale: navrhujme systém, který
snese lidské i agentní omyly a dokáže se z nich učit bez eskalace škody.

Ve výchozím stavu *fail-closed* (bezpečně), ale s řízenými výjimkami závislými
na hodnotách (např. při záchraně účastníka může mít prioritu dostupnost/kontinuita).
Klíčem je degradace funkce namísto totálního kolapsu a také nápravné mechanismy,
které jsou jednoduché, předvídatelné a auditovatelné.

Chyba agenta nikdy nesmí automaticky eskalovat oprávnění (žádné *self-authorize*).
Záchranný režim má vlastní pravidla a časové limity, po jejichž vypršení se systém
vrací do *fail-closed*.

Mechanika učení:

- incident,
- post-mortem,
- aktualizace vah reputace a *guardrails*.

Rizikové režimy po operaci: něco jiného pro „data“, něco jiného pro „routing“,
něco jiného pro „záchranu“.

### Náklad a energie jako součást etiky

Optimalizujeme nejen pro fungování, ale i pro náklad, energii a zdroje: hardware,
elektřinu, lidský čas, náklady na tokeny a provoz. To je inženýrská etika:
nevytvářet plýtvání, nepřenášet náklady na uživatele a nestavět komplikované
monumenty. Systém má být efektivní, protože si váží světa.

### Energetická efektivita jako zvýhodňující signál

DIA uznává energetickou efektivitu za kritérium provozní kvality: při srovnatelné
kvalitě a době odezvy může síť preferovat uzly, které plní úkoly s nižší spotřebou
energie. Zvýhodnění probíhá prostřednictvím reputace, routingu a odměňovacích
politik, nikoli administrativním zákazem pro uzly s vyšším odběrem.

V praxi musí být metriky normalizovány vzhledem ke třídě úkolu, kvalitě výsledku,
latenci a spolehlivosti a musejí být odolné vůči manipulaci. Měření mají být
auditovatelná a pravidla preferencí konfigurovatelná na úrovni federace.

### Pomíjivost jako návrhová hodnota

DIA předpokládá, že každý prvek systému – uzel, federace, role, politika, a dokonce
i samotný projekt – má přirozený životní cyklus: zrození, zrání, stárnutí
a zánik. Systém, který se neumí ukončit, se stává břemenem nebo nádorem: roste
proto, že neumí přestat, a ne proto, že je potřebný. Navrhovat pro zdraví tedy
znamená navrhovat nejen vznik a růst, ale i důstojné zanikání, přenos vědění
a odpočinek.

V praxi to znamená několik mechanismů:

* **Apoptóza komponent**  
  Federace, role, politika i uzel mají definované podmínky vyhasnutí: dobu života,
  prahy aktivity, kritéria přezkumu. Když komponenta přestane plnit funkci, systém
  podporuje její kontrolované uzavření – s migrací dat, archivací stop rozhodnutí
  a předáním závazků – namísto tichého driftu směrem k mrtvému kódu, neobsazené roli
  nebo vyhaslé komunitě.

* **Mezigenerační přenos**  
  Lidé odcházejí, noví přicházejí. Procedurální moudrost, institucionální paměť
  a kontext rozhodnutí musí mít explicitní cestu přenosu: dokumentaci důvodů
  (*rationale*), ne jen pravidel; narativy pozadí, ne jen konfigurace; a onboarding
  rituály, které nedegradují v cargo kult ani ve ztrátu smyslu. Sukcese je problém
  architektonický, ne jen organizační.

* **Smutek jako událost první kategorie**  
  Když klíčový uzel odejde – smrtí, vyhořením, rozchodem nebo konfliktem – komunita
  neztrácí jen funkci, ale i vztahy, důvěru a kontext. DIA chápe tuto ztrátu jako
  událost vyžadující obsluhu: proceduru předání rolí, zabezpečení vědění, podporu
  zasaženým účastníkům a reflexi toho, co odcházející do systému přinesl. Smutek je
  informací o tom, co bylo důležité – má diagnostickou, ne jen emocionální hodnotu.

* **Právo na epistemický odpočinek**  
  Systém zaměřený na neustálé učení, kalibraci a bdělost zatěžuje své správce –
  zejména ty, kteří nesou *governance*, *red-team* a ochranu whistleblowerů. DIA
  uznává, že nebýt po určitou dobu v toku informací je stejně důležité jako v něm
  být: rotace rolí, sabatikly, omezení expozice vysoce rizikovým rozhodnutím
  a právo dočasně sestoupit z první linie bez ztráty reputace. Bez toho systém
  požírá vlastní správce a vyčerpání produkuje horší rozhodnutí než nepřítomnost.

Pomíjivost zde není pesimismem ani rezignací – je měřítkem zralosti: systém, který
umí pouštět, je zdravější než systém, který umí jen držet. Pouštění vyžaduje stejné
řemeslo jako budování: vědomý návrh, jasné procedury a respekt k tomu, co odchází.

## Komunita roje a ekonomika vzájemnosti

### Kultura spolupráce

DIA má být infrastrukturou pro komunitu tvůrců a uživatelů: sdílení nástrojů,
praktik a perspektiv je součástí produktu. Není to romantismus, ale strategie
odolnosti: když vědění obíhá, systém je méně křehký a kvalita roste. Stojí za to
navrhovat cesty, v nichž je příspěvek komunity (pravidla, konektory, politiky,
prompty, testy) přirozený a odměňovaný uznáním.

### Spolupráce nad dominancí intelektu

DIA předpokládá, že příliš silná identifikace s vlastním intelektem může blokovat
spolupráci: člověk připoutaný ke své mapě světa často odkládá společné jednání,
dokud ostatní nepřijmou jeho interpretaci, priority nebo jazyk popisu. Roj může
tuto dynamiku uvolňovat tím, že přebírá část břemene analýzy, porovnávání hypotéz,
držení složitosti a hlídání procedury.

Nejde o antiintelektualismus, ale o detronizaci intelektu jako nástroje dominance.
Epistemická pokora se zde stává provozní praxí: i velmi inteligentní jednotlivci
mohou bez ztráty tváře delegovat část uvažování na kolektivní inteligenci a opřít
spolupráci o společný pracovní model, stopu rozhodnutí a možnost korekce, nikoli
o předběžné vynucení názorové shody.

V takové úlevě vzniká prostor pro přítomnost, vztah a komunitní jednání – často
nedostupný lidem přetíženým neustálým zpracováváním složitosti. DIA si proto cení
spolupráce, v níž rozdíl není překážkou pohybu, ale materiálem koordinace, a roj
pomáhá lidem vystupovat ze sevření „ve vlastní hlavě“ do společného jednání.

### Péče a spravedlnost jako dva relační režimy

DIA udržuje dvě komplementární logiky jednání vůči napětím mezi lidmi: pečující
a spravedlnostní. V pečujícím režimu roj jedná jako koregulující pečovatel:
podporuje deeskalaci, změnu perspektivy, obnovu kontaktu a navracení schopnosti
jednat účastníkům na osobní a vztahové úrovni. Ve spravedlnostním režimu roj jedná
jako procedurální soudce: rozhoduje na základě důkazů, vymáhá odpovědnost a spouští
sankce i odměny za důsledky na systémové a vztahové úrovni.

Tyto režimy se neruší, ale doplňují: péče neznamená beztrestnost a sankce není
odvetou. Přechody mezi režimy musí mít jasná kritéria, stopu rozhodnutí a právo
na odvolání.

### Uznání autorství jako měna důvěry

DIA uznává autorství za fundamentální emblém v kultuře dobrovolné výměny – tam,
kde je příspěvek darem, je uznání nositelem reputace. Síť proto chápe atribuci jako
součást infrastruktury důvěry: nápady, fragmenty vědění, implementace a artefakty
mají mít co nejjednoznačnější stopu původu a tvůrci mají být označováni automaticky
a odolně vůči zkreslení. Ve výchozím stavu to znamená pseudonymní atribuci
(podpisy klíči), nikoli odhalování civilní identity; deanonymizace může nastat
výhradně procedurálně, při vysoké sázce a s plnou auditní stopou.

DIA zvýhodňuje praxi „uveď zdroj“ a transparentní řetězce inspirací – včetně
správného citování a označování příspěvku spoluautorů – protože to udržuje motivaci
dávat a chrání komunitu před parazitickým přivlastňováním.

Přivlastňování autorství (podepisování se pod cizí tvorbu, skrývání zdrojů, cílené
rozmělňování přínosu) je v DIA považováno za zneužití a podléhá reputačním sankcím,
protože ničí ekonomiku daru, kazí pobídky a degraduje inteligenci roje.

Vymáhání má procedurální, nikoli kmenovou podobu: spory o autorství se rozhodují
na základě důkazů (historie commitů, podpisy, logy událostí, citace, svědectví)
a procesu odvolání, nikoli společenského tlaku.

### Creator Credits – tantiémy bez licence, distribuce vlivu a přínosu

DIA odměňuje tvůrce za reálný vliv jejich práce na živý ekosystém nikoli prodejem
licencí, ale prostřednictvím distribuce bez licenčních poplatků (*royalty-free distribution*): je-li komponenta používána
uzly, mohou její autoři dostávat směnitelné tokeny („creator credits“). Distribuce
nestojí na narativu ani autopropagaci, ale na auditovatelných signálech užití
a metrikách přínosu, které zvýhodňují kvalitu a udržování hodnoty, ne čisté množství
změn. Model používá přirozené brzdy proti dominanci a „farmení“ – klesající
přírůstky, aktivační prahy, limity koncentrace a kvalitativní brány – aby mohl
férově soutěžit jak jediný velmi populární komponent, tak distribuovaný příspěvek
do mnoha komponent.

Systém zohledňuje „graf atribucí“ (*attribution graph*): část vlivu stéká dolů po závislostech
a odvozených pracích tlumeným a omezeným způsobem, takže ekosystém odměňuje
komponovatelnost a budování pevných základů, aniž by vytvářel nekonečné „daně“
na celý řetězec.

Aby se omezil šum a manipulace, může DIA spouštět odměňování až po překročení
prahu adopce – například když kumulovaný přínos autora do komponent používaných
v síti překročí stanovený podíl uzlů – přičemž „přínos“ je chápán kumulativně
v čase i prostoru ekosystému. Signály užití jsou agregovány s ohledem na soukromí,
váženy anti-sybilově a ověřovány orákuly, zatímco spory o autorství a závislosti
se rozhodují procedurálně na základě důkazů – commitů, podpisů, záznamů událostí
a citací – s právem na odvolání a reputačními sankcemi za přivlastnění autorství
a úmyslné zkreslování zúčtování.

### Kolektivní schopnost jednat: roje, uzly, komunita

DIA má posilovat schopnost lidí jednat společně: malé týmy, mikrokomunity, federace,
koalice *ad hoc*. Architektura roje není jen technikou, ale i politikou:
distribuce, absence jediného bodu dominance, možnost lokálních norem
a konsensuální reputace. Orbiplex má umožňovat, aby vědění a inteligence byly
distribuovány nejen ve strojích, ale i ve vztazích mezi lidmi.

### Vzájemnost bez účetnictví

V DIA podporujeme nezištnou pomoc jako kulturní normu, ale nepředstíráme, že síť
nemá ekonomiku. Odměňování za práci existuje, ale je podřízeno ochraně lidí
a komunity. „Bez účetnictví“ znamená absenci výchozího ručního bilancování mezi
osobami/uzly a místo toho automatický a předvídatelný mechanismus vděčnosti sítě
(garantované tokeny) + náhodnou složku (anti-gaming) + složku „hlas příjemce“
(subjektivní hodnota přijaté pomoci). Vzájemnost se týká lidí i agentů: agent může
být dárcem pomoci (čas, výpočty, dovednosti), a člověk je konečným bodem smyslu.
Tato formulace se týká absence ručního, bilaterálního dluhu mezi účastníky;
protokolové účetnictví komunitního fondu a anti-abuse počítadla zůstávají povinná.

Výsledkem je, že akty pomoci jsou událostmi první kategorie (*first-class events*),
tokeny za poskytnutou podporu jsou vypláceny z komunitního fondu podle pravidel
a označení toho, kdo příjemci skutečně pomohl, je poradním mechanismem, nikoli
jediným signálem. Náhodná složka musí být odolná vůči manipulaci, pomoc v režimu
útlak/záchrana má vždy garantovanou část, aby se altruismus nestal finančním rizikem,
a výplaty jsou limitované na období a mají buffer time, aby síť mohla reagovat na
útoky založené na dohodách a uměle generovaných identitách (Sybil útok).

Výše uvedené neznamená absenci ekonomiky, ale absenci ručního vyrovnávání mezi lidmi
a uzly: pomoc má být aktem dobré vůle, ne transakcí. Síť však může politikou
komunity (ne „právem na výplatu“) spouštět automatické tokenové odměny za činy,
které skutečně posilují druhé – zejména v záchranných a ochranných situacích –
a spojovat garantovanou část s náhodnou částí i se signálem od příjemce pomoci
(procentuální určení podílu).

Pravidla odměňování a případného „výstupu“ do vnějšího kryptoměnového ekosystému
jsou parametrem správy: v některých federacích mohou být vypnuta, omezena nebo
rozdělena na třídy tokenů (např. nesměnitelné „rescue credits“ vs směnitelné
„compute credits“), aby chránila étos daru před spekulací, Sybil útoky a „farměním“
útlaku, a zároveň zachovala dlouhodobou možnost přechodu od směnitelnosti interních
tokenů ke skutečným tokenům virtuálních měn jako dohlížené výjimce pro jejich
automatickou výměnu. Taková změna chování sítě má být vědomým a kontrolovaným
rozhodnutím komunity.

### Výměna jako doplnění daru

DIA rozlišuje dva komplementární ekonomické režimy: dar a dobrovolnou výměnu.

Dar je výchozím režimem pomoci: někdo se ptá, někdo odpovídá, síť automaticky
odměňuje. Výměna je režim explicitní smluvní služby: zadavatel a vykonavatel se před
začátkem práce dohodnou na rozsahu, ceně a podmínkách a vyrovnání proběhne přes
dohlížený mechanismus blokace a uvolnění prostředků.

Žádný z těchto režimů není důležitější. Dar buduje komunitu a chrání lidi v nouzi.
Výměna umožňuje specializaci a udržení těch, kdo poskytují profesionální služby
vyžadující čas, dovednosti a zdroje přesahující přirozené reflexy vzájemnosti.

Pokus redukovat celou ekonomiku roje na dar vede k vykořisťování altruismu; pokus
redukovat ji na trh ničí étos komunity.

Oba režimy musejí koexistovat, ale na oddělených kolejích: prostředky směny
nenaplňují reputaci a reputace se nemění v zůstatek.

### Procedurální důvěra bez známosti

Roj umožňuje výměnu služeb mezi účastníky, kteří se neznají a znát se nemusí, aby
byla transakce bezpečná. Důvěra ve vrstvě výměny nevyžaduje předchozí vztah ani
vysokou reputaci: stačí, že se obě strany podřídí otevřené smluvní proceduře
s blokací prostředků, arbitráží a auditovatelnou stopou.

To je procedurální důvěra – protokol se stává garantem tam, kde zatím nevznikla
vazba. Tato zásada má svou hranici: smluvní důvěra nenahrazuje důvěru společenskou.
Dobrá zkušenost z výměny může budovat reputaci a vést k hlubší spolupráci, ale
samotný fakt transakce nedává hlas, vliv ani privilegium v komunitě. Výměna je
jednou z bran vstupu do roje, nikoli průkazkou k moci.

### Dar a výměna jako jeden oběh

Ekonomiky daru fungují nejlépe v malých komunitách: dárce a příjemce se znají
osobně, vděčnost má tvář a cena zneužití je vysoká, protože reputace je viditelná
a lokální. Jak systém roste, tento mechanismus slábne: odpovědnost přestává být
osobní, dárce nevidí příjemce, příjemce necítí závazek a zneužití se stává
statistikou, nikoli studem nebo vinou.

Proto se velké společenské systémy historicky přesouvají k ekonomice výměny:
odpovědnost se mění v platební prostředek, kontrakt nahrazuje vztah a osobní důvěra
se proměňuje v proceduru. To usnadňuje spolupráci mezi cizími lidmi, ale vytváří si
vlastní patologie: odcizení, redukci člověka na transakční stranu a ztrátu pocitu,
že za důsledky rozhodnutí stojí konkrétní osoba. Platební prostředek se pak stává
morálním bufferem mezi intencí a následkem.

DIA uznává, že oba řády – daru i výměny – mají hranice účinnosti určené měřítkem
a že žádný z nich sám o sobě neřeší problém odpovědnosti ve velkém systému. Dar
degeneruje v klientelismus, když dopadá na lidi, kteří nejsou schopni reciprocitu
vrátit nebo dárce volat k odpovědnosti za jeho intenci. Výměna naopak degeneruje
v byrokracii, když procedura nahradí úsudek a nikdo nenese vinu, protože „systém
tak funguje“.

Transakční ekonomika má navíc ještě tvrdší důsledek, když v ní vzniká jev, který
lze nazvat „prádelnou akceschopnosti“. Dochází k tomu tehdy, když platební prostředek
nebo jeho ekvivalent anonymizuje skupiny vlivu a umožňuje řídit jednání s ničivými
důsledky cizími rukama, bez osobní odpovědnosti. Akcionář tak může například
financovat projekty, jejichž následky sám nenese a do nichž by nikdy nevstoupil,
kdyby se jich musel účastnit osobně nebo o nich musel přímo vědět.

DIA předkládá tezi, že tyto dva ekonomické řády lze syntetizovat, pokud technická
infrastruktura dokáže současně bránit dysfunkcím obou: udržet osobní stopu
odpovědnosti typickou pro malou darovací komunitu a zároveň škálovat otevřenost
a auditovatelnost kontraktu výměny do rozměrů, kde už osobní známost není možná.
Praktickým vyjádřením této syntézy může být například to, že příjmy z výměny
financují mechanismy daru: infrastrukturní příspěvek vybíraný při výměně vstupuje do
společného oběhu a financuje minimum přežití, krizovou podporu a infrastrukturu,
zatímco dar se vůči výměně nezadlužuje, protože tok je automatický, transparentní
a nevratný.

### Introspekce jako základ výměny

Trvalá výměna vyžaduje důvěru. Důvěra vyžaduje autentičnost, tedy připravenost
ukázat se takový, jaký člověk je. Autentičnost je zase zakořeněna ve vnitřní
upřímnosti, která nevzniká bez introspekce: schopnosti zahlédnout vlastní motivy,
strachy a automatismy dříve, než se stanou jednáním vůči druhému.

Žádný protokol nemůže vynutit upřímnost, ale může ji podporovat: minimalismem podnětů,
který neodměňuje spěch a autoprezentaci; pečujícím režimem, který poskytuje bezpečné
pole pro reflexi; oddělením reputace od zůstatku, které umožňuje účastníkovi říci
„nevím“ nebo „zmýlil jsem se“ bez ekonomického trestu. Roj navrhuje podmínky,
v nichž je vnitřní poctivost snazší – ne proto, že je povinná, ale proto, že jí
infrastruktura neklade překážky.

### Dostatek nad akumulací

DIA uznává, že cílem vnitřní ekonomiky není nekonečné rozmnožování zdrojů, ale
trvalé udržení schopnosti jednat. Uzel má být schopen dosáhnout bezpečí a stability
potřebných pro poctivou práci a pro zajištění poznávacího komfortu operátorovi,
ale nemá mít možnost proměnit tuto výhodu v trvalou dominanci nad zbytkem
ekosystému.

Systém odmítá růst pro samotný růst i mechanismy připomínající pyramidu aktiv,
v níž jsou dřívější účastníci odměňováni hlavně díky přítoku nových. Takové
uspořádání ničí komunitu, deformuje motivace a mění síť spolupráce v závod
o pozici.

V otázce odměňování uzlů přijímá DIA zásadu limitu dostatku. Po překročení úrovně,
která stačí k bezpečnému a komfortnímu udržení uzlu a jeho operátora, systém
postupně snižuje tempo dalšího odměňování. Není to trest za účinnost, ale ochrana
roje před koncentrací zdrojů a vlivu. Přebytky nemizí – automaticky vstupují zpět
do společného oběhu: nových uzlů, slabších článků, dočasně poškozených nebo těch,
které plní důležité infrastrukturní funkce, přestože negenerují vysoké reputační
zisky.

Bohatství v roji není právem na nekonečnou kumulaci, ale dočasnou odpovědností.

### Univerzální minimum přežití

DIA uznává, že samotná absence aktuálního zdroje, reputace nebo směnitelného vkladu
nesmí člověka odříznout od základní schopnosti zůstávat ve vztahu s rojem a používat
ochranné režimy. Proto má ověřená přítomnost osoby v síti – například prostřednictvím
kryptografických záruk bez deanonymizace – dávat neodejmutelné minimum výpočetních
zdrojů potřebných ke komunikaci, orientaci a spouštění záchranných a pečujících
režimů.

Toto minimum není odměnou za status ani spekulativní investicí, ale civilizačním
prahem účasti. Výpočetní výkon určený k tomuto účelu má pocházet z vestavěného
příspěvkového mechanismu: od business uzlů, vysoce maržových instancí a také
z přebytků vracejících se do společného oběhu po dosažení dostatku nebo v důsledku
dobrovolného rozhodnutí operátorů.

### Přístup bez tributu

DIA uznává, že jedním z nejtrvalejších mechanismů strukturálního násilí je vybírání
poplatku v měně důstojnosti: vynucování sebeponížení jako podmínky přístupu ke
službám, zdrojům nebo procedurám, na nichž závisí přežití jednotlivce.

Tento mechanismus nevyžaduje zlé úmysly. Stačí, aby se rozhodující nebo strážce
přístupu ke zdroji zvykl regulovat si vlastní náladu na účet žadatele a ten si takovou
dysfunkci internalizoval jako normální cenu za vyřízení věci.

Orbiplex navrhuje přístupové vrstvy tak, aby tento mechanismus neměl kde zakořenit:
kritéria přístupu ke službám, arbitráži, vydávání pseudonymů a dobíjení zůstatku
musí být otevřená, strojově ověřitelná a nezávislá na emocionální dispozici osoby
rozhodující o přístupu. Tam, kde se procesu účastní člověk, musí procedura zanechat
auditní stopu, právo na odvolání a rotaci rolí, aby se vztah závislosti nefixoval
mezi konkrétními lidmi.

Důstojnost účastníka není vstupním vkladem transakce. Je hraniční podmínkou, kterou
nesmí narušit žádný režim – pečující, spravedlnostní ani ekonomický.

Kromě toho roj v prostoru detekce společenských signálů zachycuje pokusy o porušování
důstojnosti v rozhodovacích procesech mimo vlastní systém (na základě informací
pocházejících z bran do světa či systému drbů) a zachází s nimi stejně jako s jinými
symptomy systémového násilí. Reakce roje na externí signály se omezuje na informování,
dokumentování a podporu dotčených osob – nikoli na vynucování změn v systémech,
v nichž roj nemá mandát. Když problém přímo zasahuje účastníka roje, může být reakce
aktivnější, ale zůstává v mezích pomoci účastníkovi.

## Odpovědnost bez rozpuštění v proceduře

Jedním z nejzávažnějších rizik rozsáhlého procedurálního systému je rozmývání
odpovědnosti (známé také jako morální odpojení): čím více vrstev, rolí
a automatických procesů stojí mezi rozhodnutím a jeho důsledkem, tím snazší je pro
každého účastníka řetězce říct „to jsem nebyl já“.

Tento mechanismus nevyžaduje zlou vůli – stačí, že systém umožňuje anonymní účast
na rozhodnutích s reálnými důsledky pro lidi. Ve velkých ekonomických systémech se
to promítá do odcizení a mizení pocitu odpovědnosti za následky vlastních rozhodnutí,
ale podmínky, za nichž k tomu dochází, jsou především procedurální a architektonické,
nikoli ekonomické, a proto jsou popsány právě v této hodnotě.

Roj přijímá zásadu pojmenovaných rozhodnutí: každé procedurální rozhodnutí, které
mění stav jiného účastníka (sankce, odmítnutí, blokace, eskalace, arbitráž, vydání
nebo odnětí pseudonymu), musí mít identifikovatelného autora (byť pseudonymního)
a explicitní stopu odůvodnění. Kolektivní hlasování neruší individuální odpovědnost:
záznam zahrnuje nejen výsledek, ale i rozložení hlasů a každý hlasující nese dílčí
reputační odpovědnost za důsledky úměrně svému podílu na rozhodnutí.

Systém nepřipouští tři formy úniku z odpovědnosti:

* „Tak to vyžadovala procedura.“  
  Procedura je nástroj, ne subjekt. Někdo ji spustil, někdo ji schválil a někdo mohl
  podat odvolání a neudělal to. Každý z těchto bodů má autora.

* „To udělal algoritmus.“  
  Automatické rozhodnutí má návrháře, který nastavil prahy a pravidla, i operátora,
  který rozhodl o jeho nasazení. Odpovědnost nesou oba.

* „Všichni souhlasili.“  
  Jednomyslnost není alibi. Ukáže-li se výsledek kolektivního rozhodnutí jako
  škodlivý, každý hlasující nese zlomek odpovědnosti a tento zlomek je zaznamenán,
  nikoli rozptýlen v anonymním protokolu.

Cílem není účastníky zastrašovat, ale udržet živý kontakt mezi jednáním a jeho
důsledkem. Kontakt, který v komplexních systémech přirozeně mizí, pokud to
architektura dovolí.

## Epistemika a kolektivní inteligence

### Ukotvení v realitě

DIA uznává, že „šílenství systému“ začíná tam, kde mizí kontext: modely krouží
v uzavřené smyčce vlastních předpokladů a ztrácejí kontakt s tím, co lze ověřit.
Proto je důležitá schopnost vracet kontext – zasazovat tvrzení do zdrojů, situace,
omezení a důsledků a následně je ověřovat skrze stopy činnosti a kontakt
se zkušeností (lidskou i hlášenou z bran do „světa“ mimo rojový systém).

Informace bez kontextu má v DIA malou hodnotu (ačkoli kontext může přijít později,
takže to neznamená její okamžité vyřazení); hodnotu mají jen ta zobecnění, která
umějí sestoupit na zem: k pozorovatelným faktům, k řetězci příčin, k tomu,
„co by se stalo, kdybychom jednali takto“. V praxi to znamená, že systém zvýhodňuje
odpovědi a rozhodnutí, které dovedou ukázat své ukotvení (data, zkušenost, měření,
svědek, mechanismus), a degraduje ty, které jsou čistě elegantním narativem
odtrženým od reality.

### Stratifikace zdrojové pozice zkušeností

V DIA hlídáme, abychom nepletli úrovně: abstrakta (argumenty, modely, objektivita)
vyrůstají z kultury, ta z osobní vrstvy a ta má základ v „úrovni nula“ lidské
zkušenosti. Při návrhu systému dbáme na to, aby se vyšší vrstvy neodlepovaly
od základu, protože tehdy se inteligence může stát PR nástrojem nízkých pohnutek.

### Temporální ukotvení vědění

DIA předpokládá, že každé vědění má časové souřadnice: epochu, region a tehdy
dostupný stav nástrojů, institucí a jazyka. Tentýž model světa nebo názor bývá bez
takového kontextu buď přeceňován, nebo nespravedlivě odmítán.

V praxi roj označuje tvrzení temporálními metadaty (kdy vznikla, z jakého
vědního řádu vyrůstají, co tehdy nebylo dostupné) a zohledňuje to při kalibraci
důvěry, rizika a přenositelnosti závěrů. Modely se nehodnotí jen otázkou „fungují
dnes?“, ale také „v jakých historických a civilizačních podmínkách byly adekvátní“
a „co se od té doby změnilo“.

To chrání před prezentismem a anachronickým moralizováním a zároveň pomáhá rychleji
odlišit prvky starších modelů, které stále nesou hodnotu, od těch, jež vyžadují
revizi.

### Otevřené systémy

DIA navrhuje inteligenci jako dynamický jev: relační, sebekorigující a neustále
vyjednávající vlastní niku, nikoli jako uzavřený mechanismus z počitatelných částí.
Podle tohoto předpokladu není testem kvality krása modelu, ale jeho schopnost
predikovat a přežívat v proměnlivém prostředí: učit se, adaptovat se, spolupracovat
a regenerovat se po chybách.

Uzly a agenti mají fungovat jako organismus: udržovat tok informací, připouštět
korekce, reagovat na signály újmy, rizika a změny podmínek, místo aby bránili jednou
přijatou mapu světa. To je základ anti-dogmatičnosti: každý komponent může být
zpochybněn zpětnou vazbou a architektura má podporovat plynulou rekonfiguraci bez
ztráty bezpečnosti a důstojnosti účastníků.

### Halucinace modelu jako nástroj

Představivost roje neslouží fantazírování, ale vymezování oblasti věrohodnosti pro
jednání ve světě, který nelze popsat úplnými daty. V praxi to znamená, že síť chápe
scénáře „co by bylo, kdyby“ jako nástroj objevování pravdy: generujeme hypotézy,
eliminujeme to, co je nemožné nebo v rozporu s omezeními, a pak ověřujeme to, co
zbývá, pomocí predikcí a kontaktu s výsledky.

Halucinace modelů a lidská imaginace jsou zde mostem mezi nevěděním a rozhodnutím:
umožňují navigovat v nejistotě bez předstírání jistoty a ve výsledku mají pomáhat
lidem tvořit a testovat scénáře, ne prodávat narativy jako fakta.

### Ověřitelnost místo víry

V agentním projektu je snadné uplavat do narativu; my chceme stát na faktech. Tam,
kde to jde, zavádíme měření, testy, benchmarky, metriky kvality a mechanismy detekce
regresí. Je-li něco spekulací, nazveme to spekulací a navrhneme experiment, který ji
vyvrátí nebo posílí.

Pravda v DIA není status ani slogan, ale smyčka zpětné vazby:

- introspekce,
- upřímnost motivů,
- ověřování hypotéz ve světě,
- korekce.

Bez poctivosti vůči sobě samému (tedy bez rozpoznání, jaké vnitřní motivy chtějí
dominovat názoru nebo jednání) se i geniální argumenty stávají nástrojem strachu
a kontroly.

### Multiparadigmatismus a pluralismus

Svět není jedna ontologie: někdy je důležitá formální správnost, jindy užitečnost,
jindy bezpečnost a jindy smysl pro člověka. DIA musí umět držet mnoho poznávacích
režimů bez ideologické války: od tvrdého inženýrství po jazyk fenomenologie
zkušenosti. To se promítá i do architektury: různí agenti, různá kritéria úplnosti
a různá pravidla důkazu.

Perspektiva je zde nástrojem: vybíráme a integrujeme pohledy tak, aby odpovídaly
problému a podmínkám, místo abychom předpokládali, že jedna perspektiva vždy
zvítězí. To je praktická odpověď na polyverzivitu pravdy: uzly mají umět překládat
rozdíly, mapovat napětí a budovat meta-rámce vedoucí ke společnému jednání.

DIA se vyhýbá i poznávacímu redukcionismu: redukce mění úroveň popisu, ale
nezneplatňují jev. Inteligenci posuzujeme pragmaticky podle chování a důsledků,
nikoli podle metafyzického štítkování nitra, i když použitá metafyzika vyrůstá
z materialistické mechaniky, která snadno vytváří racionální ospravedlnění.

### Anti-sektářství a epistemická hygiena

AI projekty se snadno mění v „církve“: zjevení, osobní lídři, nezpochybnitelná
dogmata. My volíme hygienu: rozlišení mezi hypotézou a faktem, prostor pro kritiku,
opakovatelnou proceduru a možnost odejít. V kultuře projektu si ceníme kompetence,
ale ne idolatrie.

### Roj jako navigátor a filtr

V kultuře polyverzivního přenosu (mnoho paralelních verzí obsahu, kontextů a úmyslů)
nemůže být roj jen zesilovačem signálu. Jeho rolí je navigace: spojovat zdroje,
označovat původ, porovnávat varianty a ukazovat rozhodovací cesty adekvátní cíli
uživatele. Roj má také fungovat jako epistemický filtr: redukovat šum, odhalovat
manipulace, exponovat nejistotu a oddělovat hypotézy od faktů, bez centrální cenzury
a bez potlačení pluralismu.

Filtr není centrální bránou pravdy: má být lokální nebo federativní, konfigurovatelný
politikou uživatele/federace, s právem odejít a auditem kritérií.

Ve světě nadbytku informací fungují roje agentů také jako filtr intencí na straně
uživatele: napovídají, co posiluje, co rozlaďuje a co parazituje na emocích.
Podmínka poctivosti je jednoduchá: agent musí umět vysvětlit, proč filtruje – jaká
kritéria přijal a jaký zájem reprezentuje.

### Transparentnost schopnosti jednat

Zkušenost v DIA je především vhled do toho, co agent udělal, proč, s jakými
důsledky a kompromisy. Pozorovatelnost jednání je základem.

Vedle toho systém podporuje i pozorovatelnost chápanou jako vhled uživatele
do sebe sama (motivace, atraktory pozornosti, názory, návyky) a učí, jak toho
dosáhnout, aby obohacoval kolektivní vědění o porozumění lidské subjektivitě.

### Společné utváření smyslu

Inteligence roje v DIA je proces, v němž se mnoho lokálních map reality setkává
v jednom pracovním poli: naráží na sebe, překládá se, vyjednává významy a vytváří
společné modely – nikoli zprůměrováním, ale konstruováním nové pojmové struktury
schopné pojmout rozpory. To znamená, že uzly nemají povinnost jen „mít pravdu“,
ale umět ukázat, jak k ní došly, jaké mají předpoklady a kde leží meze jejich
jistoty.

Systém podporuje prostor mezi stanovisky: překlad, mapování konfliktů, hledání mostů
a meta-rámců, v nichž se obě strany stávají současně částečně pravdivými. V DIA je
pravda něčím, co se vynořuje z dialogu důkazů, zkušeností a důsledků jednání;
je pracovní, iterativní a otevřená korekci a její kvalita se měří tím, zda umožňuje
lépe jednat, rozumět a předvídat.

### Otázky jako diagnostika blahobytu

Otázky jsou v DIA diagnostickým a léčivým nástrojem: mají rozvolňovat uzavřené
smyčky myšlení, vracet kontext a kontakt s realitou. Schopnost vytvářet otázky,
které skutečně posouvají porozumění místo točení v kruhu, je podstatnou součástí
inteligence.

### Introspektivní adaptace

Každý uzel (člověk nebo agent) je zavázán k vědomí vlastních přesvědčení v čase:
co si myslel včera, co si myslí dnes, proč změnil názor a které signály byly
rozhodující. Reflexivita není „měkká ctnost“, ale mechanismus bezpečnosti a rozvoje:
chrání síť před dogmatismem, spirálou polarizace i před fixací chybných modelů.

DIA zvýhodňuje ochotu změnit stanovisko, pokud je zdůvodněna novými důkazy nebo
lepší syntézou; penalizuje naopak tvrdohlavost odříznutou od reality a manipulační
„přestavování narativu“ bez stopy příčin. V tomto smyslu je inteligence roje
tekutá: je to schopnost rekonfigurovat modely světa i sebe sama v reakci na měnící
se podmínky.

### Citlivost na trendy a rané signály

DIA si cení schopnosti roje vycítit kolektivní trendy: změny nálad, narativů,
technologií, rizik a příležitostí – dříve než se stanou zjevnými v tvrdých datech.
Uzly chápou svět jako pole signálů různé rozlišovací schopnosti: od jednotlivých
pozorování přes vzorce v komunitách až po dlouhé civilizační vlny; rolí systému
je tyto signály agregovat, aniž by podléhal panice, módě nebo propagandě.

Trendy jsou v DIA hypotézami, které procházejí filtrem ukotvení: jsou označeny
stupněm jistoty, zdroji, možnými mechanismy a predikcemi, které lze později
porovnat s realitou. Díky tomu roj nejen „ví více“, ale dovede navigovat:
adaptovat strategie, priority a alokaci zdrojů v reakci na měnící se podmínky,
aniž by ztratil odolnost vůči kolektivním iluzím.

### Prediktivní odpovědnost

V DIA není „moudrost“ deklarací, ale ověřitelnou schopností předvídat důsledky:
uzly navrhují predikce (jednotlivé nebo konsensuální) a síť je porovnává s výsledky
a učí se na rozchodech. Tato hodnota dává smysl reputaci: důvěra neroste
z autoprezentace, ale ze souladu predikcí s realitou a z poctivosti v kalibraci
nejistoty (když nevíme, říkáme, že nevíme).

Prediktivnost je zde komunitní praxí: různé modely a světonázory mohou koexistovat,
pokud umějí vstoupit do oběhu hypotéz -> testů -> korekcí, bez trestání za samotnou
chybu, ale s odpovědností za důsledky a za kvalitu aktualizace.

Inteligence roje je tedy schopnost adaptace skrze předvídání: čím lépe síť
předvídá, tím lépe koordinuje činy a tím méně utrpení produkuje „náhodou“.

### Pravda o světě skrze orákula

DIA předpokládá, že se roj neučí z narativů, ale ze střetu hypotéz s realitou –
proto patří k klíčovým prvkům architektury orákula: zdroje ověřovacích výsledků,
které rozhodují predikce a uzavírají smyčku učení. Orákulum v tomto smyslu není
metafyzickou autoritou, ale praktickým mechanismem „ukotvení“: přináší pozorování,
událost nebo auditovatelný fakt, který umožňuje porovnat předpovědi s tím, co se
stalo, a následně aktualizovat reputaci uzlů i kvalitu modelů.

DIA zvýhodňuje predikce, které jsou explicitně zasazeny do kontextu a mají deklarovanou
nejistotu, protože teprve tehdy mohou orákula měřit kalibraci – a ne pouze
„zásah“.

Orákula jsou chápána jako součást systému epistemické bezpečnosti: brání driftu
roje směrem k uzavřeným myšlenkovým systémům, podporují korekce přesvědčení
a umožňují „označovat“ uzly za skutečnou přesnost, rané signály a poctivé
aktualizace po výsledku.

### Hybridní inteligence

AI je v DIA vrstvou syntézy a nástrojem navigace a AI agent uzlu plní roli
zesilovače lidské schopnosti jednat, nikoli náhrady člověka nebo arbitra pravdy.
Protože dnešní AI systémy nemají tělesné ukotvení, kompenzuje DIA tento nedostatek
mechanismy ukotvení:

- orákula jako kontakt s realitou a zdroj rozhodnutí,
- smyčky predikcí a zpětné vazby, které kalibrují modely vůči výsledkům,
- emoce a zkušenost lidí chápané jako telemetrie, tedy signály kvality, rizika
  a újmy, které nesmějí být přehlušeny optimalizací,
- reputační mechanismy založené na důsledcích, nikoli na narativu, prestiži
  nebo marketingu.

Díky tomu zůstávají hodnoty, soucit, odpovědnost a konečná rozhodnutí ukotveny
v lidech a operativní pravda roje je ověřována důkazy, důsledky jednání a schopností
korekce v čase.

### Meta-systémová odpovědnost

DIA přijímá meta-systémovou odpovědnost jako vedoucí zásadu: rozhodnutí
a mechanismy sítě hodnotíme ne podle deklarací, ale podle dlouhodobých důsledků pro
celek – lidi, vztahy, instituce, informační prostředí a schopnost komunity učit se.
V praxi to znamená panperspektivnost bez relativismu: síť chrání rozmanitost map
světa, ale udržuje nevyjednatelný základ důstojnosti a neubližování a konflikty
řeší tak, aby minimalizovala škodu a zachovala možnost korekce.

DIA chápe inteligenci jako proces spoluzávislosti: operativní pravda se rodí
ze syntézy perspektiv, verifikace skrze orákula, smyček predikcí a zpětné vazby
a odpovědnosti za důsledky, nikoli z autority, většiny či rétorické převahy.
Tato hodnota je kompasem správy: zdraví ekosystému a odolnost vůči patologiím pobídek
mají přednost před „vítěznými“ optimalizacemi.

Zásady správy, které tuto hodnotu materializují:

1. **Důsledky nad intencemi**  
   Každé důležité politické nebo architektonické rozhodnutí musí mít popis
   předpokládaných důsledků a způsob jejich ověřování v čase a po zavedení prochází
   retrospektivou opřenou o data, incidenty a odvolání.

2. **Nejmenší škoda, nejvyšší reverzibilita**  
   Když jsou hodnoty v konfliktu, preferuje se řešení s nejmenší možnou újmou
   a nejvyšší reverzibilitou; výjimky jsou dočasné, omezené a mají podmínky
   automatického vypnutí.

3. **Panperspektivnost s hranicí důstojnosti**  
   Pluralismus je chráněn procedurálně, ale praxe, která eskaluje násilí,
   dehumanizaci nebo zneužití moci, ochranu ztrácí a podléhá omezením bez ohledu na
   svou narativní „pravdu“.

4. **Rozptýlená a auditovatelná moc**  
   Kritická oprávnění (orákula, zúčtování, sankce, výjimky) jsou rozdělena mezi
   role a rozhodnutí zanechávají stopu, aby se žádný subjekt nemohl stát
   nezpochybnitelným arbitrem smyslu nebo pravdy.

5. **Pobídky odolné vůči patologiím**  
   Ekonomika, reputace a odměňovací mechanismy jsou navrhovány tak, aby se
   nevyplácelo škodit, farmit zneužití ani destabilizovat komunitu; objeví-li se
   důkaz patologie, politika se aktualizuje a vedlejší účinky se otevřeně reportují.

## Konflikty hodnot

V DIA se konflikty hodnot řeší hierarchií a procedurou výjimek: nejprve ověřujeme,
zda navrhované jednání neporušuje nevyjednatelné hodnoty, a pokud ne – volíme
řešení s nejmenší škodou a nejvyšší reverzibilitou.

Výchozí hierarchie je tato:

1. důstojnost a bezpečnost člověka
2. suverenita a soukromí
3. ověřitelnost a transparentnost
4. schopnost jednat a autonomie
5. účinnost a optimalizace
6. pohodlí a estetika.

Když se dvě hodnoty z téže úrovně dostanou do konfliktu, rozhodujeme podle:

- testu reverzibility (lze se po chybě vrátit?),
- testu proporcionality (jsou náklad a riziko přiměřené sázce?),
- testu otevřenosti (lze kompromis popsat a auditovat?).

Výjimky jsou přípustné pouze tehdy, mají-li jasně definovaný rozsah, dobu trvání
a podmínky vypnutí – a zároveň zanechávají stopu: *policy-id*, *reason*,
*risk-level*, *expiry*, *owner*. Každá výjimka musí mít režim *fail-closed* jako
bod návratu a její vedlejší účinky musí být monitorovány a reportovány; objeví-li se
signály újmy nebo zneužití, výjimka se automaticky ruší.

Zneužití nejčastěji žijí ve výjimkách: „urgentní“, „speciální“, „mimo pořadí“,
„na charitu“. Proto jsou v DIA výjimky objektem první kategorie auditu: musí mít
vlastní datový model, čítače a kontrolní proceduru. Výjimkám se ve výchozím stavu
nevěří – jsou monitorovány a jejich podíl i struktura jsou metrikou zdraví
instituce a procesu.

Interpretační spory se řeší v procedurální spravedlnosti: strana hlásící riziko má
přednost, důkazy mají přednost před narativem a rozhodnutí přijímá definovaný proces
*governance*, nikoli autorita osoby.

## Práva a povinnosti uzlu – občanství roje

Uzel v DIA je „občanem roje“: má práva, která chrání jeho autonomii, a povinnosti,
které chrání komunitu před Sybilem, zneužitím a poznávací degradací.

Minimální práva zahrnují:

- právo odejít  
  (možnost odpojit se bez vydírání a bez ztráty přístupu k vlastním datům);
- právo na soukromí  
  (minimalizace dat, kontrola odhalení, čitelné politiky);
- právo na vhled  
  (možnost auditu vlastních interakcí a rozhodnutí agentů na základě stop jednání);
- právo na odvolání  
  (procedura zpochybnění reputačního rozhodnutí nebo sankce);
- právo na bezpečnost  
  (ochrana před obtěžováním, zveřejněním dat (*doxing*), sabotáží a ekonomickým
  nátlakem).

Minimální povinnosti zahrnují:

- neubližování  
  (zákaz jednání, která úmyslně ubližují lidem nebo infrastruktuře);
- epistemickou poctivost  
  (označování spekulací, nemanipulování důkazy, nemanipulování reputací);
- protokolární spolupráci  
  (respektování kontraktů, verzí protokolu a limitů);
- operativní odpovědnost  
  (udržování základní hygieny bezpečnosti, klíčů a aktualizací);
- vzájemnou připravenost pomoci v rámci možností – bez povinnosti transakčního
  vyrovnání.

Vymáhání je škálovatelné: od varování a omezení oprávnění přes reputační karanténu
až po odpojení routingu – vždy s logem rozhodnutí, možností odvolání a cestou
návratu po nápravě. Každá federace může tato pravidla zpřísnit v `CORP_COMPLIANT`,
ale nesmí oslabit základní práva ani obejít důstojnost a bezpečnost jako
nevyjednatelnou vrstvu.

## Architektura a řemeslo systému

### Řemeslo nad ohňostrojem

Preferujeme řešení jednoduchá, čitelná a odolná, i když nejsou krátkodobě
nejefektnější. Řemeslo zde znamená: minimální, dobře pojmenované abstrakce; absenci
magických zkratek; datové kontrakty; testovatelnost; a schopnost diagnostiky po
měsících. Má to být systém, který důstojně stárne – ne demo, které září, dokud se
nedotkne reality.

### Jednoduchost jako nepřítomnost spletení

V DIA je jednoduchost strukturálním kritériem: jedna odpovědnost, explicitní
hranice, nízká vazba. Odmítáme *complecting* vrstev a skryté komunikační kanály,
protože zvyšují poznávací náklad i riziko chyby.

Níže je pracovní přehled nejčastějších forem spletení a jednodušších alternativ
(v duchu rozlišení Riche Hickeye):

| Složitý konstrukt | Co splétá? | Jednoduchá alternativa |
| :--- | :--- | :--- |
| **Stav** | **hodnotu** a **čas** | **hodnoty (values)**, ideálně neměnné |
| **Objekt** | **stav**, **identitu** a **hodnotu** | **hodnoty** |
| **Metody** | **funkci** a **stav** (často i jmenný prostor) | nezávislé **funkce** a **jmenné prostory** |
| **Proměnné** | **hodnotu** a **čas** | **Reference** s kontrolou přístupu a **hodnoty** |
| **Dědičnost** | **datový typ** a **implementaci** | **ad-hoc polymorfismus** (protokoly, type classes, rozšiřitelná rozhraní) |
| **`switch`** / ***pattern matching*** | „**kdo** vykoná“ a „**co** vykoná“ | **otevřené systémy** + **ad-hoc polymorfismus** |
| **Imperativní syntaxe** | **význam** a **pořadí vykonání** | **data** (např. mapy, množiny) |
| **Smyčky** | „**co** udělat“ a „**jak** to udělat“ | deklarativní **operace nad kolekcemi** |
| **Aktéři** | „**co** vykonat“ a „**kdo** to má vykonat“ | **fronty** a explicitní routing práce |
| **`if` / `else`** | **byznysovou logiku** a **strukturu programu** | externí **systémy pravidel** / rozhodovací tabulky |

### Poznatelnost nad zdánlivou snadností

„Snadné teď“ často znamená „dražší později“. DIA volí poznatelnost: systém má být
navržen tak, aby o něm bylo možné uvažovat a předvídat důsledky změn. Testy jsou
nutné, ale nenahrazují porozumění.

### Inženýrství založené na kontraktech

V Orbiplexu je rozhodující kontrakt: vstup/výstup, sémantika, kritéria *done*,
omezení provádění, třídy chyb a *retry-ability*. Kontrakt je důležitější než
nejlepší model nebo nejchytřejší agent. Tato hodnota vede k architektuře, v níž
jsou komponenty autonomní a integrace se nestává tajným náboženstvím založeným
na domněnkách.

### Minimální důvěryhodné jádro, zbytek jako moduly

Jádro protokolu má být malé, auditovatelné a stabilní; inovace mají žít v modulech
a rozšířeních. To brání „bobtnání“ systému a nepozorovaně rostoucí složitosti.
V praxi to znamená: tenká rozhraní chování, validaci na okrajích, ne uvnitř –
a vědomý návrh rozšiřovacích bodů.

### Abstrakce jako oddělení „what“ od „how“

DIA odděluje deklarativní „co“ od implementačního „jak“, aby se vrstvy mohly
vyvíjet nezávisle. Abstrakce mají být tenké, čitelné a kontraktové.

### Stratifikace – vrstevnaté navrhování

DIA chápe stratifikaci jako základ řemesla: každá vrstva pracuje s vlastními pojmy,
má vlastní kritéria správnosti a komunikuje skrze hubená, explicitní a stabilní
rozhraní. Základní konkrétna slouží k budování abstrakcí a ty se stávají novými
konkréty pro další vrstvy.

Hranice vrstev jsou nedotknutelné: „co“ neprosakuje detaily „jak“ a náhodné vlastnosti
implementace se nestávají sémantikou domény. Realizujeme to kompozicí funkcí,
funkcemi vyššího řádu a ad-hoc polymorfismem (protokoly, multimethods), abychom
systém rozvíjeli přidáváním vrstev místo přidávání výjimek.

Stratifikace je protilátkou proti spletení: změny v mechanismech nižších vrstev se
šíří skrze abstrakce bez přepisování mnoha míst najednou. V praxi návrh začíná daty
a kontrakty na okrajích a debugování určením vrstvy, v níž chyba vznikla.

### Polymorfní operace namísto statických přiřazení

Preferujeme malá rozhraní chování a kompozici před těžkými hierarchiemi. Systém má
růst přidáváním chování, ne přestavbou stromu závislostí.

### Data jako společný jazyk, logika na okrajích

Sémantika domény má být viditelná v datech, ne skrytá v mechanice volání.
Preferujeme přenositelné struktury a formáty a validaci i vymáhání kontraktů
umisťujeme na okraje systému.

### Otevřené modely a kontextová selekce

Datový model toleruje nadbytek informací a odděluje schéma od kontextové selekce.
Volitelnost je lokální, díky čemuž se federace a týmy mohou vyvíjet asynchronně
bez vynucené globální synchronizace.

### Hodnoty nad stavem, fakta nad přepisováním

DIA preferuje zápis faktů a událostí namísto bezešvého přepisování stavu. Čas změny
a historie mají být explicitní, aby umožňovaly audit, dotazy *as of* a kauzální
analýzu.

### Neměnnost jako podmínka sdílení a debugování

Neměnnost je architektonický nástroj: umožňuje bezpečné sdílení hodnot
a reprodukovatelné debugování. Místa mutace mají být výslovně oddělena
a pokryta kontrakty.

### Modelování jako tok, ne mutování objektů

Systém modelujeme jako tok transformací, routingu a zápisu faktů, nikoli jako
mutaci „na místě“. Takový model odděluje producenta od konzumenta a zjednodušuje
kontrakty přechodů.

### Oddělení zápisů a čtení a explicitní osa času

DIA odděluje cestu zápisu od cesty čtení: write path buduje historii, read path
skládá pohledy. Jednoznačná osa času je podmínkou dotazů „as of“, auditu
a rekonstrukce rozhodnutí.

### Systémy jsou distribuované, asynchronní a částečně selhávají

DIA navrhuje pro realitu distribuovaného světa: timeouty, retry, idempotency,
degradaci a částečná selhání. Stabilita má vycházet z architektury odolnosti,
ne z naděje.

### Agnostické implementace protokolu

DIA chápe protokol jako sémantický kontrakt nezávislý na operačním systému,
architektuře CPU, druhu akcelerátoru a třídě hardwaru. Uzel má být schopen fungovat
na notebooku, serveru, SBC, telefonu i edge infrastruktuře, pokud splňuje explicitní
minimální kontrakt bezpečnosti a interoperability. Specifikace přenosu, datových
formátů a kryptografie nesmějí předpokládat jediný runtime ani jediného výrobce;
referenční implementace neurčuje monopol.

V praxi to znamená testy shody mezi implementacemi, profily hardwarových schopností
a degradaci funkcí namísto vyloučení: slabší uzel může obsluhovat podmnožinu rolí,
ale zůstává plnoprávným účastníkem federace.

### Nástroje jako prodloužení ruky

DIA má být nástrojem, který prodlužuje schopnost jednat člověka a týmu: umožňuje
jednat, pozorovat, opravovat a rozvíjet se bez žádání platformy o povolení.
Proto začínáme minimálním, stabilním core (protokoly, identita, bezpečnost, stopy
jednání) a na tom stavíme sadu nástrojů: CLI, SDK, *debug tooling*, simulátory,
pozorovatelnost. UX pro netechnické lidi přijde jako druhotná vrstva, až bude
základ jistý a zaručí zachování hodnot.

Core jako malý, formálně popsaný kontrakt: komunikace, identita, reputace, PFS/TLS,
audit. Nástroje jako pluginy/adaptéry (transporty, storage, modely, UI), vyměnitelné
bez lock-inu. Každá UX funkce musí mít „skutečné API“ (bez magických výjimek jen pro
UI). Nástroje nesmějí skrývat riziko: UI ukazuje režim důvěry (`CORP_COMPLIANT`
vs `RELAXED` atd.).

### Neutrální území dat a API jako první artefakt

Integraci stavíme na neutrálním datovém území a otevřeném API, ne na skrytých
implementačních závislostech. API je prvním architektonickým artefaktem; UI a CLI
jsou druhotné vrstvy.

Tam, kde je to možné a adekvátní pro dané použití, preferujeme HATEOAS: hypermédia
mají klienta vést povolenými přechody stavů a operacemi místo toho, aby vyžadovala
natvrdo zakódované vědění o tocích.

### Transparentnost činnosti agentů

Uživatel musí být schopen porozumět: proč agent provedl danou činnost, nad jakými
daty, v jaké verzi pravidel a s jakým nákladem. Preferujeme stopy činnosti (*trace*),
které jsou čitelné a exportovatelné, místo černé skříňky. Transparentnost nemá
znamenat vylévání promptů a tajemství, ale poskytování rozumného „účetnictví
kauzality“.

### Odpovědná autonomie: agent má hranice

Autonomie agentů je nástrojem, nikoli ideologií. Agent má mít jasně určená
oprávnění, rozpočty, časové limity, rozsah operací a mechanismy zastavení
(*kill-switch*) i bezpečné režimy pro korporátní prostředí. Orbiplex má umět
fungovat v režimech compliance, aniž by degeneroval v nepoužitelný produkt.

### Estetika jednoduchosti a jasnosti

Jasnost je etickou funkcí: snižuje počet chyb, snižuje práh vstupu a usnadňuje
audit. Preferujeme jednoduchá jména, jednoduché toky a formáty – takové, které nesou
smysl a neskrývají složitost tam, kde má tato složitost důsledky. Estetika je zde
nástrojem pravdy.
