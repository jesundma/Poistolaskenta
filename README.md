# Poistolaskenta
Tietokannat ja web-ohjelmointi julkinen repo kurssisovellusta varten. Repossa on kolme .sql- tiedostoa, joista kaksi liittyy sovelluksen käynnistykseen ja kolmas on tarkoitettu sovelluksen koekäyttöön. Jos tiedosto ajetaan, luo se tietokantaan esimerkkiprojekteja.

TEKNINEN KUVAUS:

Sovellukseen lisätään projektiobjekteja, jotka sisältävät tietoja projektin investoinneista ja investointien ajankohdasta. Projekteille tallennetaan perustiedot, kuten projektin nimi, yksilöllinen projektitunniste ja poistotapa, joka voi olla joko tasapoisto tai menojäännöspoisto. Kaikki projektien perustiedot talletetaan Projects-tauluun, jossa projektin numerotunnus toimii yksilöllisenä avaimena.

Investointien hallinta perustuu siihen, että käyttäjä syöttää valituille vuosille investointiarvot sovelluksen syöttöikkunan kautta. Nämä tiedot tallennetaan projektikohtaisesti Investments-tauluun. Samalle vuodelle on mahdollista syöttää uusi tieto, joka korvaa vanhan tiedon. Investoinnit syötetään tällä hetkellä vuosi–investointi-parina, eli jokainen tieto lisätään erikseen.

Sovelluksessa on käyttäjähallinta, jossa määritellään käyttäjät sekä heidän hash-muodossa tallennetut salasanansa. Tiedot sijaitsevat Users-taulussa. Kun sovellus käynnistetään ensimmäistä kertaa, käyttäjä ohjataan aina uuden käyttäjän luomiseen.

Projektien luomis- ja muutostiedot tallennetaan käyttäjäkohtaisesti. Inserted-tauluun tallentuu tieto projektin luojasta ja Modified-tauluun tallentuvat tiedot käyttäjistä, jotka ovat muokanneet projektia. Projektien käsittelyoikeuksia hallitaan ProjectPermissions-taulun avulla. Projektinhallinta näyttää sekä projektin luojan että projektiin tehdyt muutokset. Projektin poistaminen tai perustietojen muuttaminen on mahdollista vain projektin luojalle tai sellaiselle käyttäjälle, jolle luoja on erikseen antanut muokkausoikeudet. Käyttäjäoikeudet määräytyvät siis projektin luojan kautta. Ainoastaan projektin luoja pystyy poistamaan projektin. Projektin muokkaustapahtumat kirjautuvat Modified-tauluun, ja muokkaaminen edellyttää projektin luojan myöntämiä oikeuksia. Poikkeuksena tähän ovat kassavirtojen muutokset, sillä niitä voivat muokata kaikki käyttäjät kaikissa projekteissa.

Sovellus tarjoaa lisäksi käyttäjäkohtaisen tilaston, joka näyttää käyttäjän luomat projektit ja niiden luomisajankohdan. Tilastosta on mahdollista siirtyä suoraan kyseiseen projektiin.


SOVELLUKSEN KÄYNNISTÄMINEN:

- asenna flask- kirjasto komennolla: pip install flask
- sovellus käynnistyy komennolla: flask run
- sovelluksen verkko-osoite on http://127.0.0.1:5000/

Sovelluksen käynnistämisen jälkeen voidaan tietokantaan halutessa lisätä esimerkkiprojekteja. Jos haluat lisätä esimerkkiprojekteja, tee sovelluksen hakemistossa pääteikkunassa seuraavat komennot: 
- sqlite3 database.db
- .read dummy_projects.sql


KÄYTTÖOHJEET:

