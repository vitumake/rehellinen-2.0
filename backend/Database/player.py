#player.py
from datetime import datetime
import hashlib
from time import sleep
from Database.db import sqlQuery, sqlSafeQuery
from Database.location import getAirportName, icaoDistance
from Game import event, framework
from Game import quest
#Pelaajan muuttujat
pid = None
logged = False
#Valitsee pelaajan ajetaan pelin alussa. (Täytyy tehdä vielä player creation skripti)
def doLogin(name:str, pwd:str):
    #print(hashlib.sha224(b"pwd").hexdigest())
    login = sqlSafeQuery("""
            SELECT EXISTS(
            SELECT
                id
            FROM
                game
            WHERE
                screen_name = %(usr)s
            AND
                pass = %(pwd)s
        )""", {
            'usr': name,
            'pwd': hashlib.sha224(b"pwd").hexdigest()
        }, 0)
    if login[0] == 1: login = sqlQuery(f'SELECT id FROM game WHERE screen_name = "{name}"', 0)
    return login[0]

def doRegister(name:str, pwd:str, pwd2:str):
    if sqlQuery(f'SELECT EXISTS(SELECT id FROM game WHERE screen_name="{name}")', 0)[0] == 1: return 'Nimi ei kelpaa!'
    if len(name) > 10: return 'Nimi on liian pitkä!'
    if not name.isalnum(): return 'Nimi ei kelpaa!'
    if pwd != pwd2: return 'Salasanat eivät täsmää!'
    sqlSafeQuery("""
        INSERT INTO
        game (screen_name, pass, time)
        VALUES ( %(name)s, %(pwd)s, %(date)s)
        """, {
            'name': name,
            'pwd': hashlib.sha224(b"pwd").hexdigest(),
            'date': datetime.now().timestamp()
        })
    return sqlQuery(f'SELECT id FROM game WHERE screen_name="{name}"', 0)[0]
    

#Pelaajan nimi
def getName(): return sqlQuery(f'SELECT screen_name FROM game WHERE id="{pid}"')[0][0]

#Pelaajan rahamuuttuja
def getMoney(): return sqlQuery(f'SELECT money FROM game WHERE id="{pid}"')[0][0]

#Pelaajan bensa muuttuja
def getFuel(): return sqlQuery(f'SELECT fuel FROM game WHERE id="{pid}"')[0][0]

#Pelaajan aktiivinen lentokone
def getPlane(): return sqlQuery(f'SELECT active_plane FROM game WHERE id="{pid}"')[0][0]

#Pelaajan lokaatio (ICAO)
def getLocICAO(): return sqlQuery(f'SELECT location FROM game WHERE id="{pid}"')[0][0]

#Pelaajan lokaatio (kenttä)
def getLocField(): return sqlQuery(f'SELECT airport.name FROM airport, game WHERE game.id="{pid}" '
                          f'AND game.location = airport.ident')[0][0]

#Pelaajan lokaatio (maa)
def getLocCountry(): return sqlQuery(f'SELECT country.name FROM country, airport, game WHERE game.id="{pid}" '
                            f'AND game.location = airport.ident '
                            f'AND airport.iso_country = country.iso_country')[0][0]

def getLocAll(): return sqlQuery(f'SELECT location, airport.name, country.name FROM country, airport, game WHERE game.id="{pid}" '
                            f'AND game.location = airport.ident '
                            f'AND airport.iso_country = country.iso_country')[0][0:3]

#Palauttaa pelaajan aktiivisen lentokoneen maksimi bensamäärän
def getMaxFuel(): return sqlQuery(f'SELECT max_fuel FROM game, planes WHERE game.id = "{pid}" AND active_plane = planes.id', 0)[0]

#Palauttaa pelaajan aktiivisen lentokoneen tavaratilan koon 
def getPlaneMaxVolume(): return sqlQuery(f'SELECT volume FROM game, planes WHERE game.id = "{pid}" AND active_plane = planes.id', 0)[0]

#Palauttaa pelaajan aktiivisen lentokoneen painorajan
def getPlaneMaxWeight(): return sqlQuery(f'SELECT max_cargo FROM game, planes WHERE game.id = "{pid}" AND active_plane = planes.id', 0)[0]

def getPlaneSpeed(): return sqlQuery(f'SELECT speed FROM game, planes WHERE game.id = "{pid}" AND active_plane = planes.id', 0)[0]

def getPlaneMaxHealth(): return sqlQuery(f'SELECT max_health FROM game, planes WHERE game.id = "{pid}" AND planes.id = active_plane', 0)[0]

def getPlaneHealth(): return sqlQuery(f'SELECT plane_health FROM game WHERE game.id = "{pid}"', 0)[0]

