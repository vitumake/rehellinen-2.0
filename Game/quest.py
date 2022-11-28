from Database.db import sqlQuery, sqlSafeQuery
from Database import player
from Database.location import findAirports, getAirportName, raffleHeading
from Database.inventory import getItem, incItem
from random import randint, shuffle
from geopy.distance import distance



#Generoi tehtävän ja palauttaa tehtävän tiedot kirjastona
def genQuest(simCount:int=3, destDist:int=100, srcRad:int=5) -> dict:
    dest = genDest(simCount, destDist, srcRad)
    qid = randint(1, sqlQuery('SELECT COUNT(id) FROM quests')[0][0])
    cid = randint(1, sqlQuery('SELECT COUNT(id) FROM cargo')[0][0])
    cargo = sqlQuery(f'SELECT name FROM cargo WHERE id = {cid}')[0][0]
    title = sqlQuery(f'SELECT quest_name FROM quests WHERE id = {qid}')[0][0].replace('%cargo%', cargo).replace('%dest%', getAirportName(dest[0]))
    desc = sqlQuery(f'SELECT quest_description FROM quests WHERE id = {qid}')[0][0].replace('%cargo%', cargo).replace('%dest%', getAirportName(dest[0]))
    
    #Palkkio kaava
    #maksu = riski * perusmaksu * rahdattavien yksiköiden määrä, missä riski = rahdattavan tavaran paino * riskikerroin
    
    return {
        'questId' : qid,
        'title' : title,
        'desc' : desc,
        'cargo' : cargo,
        'dest' : dest[0],
        'dist' : dest[1],
        'cid' : cid,
        'unitPrice' : sqlQuery(f'SELECT base_value FROM cargo WHERE id = "{cid}"', 0)[0],
        'risk' : sqlQuery(f'SELECT base_risk FROM cargo WHERE id = "{cid}"', 0)[0]
    }

#Tekee argumentin määrän verran satunnaisia hyppyjä kenttien välillä
#Hypyt ovat aina kauemmas pelaajan kohteesta
#Palauttaa päämäärän sekä etäisyyden listassa
def genDest(simCount, destDist, srcRad) -> list:
    icao = player.getLocICAO()
    origin = (sqlQuery(f'SELECT latitude_deg FROM airport WHERE ident = "{player.getLocICAO()}"')[0][0], 
              sqlQuery(f'SELECT longitude_deg FROM airport WHERE ident = "{player.getLocICAO()}"')[0][0])
    lastLoc = origin
    heading = raffleHeading(srcRad)
    while simCount > 0:
        airports = findAirports(icao, 50, heading[0], heading[1])
        shuffle(airports)
        for i in airports:
            currLoc = (sqlQuery(f'SELECT latitude_deg FROM airport WHERE ident = "{i[0]}"')[0][0],
                       sqlQuery(f'SELECT longitude_deg FROM airport WHERE ident = "{i[0]}"')[0][0])
            if distance(origin, currLoc).km > distance(origin, lastLoc).km and distance(currLoc, lastLoc).km > destDist:
                icao = i[0]
                break
        simCount-=1
        lastLoc = currLoc
    return icao, distance(origin, currLoc).km

def calcReward(pid, quest:dict, cargoAmount:int) -> int:
    #yksikköhinta * välityspalkkio * yksiköiden määrä potenssiin tuhannet kilometrit * riskikerroin
    
    unitVolume = sqlQuery(f'SELECT volume FROM cargo WHERE id = "{quest["cid"]}"', 0)[0]
    unitWeight = sqlQuery(f'SELECT weight FROM cargo WHERE id = "{quest["cid"]}"', 0)[0]
    
    #Jos kyseistä tavara tyyppiä ei voi ottaa näin montaa
    if cargoAmount > sqlQuery(f'SELECT max_qty FROM cargo WHERE id = "{quest["cid"]}"', 0)[0]:
        return -1
    
    #Jos pelaajan lentokoneessa ei riitä tilavuus
    if unitVolume * cargoAmount > (player.getPlaneMaxVolume() - player.getCargoVolume()):
        return -2
    
    #Jos pelaajan lentokoneessa ei riitä kuormitus
    if unitWeight * cargoAmount > (player.getPlaneMaxWeight() - player.getCargoWeight()):
        return -3
    
    risk = quest["risk"]
    dist = quest["dist"]
    unitPrice = quest["unitPrice"]
    RpTKm = quest['dist']/1000 * quest['risk']
    reward = (risk * unitPrice * cargoAmount * (dist/1000))/100 + (2000*(dist/1000))
    return reward

def setQuest(pid:int, quest:dict, amount:int, reward:float):
    sqlSafeQuery("""
                 INSERT INTO
                 active_quests(game_id, quest_id, cargo_id, destination, reward, amount)
                 VALUES(%(pid)s, %(qid)s, %(cid)s, %(dest)s, %(reward)s, %(amount)s)
                 """,{
                     'pid' : pid,
                     'qid' : quest["questId"],
                     'cid' : quest["cid"],
                     'dest' : quest["dest"],
                     'reward' : reward,
                     'amount' : amount
                },0)
    incItem(pid, quest["cid"], amount)

def checkQuest(pid, dest):
    complete = sqlQuery(f'SELECT reward, id FROM active_quests WHERE game_id = "{pid}" AND destination = "{dest}"')
    completed = 0
    reward = 0
    for i in complete:
        reward =+ i[0]
        completed += 1
    sqlQuery(f'DELETE FROM active_quests WHERE game_id = "{pid}" AND destination = "{dest}"')
    return completed, reward