Jos sovellusta ei ole asennettu aiemmin tai sovellukseen ei ole määritelty käyttäjiä, sovellus luo tietokannan ja ohjaa luomaan ensimmäisen käyttäjän. Luo sivulla käyttäjätunnus ja anna käyttäjälle salasana. Onnistunut käyttäjän luonti näkyy viestinä. Jos et halua luoda enempää käyttäjiä, niin siirry pääsivulle linkistä. Ensimmäinen luotu tunnus on automaattisesti kirjautunut sisään ja siirryt sovelluksen pääsivulle.

 Jos tietokannasta löytyy jo käyttäjiä, ohjaa sovellus kirjautumissivulle. Anna kirjautumistiedot ja siirryt sovelluksen pääsivulle.

 Lisää projekti lisää uuden projektin, jolle käyttäjä antaa nimen ja perustiedot. Projektinumero on järjestelmän automaattisesti luoma yksilöllinen tunniste.

 Hae projektilistaus näyttää tallennetut projektit ja ilmoittaa Ei projekteja, jos tallennettuja projekteja ei ole. Listauksen yläosassa on suodattimia, joilla projekteja voi suodattaa eri projektitietojen perusteella. Projektin toiminnoista Projektin kassavirrat- toimintoa voi käyttää kaikki käyttäjät. Projektihallinta näyttää projektin tarkempia tietoja, kuten projektin luojan ja siihen tehdyt muutokset.
 
 Projektihallinta- sivulla olevia toimintoja Projektin tietojen muuttaminen, projektin oikeuksien muuttaminen tai peruuttamattoman projektin poistaminen ovat sallittuja vain projektin luojalle tai käyttäjille, joille projektin luoja on antanut oikeudet. Projektin tietojen muuttaminen koskee projektin perustietoja. Projektin oikeuksien muutoksella voi antaa toiselle käyttäjälle oikeuden muuttaa projektin perustietoja. Projektin poistaminen on mahdollista vain projektin luojalle.

Siirry käyttäjähallintaan siirtää käyttäjän uusien käyttäjien luomiseen. Kaikki käyttäjät voivat luoda uusia käyttäjiä.

Siirry käyttäjätilastoon näyttää kaikki projektit, joissa käyttäjä on luojana sekä näiden projektin luomisajankohdan.



Tunnettuja virheitä ja ongelmia:
- Projektisuodatin ei säily, jos käyttäjä yrittää muuttaa projektin oikeuksia ja saa sitä koskevan virheilmoituksen
- Projektin muokkausoikeudet voi antaa vain omistaja, mikä on oikein, mutta projektin oikeuksien poistaminen ei toimi
- Kaikilla sivuilla muotoilu ei tule .css muotoilusta
- validoinnit on siirretty palvelinpuolelle, mutta kaikkia ei ole tarkistettu ja osa validoinneista puuttuu kokonaan asiakas- ja palvelinpuolelta tai sitten palvelinpuolelta.

Puuttuvia ominaisuuksia:
- poistettu väliversiosta

Suuret tietomäärät

Seed.py on jätetty sovellukseen reitiksi /seed ja se käynnistyy ilman oikeuksien tarkastamista reitille siirryttäessä. Tämä ei tuotantovalmiissa sovelluksessa tietenkään olisi käytössä oleva reitti. Alunperin lisäykset oli tehty erittäin jakamalla lisättävät rivit määriteltyihin eräkokoihin, esimerkiksi 5 000 tai 10 000 riviä. Kurssiaineistossa olleessa seed.py ei tätä tekniikkaa oltu käytetty ja tietokannan täyttäminen muutettiin esimerkin mukaiseksi. Yllättävä havainto vain muutaman ajon perusteella oli, että eräajo ei näyttänyt olevan nopeampi tapa, itse asiassa se oli aavistuksen hitaampi tietokannan täyttämistapa. Tietokannan ja sovelluksen ollessa samalla koneella sekä vain muutaman kokeilun perusteella ei kannata tehdä pitkälle vietyjä oletuksia. Reittien pyynnöt kirjattiin app.log tiedostoon, joka on jätetty sovellukseen lokiksi. App.py tiedostossa on määritelty @app.before_request ja @app.after_request funktiot, jotka mittaavat ja lokittavat pyyntöjä ja niiden kestoa.

1000 käyttäjää, 100 000 projektia ja 5 kassavirtaa kussakin (500 000 kassavirtaa) sekä jokaisella projektilla 2 määrettä (100 000 ja 100 000):

