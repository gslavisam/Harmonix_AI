from __future__ import annotations

from typing import Any

from .harmony import ChordSequence, note_to_pitch_class


def _section(title: str, accent: str, items: list[str]) -> dict[str, str]:
    return {
        "title": title,
        "accent": accent,
        "body": "\n".join(f"- {item}" for item in items),
    }


THEORY_LIBRARY: dict[str, dict[str, Any]] = {
    "ii_v_i_major": {
        "title": "Theory Lab: ii-V-I u duru",
        "overview": "Dur ii-V-I je osnovna laboratorija za voice leading, dominantnu napetost i ekonomično kretanje bass linije. Nije samo pitanje da li ćeš odsvirati ii-V-I, već kako ćeš raspodeliti napetost i rezoluciju kroz više nivoa aranžmana.",
        "sections": [
            _section("Harmonska funkcija", "amber", [
                "ii akord priprema dominantu i otvara pre-dominantni prostor za dalje kretanje.",
                "V7 je mesto gde se najviše menja boja: od čistog dominantnog zvuka do alterovanih i substitucijskih varijanti.",
                "I nije uvek kraj fraze; često je samo privremena tačka stabilnosti pre sledećeg ciklusa.",
            ]),
            _section("Supstitucije i varijante", "blue", [
                "Na V7 možeš primeniti b9, #9, b13 ili alt boju ako rezolucija ostane jasna.",
                "Tritonus supstitucija menja V7 u bII7 i stvara hromatski bass ulaz ka tonici.",
                "ii se često svodi na njegovu funkciju kroz guide tone kretanje, pa ga možeš reharmonizovati sus ili kvartnim voicing-om.",
            ]),
            _section("Bass Line ideje", "green", [
                "Osnovna linija root-third-chromatic-approach radi jer jasno nosi funkciju svakog takta.",
                "Druga opcija je silazna ili uzlazna diatonska linija koja na četvrtom pulsu ipak cilja sledeći root ili treću.",
                "Treća opcija je guide-tone pristup: na jakim dobama ostavi root i septimu/tercu kao stub, a između njih koristi passing tonove.",
            ]),
            _section("Standardna praksa", "gray", [
                "U standardima se ii-V-I često ne tretira izolovano, već kao deo dužeg lanca kadenci.",
                "Gitarski voicing-i često čuvaju ekonomično kretanje između terce i septime, umesto velikih skokova u svim glasovima.",
                "U improvizaciji se često misli unapred: ideje za ii se oblikuju tako da već ciljaju boju dominante i rezolucije.",
            ]),
        ],
    },
    "ii_v_i_minor": {
        "title": "Theory Lab: ii-V-i u molu",
        "overview": "Minor ii-V-i uvodi tamniji zvuk i više mogućnosti za alterisanu dominantu. Half-diminished ii akord ne traži samo tehničku tačnost, već i jasnu predstavu o tome kako dominanta vodi ka molskoj tonici.",
        "sections": [
            _section("Harmonska funkcija", "amber", [
                "iiø7 je pre-dominantni akord koji već nosi nestabilnost i traži pažljivo vođenje glasova.",
                "V7 u molu skoro uvek podnosi više alteracija nego u duru, jer je rezolucija tamnija i manje 'čista'.",
                "i može zvučati kao završetak, ali i kao prolazna tačka za novu modulaciju ili sekvencu.",
            ]),
            _section("Supstitucije i varijante", "blue", [
                "Na V7 su česte b9 i #9 boje, a alt dominantni pristup često zvuči prirodnije nego neutralan dominantni akord.",
                "Možeš koristiti diminished logiku preko dominante da naglasiš simetriju i napetost.",
                "iiø7 se može skratiti kroz manje pun voicing ako želiš da dominanta ponese veći deo drame.",
            ]),
            _section("Bass Line ideje", "green", [
                "Root-third-approach radi, ali u molu je često zanimljivije ostaviti više prostora za b9 ili leading tone oko dominante.",
                "Silazna hromatika od iiø ka V7 pa u i daje prirodno mračniji tok.",
                "Možeš graditi liniju oko arpeđa iiø i zatim zategnuti završetak takta ka dominanti preko half-step approach tona.",
            ]),
            _section("Standardna praksa", "gray", [
                "U minor standardima dominanta često nosi najveći emotivni naboj cele kadence.",
                "Gitarski voicing-i se često biraju tako da zadrže malu distancu između terce i septime kroz celu kadencu.",
                "U solaži je korisno misliti o i akordu kao cilju, a ne o svakoj promeni kao zasebnoj tonalnosti.",
            ]),
        ],
    },
    "turnaround_major": {
        "title": "Theory Lab: Major Turnaround",
        "overview": "Turnaround nije samo završetak forme nego i motor koji vraća harmoniju nazad na početak. Njegova jačina je u tome što može ostati veoma jednostavan ili se otvoriti u bogatu reharmonizaciju.",
        "sections": [
            _section("Harmonska funkcija", "amber", [
                "I-vi-ii-V postavlja jasnu hijerarhiju: stabilnost, pokret, priprema, dominanta.",
                "Svaki akord ima funkciju kretanja, pa turnaround traži dobar osećaj za smer, ne samo za boju.",
                "Čak i kada se skrati na dva takta, osećaj povratka mora ostati čujan.",
            ]),
            _section("Supstitucije i varijante", "blue", [
                "vi akord se često menja dominantom ili secondary dominant pristupom da pojača lanac napetosti.",
                "Poslednja dominanta može dobiti tritone substitution ili altered dominant tretman.",
                "Turnaround se može sekvencirati preko chromatic dominant chain pristupa bez gubitka funkcije.",
            ]),
            _section("Bass Line ideje", "green", [
                "Linearna bass linija može pratiti roots, ali i praviti silazni ili uzlazni oblik kroz voice-led povezivanje.",
                "Na turnaround-u je korisno menjati odnos chord tone i passing tone da linija ne zvuči mehanički.",
                "Četvrti puls poslednjeg takta skoro uvek treba da najavi povratak na prvi akord sledećeg kruga.",
            ]),
            _section("Standardna praksa", "gray", [
                "U swingu je turnaround često mesto gde ritam sekcija najjasnije pokazuje stilsku sigurnost.",
                "Gitaristi i pijanisti obično traže najkraći put između guide tonova umesto velikog voicing pomeranja.",
                "U standardima isti turnaround može zvučati neutralno, bluesy ili potpuno alterisano u zavisnosti od konteksta.",
            ]),
        ],
    },
    "circle_of_fifths": {
        "title": "Theory Lab: Circle of Fifths",
        "overview": "Lanac kvinti je jedan od najorganizovanijih načina da harmonija zvuči logično i neprekidno. Kada se svira dobro, svaki akord već unapred sugeriše naredni.",
        "sections": [
            _section("Harmonska funkcija", "amber", [
                "Sekvenca kvinti pravi osećaj neprekidnog funkcionalnog toka.",
                "Svaki novi dominantni ili pre-dominantni odnos pojačava smer kretanja ka sledećem centru.",
                "Ovakav tok je idealan za učenje dugih voice-leading lanaca.",
            ]),
            _section("Supstitucije i varijante", "blue", [
                "Pojedini koraci mogu se zameniti tritone dominantama ako želiš hromatski tok u bass-u.",
                "Neki akordi mogu biti skraćeni na shell voicing-e da bi se čuo kontinuitet sekvence.",
                "Sekvenca se može proširiti additional dominantnim prilazima bez gubitka osećaja kvintnog lanca.",
            ]),
            _section("Bass Line ideje", "green", [
                "Bass ne mora samo da svira root svakog akorda; može naglašavati padove po kvintama ili njihove inverzne uzlaze po kvartama.",
                "Passing tonovi između roots daju osećaj jednog dužeg luka umesto odvojenih taktova.",
                "Sekvencijalna logika pomaže da isti ritmički motiv vodi kroz više akorada bez monotonije.",
            ]),
            _section("Standardna praksa", "gray", [
                "Ovaj obrazac je centralan u standardima, turnarounds i modulacionim mostovima.",
                "Praksa je da se razmišlja o povezivanju guide tonova kroz celu sekvencu, a ne samo po jednom akordu.",
                "U aranžmanu je korisno rotirati gustinu voicing-a da ciklus ne zvuči statično.",
            ]),
        ],
    },
    "tritone_sub": {
        "title": "Theory Lab: Tritonus supstitucija",
        "overview": "Tritonus supstitucija zamenjuje dominantu akordom čiji root leži na tritonu. Funkcija rezolucije ostaje slična, ali bass i gornji glasovi dobijaju drugačiji, često elegantniji hromatski tok.",
        "sections": [
            _section("Harmonska funkcija", "amber", [
                "Supstitucija zadržava ključnu napetost dominante kroz isti triton u unutrašnjim glasovima.",
                "Osećaj rezolucije ostaje funkcionalan iako se root dominante menja.",
                "Slušalac najčešće čuje bogatiji prelaz, a ne gubitak funkcije.",
            ]),
            _section("Supstitucije i varijante", "blue", [
                "Najčešće se V7 menja bII7, ali možeš dodavati altered extensions da pojačaš moderniji zvuk.",
                "Supstituisana dominanta može se povezati sa originalnom kroz chromatic dominant chain pristup.",
                "U nekim kontekstima dovoljno je samo promeniti bass, a zadržati sličan gornji raspored tonova.",
            ]),
            _section("Bass Line ideje", "green", [
                "Hromatski silazak ka tonici je jedan od najprirodnijih razloga zašto ova supstitucija dobro radi u bass-u.",
                "Bass može ostati vrlo jasan čak i kada harmonija postane gušća, ako prvi puls stabilizuje novu funkciju.",
                "Approach tonovi postaju još efektivniji kada se nova dominanta koristi kao kratki prelaz, ne kao statična stanica.",
            ]),
            _section("Standardna praksa", "gray", [
                "Često se koristi u jazz standardima, aranžmanima i comping-u kao zamena za očekivanu dominantu.",
                "Dobar ukus je važan: ako je melodija vrlo specifična, nisu sve supstitucije jednako ubedljive.",
                "Najbolje zvuči kada rezolucija postane još glatkija, a ne samo kada je harmonija 'teoretski komplikovanija'.",
            ]),
        ],
    },
    "backdoor": {
        "title": "Theory Lab: Backdoor rezolucija",
        "overview": "Backdoor kadenca donosi mekšu, 'zaobljenu' rezoluciju od klasične V-I logike. Umesto direktne dominante, koristi se subdominantno-bluesy put ka tonici.",
        "sections": [
            _section("Harmonska funkcija", "amber", [
                "Backdoor tipično koristi ivm7-bVII7-I osećaj, sa više topline nego direktne dominantne sile.",
                "Funkcija nije manje jasna, već drugačije raspoređena u boji i gravitaciji.",
                "Ovakav pristup često povezuje jazz sa gospel i soul senzibilitetom.",
            ]),
            _section("Supstitucije i varijante", "blue", [
                "bVII7 može biti obogaćen sus ili altered bojama u zavisnosti od melodije.",
                "ivm7 se može proširiti dodatnim napetostima ako želiš bogatiji prelaz ka bVII7.",
                "Backdoor se često kombinuje sa regularnom dominantom kao kontrastom unutar duže forme.",
            ]),
            _section("Bass Line ideje", "green", [
                "Bass može naglasiti mekši silazak ili subdominantni osećaj umesto agresivne dominantne sile.",
                "Guide tone pristup često bolje radi od čistog arpeggio pristupa, jer čuva toplinu kretanja.",
                "Chromatic approach ostaje koristan, ali cilj je glatka rezolucija, ne dramatičan 'push'.",
            ]),
            _section("Standardna praksa", "gray", [
                "Backdoor se često pojavljuje kao boja u standardima i kao iznenađenje pred tonikom.",
                "Posebno je koristan kada želiš da tonika zvuči bogato, a ne strogo funkcionalno.",
                "U comping-u je važnije kako gornji glasovi klize nego koliko je akord gust.",
            ]),
        ],
    },
    "rhythm_changes_bridge": {
        "title": "Theory Lab: Rhythm Changes bridge",
        "overview": "Bridge iz Rhythm Changes je školski primer lanca dominanti. Prava vrednost mu nije samo u tome što se pamti lako, već što tera muzičara da čuje kontinuitet kroz seriju jakih funkcionalnih centara.",
        "sections": [
            _section("Harmonska funkcija", "amber", [
                "Svaki dominantni akord ima privremenu težinu tonalnog centra, ali i dalje služi kao most ka sledećem.",
                "Ovo je odličan primer kako više dominanti može zvučati logično bez potpune modulacije.",
                "Bridge stvara snažan kontrast u odnosu na A sekcije jer se harmonija pokreće bez odmora.",
            ]),
            _section("Supstitucije i varijante", "blue", [
                "Dominantni lanac može dobiti altered ili sus boje bez narušavanja osnovnog toka.",
                "Tritonus supstitucija može se primeniti selektivno da bi bass dobio hromatski luk.",
                "Ponekad se pojedine dominante skraćuju na shell formu radi jasnijeg ritmičkog comping-a.",
            ]),
            _section("Bass Line ideje", "green", [
                "Bass često koristi vrlo jasan root-led pristup kako bi slušalac čuo lanac dominanti bez zabune.",
                "Kretanje može biti sekvencijalno: isti ritmički model kroz više akorada uz male tonske promene.",
                "Approach note na kraju takta je posebno važan jer svaki sledeći akord menja centar gravitacije.",
            ]),
            _section("Standardna praksa", "gray", [
                "Ovaj bridge je standardni trening za dominantnu kontrolu i voice leading.",
                "Solo ideje se često grade iz motiva koji se sekvencijalno pomeraju kroz lanac.",
                "U pratnji je presudno zadržati groove stabilan dok harmonija ostaje veoma pokretna.",
            ]),
        ],
    },
    "jazz_blues": {
        "title": "Theory Lab: Jazz blues",
        "overview": "Jazz blues je više od 12 taktova sa dominantnim akordima. To je forma u kojoj se blues osećaj spaja sa funkcionalnim jazz jezikom, turnarounds, sekundarnim dominantama i reharmonizacijom.",
        "sections": [
            _section("Harmonska funkcija", "amber", [
                "Osnovni blues okvir ostaje prepoznatljiv, ali mnogi taktovi dobijaju dodatnu funkcionalnu preciznost.",
                "Subdominanta i povratak na toniku često zvuče sofisticiranije nego u sirovijem blues obliku.",
                "Završni taktovi skoro uvek služe kao platforma za turnaround ili novi krug forme.",
            ]),
            _section("Supstitucije i varijante", "blue", [
                "Secondary dominants, diminished passing akordi i ii-V ulazi su standardna praksa.",
                "Tritone substitution može pojačati neke dominantne tačke, ali forma mora ostati prepoznatljiva.",
                "Reharmonizacija je korisna samo ako ne izgubiš blues identitet fraze.",
            ]),
            _section("Bass Line ideje", "green", [
                "Walking bass može biti jednostavan i snažno groove-orijentisan ili vrlo voice-led i jazz obojen.",
                "Dobar pristup je menjati odnos roots, chromatic approaches i guide tones kroz formu.",
                "Nisu svi taktovi jednako gusti; neki bolje zvuče sa više prostora i stabilnijim anchoring-om.",
            ]),
            _section("Standardna praksa", "gray", [
                "U praksi se jazz blues uči kao forma na kojoj se testira skoro ceo funkcionalni jazz vokabular.",
                "Voicing-i su često kompaktniji da bi ostao osećaj blues pulsa i fraze.",
                "Najbolje interpretacije zadržavaju blues artikulaciju čak i kada je harmonija bogata.",
            ]),
        ],
    },
    "minor_blues": {
        "title": "Theory Lab: Minor blues",
        "overview": "Minor blues čuva formu bluesa, ali otvara više prostora za mračniju boju, diminished prelaze i snažnije dominantne povratke. Zato je odličan za teorijsko povezivanje modalnog osećaja i funkcionalnog razmišljanja.",
        "sections": [
            _section("Harmonska funkcija", "amber", [
                "Molski centar ostaje osnova, ali dominanta i passing akordi često donose veoma jaku funkcionalnu napetost.",
                "Diminished prolazi nisu samo dekoracija, nego sredstvo za pojačavanje smerova u formi.",
                "Minor blues lako klizi između blues i jazz jezika, pa traži disciplinu u izboru boje.",
            ]),
            _section("Supstitucije i varijante", "blue", [
                "Diminished passing akordi i alterisane dominante su prirodan deo jezika minor bluesa.",
                "ii-V ulazi ka molskoj tonici ili privremenim centrima mogu se rasporediti veoma ukusno.",
                "Neke mere podnose reharmonizaciju bolje od drugih; forma mora ostati čujna.",
            ]),
            _section("Bass Line ideje", "green", [
                "Bass može kombinovati roots, chromatic motion i arpeggio fragmente da zadrži težinu i tamu forme.",
                "Diminished prelazi daju prirodnu priliku za simetrične ili poluhromatske linije.",
                "Kraj fraze treba jasno usmeriti ka sledećem centru, inače forma zvuči ravno.",
            ]),
            _section("Standardna praksa", "gray", [
                "Minor blues je standardan teren za istraživanje tamnijih voicing-a i dominantnih boja.",
                "U pratnji je korisno balansirati otvoreniji zvuk sa dovoljno jasnom funkcionalnom signalizacijom.",
                "U solaži često bolje rade kratki motivi i razvoj kroz formu nego previše 'skala po akordu'.",
            ]),
        ],
    },
    "doo_wop": {
        "title": "Theory Lab: 50s / Doo-wop",
        "overview": "I-vi-IV-V deluje jednostavno, ali upravo zato traži dobar osećaj za frazu, stabilnost i emotivni tok. U jazz-friendly okruženju možeš ga obogatiti bez gubitka prepoznatljivosti.",
        "sections": [
            _section("Harmonska funkcija", "amber", [
                "I daje početnu stabilnost, vi otvara emotivni pad ili nostalgiju, IV širi prostor, a V priprema povratak.",
                "Ovaj tok je snažan jer ravnoteža između poznatosti i kretanja ostaje vrlo jasna.",
                "Jednostavna forma ne znači siromašnu interpretaciju; mnogo zavisi od raspodele boje i ritma.",
            ]),
            _section("Supstitucije i varijante", "blue", [
                "Maj7, m7 i dominantne varijante mogu dati urbaniji ili jazzier karakter bez gubitka prepoznatljivog obrasca.",
                "Secondary dominant pristup ka vi ili V može pojačati funkcionalni tok.",
                "Slash-chord i gospel voicing pristupi mogu obogatiti sredinu progresije bez narušavanja osnovne pesme.",
            ]),
            _section("Bass Line ideje", "green", [
                "Osnovna bass linija može ostati vrlo pevačka: root, chord tone, passing tone, approach.",
                "Silazni dijatonski luk između I i vi često zvuči prirodno i emotivno.",
                "Ako želiš više pokreta, četvrti puls svakog takta može najavljivati sledeći root bez previše hromatike.",
            ]),
            _section("Standardna praksa", "gray", [
                "U pop/soul kontekstu groove i fraza često znače više od kompleksne reharmonizacije.",
                "U jazz obradi treba dodavati boju tako da progresija i dalje ostane odmah prepoznatljiva.",
                "Najbolje verzije ne pokušavaju da 'sakriju' jednostavnost, nego da je profine.",
            ]),
        ],
    },
    "pachelbel": {
        "title": "Theory Lab: Pachelbel tip sekvence",
        "overview": "Kanonska sekvenca ovog tipa funkcioniše jer kombinuje stabilne tačke sa dugim linearnim tokom. U praksi je korisna za učenje kako se jednostavan harmonic loop pretvara u aranžmanski bogat materijal.",
        "sections": [
            _section("Harmonska funkcija", "amber", [
                "Sekvenca deluje kao duga fraza, ne kao niz izolovanih akorada.",
                "Promene često zvuče prirodno jer kombinacija tonike, dominante i relativnih funkcija stvara jasan luk.",
                "Ovakve sekvence su odlične za razumevanje 'horizontalne' harmonije.",
            ]),
            _section("Supstitucije i varijante", "blue", [
                "Možeš zameniti pojedine dominante ili uvesti sus/maj7/m7 nijanse bez rušenja prepoznatljive sekvence.",
                "Sekvenca dobro podnosi dodatne unutrašnje linije i slash akorde.",
                "Kada menjaš boju, važno je sačuvati opšti smer kretanja, ne samo naziv akorda.",
            ]),
            _section("Bass Line ideje", "green", [
                "Bass može slediti roots, ali jednako dobro radi i linearni pevački pristup koji prati dugi oblik fraze.",
                "Dijatonski passing tonovi su često prirodniji od agresivne hromatike.",
                "U ovoj sekvenci je važno misliti na luk od više taktova, ne samo na mikro-rezolucije po taktu.",
            ]),
            _section("Standardna praksa", "gray", [
                "Primenjuje se u pop, filmskoj i crossover muzici, ali se lako može čitati i kroz jazz-friendly voicing pristup.",
                "Aranžmanska vrednost je velika jer forma prihvata slojeve, pedal tonove i unutrašnje melodijske linije.",
                "U comping-u je često korisnije graditi kontinuirani tok nego naglašavati svaki akord podjednako.",
            ]),
        ],
    },
    "andalusian": {
        "title": "Theory Lab: Andalusian kadenca",
        "overview": "Andalusian tip kadence koristi silazni tok koji odmah stvara snažnu boju. Iako se često vezuje za jedan idiom, u praksi je korisna kao model za kontrolu dramskog luka i silazne bass linije.",
        "sections": [
            _section("Harmonska funkcija", "amber", [
                "Silazni tok nosi više drame nego statična tonika-dominanta logika.",
                "Akordi se slušaju kao jedan kontinuirani pad, ne samo kao pojedinačni događaji.",
                "Upravo ta linearna priroda daje kadencom snažan identitet.",
            ]),
            _section("Supstitucije i varijante", "blue", [
                "Moguće su jazzier boje kroz m7, maj7 ili dominantne varijante, ali silazni karakter treba da ostane netaknut.",
                "Možeš dodati sus ili altered boju na poslednjoj dominanti ako želiš jaču rezoluciju.",
                "Neke verzije bolje rade sa pedal bas pristupom, a neke sa jasnim silaznim roots.",
            ]),
            _section("Bass Line ideje", "green", [
                "Ovde je bass gotovo kompozicioni element: silazak mora zvučati prirodno i autoritativno.",
                "Passing tonovi treba da pojačaju tok, a ne da ga zamagle.",
                "U sporijem tempu možeš ostaviti više prostora između ključnih tonova da silazni luk bude ubedljiviji.",
            ]),
            _section("Standardna praksa", "gray", [
                "Forma je korisna i van svog izvornog stila jer razvija osećaj za harmonski pad i napetost.",
                "Voicing-i i bass najčešće rade najbolje kada jasno pokažu silazni pravac kroz celu sekvencu.",
                "U teorijskom radu dobro služi kao kontrast klasičnim ii-V-I obrascima.",
            ]),
        ],
    },
    "secondary_dominant": {
        "title": "Theory Lab: Secondary dominants",
        "overview": "Secondary dominant pristup koristi privremene dominante da kratko osvetli akord koji dolazi, bez pune modulacije. To je jedan od najpraktičnijih načina da progresija zvuči pokretnije i funkcionalno bogatije.",
        "sections": [
            _section("Harmonska funkcija", "amber", [
                "Privremena dominanta daje lokalni centar gravitacije sledećem akordu.",
                "Slušalac čuje pojačan smer, ali forma ne mora da napusti osnovni tonalni okvir.",
                "Ovo je jedan od najčešćih načina da se jednostavna progresija učini funkcionalno aktivnijom.",
            ]),
            _section("Supstitucije i varijante", "blue", [
                "Applied dominant može biti čist, altered ili zamenjen tritone substitution pristupom.",
                "Nije svaki akord dobar cilj za applied dominant; funkcija mora ostati muzički ubedljiva.",
                "U voicing-u se često čuvaju treća i sedma kao glavni nosioci funkcije.",
            ]),
            _section("Bass Line ideje", "green", [
                "Bass linija treba da pokaže trenutak pojačane napetosti, a zatim jasnu rezoluciju u ciljni akord.",
                "Approach ton na kraju takta postaje posebno važan jer applied dominant traži preciznu najavu sledeće funkcije.",
                "Dobar bass ovde često zvuči kao kratka mini-kadenca unutar šire forme.",
            ]),
            _section("Standardna praksa", "gray", [
                "Secondary dominants su standardan jezik u jazzu, standardima i aranžmanima.",
                "Najbolje rade kada pojačaju tok, a ne kada svaku progresiju pretvore u gustu dominantsku mrežu.",
                "U praksi se često koriste selektivno: na najvažnijim tačkama forme, ne svuda jednako.",
            ]),
        ],
    },
    "modal_interchange": {
        "title": "Theory Lab: Modal interchange",
        "overview": "Modal interchange ili borrowed chord pristup unosi akorde iz paralelnog moda kako bi se promenila boja bez potpunog menjanja centra. To je više pitanje boje i karaktera nego čiste funkcionalne nužnosti.",
        "sections": [
            _section("Harmonska funkcija", "amber", [
                "Borrowed chord ne mora imati jaku funkcionalnu logiku kao dominantni akord; često mu je glavna uloga promena boje.",
                "Paralelni dur/mol odnos daje najčešće izvore za ovakve akorde.",
                "Kada se koristi pažljivo, modal interchange proširuje frazu bez gubitka osećaja centra.",
            ]),
            _section("Supstitucije i varijante", "blue", [
                "bVI, bVII, ivm i srodne boje su česti borrowed kandidati.",
                "Takvi akordi se mogu dalje obogatiti maj7, m7 ili dominantnim nijansama, ali osnovna boja mora ostati čitljiva.",
                "U reharmonizaciji je važno da borrowed chord ne zvuči kao slučajna greška, nego kao nameran koloristički izbor.",
            ]),
            _section("Bass Line ideje", "green", [
                "Bass ovde često radi bolje kada naglasi karakter novog kolorita nego kada insistira na strogoj kadencijalnoj logici.",
                "Dijatonski i poluhromatski lukovi mogu pomoći da borrowed chord zvuči organski uklopljen.",
                "Ponekad je manje passing tonova bolji izbor, da bi promena boje ostala jasna.",
            ]),
            _section("Standardna praksa", "gray", [
                "U praksi se modal interchange koristi da otvori emocionalni kontrast ili neočekivani obrt.",
                "Voicing-i često nose veći deo efekta nego sama promena root-a.",
                "Najbolje radi kada nova boja ima dramaturšku svrhu, a ne samo teorijsku zanimljivost.",
            ]),
        ],
    },
    "dominant_chain": {
        "title": "Theory Lab: Dominantni lanac",
        "overview": "Kada se više dominantnih akorada niže jedan za drugim, progresija dobija snažan osećaj neprekidnog guranja napred. To je idealan teren za voice leading, sekvencijalno mišljenje i čistu ritmičku disciplinu.",
        "sections": [
            _section("Harmonska funkcija", "amber", [
                "Svaka dominanta privremeno se ponaša kao centar napetosti, ali istovremeno gura dalje.",
                "Takav lanac zvuči logično kada su unutrašnji glasovi i bass povezani jasno i ekonomično.",
                "Slušalac ne mora da doživi svaku promenu kao modulaciju; često je važniji osećaj neprekidnog toka.",
            ]),
            _section("Supstitucije i varijante", "blue", [
                "Dominante mogu dobiti alt, sus ili tritone substitution tretman bez rušenja lanca.",
                "Neke dominante mogu ostati shell-only ako želiš da tok zvuči čistije i ritmički stabilnije.",
                "Sekvencijalni pristup znači da mali motiv ili boja može putovati kroz ceo lanac.",
            ]),
            _section("Bass Line ideje", "green", [
                "Bass ovde mora biti izrazito jasan: root-led pristup često pobeđuje previše dekorisan pristup.",
                "Approach note na kraju svakog takta drži lanac zategnutim i preglednim.",
                "Sekvencijalne figure u bass-u mogu pomoći da više dominanti zvuči kao jedna velika ideja.",
            ]),
            _section("Standardna praksa", "gray", [
                "Dominantni lanci su standardni trening za comping, bass i improvizaciju.",
                "Najčešća greška je da harmonija bude bogata, a groove neubedljiv; lanac traži ritmičku stabilnost.",
                "Udobnost sa ovim tipom toka direktno poboljšava čitanje bridge-a, turnarounds i reharmonizovanih standarda.",
            ]),
        ],
    },
}


