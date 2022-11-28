# rehellinen-lentorahti-ky

Kauppisen Pete omistaa firman. Petellä on paljon velkaa. Peten pitää kerätä tarpeeksi rahaa maksaakseen velkansa.

- lento rpg
- pelaajan tehtävä on kerätä rahaa 
- satunnaisia tehtäviä
- hypitään kentästä toiseen tehtäviä suorittaen
- satunnaisia tapahtumia kenttien välillä/ kentillä
- konetta voi upgradee (progressio)

# Sisällys
1. [Tavoitteet](#Tavoitteet)
	- [Luuppi](#Luuppi)
	- [Must](#Must)
	- [Want](#Want)
	- [Plus](#Plus)
2. [Tiimin tavoitteet](#tiimin-tavoitteet)
3. [Pelin laatu tavoitteet](#pelin-laatu-tavoitteet)
4. [Käyttöliittymän rakenne](#Käyttöliittymän-rakenne)
5. [MySql Database](#mysql-database)
	- [My Sql Salasana tiedosto](#mysql-database-salasana-tiedosto)

# Tavoitteet

## Luuppi:

1. pelaaja hyväksyy tehtävän
2. pelaaja "lentää" kentältä toiselle suorittaakseen tehtävän
3. pelaaja saa satunnaisia tapahtumia kentillä ja kenttien välissä jotka tuovat peliin haastetta tai auttavat pelaajaa
4. pelaaja ansaitsee rahaa suoritettuaan tehtävän
5. ansaittua rahaa voi käyttää bensaan, upgradeen, koneen korjaamiseen tai säästää voittoa varten

WIN: pelaaja saavuttaa tavoite määrän rahaa <br> LOSE: pelaajalta loppuu raha (ei voi ostaa bensaa), koneelta loppuu kuntopisteet tai pelaaja saadaan kiinni

## Must:
- selkeä käyttöliittymä
- pelaaja voi vaihtaa kenttää "lentää"
- pelaaja voi suorittaa tehtäviä (basic vie tavara paikasta A paikkaan B)
- pelaaja voi ansaita rahaa
- pelaaja voi voittaa

## Want:

- erinlaisia tehtäviä
- satunnaisia tapahtumia kenttien välillä
- pelaaja joutuu käyttämään polttoainetta kenttien välillä liikkumiseen ja pelaaja voi ostaa bensaa ansaitulla rahalla
- kone voi hajota ja konetta voi korjata kentällä
- lose states
	- raha loppuu tai menee miinukselle: konkurssi
	- koneen kuntopisteet loppuvat: kuolema

## Plus:

- konetta voi upgradee
- satunnaisten tapahtumien laajentaminen
- satunnaiset tapahtumat kentillä
- hard codatut satunnaiset tapahtumat
- satunnaistapahtuma "sinua jahdataan"
	- jäät kiinni: vankila
- kuljetettavalla tavaralla on paino
- intro missä kerrotaan "tarinaa"
	- kirjoituskone tyyli printtiin?
- outro missä kerrotaan "tarinaa"
	- kirjoituskone tyyli printtiin?

# Tiimin tavoitteet:

- aikataulussa pysyminen
- selkeää koodia kommenttikenttiä hyödyntäen
- yksinkertainen > monimutkainen
- push peliin vain valmiista koodista. Kehityksessä oleva koodi master branch
- kommentointi Gittiin
- kerrotaan tiimille kun on tehnyt jtn. Ei sooloilla. Pidetään paketti kasassa ja tiimi tietoisena mitä tapahtuu ja milloin.
	
# Pelin laatu tavoitteet:

- toimiva (koodi testattua)
- helppo käyttöinen
- tavoitteiden mukainen

# Käyttöliittymän rakenne:

- käyttöliittymän ominaisuudet voivat muuttua ulkoasultaan ja toiminnot ovat riippuvaisia peliin sisälletyistä ominaisuuksista
- käyttöliittymä pyyhkii edelliset inputit ja statit kun annetaan uusi komento ennen kuin printtaa seuraavat tiedot ja antaa uuden input kentän
- väärä input antaa käyttäjälle "väärä käsky" syötteen ja kysyy uusestaan mitä pelaaja haluaa tehdä
- jokaisesta valikosta pitää voida palata edelliseen valikkoon

	- selitys inputeista
	- pelaaja
		- statit
			- koneen kunto
			- bensan määrä
			- koneen statit
				- mikä kone
				- paljon kuluttaa bensaa
				- max kuntopisteet 
				- paljonko voi kuljettaa
			- paljonko rahaa ja tavoite raha
		- tehtävät
			- suoritettujen tehtävien lukumäärä
			- aktiivinen tehtävä
				- mitä kuljetetaan ja paljon kuljetetaan
				- tehtävästä saatava palkkio
				- mistä kuljetetaan ja minne
	- kenttä
		- osta bensaa
			- paljonko ostetaan
			- hyväksy osto
		- korjaa kone
			- hyväksy korjaus
		- katso tehtäviä
			- hyväksy tehtäviä
		- upgradee kone
			- mikä upgrade
			- hyväksy upgrade
		- vieraile kentällä
			- satunnais tapahtumat


# MySql database

![MySql diagrammi](https://leopard.hosting.pecon.us/dl/jmkqp/kuva_2022-10-13_183906758.png)

# MySql database salasana tiedosto
Tietokanta ylläpidetään nykyään servervillä joten tähän ei tarvitse kiinnittää huommiota.
<br>
~~Kaikkilla on oma salasana mysql tietokantaan joten elämän helpottamiseksi jokaisella on myös oma "pass.txt"~~

### Ohje "pass.txt" tiedoston luomiseen
1. Tee tiedosto nimeltä "pass.txt" ylipään kansioon
2. Ensimmäiselle riville kirjoitat tietokannan nimen esim. "lentopeli"
3. Toiselle riville kirjoitat tietokannan salasanan

### Esimerkki pass.txt tiedoston sisällöstä
	lentopeli
	salasana1234