2025-10-19 11:47:20,447 [INFO] 127.0.0.1 - - [19/Oct/2025 11:47:20] "GET /seed HTTP/1.1" 200 -
2025-10-19 12:06:04,224 [INFO] Clearing Users, Projects, Investments, and Project_definitions
2025-10-19 12:07:22,305 [INFO] Loaded 4 Projektityyppi and 4 Poistomenetelmä options
2025-10-19 12:08:53,628 [INFO] Added default login user 'admin' with password 'admin123'
2025-10-19 12:08:53,636 [INFO] Inserted 1001 users in 91.33 seconds
2025-10-19 12:08:55,041 [INFO] Inserted 1000000 projects in 1.4 seconds
2025-10-19 12:09:02,936 [INFO] Inserted 2000000 project definitions in 7.9 seconds
2025-10-19 12:09:19,496 [INFO] Inserted 5000000 cashflows in 16.56 seconds
2025-10-19 12:09:19,496 [INFO] ---- Seeding Summary ----
2025-10-19 12:09:19,496 [INFO] Users inserted in 91.33s
2025-10-19 12:09:19,497 [INFO] Projects inserted in 1.4s
2025-10-19 12:09:19,498 [INFO] Definitions inserted in 7.9s
2025-10-19 12:09:19,498 [INFO] Cashflows inserted in 16.56s
2025-10-19 12:09:19,499 [INFO] Total seeding time: 117.19s
2025-10-19 12:09:19,499 [INFO] --------------------------
2025-10-19 12:09:19,501 [INFO] Database seeding completed successfully
2025-10-19 12:09:19,517 [INFO] Database seeded successfully.

Projektilistauksen haku (toiminta, jossa haetaan projektit sivutettuina viisi proktia sivulla), haku projektin nimeä käyttäen (nimessä: 34), haku proktityypillä Muutostyö ja haku projektin poistomenetelmällä tasapoisto 10 vuotta:

2025-10-19 15:32:19,591 [INFO] GET /list_projects took 26.47s
2025-10-19 15:32:19,593 [INFO] 127.0.0.1 - - [19/Oct/2025 15:32:19] "GET /list_projects HTTP/1.1" 200 -
2025-10-19 15:34:18,891 [INFO] GET /list_projects took 18.74s
2025-10-19 15:34:18,891 [INFO] 127.0.0.1 - - [19/Oct/2025 15:34:18] "GET /list_projects?project_name=34&project_type=&depreciation_method= HTTP/1.1" 200 -
2025-10-19 15:36:18,540 [INFO] GET /list_projects took 26.59s
2025-10-19 15:36:18,541 [INFO] 127.0.0.1 - - [19/Oct/2025 15:36:18] "GET /list_projects?project_name=&project_type=Muutostyö&depreciation_method= HTTP/1.1" 200 -
2025-10-19 15:40:33,670 [INFO] GET /list_projects took 4.46s
2025-10-19 15:40:33,670 [INFO] 127.0.0.1 - - [19/Oct/2025 15:40:33] "GET /list_projects?project_name=&project_type=&depreciation_method=Tasapoisto+10+vuotta HTTP/1.1" 200 -

Projektilistan latauduttua siirtymä toiselle sivulle sivutetussa projektilistassa:

2025-10-19 15:44:13,863 [INFO] GET /list_projects/39 took 7.57s
2025-10-19 15:44:13,863 [INFO] 127.0.0.1 - - [19/Oct/2025 15:44:13] "GET /list_projects/39?project_name=&project_type=&depreciation_method= HTTP/1.1" 200 -

Taulussa Users id on pääavain (PRIMARY KEY) ja siten automaattisesti indeksoitu, kuten myös username yksilöllinen- rajoittimen (UNIQUE) takia. 

Projects- taulun pääavain (PRIMARY KEY) on id ja siten id- perustuvien hakujen osalta indeksoitu. Projektin nimeen (project_name) perustuville hauille, esimerkiksi suodattimet luotiin indeksi (CREATE INDEX idx_projects_name ON Projects(project_name);)

ProjectTypes pääavain (PRIMARY KEY) on project_id. Kenttä on nimetty muista tauluista poikkeavasti ja nimen muutos olisi hyvä tehdä (id). Esimerkiksi suodattamissa käytetään hakutekijänä taulukon arvoja, joten niitä varten luotiin oma indeksi (CREATE INDEX idx_projecttypes_type ON ProjectTypes(project_type);)

