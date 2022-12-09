#Epämääräsiä funktioita jotka ei sovi luokkiin

from db import sqlQuery
import classes

#Hae koordinaatteja lähinnä olevat kentät
#origin = pelaajan sijainti
#konditionaalit korjaa mahdolliset ongelmat piirien ääriarvojen kohdalla
def findAirports(origin:object, limit:int=10, offset:int=-1, srcSize:int=1) -> list:
    
    begin=addCoord(origin.pos, (offset, offset))
    strt=subCoord(begin, (srcSize, srcSize))
    end=addCoord(begin, (srcSize, srcSize))
    
    #hae kenttiä (ident) käyttäen edellisiä arvoja
    airports = sqlQuery(f'SELECT ident, airport.name, country.name FROM airport, country '
             f'WHERE airport.iso_country = country.iso_country '
             f'AND airport.longitude_deg BETWEEN {strt[1]} AND {end[1]} '
             f'AND airport.latitude_deg BETWEEN {strt[0]} AND {end[0]} '
             f'AND (type = "large_airport" OR type = "medium_airport") AND ident != "{origin.icao}"'
             f'limit {limit}')
    
    #luodaan lentokenttä objektit
    for i in range(len(airports)):
        airports[i]=classes.Airport(airports[i][0])
    
    return airports

def addCoord(coord1:tuple, coord2:tuple) -> tuple:
    lon = coord1[0] + coord2[0] if coord1[0] + coord2[0] < 180 else -360 + coord1[0] + coord2[0]
    lat = coord1[1] + coord2[1] if coord1[1] + coord2[1] < 90 else 180 - coord1[1] - coord2[1]
    return (lon, lat)

def subCoord(coord1:tuple, coord2:tuple) -> tuple:
    lon = coord1[0] - coord2[0] if coord1[0] - coord2[0] > -180 else 360 - coord1[0] - coord2[0]
    lat = coord1[1] - coord2[1] if coord1[1] - coord2[1] > -90 else -180 + coord1[1] + coord2[1]
    return (lon, lat)