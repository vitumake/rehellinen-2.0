# Rehellinen 2.0 Backend

## Sisällys

1. [Luokat](#luokat)
   - [Player](#player)
   - [Airport](#airport)
   - [Country](#country)
   - [Item](#item)
   - [Cargo](#cargo-item)
   - [Plane](#plane-item)
2. [API](#api)
   - [Login](#login)
   - [Logout](#logout)

<br>

## **Luokat**

### **Tämä on vain python backend koodin dokumentaatio. Rajapinta Ks. [API](#api)**

Hakasulkeet sisältävät muutujan tyypin. Jos kyseessä on objekti linkittää se kyseiseen luokkaan. Jos kyseessä on lista jälkimmäiset hakasulkeet kertovat alkioiden tyypin. Metodeissa sulkeet sisältävät argumenttien tyypin. Luokissa sulkeet sisältävät emo luokan.

<br>


### **Player ( )**

#### Initialization

- pid (pelaajan id) [int]

#### Muuttujat

- uid (pelaajan id) [int]
- name (pelaajan nimi) [str]
- money (pelaajan raha) [float]
- fuel (pelaajan bensa) [float]
- health (pelaajan kunto) [int]
- time (pelaajan aikaleima) [time]
  - *Vissiin turha*
- last_event (edellinen tapahtuma) [Obj] *kesken*
- plane (aktiivinen lentokone [[Obj](#plane)]
- location (pelaajan lokaatio) [[Obj](#airport)]
- inventory (pelaajan tavaralista) [list] [[Obj](#item)]
- quests (pelaajan tehtävälista) [list] [[Obj](#quest)]
  
#### Atribuutit

- incItem([Obj](#Item))
  - Lisää pelaajalle tavaran
- incMoney(int)
  - Muuttaa pelaajan rahamäärää
  - toimii myös negatiivisilla arvoilla
- incFuel(int)
  - Muuttaa pelaajan bensamäärää
  - toimii myös negatiivisilla arvoilla
- incHealth(int)
  - Muuttaa pelaajan kestopisteiden määrää
  - Max ja Min arvot otetaan pelaajan aktiivisesta lentokoneesta
- setActivePlane(int)
  - Argumentti on lentokoneen id
  - Muuttaa pelaajan aktiivista lentokonetta.
  - Jos kyseinen id ei vastaa olemassa olevaa lentokonetta pysyy lentokone samana
- update()
  - Käytetään muutujien päivittämiseen tietokannasta
  - Ei tarvitse kutsua erikseen käyttettäessä muita metodeita
- updateQuests()
  - Käytetään tehtävälistan päivittämiseen tietokannasta
  - Ei tarvitse kutsua erikseen
- updateInv()
  - Käytetään tavaralistan päivittämiseen tietokannasta
  - Ei tarvitse kutsua erikseen

#### Esimerkki

```json
{
    "fuel": 0.0,
    "health": 0,
    "inventory": [],
    "last_event": null,
    "location": {
      "country": {
        "fuelprice": 3.33,
        "iso": "FI",
        "name": "Finland"
      },
      "icao": "EFHK",
      "municipality": "Helsinki",
      "name": "Helsinki Vantaa Airport",
      "pos": [
        60.3172,
        24.963301
      ],
      "type": "large_airport"
    },
    "money": 40.0,
    "name": "make",
    "plane": {
      "fuel_consumption": 26,
      "id": 1,
      "isPlane": true,
      "max_cargo": 250.0,
      "max_fuel": 200,
      "max_health": 5,
      "name": "Cessna 172",
      "speed": 226,
      "value": 50000,
      "volume": 3000
    },
    "quests": [],
    "time": 1665600000.0,
    "uid": 13
}
```

<br>


### **Airport ( )**

#### Initialization

- icao (kentän icao tunnus) [str]
#### Muuttujat

- icao (kentän icao tunnus) [str]
- name (kentän mini) [str]
- pos (kentän koordinaatit) [tuple]
  - (lon, lat)
- type (kentän koko) [str]
- municipality (kentän kunta) [str]
- country (maa jossa kenttä sijaitsee) [[Obj](#country)]
  
#### Esimerkki

```json
{
    "icao": "EFHK",
    "municipality": "Helsinki",
    "name": "Helsinki Vantaa Airport",
    "pos": [
    60.3172,
    24.963301
    ],
    "type": "large_airport"
}
```

<br>

### **Country ( )**

#### Initialization

- iso (maan iso koodi) [str]

#### Muuttujat

- iso (maan iso koodi) [str]
- name (maan nimi) [str]
- fuelprice (maan bensan hinta) [float]

#### Esimerkki

```json
{
    "fuelprice": 3.33,
    "iso": "Fi",
    "name": "Finland"
  }
```

<br>

### **Item ( )**

Tämä on emo luokka joten sitä ei koskaan kutsuta suoraan
#### Initialization

- id (tavaran id) [int]
- name (tavaran nimi) [str]
- isPlane (kyseessä lentokone) [bool]

#### Muuttujat

- id (tavaran id) [int]
  - jos kyseessä lentokone lentokoneen id
- name (tavaran nimi) [str]
- isPlane (onko kyseesä lentokone) [bool]

#### Atribuutit

incItem([Obj](#player))
- Lisää kyseisen tavaran pelaajalle

[Plane](#airport) ja [Cargo](#cargo) luokat viittaavat tähän luokkaan.

<br>

### **Cargo ([Item](#item))**

#### Initialization 

- cid *(tavaran id)* [int]
- amount *(tavaran määrä)* [int]
#### Muuttujat

- amount *(tavaran määrä)* [int]
- weight *(tavaran paino)* [int]
  - Tavaran paino lasketaan kertomalla tavaran perusmassa sen määrällä
- base_risk *(tavaran riskikerroin)* [float]
- base_value *(tavaran arvo)* [float]
  - Tavaran arvo lasketaan kertomalla tavaran perusarvo sen määrällä
- volume *(tavaran tilavuus)* [float]
  - Tavaran tilavuus lasketaan kertomalla tavaran perustilavuus sen määrällä
- max_qty *(tavaran maksimi määrä)* [int]
  - Maksimi määrä jota tavaraa saa kuljettaa. Tämä otetaan automaattisesti huomioon koodissa.

#### Esimerkki

```json
{
    "amount": 2,
    "base_risk": 10.0,
    "base_value": 10000000,
    "id": 6,
    "isPlane": false,
    "max_qty": 2,
    "name": "ydinaseita",
    "volume": 1000,
    "weight": 2000.0
}
```

<br>

### **Plane ([Item](#item))**

#### Initialization

- pid *(lentokoneen id)* [int]

#### Muuttujat

- fuel_consumption *(koneen bensan kulutus)* [int]
- max_fuel *(koneen maksimi bensamäärä)* [int]
- max_cargo *(koneen maksimi kuorma)* [int]
- max_health *(koneen maksimi kestopisteet)* [int]
- speed *(koneen nopeus)* [int]
- value *(koneen hinta)* [int]
- volume *(koneen ruuman koko)* [int]

#### Esimerkki

```json
{
    "fuel_consumption": 378,
    "id": 2,
    "isPlane": true,
    "max_cargo": 2500.0,
    "max_fuel": 3100,
    "max_health": 3,
    "name": "Douglas DC-3",
    "speed": 333,
    "value": 180000,
    "volume": 15000
  }
```

<br>

## **API**

### Kirjautuminen

Kirjautuminen on tehtävä ennen kyselyiden lähettämistä. Yhdistettäessä [/login](#login) päätepisteeseen tallentaa flask selaimeen keksin, jonka avulla se tunnistaa käyttäjän. Keksin voi poistaa kirjautumalla ulos API:sta käyttäen [/logout](#logout) päätepistettä.

<br>

### **/login**

Login päätepiste ottaa vastaan vain post metodilla lähetettyjä pyyntöjä. 

#### Argumentit

- name *(Pelaajan nimi)*
- pwd *(Pelaajan salasana)*

#### Esimerkki

```html
<form action="http://127.0.0.1:3000/login" method="post">
    <p><input type=text name=name>
    <p><input type=text name=pwd>   
    <p><input type=submit value=Login>
</form>
```

### **/logout**

Logout ei tarvitse parametreja. Lähetettäessä pyyntö se poistaa automaattisesti pelaajan selaimesta keksin ja täten kirjaa hänet ulos.

#### Esimerkki

```http
http://127.0.0.1:3000/logout
```

### **/user**

