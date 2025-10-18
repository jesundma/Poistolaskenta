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
- Jos rekisteröinti (register.html) sivulta siirtyy Pääsivulle (main_layout) käyttäen linkkiä, sivulle pääsee vaikka tietokannassa ei olisi ainuttakaan käyttäjää. Pääsivun linkit ohjaavat takaisin rekisteröintisivulle, mutta rekisteröinnistä ei pitäisi päästä pääsivulle ilman, että käyttäjiä olisi vähintään yksi.
- Yritys projektihallinnan oikeuksien antamiseen ilman käyttäjän oikeuksia siihenrikkoo sivun, ongelma sivun templatessa.

Puuttuvia ominaisuuksia:
- Käyttäjien poistaminen tietokannasta. Jos toteutetaan, niin ratkaistava ristiriita puuttuvan käyttäjän ja olemassa olevien projektien välillä. Mahdollinen uusi taulu "lukituille" projekteille. Voi vaatia ison uudelleen koodauksen ja tietokannan taulujen muokkauksen
- Tietokannan taulut ovat indeksoimattomia.
- Käyttäjätilastojen tietojen laajentaminen, projektikohtaisten muutoksien näkeminen.
- Vakiomuotoiset raportit puuttuvat, toteuttaminen riippuu ajan riittävyydestä
- Projektien tietosisältöä voi laajentaa lisäämällä projektin muistiinpanot ja mahdollisuus liittää projektiin liittyviä "rakennuspiirustuksia". Toteuttaminen riippuu ajan riittävyydestä.
- template- muotoiluja ei ole, kaikki muotoilut (jos niitä on) ovat template- kohtaisia, CSS- rakenne puuttuu.

Suuret tietomäärät

1000 käyttäjää, 100 000 projektia ja 5 kassavirtaa kussakin (500 000 kassavirtaa):
2025-10-18 18:21:43,958 [INFO] Clearing Users, Projects, and Investments
2025-10-18 18:23:17,483 [INFO] Inserted 1001 users in 91.0 seconds
2025-10-18 18:23:19,364 [INFO] Inserted 100000 projects with 500000 cashflows in 1.88 seconds
2025-10-18 18:23:19,367 [INFO] GET /seed took 95.41s
2025-10-18 18:26:26,901 [INFO] GET /list_projects took 0.71s
2025-10-18 18:26:42,539 [INFO] GET /list_projects took 0.3s (projektin haku nimellä)
2025-10-18 18:28:14,040 [INFO] GET /cashflow_project/993 took 0.02s
2025-10-18 18:28:20,921 [INFO] GET /add_new_cashflow/993 took 0.01s
2025-10-18 18:28:43,292 [INFO] POST /add_new_cashflow/993 took 0.04s
2025-10-18 18:28:43,309 [INFO] GET /cashflow_project/993 took 0.01s
2025-10-18 18:28:55,618 [INFO] GET /list_projects took 0.67s

1000 käyttäjää, 1 000 000 projektia ja 5 kassavirtaa kussakin (5 000 000 kassavirtaa):

2025-10-18 18:38:03,343 [INFO] Clearing Users, Projects, and Investments
2025-10-18 18:39:38,646 [INFO] Inserted 1001 users in 89.87 seconds
2025-10-18 18:39:56,618 [INFO] Inserted 1000000 projects with 5000000 cashflows in 17.97 seconds
2025-10-18 18:39:56,620 [INFO] GET /seed took 113.28s
2025-10-18 18:50:04,889 [INFO] GET /list_projects took 16.62s
2025-10-18 18:50:35,140 [INFO] GET /list_projects took 12.04s
2025-10-18 18:50:47,522 [INFO] GET /list_projects took 2.96s (projektin haku nimellä)

Taulussa Users id on pääavain (PRIMARY KEY) ja siten automaattisesti indeksoitu, kuten myös username yksilöllinen- rajoittimen (UNIQUE) takia. Projects- taulun pääavain (PRIMARY KEY) on id ja siten id- perustuvien hakujen osalta indeksoitu. Projektin nimeen (project_name) perustuville hauille, esimerkiksi suodattimet luotiin indeksi (CREATE INDEX idx_projects_name ON Projects(project_name);)

