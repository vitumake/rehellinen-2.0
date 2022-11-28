#quest.py

from random import randint, shuffle
from time import sleep
from Database import player
from Database.db import sqlQuery
from Game import framework

def eventRaffle(pid):
    #tapahtuma tyypit
    #1 satunnainen
    #2 riski
    #3 kunto
    if randint(1, 100) > 85:
        return
    else:
        for i in range(10):
            framework.clear()
            print(randint(1, 100))
            sleep(0.1)
        keno = randint(1, 100)
        sleep(1)
            
        quest = 0
        if keno > 70: quest = 1 
        elif keno < 10: quest = 2
        elif keno > 50 and keno < 60: quest = 3
        else: 
            framework.clear()
            print(':)')
            sleep(0.05)
            return
    
        questList = sqlQuery(f'SELECT title, description FROM events WHERE type = "{quest}"')
        shuffle(questList)
        framework.clear()
        if quest == 3: 
            print(questList[0][0])
            framework.typewriter(questList[0][1], 0.5)
            print('\n -1 Koneen kunto')
            player.incPlaneHealth(-1)
            sleep(1)
        if quest == 2 and player.getCargoRisk() != 0:
            keno = randint(1, 100)
            print(questList[0][0])
            framework.typewriter(questList[0][1], 0.5)
            if keno < 5:
                qid = player.getActiveQuests()[0][0]
                sqlQuery(f'DELETE FROM active_quests WHERE game_id = "{pid}" AND id = "{qid}"')
                print('\nJouduit jättämään toisen tehtävistäsi.')
                sleep(1)
            elif keno > 80 and player.getMoney() > 500:
                print('\nJouduit maksamaan sakkoja 300€')
                player.incMoney(-500)
                sleep(1)
            else:
                print('Sait puhuttua itsesi pälkähästä.')
                sleep(1)
        elif quest == 1:
            keno = randint(1, 100)
            print(questList[0][0])
            framework.typewriter(questList[0][1], 0.5)
            if keno > 70 and player.getMoney() > 100:
                print(f'Menetit {keno}€')
                player.incMoney(keno*-1)
                sleep(1)
            elif keno < 30:
                print(f'Löysit {keno}€')
                player.incMoney(keno)
                sleep(1)
            else:
                sleep(1)