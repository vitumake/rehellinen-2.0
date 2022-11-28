from datetime import datetime
import sys
import time
import random
from os import system, name

from Database.db import sqlQuery
from Database.location import getAirportName
# from Database.db import sqlQuery


# tyhjentää konsolin (vain kun run > edit configuration > execution > Emulate terminal in output console on valittu!)
def clear():
    # windows
    if name == 'nt':
        _ = system('cls')
    # mac ja linux
    else:
        _ = system('clear')


# funktio kirjoitus kone tyylille
def typewriter(message, speed=1):
    speed /= 10 #nopeus argumentti pidemmille tekstipätkille
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)


# funktio INTRO
def instructions():
    intro = '\nTervetuloa!'

    how = '\nKirjoita komento mitä haluat tehdä. Esimerkiksi jos haluat lentää kentästä toiseen niin kirjoita ' \
          '"Lennä". \nValinnat avaavat uusia valikoita. Toimi niissä samalla tavalla. '

    # aja 'intro' ja 'how' tekstit typewriter funktiota hyödyntäen
    typewriter(intro)
    time.sleep(2)
    clear()
    typewriter(how, 0.5)
    time.sleep(5)


# käyttöliittymä
# menu
def menu(name, location, money, fuel, time):
    clear()
    separator = ", "
    # Ohjeet
    print(f'\nRehellinen Ky, Kapteeni {name}')
    print(datetime.fromtimestamp(time))
    print(f'Sijainti: {separator.join(location)}')
    print(f'Rahaa: {money:,.2f} €'.replace(","," "))
    print(f'Polttoaineen määrä: {fuel} l')
    print('\n-Aika matkustaa jonnekkin? --> Lennä \n-Tarkista tilanteesi --> Pelaaja \n-Vieraile lentokentällä --> Kenttä\n\n')
    print('-Poistu pelistä --> Lopeta')
    # Komento
    command = input('\n--> ').lower()
    return command


# pelaaja (vaatii työtä)
def player(raha):
    clear()
    print('\n-Tarkastele aktiivisia tehtäviä --> Tehtävät\n-Palaa edelliseen valikkoon --> Palaa')
    print(f'Rahaa: {raha:,.2f} €'.replace(","," "))
    command = input('\n--> ').lower()
    return command



# kenttä (vaatii työtä)
def airport():
    clear()
    print('\n-Osta bensaa --> Bensa\n-Tarkastele tehtäviä --> Tehtävät\n-Mene kauppaan --> Kauppa\n-Mene varikolle --> Varikko\n-Palaa edelliseen valikkoon --> Palaa')
    command = input('\n--> ').lower()
    return command

def checkLogin():
    while not logged:
        login = player.doLogin(input('Nimi: '), input('Salasana: '))
    if  login == 0:
        print('Väärä salasana')
    else: 
        player.pid = login
        logged = True

def randomizeShop(val):
    list = []
    while val > 0:
        i = random.randint(1, sqlQuery('SELECT COUNT(*) FROM planes', 0)[0])
        if not i in list: 
            list.append(i)
            val -= 1
    return list

def printQuests(pid):
    qid = sqlQuery(f'SELECT quest_id, destination, reward, amount, cargo_id FROM active_quests WHERE game_id = "{pid}"')
    questList = [('TEHTÄVÄ', 'KUVAUS', 'KOHDE', 'PALKKIO', 'MÄÄRÄ')]
    for i in qid:
        quest = sqlQuery(f'SELECT quest_name, quest_description FROM quests WHERE id = "{i[0]}"', 0)
        cargo = sqlQuery(f'SELECT name FROM cargo WHERE id = "{i[4]}"', 0)[0]
        title = quest[0].replace('%cargo%', cargo).replace('%dest%', getAirportName(i[1]))
        desc = quest[1].replace('%cargo%', cargo).replace('%dest%', getAirportName(i[1]))
        questList.append((title, desc, i[1], i[2], i[3]))
    return questList
