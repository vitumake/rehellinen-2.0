#player.py
from random import randint
from datetime import datetime
from db import sqlQuery, sqlSafeQuery, sqlExists
from misc import findAirports

class Item():
    
    def __init__(self, id:int, name:str, isPlane:bool) -> None:
        self.id = id
        self.name = name
        self.isPlane = isPlane
        
    def inc(self, user:object):
        user.incItem(self)

class Quest():
    
    def __init__(self, quest:dict) -> None:
        
        self.id = quest['id']
        self.qid = quest['qid']
        self.reward = quest['reward']
        self.cargo = quest['cargo']
        self.dest = quest['dest']
        self.title = sqlQuery(f'SELECT quest_name FROM quests WHERE id = {quest["qid"]}')[0][0].replace('%cargo%', self.cargo.name).replace('%dest%', self.dest.name)
        self.desc = sqlQuery(f'SELECT quest_description FROM quests WHERE id = {quest["qid"]}')[0][0].replace('%cargo%', self.cargo.name).replace('%dest%', self.dest.name)
    
    def add(self, uid):
        
        sqlSafeQuery("""
            INSERT INTO
            active_quests(game_id, quest_id, cargo_id, destination, reward, amount)
            VALUES(%(pid)s, %(qid)s, %(cid)s, %(dest)s, %(reward)s, %(amount)s)
            """,{
                'pid' : uid.uid,
                'qid' : self.qid,
                'cid' : self.cargo.id,
                'dest' : self.dest.icao,
                'reward' : self.reward,
                'amount' : self.cargo.amount
        },0)
        self.cargo.add(uid)
    
    def complete(self):
        
        pid = sqlQuery(f'SELECT game_id FROM active_quests WHERE id = "{self.id}"', 0)[0]
        sqlQuery(f'DELETE FROM active_quests WHERE id="{self.id}"')
        self.cargo.inc(self.cargo.amount*-1)
        Player(pid).incMoney(self.reward)
        
class Plane(Item):
    
    def __init__(self, pid) -> None:
        
        plane = sqlQuery(f'SELECT * FROM planes WHERE id= "{pid}"', 1)[0]
        super().__init__(pid, plane[1], True)
        
        self.fuel_consumption = plane[2]
        self.max_fuel = plane[3]
        self.max_cargo = plane[4]
        self.max_health = plane[8]
        self.speed = plane[5]
        self.value = plane[6]
        self.volume = plane[7]
        
class Cargo(Item):
    
    def __init__(self, cid, amount) -> None:
        
        cargo = sqlQuery(f'SELECT * FROM cargo WHERE id= "{cid}"', 1)[0]
        super().__init__(cid, cargo[1], False)
    
        self.amount = amount
        self.weight = cargo[2]
        self.base_risk = cargo[3]
        self.base_value = cargo[5]        
        self.volume = cargo[4]
        self.max_qty = cargo[6]

class Country():
    
    def __init__(self, iso) -> None:
        
        country = sqlQuery(f'SELECT * FROM country WHERE iso_country="{iso}"')[0]
        
        self.iso = iso
        self.name = country[1]
        self.fuelprice = country[5]

class Airport():
    
    def __init__(self, icao:str) -> None:
        
        airport = sqlQuery(f'SELECT * FROM airport WHERE ident = "{icao}"')[0]
        
        self.icao = icao
        self.name = airport[3]
        self.pos = (airport[4], airport[5])
        self.type = airport[2]
        self.municipality = airport[10]
        self.country = Country(airport[8])

class Player():
        
    def __init__(self, uid:int) -> None:
        
        player = sqlQuery(f'SELECT * FROM game WHERE id = "{uid}"')[0]
        
        self.uid = uid
        self.name = player[2]
        self.money = player[4]
        self.fuel = player[3]
        self.health = player[8]
        self.time = player[9]
        self.last_event = None if player[6]=='NULL' else player[6]
        self.plane = Plane(player[5])
        self.location = Airport(player[1])
        self.inventory = []
        self.quests = []
        self.updateInv()
        self.updateQuests()

    def update(self):
        sqlSafeQuery("""
            UPDATE
            game
            SET
                location = %(location)s,
                screen_name = %(name)s,
                fuel = %(fuel)s,
                money = %(money)s, 
                active_plane = %(active_plane)s,
                last_event = %(lastEvent)s,
                plane_health = %(health)s,
                time = %(time)s
            WHERE
                id = %(id)s
        """,{
            'id': self.uid,
            'location': self.location.icao,
            'name': self.name,
            'fuel': self.fuel,
            'money': self.money,
            'active_plane': self.plane.id,
            'lastEvent': self.last_event,
            'health': self.health,
            'time': self.time
        })
        
    def updateInv(self):
        inv = sqlQuery(f'SELECT * FROM inventory WHERE pid = "{self.uid}"',)
        
        for i in inv:
            if i[3]: self.inventory.append(Plane(i[2]))
            else: self.inventory.append(Cargo(i[2], i[4]))
            
    def updateQuests(self):
        quests = sqlQuery(f'SELECT * FROM active_quests WHERE game_id = "{self.uid}"',)
        
        for i in quests:
            self.quests.append(Quest({
                'id': i[0],
                'qid': i[2],
                'cargo': Cargo(i[3], i[6]),
                'dest': Airport(i[4]),
                'reward': i[5]
            }))
    
    def incItem(self, item:object):
        
        iid = item.id
        isPlane = item.isPlane
        amount = item.amount
        
        if isPlane:
            exists = any(x for x in self.inventory if x.id == iid and x.isPlane)
            if amount >= 0 and not exists:
                sqlQuery(f'INSERT INTO inventory (pid, itemId, isPlane, amount) VALUES ({self.uid}, {iid}, "1", "1")')
            elif amount < 0 and exists:
                sqlQuery(f'DELETE FROM inventory WHERE pid = "{self.uid}" AND itemId = "{iid}" AND isPlane = "1"', 0)
        else:
            for i in self.inventory:
                if i.id == iid and not i.isPlane:
                    i.amount += amount
                    if i.amount < 1: sqlQuery(f'DELETE FROM inventory WHERE pid = "{self.uid}" AND itemId = "{iid}" AND isPlane = "0"', 0)
                    else: sqlQuery(f'UPDATE inventory SET amount="{i.amount}" WHERE pid = "{self.uid}" AND itemId = "{iid}" AND isPlane = "0"')
                    break
            else:
                if amount > 0: sqlQuery(f'INSERT INTO inventory (pid, itemId, isPlane, amount) VALUES ({self.uid}, {iid}, "0", {amount})')
                
        self.updateInv()
    
    def incMoney(self, val:int):
        self.money += val
        self.update()

    def incFuel(self, val:int):
        self.fuel += val
        self.update()
        
    def incHealth(self, val:int):
        self.health += val
        if self.health < 0: self.health = 0
        elif self.health > self.plane.max_health: self.health = self.plane.max_health
        self.update()
    
    def setActivePlane(self, pid:int):
        self.plane = Plane(pid) if sqlExists('planes', 'id', pid) else self.plane
        self.update()
        
    