def build_theory_profile(
    pattern_key: str,
    pattern_label: str = "",
    cadence_items: list[str] | None = None,
    sequence: ChordSequence | None = None,
) -> dict[str, Any]:
    cadence_items = cadence_items or []
    if pattern_key and pattern_key in THEORY_LIBRARY:
        profile = THEORY_LIBRARY[pattern_key]
        return {
            "title": profile["title"],
            "overview": profile["overview"],
            "sections": profile["sections"],
            "resource_hint": "Za dalje istraživanje korisno je uporediti ove ideje sa modernim jazz guitar lekcijama o voice leading-u, dominantnim bojama, supstitucijama i walking bass pristupu, uključujući edukativne kanale poput Jens Larsen teme na YouTube-u.",
        }

    raw_joined = " ".join(cadence_items)
    joined = raw_joined.lower()
    inferred_key = ""
    if "ii-v-i ka" in raw_joined:
        inferred_key = "ii_v_i_minor"
    elif "ii-V-I" in raw_joined or "ii-v-i" in pattern_label.lower() or "ii-v-i" in joined:
        inferred_key = "ii_v_i_major"
    elif "turnaround" in joined or "turnaround" in pattern_label.lower():
        inferred_key = "turnaround_major"
    elif "backdoor" in joined or "backdoor" in pattern_label.lower():
        inferred_key = "backdoor"
    elif "blues" in pattern_label.lower():
        inferred_key = "minor_blues" if "minor" in pattern_label.lower() else "jazz_blues"
    elif "bridge" in pattern_label.lower():
        inferred_key = "rhythm_changes_bridge"
    elif sequence and _has_dominant_chain(sequence):
        inferred_key = "dominant_chain"
    elif sequence and _has_secondary_dominant(sequence):
        inferred_key = "secondary_dominant"
    elif sequence and _has_modal_interchange(sequence):
        inferred_key = "modal_interchange"

    if inferred_key and inferred_key in THEORY_LIBRARY:
        return build_theory_profile(inferred_key, pattern_label, cadence_items)

    return {
        "title": "Theory Lab: Funkcionalna mapa progresije",
        "overview": "Za ovu progresiju još nemamo specifičan preset profil, ali i dalje možeš čitati odnos između funkcije, bass kretanja, mogućih supstitucija i standardne prakse izvođenja.",
        "sections": [
            _section("Harmonska funkcija", "amber", [
                "Prvo identifikuj koje tačke rade kao stabilnost, koje kao priprema, a koje kao napetost.",
                "Zatim slušaj da li progresija više deluje kao kadenca, sekvenca ili loop.",
                "Tek posle toga biraj reharmonizaciju ili bogatije voicing-e.",
            ]),
            _section("Supstitucije", "blue", [
                "Supstitucije imaju smisla samo ako čuvaju pravac linije i rezoluciju ključnih glasova.",
                "Najčešće menjamo dominantu, pre-dominantu ili unutrašnje boje, ne celu logiku progresije.",
                "Dobar ukus je važniji od broja teorijskih opcija.",
            ]),
            _section("Bass Line opcije", "green", [
                "Osnovni root-third-approach model je dobar kostur, ali nije jedina opcija.",
                "Dijatonski passing tonovi, guide-tone orijentacija i ritmičke varijacije mogu dati prirodniji tok.",
                "Svaka linija treba da najavi sledeći akord, ne samo da popuni takt.",
            ]),
            _section("Standardna praksa", "gray", [
                "Voicing-i i bass treba da zvuče kao deo iste harmonske priče.",
                "Najbolja teorijska rešenja obično su ona koja ostanu muzički čitljiva pri realnom izvođenju.",
                "Posmatraj progresiju kao platformu za više interpretacija, ne kao jedini tačan odgovor.",
            ]),
        ],
        "resource_hint": "Za dalje proučavanje fokusiraj teme kao što su ii-V-I voice leading, dominant substitutions, jazz blues reharmonization i walking bass design u savremenim jazz edukativnim izvorima.",
    }


