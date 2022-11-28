#inventory.py

from webbrowser import get
from Database.db import sqlSafeQuery, sqlQuery

def getItem(pid:int, itemId:int, isPlane:bool=0) -> int:
    """Palauttaa tavaran määrän

    Args:
        pid (int): pelaajan id
        itemId (int): tavaran id (lentokoneen id jos lentokone)
        isPlane (int): onko kyseessä lentokone. Defaults to 0

    Returns:
        int: tavaran määrä
    """    
    if isPlane: return sqlQuery(f'SELECT EXISTS(SELECT * FROM inventory WHERE pid = "{pid}" AND itemId = "{itemId}" AND isPlane = "1")', 0)[0]
    else: 
        try:
            val = sqlQuery(f'SELECT amount FROM inventory WHERE itemId = "{itemId}" AND isPlane = "{isPlane}"', 0)[0]
        except TypeError:
            val = 0
    return val

def incItem(pid:int, itemId:int, amount:int, isPlane:int=0) -> any:
    """Lisää pelaajan tavaraluetteloon tavaroita tai lentokoneita

    Args:
        pid (int): pelaajan id
        itemId (int): tavaran id (koneen id jos kyseessä kone)
        amount (int): lisättävän tavaran määrä (amount > 0 lisää koneen amount < 0 poistaa koneen)
        isPlane (bool, optional): onko kyseessä lentokone. Defaults to 0.

    Returns:
        bool: palauttaa epätosi jos tavaraa ei voi lisätä muuten tosi
    """    
    #Jos kyseessä lentokone
    if isPlane >= 1:
        #Jos luku on positiivinen lisätään kone muuten poistetaan
        if amount >= 1:
            #Jos lisättävä kone on jo pelaajalla palauta vikakoodi
            if getItem(pid, itemId, 1) > 0: return 0
            else: sqlQuery(f'INSERT INTO inventory (pid, itemId, isPlane, amount) VALUES ({pid}, {itemId}, "1", "1")')
        else: 
            #Jos pelaajalla ei ole konetta ei sitä voi vähentää
            if getItem(pid, itemId, 1): return 0
            else: sqlQuery(f'DELETE FROM inventory WHERE pid = "{pid}" AND itemId = "{itemId}" AND isPlane = "1"')
    else:
        if amount >= 0:
            #Jos pelaajalla ei ole kyseistä tavaraa voimme lisätä sen suoraan taulukkoon
            if not getItem(pid, itemId, 0): sqlQuery(f'INSERT INTO inventory (pid, itemId, isPlane, amount) VALUES ({pid}, {itemId}, 0, "{amount}")')
            #Jos pelaajalla on jo tavara täytyy se lisätä jo pelaajalla olevaan määrään
            else: sqlQuery(f'UPDATE inventory SET amount = amount + "{amount}" WHERE pid = "{pid}" AND itemID = "{itemId}"')
        else:
            #Jos pelaajalla ei ole kyseistä tavaraa ei sitä voi vähentää
            if not getItem(pid, itemId, 0): return 0
            #Jos pelaajalla on tavara täytyy se vähentää nykyisestä määrästä
            else: 
                currVal = getItem(pid, itemId, 0)
                #Jos määrä on 0 tai pienempi voimme poistaa arvon taulusta
                if currVal + amount <= 0: sqlQuery(f'DELETE FROM inventory WHERE pid = "{pid}" AND itemId = "{itemId}" AND isPlane = "0"')
                #Muuten päivitetään määrä
                else: sqlQuery(f'UPDATE inventory SET amount = amount + "{amount}" WHERE pid = "{pid}" AND itemID = "{itemId}"')
    return 1