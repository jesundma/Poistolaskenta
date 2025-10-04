# Poistolaskenta
Tietokannat ja web-ohjelmointi julkinen repo kurssisovellusta varten. Repossa on kolme .sql- tiedostoa, joista kaksi liittyy sovelluksen käynnistykseen ja kolmas on tarkoitettu sovelluksen koekäyttöön. Jos tiedosto ajetaan, luo se tietokantaan esimerkkiprojekteja.

Sovellukseen lisätään projektiobjekteja, jotka sisältävät tietoja projektin investoinneista ja investointien ajankohdasta. Projekteille määritellään tieto poistotavasta (tasapoisto, menojäännöspoisto), projektin nimi, yksilöllinen projektitunniste ja muita mahdollisia projektiin liittyviä määritteitä. Tiedot talletetaan tietotauluun Projects, jossa projektin numerotunnus on yksilöllinen avain.

Käyttäjä syöttää syöttöikkunaan haluamilleen vuosille investointiarvot, jotka talletetaan projektille tietotauluun Investments. Tällä hetkellä investoinnit syötetään yksi tieto kerrallaan vuosi - investointi- parina.

Sovelluksessa on käyttäjähallinta, johon on määritelty käyttäjät ja käyttäjien hash- salasanat. Tiedot ovat tietotaulussa Users. Sovellusta käynnistettäessä ensimmäistä kertaa, sovellus ohjaa käyttäjän aina käyttäjän luomiseen.

Projektien muutostiedot talletetaan käyttäjittäin, projektista tiedetään projektin luonut käyttäjä ja projektia muokanneet käyttäjät. Tiedot luojasta ovat tietotaulussa Inserted ja muuttajista Modified.

Projektien poistolaskentaa ei toteuteta ainakaan tällä kurssilla, koska pandas- kirjastoa ei voi käyttää. Projekteja ja projektien investointeja voi syöttää yksitellen. Massasyöttömahdollisuus riippuu toiminnon toteuttamiskelpoisuudesta kurssilla sallituilla kirjastoilla.

Sovelluksessa on käyttäjähallinta, jolla määritellään tietoja lisännyt, muuttanut tai poistanut käyttäjä sekä oikeudet projektien käsittelyyn.

Sovellus tuottaa ennalta määriteltyjä raportteja, joihin käyttäjä voi syöttää parametreja raporttien muodostamista varten. Raportteja tai niiden sisältöä ei ole vielä määritelty.


SOVELLUKSEN KÄYNNISTÄMINEN:

- asenna flask- kirjasto komennolla: pip install flask
- sovellus käynnistyy komennolla: flask run

Sovelluksen käynnistämisen jälkeen voidaan tietokantaan halutessa lisätä esimerkkiprojekteja. Jos haluat lisätä esimerkkiprojekteja, tee sovelluksen hakemistossa pääteikkunassa seuraavat komennot: 
- sqlite3 database.db
- .read dummy_projects.sql

Jos sovellusta ei ole asennettu aiemmin tai sovellukseen ei ole määritelty käyttäjiä, sovellus luo tietokannan ja ohjaa luomaan ensimmäisen käyttäjän. Jos tietokannasta löytyy jo käyttäjiä, ohjaa sovellus kirjautumissivulle.

Käyttäjäoikeudet toimivat projektin luoja- tasolla. Vain projektin luoja pystyy poistamaan projektin. Projektin muuttajat tallentuvat kantaan Modified- tauluun, mutta vielä kaikilla käyttäjillä on mahdollisuus muokata mitä tahansa projektia.

Tunnettuja virheitä ja ongelmia:
- projektisuodatin ei säily, jos käyttäjä yrittää muuttaa projektin oikeuksia ja saa sitä koskevan virheilmoituksen