Taulun Investments yhdistelmäavain (PRIMARY KEY) on kenttien project_id ja investment_year yhdistelmä, joka tarkoittaa projektissa samalle vuodelle ei voi projektissa olla useampaa kassavirtaa. Sovelluksessa ei käytetä aikaväli tai vuosiväli kyselyitä, mutta mahdollista jatkokehittelyä varten tauluun lisättiin tätä varten indeksi CREATE INDEX idx_investments_year ON Investments(investment_year);

Taulu Project_definitions sisältää projektin määritteet. Määritteet on määritelty taulussa Classes. Tauluun lisättiin indeksit CREATE INDEX idx_projdef_project ON Project_definitions(project_id); ja CREATE INDEX idx_projdef_title ON Project_definitions(title);, jonka avulla suodattimiin Projektityyppi ja Poistomenetelmä perustuvat kyselyt toimivat nopeammin.

Tietokannan tietojen syöttäminen ei olennaisesti muutu, vaikka tietokantaan on rakennettu indeksit.

2025-10-19 17:47:59,867 [INFO] Users inserted in 90.37s
2025-10-19 17:47:59,867 [INFO] Projects inserted in 1.51s
2025-10-19 17:47:59,867 [INFO] Definitions inserted in 6.99s
2025-10-19 17:47:59,867 [INFO] Cashflows inserted in 17.26s
2025-10-19 17:47:59,870 [INFO] Total seeding time: 116.12s

Indeksi lisättynä koko projektilistan noutaminen kestää 19 - 20 sekuntia verrattuna ennen indeksiä noin 26 sekunnin kestoon. Itse en kyllä ymmärrä, miten indeksin lisäys vaikuttaisi tähän.

2025-10-19 20:35:54,782 [INFO] GET /list_projects took 19.22s
2025-10-19 20:35:54,783 [INFO] 127.0.0.1 - - [19/Oct/2025 20:35:54] "GET /list_projects HTTP/1.1" 200 -

Projektin nimihaulla hakuaika laski 9 - 10 sekunnin välille, joka oli melkein puolittuminen ilman indeksointia.

2025-10-19 20:40:04,054 [INFO] GET /list_projects took 9.24s
2025-10-19 20:40:04,054 [INFO] 127.0.0.1 - - [19/Oct/2025 20:40:04] "GET /list_projects?project_name=34&project_type=&depreciation_method= HTTP/1.1" 200 -

Hakemalla projektityypillä muutos ei näyttäisi olevan kuin muutaman sekuntin luokkaa, hakuaika muuttui 26 - 27 sekunnista 24 - 25 sekunttiin. Poistometodilla hakuaika oli hieman nopeampi 22 - 23 sekunnin välillä suhteessa projektityypillä hakemiseen. Saattaa olla, että olen lokista kopioinut väärän rivin, mutta ilman indeksointia tähän kului noin 4,8 sekuntia. Jos tämä on oikea tulos, niin en ymmärrä, miksi ero olisi tämä.

2025-10-19 20:42:38,194 [INFO] GET /list_projects took 24.53s
2025-10-19 20:42:38,194 [INFO] 127.0.0.1 - - [19/Oct/2025 20:42:38] "GET /list_projects?project_name=&project_type=Muutostyö&depreciation_method= HTTP/1.1" 200 -
2025-10-19 20:45:11,160 [INFO] GET /list_projects took 22.71s
2025-10-19 20:45:11,160 [INFO] 127.0.0.1 - - [19/Oct/2025 20:45:11] "GET /list_projects?project_name=&project_type=&depreciation_method=Tasapoisto+10+vuotta HTTP/1.1" 200 -

Kokonaisuutena indeksointi kyllä paransi hakuaikoja vaikuttamaan kirjoitusaikoihin. Uskoisin eron tulevan paremmin esille, jos sovelluksessa olisi enemmän JOIN- tyyppisiä kyselyitä. Tällä hetkellä kyselyt ovat suurimmaksi osaksi helppoja yhteen tauluun kohdistuvia suodatuskyselyitä.

Pylint

Repossa on viimeisin pylint- raportti, mutta sitä ei ole ehditty käsitellä. Raportissa on normaaleja, ohitettavia huomioita ja oikeita koodivirheitä tai -puutteita.