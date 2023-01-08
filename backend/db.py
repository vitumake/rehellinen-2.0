#db.py

from mysql.connector import connect as con

#try:
#    with open('./pass.txt', 'r') as file:
#        dbData = [i.rstrip() for i in file]
#except FileNotFoundError:
#    exit('Ei pass.txt tiedostoa. Katso README.md')

#Sql yhteys muuttuja
conf = {
        'host' :'86.115.204.188',
        'port': 3306,
        'database': 'rehellinen',
        'user': 'koulu',
        'password': 'Koulu1-sql',
        'autocommit': True,
        'auth_plugin': 'mysql_native_password'
    }

#nopee funktio jolla voi kattoo löytyykö kannast jotai shittii
def sqlExists(table:str, row:str, val:str) -> bool:
    return sqlQuery(f'SELECT EXISTS(SELECT * FROM {table} WHERE {row} = "{val}")', 0)[0]

#viturandom rivi kannas
def sqlRandRow(table:str) -> list:
    return sqlQuery(f'SELECT * FROM {table} ORDER BY RAND() LIMIT 1')[0]


#Yksinkertainen funktio joka palauttaa haun tietokannasta listana.
def sqlQuery(query, fetchAll=1):
    cnx = con(**conf)
    kursori = cnx.cursor(buffered=True)
    kursori.execute(query)
    try: 
        if fetchAll == 1: return kursori.fetchall()
        else:
            cnx.close() 
            return kursori.fetchone()
    except:
        print(Exception)
        cnx.close() 
        return False

#Turvallisempi versio query funktiosta jos pelaaja voi suoraan puhua serverille
def sqlSafeQuery(query, args, fetchAll=1):
    cnx = con(**conf)
    kursori = cnx.cursor(buffered=True)
    kursori.execute(query, args)
    try:
        if fetchAll == 1: return kursori.fetchall()
        else: 
            cnx.close()
            return kursori.fetchone()
    except:
        print(Exception)
        cnx.close()
        return False