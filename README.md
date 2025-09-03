# Poistolaskenta
Tietokannat ja web-ohjelmointi julkinen repo kurssisovellusta varten

Sovellukseen lisätään projektiobjekteja, jotka sisältävät tietoja projektin investoinneista ja investointien ajankohdasta. Projekteille määritellään tieto poistotavasta (tasapoisto, menojäännöspoisto), projektin nimi, yksilöllinen projektitunniste ja muita mahdollisia projektiin liittyviä määritteitä. Tiedot talletetaan tietotauluun Projects, jossa projektin numerotunnus on yksilöllinen avain.

Projektien investointivuosien syöttö on kovakoodattu vuosiksi 2026 - 2035. Käyttäjä syöttää syöttöikkunaan haluamilleen vuosille investointiarvot, jotka talletetaan projektille tietotauluun Investments.

Sovelluksessa on käyttäjähallinta, johon on määritelty käyttäjät ja käyttäjien hash- salasanat. Tiedot ovat tietotaulussa Users.

Projektien muutostiedot talletetaan käyttäjittäin, projektista tiedetään projektin luonut käyttäjä ja projektia muokanneet käyttäjät. Tiedot luojasta ovat tietotaulussa Inserted ja muuttajista Modified.

Projektien poistolaskentaa ei toteuteta ainakaan tällä kurssilla, koska pandas- kirjastoa ei voi käyttää.

Projekteja voi syöttää yksitellen tai massasyöttönä, jälkimmäinen riippuu toiminnon toteuttamiskelpoisuudesta kurssilla sallituilla kirjastoilla.

Sovelluksessa on käyttäjähallinta, jolla määritellään tietoja lisännyt, muuttanut tai poistanut käyttäjä sekä oikeudet projektien käsittelyyn.

Sovellus tuottaa ennalta määriteltyjä raportteja, joihin käyttäjä voi syöttää parametreja raporttien muodostamista varten. Raportteja voidaan muodostaa vuosittaisista investoinneista ja lasketuista poistoista.