def build_bass_theory_sections(
    sequence: ChordSequence,
    bass_bar_overview: list[dict[str, str]],
    cadence_items: list[str] | None = None,
    pattern_key: str = "",
) -> list[dict[str, str]]:
    cadence_items = cadence_items or []
    if not bass_bar_overview:
        return []

    total_bars = len(bass_bar_overview)
    root_count = sum(1 for bar in bass_bar_overview if bar.get("beat_one_role") == "root")
    approach_count = sum(1 for bar in bass_bar_overview if bar.get("beat_four_role") == "approach")
    chromatic_count = sum(1 for bar in bass_bar_overview if "chromatic motion" in bar.get("bar_comment", ""))
    guide_count = sum(1 for bar in bass_bar_overview if "guide tone emphasis" in bar.get("bar_comment", ""))
    label_join = " - ".join(chord.label for chord in sequence.chords[:4])

    current_strategy = _section(
        "Aktuelna bass logika",
        "amber",
        [
            f"Trenutna linija koristi jasan root anchor na prvom pulsu u {root_count} od {total_bars} taktova, pa funkcija akorda ostaje odmah čujna.",
            f"Na završetku takta koristi approach ton u {approach_count} taktova, što pomaže da prelazi ka sledećem akordu budu pregledni i muzički usmereni.",
            f"Srednji beatovi trenutno naglašavaju {'guide tone kretanje' if guide_count else 'osnovne chord-tone oslonce'}, pa linija zvuči više kao stabilan walking kostur nego kao melodijski rizična varijanta.",
        ],
    )

    alternative_one = _section(
        "Alternativa 1: Guide-tone skeleton",
        "blue",
        [
            "Umesto da drugi i treći puls uglavnom potvrđuju chord tone kostur, linija može više da cilja terce i septime kao glavne vodiče između akorada.",
            f"Na primeru {label_join}, to bi značilo da se sredina svakog takta više sluša kao voice leading most između funkcija, a manje kao neutralna potpora korenu.",
            "Ovaj pristup je posebno koristan kada želiš da linija zvuči 'pametnije' i povezanije sa comping-om, čak i bez više hromatike.",
        ],
    )

    alternative_two_items = [
        f"Trenutna verzija ima {chromatic_count} taktova sa izrazitijom hromatskom bojom; alternativa je duži dijatonski luk kroz po dva ili četiri takta, bez obaveznog chromatic approach-a na svakom kraju mere.",
        "Takva linija bolje radi kada želiš pevačkiji, mekši walking osećaj i manje 'demonstrativnu' funkcionalnost po taktu.",
        "Praktično: ostavi root na prvom pulsu, a zatim gradi uzlazni ili silazni oblik koji tek pred kraj fraze jasno vrati fokus na sledeću funkciju.",
    ]
    if _has_dominant_chain(sequence) or pattern_key in {"rhythm_changes_bridge", "turnaround_major"}:
        alternative_two_items[1] = "Kod dominantnih lanaca ili turnarounds, ova alternativa može koristiti sekvencijalni ritmički motiv kroz više taktova umesto istog obrasca u svakoj meri."
    elif pattern_key in {"ii_v_i_major", "ii_v_i_minor", "tritone_sub", "backdoor"} or any("ii-V" in item for item in cadence_items):
        alternative_two_items[1] = "Kod kadencijalnih ćelija, ova alternativa može spojiti dva takta u jedan logički luk: prvi takt priprema, drugi takt pojačava rezoluciju."
    alternative_two = _section(
        "Alternativa 2: Dijatonski ili sekvencijalni luk",
        "green",
        alternative_two_items,
    )

    return [current_strategy, alternative_one, alternative_two]


def _has_dominant_chain(sequence: ChordSequence) -> bool:
    chain_links = 0
    for current, following in zip(sequence.chords, sequence.chords[1:]):
        if current.quality == "dom" and (note_to_pitch_class(following.root) - note_to_pitch_class(current.root)) % 12 == 5:
            chain_links += 1
    return chain_links >= 2


def _has_secondary_dominant(sequence: ChordSequence) -> bool:
    if len(sequence.chords) < 2:
        return False
    final_root = sequence.chords[-1].root
    for current, following in zip(sequence.chords, sequence.chords[1:]):
        if current.quality == "dom" and following.root != final_root:
            if (note_to_pitch_class(following.root) - note_to_pitch_class(current.root)) % 12 == 5:
                return True
    return False


def _has_modal_interchange(sequence: ChordSequence) -> bool:
    if len(sequence.chords) < 3:
        return False
    qualities = {chord.quality for chord in sequence.chords}
    has_mixed_color = "maj" in qualities and "min" in qualities
    flat_motion = any(chord.root in {"Bb", "Eb", "Ab", "Db", "Gb"} for chord in sequence.chords)
    return has_mixed_color and flat_motion