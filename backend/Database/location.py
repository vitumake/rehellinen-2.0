#location.py
from random import randint, shuffle
from Database.db import sqlQuery
from geopy.distance import distance

#Hae koordinaatteja lähinnä olevat kentät
#origin = pelaajan sijainti
#konditionaalit korjaa mahdolliset ongelmat piirien ääriarvojen kohdalla
def findAirports(origin, limit:int=10, lon:tuple=(1, 1), lat:tuple = (1, 1)) -> list:
    #longitude +1 & latitude +1
    long_plus_tuple = sqlQuery(f'SELECT longitude_deg FROM airport WHERE ident = "{origin}"')[0][0]
    long_plus = long_plus_tuple + lon[0] if long_plus_tuple + lon[0] < 180 else -360 + long_plus_tuple + lon[0]
    lat_plus_tuple = sqlQuery(f'SELECT latitude_deg FROM airport WHERE ident = "{origin}"')[0][0]
    lat_plus = lat_plus_tuple + lat[0] if lat_plus_tuple + lat[0] < 90 else 180 - lat_plus_tuple - lat[0]
    #longitude -1 & latitude -1
    long_minus_tuple = sqlQuery(f'SELECT longitude_deg FROM airport WHERE ident = "{origin}"')[0][0]
    long_minus = long_minus_tuple - lon[1] if long_minus_tuple - lon[1] > -180 else 360 - long_minus_tuple - lon[1]
    lat_minus_tuple = sqlQuery(f'SELECT latitude_deg FROM airport WHERE ident = "{origin}"')[0][0]
    lat_minus = lat_minus_tuple - lat[1] if lat_minus_tuple - lat[1] > -90 else -180 + lat_minus_tuple + lat[1]
    #hae kenttiä (ident, nimi) käyttäen edellisiä arvoja
    found_airports = sqlQuery(f'SELECT ident, airport.name, country.name FROM airport, country '
             f'WHERE airport.iso_country = country.iso_country '
             f'AND airport.longitude_deg BETWEEN {long_minus} AND {long_plus} '
             f'AND airport.latitude_deg BETWEEN {lat_minus} AND {lat_plus} '
             f'AND (type = "large_airport" OR type = "medium_airport") AND ident != "{origin}"'
             f'limit {limit}')
    return found_airports

def icaoDistance(origin, dest):
    dest = getAirportPos(dest)
    origin = getAirportPos(origin)
    return distance(dest, origin).km

def getAirportPos(ICAO) -> tuple:
    lat = sqlQuery(f'SELECT latitude_deg FROM airport WHERE ident = "{ICAO}"', 0)[0]
    lon = sqlQuery(f'SELECT longitude_deg FROM airport WHERE ident = "{ICAO}"', 0)[0]
    return (lat, lon)

#Hea lentokentän nimi ICAO:n perusteella
def getAirportName(ICAO):
    if sqlQuery(f'SELECT EXISTS(SELECT * FROM airport WHERE ident = "{ICAO}")')[0][0] == 0: return False
    else:
        return sqlQuery(f'SELECT name FROM airport WHERE ident = "{ICAO}"')[0][0]

#Hae maa missä lentokenttä sijaitsee ICAO:n perusteella
def getAirportCountry(ICAO):
    if sqlQuery(f'SELECT EXISTS(SELECT * FROM airport WHERE ident = "{ICAO}")')[0][0] == 0: return False
    else:
        return sqlQuery(f'SELECT country.name FROM country, airport WHERE ident = "{ICAO}"'
                        f'AND airport.iso_country = country.iso_country')[0][0]
#Hakee bensan litra hinnan ICAO koodin perustella
def getFuelPrice(ICAO):
    return sqlQuery(f'SELECT fuelprice FROM country, airport WHERE airport.ident = "{ICAO}" AND airport.iso_country = country.iso_country')[0][0]

#Arpoo ilmansuunnan pituus ja leveys piirit
def raffleHeading(len:int=1) -> tuple:
    heading = randint(1, 4)
    if heading == 1: return ((0, len), (len, 0))
    if heading == 2: return ((0, len), (0, len))
    if heading == 3: return ((len, 0), (0, len))
    if heading == 4: return ((len, 0), (len, 0))

def getShopPlane(id):
    return sqlQuery(f' SELECT * FROM planes WHERE id = "{id}";')[0]

