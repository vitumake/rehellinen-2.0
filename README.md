# rehellinen-lentorahti-ky

Kauppisen Pete omistaa firman. Petellä on paljon velkaa. Peten pitää kerätä tarpeeksi rahaa maksaakseen velkansa.

- lento rpg
- pelaajan tehtävä on kerätä rahaa 
- satunnaisia tehtäviä
- hypitään kentästä toiseen tehtäviä suorittaen
- satunnaisia tapahtumia kenttien välillä/ kentillä
- konetta voi upgradee (progressio)

# rehellinen 2.0

- Visuaalinen käyttöliittymä

## Muutoksia esityksestä
- Tietokanta bugi korjattu
- Käyttöliittymä suoraviivaisempi ja nopeampi
- pää mekaniikat kunnossa

# Sisällys
- [rehellinen-lentorahti-ky](#rehellinen-lentorahti-ky)
- [rehellinen 2.0](#rehellinen-20)
	- [Muutoksia esityksestä](#muutoksia-esityksestä)
- [Sisällys](#sisällys)
- [Tavoitteet](#tavoitteet)
	- [Luuppi:](#luuppi)
	- [Must:](#must)
	- [Want:](#want)
	- [Plus:](#plus)
- [Tiimin tavoitteet:](#tiimin-tavoitteet)
- [Pelin laatu tavoitteet:](#pelin-laatu-tavoitteet)
- [Käyttöliittymän rakenne:](#käyttöliittymän-rakenne)
- [MySql database](#mysql-database)
	- [Sql luonti skripti](#sql-luonti-skripti)

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

## Sql luonti skripti
```sql
	-- --------------------------------------------------------
	-- Verkkotietokone:              192.168.50.35
	-- Palvelinversio:               8.0.31-0ubuntu0.20.04.2 - (Ubuntu)
	-- Server OS:                    Linux
	-- HeidiSQL Versio:              11.3.0.6295
	-- --------------------------------------------------------

	/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
	/*!40101 SET NAMES utf8 */;
	/*!50503 SET NAMES utf8mb4 */;
	/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
	/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
	/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

	-- Dumping structure for taulu rehellinen.active_quests
	CREATE TABLE IF NOT EXISTS `active_quests` (
	`id` int NOT NULL AUTO_INCREMENT,
	`game_id` int NOT NULL,
	`quest_id` int NOT NULL,
	`cargo_id` int NOT NULL,
	`destination` varchar(10) NOT NULL,
	`reward` float NOT NULL DEFAULT '0',
	`amount` int NOT NULL,
	PRIMARY KEY (`id`),
	KEY `active_quests_ibfk_1` (`destination`),
	KEY `active_quests_ibfk_2` (`quest_id`),
	KEY `active_quests_ibfk_3` (`game_id`),
	KEY `active_quests_ibfk_4` (`cargo_id`),
	CONSTRAINT `active_quests_ibfk_1` FOREIGN KEY (`destination`) REFERENCES `airport` (`ident`),
	CONSTRAINT `active_quests_ibfk_2` FOREIGN KEY (`quest_id`) REFERENCES `quests` (`id`),
	CONSTRAINT `active_quests_ibfk_3` FOREIGN KEY (`game_id`) REFERENCES `game` (`id`),
	CONSTRAINT `active_quests_ibfk_4` FOREIGN KEY (`cargo_id`) REFERENCES `cargo` (`id`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	-- Tietojen vientiä ei oltu valittu.

	-- Dumping structure for taulu rehellinen.airport
	CREATE TABLE IF NOT EXISTS `airport` (
	`id` int NOT NULL,
	`ident` varchar(40) NOT NULL,
	`type` varchar(40) DEFAULT NULL,
	`name` varchar(40) DEFAULT NULL,
	`latitude_deg` double DEFAULT NULL,
	`longitude_deg` double DEFAULT NULL,
	`elevation_ft` int DEFAULT NULL,
	`continent` varchar(40) DEFAULT NULL,
	`iso_country` varchar(40) DEFAULT NULL,
	`iso_region` varchar(40) DEFAULT NULL,
	`municipality` varchar(40) DEFAULT NULL,
	`scheduled_service` varchar(40) DEFAULT NULL,
	`gps_code` varchar(40) DEFAULT NULL,
	`iata_code` varchar(40) DEFAULT NULL,
	`local_code` varchar(40) DEFAULT NULL,
	`home_link` varchar(40) DEFAULT NULL,
	`wikipedia_link` varchar(40) DEFAULT NULL,
	`keywords` varchar(40) DEFAULT NULL,
	PRIMARY KEY (`ident`),
	KEY `iso_country` (`iso_country`),
	CONSTRAINT `airport_ibfk_1` FOREIGN KEY (`iso_country`) REFERENCES `country` (`iso_country`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	-- Tietojen vientiä ei oltu valittu.

	-- Dumping structure for taulu rehellinen.cargo
	CREATE TABLE IF NOT EXISTS `cargo` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` varchar(50) NOT NULL,
	`weight` float NOT NULL,
	`base_risk` float NOT NULL,
	`volume` int NOT NULL,
	`base_value` int NOT NULL,
	`max_qty` int DEFAULT NULL,
	PRIMARY KEY (`id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

	-- Tietojen vientiä ei oltu valittu.

	-- Dumping structure for taulu rehellinen.country
	CREATE TABLE IF NOT EXISTS `country` (
	`iso_country` varchar(40) NOT NULL,
	`name` varchar(40) DEFAULT NULL,
	`continent` varchar(40) DEFAULT NULL,
	`wikipedia_link` varchar(40) DEFAULT NULL,
	`keywords` varchar(40) DEFAULT NULL,
	`fuelprice` float NOT NULL DEFAULT '3.4',
	PRIMARY KEY (`iso_country`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	-- Tietojen vientiä ei oltu valittu.

	-- Dumping structure for taulu rehellinen.events
	CREATE TABLE IF NOT EXISTS `events` (
	`id` int NOT NULL AUTO_INCREMENT,
	`title` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
	`description` text NOT NULL,
	`type` int NOT NULL DEFAULT '0',
	PRIMARY KEY (`id`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	-- Tietojen vientiä ei oltu valittu.

	-- Dumping structure for taulu rehellinen.game
	CREATE TABLE IF NOT EXISTS `game` (
	`id` int NOT NULL AUTO_INCREMENT,
	`location` varchar(10) NOT NULL DEFAULT 'EFHK',
	`screen_name` varchar(40) NOT NULL,
	`fuel` float NOT NULL DEFAULT '0',
	`money` float NOT NULL DEFAULT '0',
	`active_plane` int NOT NULL DEFAULT '1',
	`last_event` int DEFAULT NULL,
	`pass` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
	`plane_health` int NOT NULL DEFAULT '5',
	`time` float NOT NULL,
	`apikey` longtext,
	PRIMARY KEY (`id`),
	KEY `location` (`location`),
	KEY `game_ibfk_3` (`last_event`),
	KEY `game_ibfk_1` (`active_plane`) USING BTREE,
	CONSTRAINT `game_ibfk_1` FOREIGN KEY (`active_plane`) REFERENCES `planes` (`id`),
	CONSTRAINT `game_ibfk_2` FOREIGN KEY (`location`) REFERENCES `airport` (`ident`),
	CONSTRAINT `game_ibfk_3` FOREIGN KEY (`last_event`) REFERENCES `events` (`id`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	-- Tietojen vientiä ei oltu valittu.

	-- Dumping structure for taulu rehellinen.inventory
	CREATE TABLE IF NOT EXISTS `inventory` (
	`id` int NOT NULL AUTO_INCREMENT,
	`pid` int NOT NULL,
	`itemId` int NOT NULL,
	`isPlane` tinyint NOT NULL DEFAULT '0',
	`amount` int NOT NULL DEFAULT '0',
	PRIMARY KEY (`id`),
	KEY `pid` (`pid`),
	CONSTRAINT `FK_inventory_game` FOREIGN KEY (`pid`) REFERENCES `game` (`id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

	-- Tietojen vientiä ei oltu valittu.

	-- Dumping structure for taulu rehellinen.planes
	CREATE TABLE IF NOT EXISTS `planes` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` varchar(255) NOT NULL,
	`fuel_consumption` int NOT NULL DEFAULT '0',
	`max_fuel` int NOT NULL DEFAULT '0',
	`max_cargo` float NOT NULL DEFAULT '0',
	`speed` int NOT NULL DEFAULT '100',
	`value` int NOT NULL DEFAULT '0',
	`volume` int NOT NULL DEFAULT '0',
	`max_health` int NOT NULL,
	PRIMARY KEY (`id`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	-- Tietojen vientiä ei oltu valittu.

	-- Dumping structure for taulu rehellinen.quests
	CREATE TABLE IF NOT EXISTS `quests` (
	`id` int NOT NULL AUTO_INCREMENT,
	`quest_name` varchar(40) NOT NULL,
	`quest_description` text NOT NULL,
	PRIMARY KEY (`id`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	-- Tietojen vientiä ei oltu valittu.

	/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
	/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
	/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
	/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
```

# Kuvakaappauksia pelistä:
Päänäkymä
![kuva](https://user-images.githubusercontent.com/111982153/211268728-924cf452-9ace-4d88-9870-035a0b245d22.png)

Karttanäkymä
![kuva](https://user-images.githubusercontent.com/111982153/211269080-ff8b3e6a-6bc6-4596-8e06-188782a64781.png)

Tankkaus
![kuva](https://user-images.githubusercontent.com/111982153/211269193-2f38d0e1-c08f-4106-8a11-778806d340bd.png)
![kuva](https://user-images.githubusercontent.com/111982153/211269350-55c359a3-2173-4fb4-9e21-11573c9b6045.png)