def getTime(): return sqlQuery(f'SELECT time FROM game WHERE game.id = "{pid}"', 0)[0]

#Palauttaa rahdin riskin
def getCargoRisk():
    items = sqlQuery(f'SELECT itemId FROM inventory WHERE pid = "{pid}" AND isPlane = "0"')
    totalRisk = 0
    for i in items:
        risk = sqlQuery(f'SELECT base_risk FROM cargo WHERE id = "{i[0]}"', 0)[0]
        totalRisk += risk
    return totalRisk

#Palauttaa rahdin tilavuuden
def getCargoVolume():
    items = sqlQuery(f'SELECT itemId FROM inventory WHERE pid = "{pid}" AND isPlane = "0"')
    totalVolume = 0
    for i in items:
        volume = sqlQuery(f'SELECT volume FROM cargo WHERE id = "{i[0]}"', 0)[0]
        amount = sqlQuery(f'SELECT amount FROM inventory WHERE itemId = "{i[0]}"', 0)[0]
        totalVolume += volume * amount
    return totalVolume

#Palauttaa rahdin painon
def getCargoWeight():
    items = sqlQuery(f'SELECT itemId FROM inventory WHERE pid = "{pid}" AND isPlane = "0"')
    totalWeight = 0
    for i in items:
        weight = sqlQuery(f'SELECT weight FROM cargo WHERE id = "{i[0]}"', 0)[0]
        amount = sqlQuery(f'SELECT amount FROM inventory WHERE itemId = "{i[0]}"', 0)[0]
        totalWeight += weight * amount
    return totalWeight

#Palauttaa pelaajan lentokoneen bensan käytön
def getFuelConsumption():
    return sqlQuery(f'SELECT fuel_consumption FROM planes, game WHERE game.id = "{pid}" AND planes.id = game.active_plane', 0)[0]

#Pelaajan metodit

def setActivePlane(val):
    sqlQuery(f'UPDATE game SET active_plane = "{val}" WHERE id="{pid}"')

#Muuta pelaajan rahamäärää (Pelaajan id, muutos)
#Palauttaa sqlQuery funktion
def incMoney(val):
    return sqlQuery(f'UPDATE game SET money = money + {round(val, 2)} WHERE id="{pid}"')
    
#Muuta pelaajan bensamäärää (Pelaajan id, muutos)
#Palauttaa sqlQuery funktion
def incFuel(val):
    return sqlQuery(f'UPDATE game SET fuel = fuel + {round(val, 2)} WHERE id="{pid}"')

def incTime(val):
    return sqlQuery(f'UPDATE game SET time = time + {val} WHERE id="{pid}"')

def incPlaneHealth(val):
    return sqlQuery(f'UPDATE game SET plane_health = plane_health + {val} WHERE id="{pid}"')

#Muuta pelaajan lokaatiota (muutos)
#Palauttaa false jos lokaatio ei ole sopiva
def setLocation(loc):
    if sqlQuery(f'SELECT EXISTS(SELECT * FROM airport WHERE ident = "{loc}")')[0][0] == 0: return False
    sqlQuery(f'UPDATE game SET location = "{loc}" WHERE id = "{pid}"')

#Palauttaa pelaajan nykyisten tehtävien id numerot active_quest taulusta
def getActiveQuests():
    return sqlQuery(f'SELECT id FROM active_quests WHERE game_id = {pid}')

# Hae tiettyä lentokenttää
def checkFly(ICAO):
    dist = icaoDistance(ICAO, getLocICAO())
    time = dist/getPlaneSpeed()
    fuelUse = getFuelConsumption() * time
    return round(fuelUse, 2)

#Kun pelaaja lentää
def doFly(dest, fuelUse):
    framework.clear()
    dist = icaoDistance(dest, getLocICAO())
    time = dist/getPlaneSpeed()
    incFuel(fuelUse * -1)
    setLocation(dest)
    framework.typewriter('Lennetään...')
    
    #Kaikki lennon aikana ajettavat funktiot
    complete = quest.checkQuest(pid, dest)
    event.eventRaffle(pid)
    
    sleep(1)
    #Perillä :)
    if complete[0] == 1:
        print('1 tehtävä suoritettu!')
        print(f'+{complete[1]}€')
    elif complete[0] > 1:
        print(f'{complete[0]} tehtävää suoritettu!')
        print(f'+{complete[1]}€')
    
    framework.clear()
    incTime(time*(60**2))
    framework.typewriter(f'{datetime.fromtimestamp(getTime())} {getAirportName(dest)}')
    sleep(1)
    input('\nPaina enter jatkaaksesi...')
    


