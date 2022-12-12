#Epämääräsiä funktioita jotka ei sovi luokkiin

from random import shuffle
from db import sqlQuery
import classes

#Hae koordinaatteja lähinnä olevat kentät
#origin = pelaajan sijainti
#konditionaalit korjaa mahdolliset ongelmat piirien ääriarvojen kohdalla
#Siirretty airport luoka metodiksi. Jätin tänne kuitenki jos tarttee
def findAirports(origin:object, limit:int=10, offset:int=-1, srcSize:int=1) -> list:
    
    begin=addCoord(origin.pos, (offset, offset))
    strt=subCoord(begin, (srcSize, srcSize))
    end=addCoord(begin, (srcSize, srcSize))
    
    airports = sqlQuery(
        f'SELECT'
        ' ident'
        ' FROM'
        ' airport'
        ' WHERE'
        f' longitude_deg BETWEEN {strt[1]} AND {end[1]}'
        f' AND latitude_deg BETWEEN {strt[0]} AND {end[0]}'
        ' AND ('
            ' type = "large_airport"'
            ' OR type = "medium_airport"'
        ' )'
        f' AND ident != "{origin.icao}"'
        f' limit {limit}'
    )
    return [i[0] for i in airports]

def addCoord(coord1:tuple, coord2:tuple) -> tuple:
    lon = coord1[0] + coord2[0] if coord1[0] + coord2[0] < 180 else -360 + coord1[0] + coord2[0]
    lat = coord1[1] + coord2[1] if coord1[1] + coord2[1] < 90 else 180 - coord1[1] - coord2[1]
    return (lon, lat)

def subCoord(coord1:tuple, coord2:tuple) -> tuple:
    lon = coord1[0] - coord2[0] if coord1[0] - coord2[0] > -180 else 360 - coord1[0] - coord2[0]
    lat = coord1[1] - coord2[1] if coord1[1] - coord2[1] > -90 else -180 + coord1[1] + coord2[1]
    return (lon, lat)

def calcReward(cargo:object ,dist):
    #yksikköhinta * välityspalkkio * yksiköiden määrä potenssiin tuhannet kilometrit * riskikerroin
    
    risk = cargo.base_risk
    dist = dist
    price = cargo.base_value
    RpTKm = dist/1000 * risk
    return (risk * price * (dist/1000))/100 + (2000*(dist/1000))