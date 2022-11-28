# main.py

#Enviroment vars
PYTHONHASHSEED = 0.69

import time

from tabulate import tabulate

# Database moduuli
from Database import inventory, player, location
from Database.db import sqlQuery

# Game moduuli
from Game import quest, framework


# Startup

# Koodi joka ajetaan käynnistettäessä
#Jos haluat ohittaa kirjautumisen niin vaihda logged "True"
#Silloin koodi käyttää ensimmäistä testi pelaajaa
main = True
logged = False

framework.clear()
framework.typewriter('Tervetuloa!\n')

#Devaamista varten jotta voidaan ohittaa kirjautuminen
if logged: player.pid = 1

#Kirjautuminen
while not logged:
    doLogin = doReg = False
    command = input('(K)irjaudu / (U)usi pelaaja / (P)oistu pelistä\n> ').upper()
    if command == '':
        framework.clear()
        print('Väärä komento!')
    elif command[0] == 'K': doLogin = True
    elif command[0] == 'U': doReg = True
    elif command[0] == 'P': exit('Hyvästi')
    else:
        framework.clear()
        print('Väärä komento!')
    
    #Kirjautuminen
    while doLogin:
        framework.clear()
        print('Kirjaudu sisään')
        login = player.doLogin(input('Nimi: '), input('Salasana: '))
        if  login == 0:
            print('Väärä nimi tai salasana!')
        else:
            logged = True
            player.pid = login
            break
        command = input('Yritä uudelleen. Kyllä / Ei\n> ').upper()
        if command[0] != 'K': doLogin = False
        
    #Rekisteröityminen
    while doReg:
        framework.clear()
        print('Pelaajan nimen tulee olla enintään 10 merkkiä pitkä\n ja se voi sisältää vain numeroita sekä kirjaimia')
        print('Älä unohda salasanaasi sillä sitä ei voi palauttaa!')
        register = player.doRegister(input('Nimi: '), input('Salasana: '), input('Salasana uudestaan: '))
        if type(register) != int: print(register)
        else:
            player.pid = register
            logged = True
            inventory.incItem(register, 1, 1, 1)
            player.incMoney(10000)
            player.incFuel(player.getMaxFuel())
            framework.instructions()
            break
        command = input('Yritä uudelleen. Kyllä / Ei\n> ').upper()
        if command[0] != 'K': doReg = False

#Arpoo ekat koneen kauppaan
shopList = framework.randomizeShop(3)
    
# intro
#Kirjautumis skripti ajaa ohjeet uusille käyttäjille
#framework.instructions()
# Game loop
while main:

    #voitto ehto
    if player.getMoney() >= 100000000:
        main = False

    # kutsutaan käyttöliittymän eka valikko
    command = framework.menu(player.getName(), player.getLocAll(), player.getMoney(), player.getFuel(), player.getTime())
    # Pelaaja valitsee "pelaaja"

    if command == 'pelaaja':
        plMenu = True
        while plMenu:  
            action = framework.player(player.getMoney())
            if action == 'tehtävät':
                framework.clear()
                print(tabulate(framework.printQuests(player.pid)))
                input('\nPaina enter jatkaaksesi...')
            elif action == 'palaa':
                plMenu = False 
            else: print('Virheellinen komento!')

    # Pelaaja valitsee "kenttä"
    elif command == 'kenttä':
        airport = True
        while airport == True:
            command = ''
            command = framework.airport()

            if command == 'varikko':
                
                hangar = True
                while hangar:
                    framework.clear()
                    planeId = player.getPlane()
                    activePlane = location.getShopPlane(planeId)
                    print(
                        f'Tervetuloa varikolle!\n\n'
                        f'Tämän hetkinen koneesi on {activePlane[1]}\n'
                        f'Koneen kunto: {player.getPlaneHealth()} / {activePlane[8]}'
                    )
                    command = input(
                                f'-Tarkastele konetta --> Kone'
                                f'\n-Korjaa kone --> Huolto'
                                f'\n-Palaa päävalikkoon --> Palaa'    
                                f'\n--> '
                            ).lower()
                    if command == 'kone':
                        framework.clear()
                        print(
                            f'Aktiivinen kone\n\n'
                            f'Nimi: {activePlane[1]}'
                            f'\nBensa kulutus: {activePlane[2]} l/h'
                            f'\nBensa: {player.getFuel()} / {activePlane[3]} l'
                            f'\nRuuman painoraja: {player.getCargoWeight()} / {activePlane[4]} kg'
                            f'\nRuuman tilavuus: {player.getCargoVolume()} / {activePlane[7]} kg' 
                            f'\nNopeus: {activePlane[5]} km/h'
                            f'\nHinta: {activePlane[6] }€'
                            f'\nKunto: {player.getPlaneHealth()} / {activePlane[8]}'
                            f'\n\nOmistamat koneesi'
                        )
                        planeIds = sqlQuery(f'SELECT itemId FROM inventory WHERE pid = "{player.pid}" AND isPlane = "1"')
                        if not planeIds[0] == '':
                            orderNum = 0
                            selection = []
                            for i in planeIds:
                                orderNum += 1
                                selection.append(str(orderNum))
                                print(f'[{orderNum}] ' + sqlQuery(f'SELECT name FROM planes WHERE id = "{i[0]}"', 0)[0])
                            select = input(f'\n-Vaihda aktiivinen kone --> {selection[0]}-{selection[-1]}'
                                           f'\nJos haluat jatkaa samalla koneella paina Enter'
                                           f'\n\n--> ')
                            if select in selection:
                                if player.getCargoWeight() <= 0:
                                    framework.clear()
                                    newPlane = planeIds[int(select) - 1][0]
                                    player.setActivePlane(newPlane)
                                    player.incPlaneHealth(player.getPlaneHealth()*-1)
                                    player.incPlaneHealth(player.getPlaneMaxHealth())
                                    
                                    framework.typewriter('Hypätään uuteen koneeseen...', 0.5)
                                else:
                                    framework.clear()
                                    print('Ruuman täytyy olla tyhjä jos haluat vaihtaa konetta!')
                                    time.sleep(1)
                                
                            
                    elif command == 'huolto':
                        framework.clear()
                        if player.getPlaneHealth() == player.getPlaneMaxHealth():
                            framework.clear()
                            print('Koneesi on kunnossa.')
                            time.sleep(1)
                        else:
                            framework.clear()
                            fixAmount = player.getPlaneMaxHealth() - player.getPlaneHealth()
                            cost = round(fixAmount * (activePlane[6]*0.005), 2)
                            fix = input(
                                f'Koneen korjaus maksaa {cost}€'
                                f'\n Korjaa k/e'
                                f'\n--->'
                            ).lower()
                            if fix == 'k':
                                player.incPlaneHealth(fixAmount)
                    elif command == 'palaa': hangar = False
            if command == 'bensa':

                gas = True
                while gas == True:
                    framework.clear()
                    print("\nTervetuloa tankkaamaan!")

                    print(f"\nSinulla on tällä hetkellä {player.getMoney():,.2f} € ja {player.getFuel()}/{player.getMaxFuel():,} l polttoainetta".replace(","," "))

                    # emptyTank tarkoittaa paljonko tankissa on tilaa
                    emptyTank = player.getMaxFuel() - player.getFuel()
                    print(f"Tankissa on tilaa {emptyTank:.2f} l")
                    wantedfuel = input(
                        f'\nPaljonko bensaa (litroina) haluat ostaa? Bensan hinta on {location.getFuelPrice(player.getLocICAO())} €/l.'
                        f'\n-Osta bensaa --> "Haluttu määrä"'
                        f'\n-Osta tankki täyteen --> Max'
                        f'\n-Palaa päävalikkoon --> Palaa'
                        f'\n--> ').lower()

                    # jos käyttäjä syöttää 0, ostamisprosessi loppuu
                    if wantedfuel.isnumeric() == False and wantedfuel != "max":
                        gas = False

                    elif wantedfuel == 'max':
                        fuelPrice = (player.getMaxFuel() - player.getFuel()) * location.getFuelPrice(player.getLocICAO())
                        if fuelPrice <= player.getMoney():
                            player.incFuel(player.getMaxFuel() - player.getFuel())
                            player.incMoney(fuelPrice * -1)

                            framework.clear()

                            print(
                                f"\nKoneesi on tankattu. Sinulla on polttoainetta {player.getFuel()}/{player.getMaxFuel()}.")
                            time.sleep(2)
                            framework.clear()
                            print("\nKiitos käynnistä!")
                            time.sleep(1)

                            gas = False

                        else:
                            framework.clear()
                            print(f'\nSinulla ei ole tarpeeksi rahaa.')
                            time.sleep(2)

                    else:
                        fuelAmount = float(wantedfuel)
                        framework.clear()

                        # Bensan hinta on haluttu bensamäärä * bensan hinta
                        fuelPrice = fuelAmount * location.getFuelPrice(player.getLocICAO())
                        fuelConfirmation = input(
                        f"\nOletko varma, että haluat ostaa {fuelAmount} l bensaa? \nSe tulee maksamaan {fuelPrice}€ (k/e)\n\n-->")

                        if fuelConfirmation == "k":
                            # Jos tyhjä tila tankissa + haluttu bensamäärä alittaa tankin maksimin ja rahamäärä pysyy ylempänä
                            # ...kuin nolla
                            if emptyTank + fuelAmount <= player.getMaxFuel() and player.getMoney() - fuelPrice > 0:

                                player.incFuel(player.getFuel() + fuelAmount)
                                player.incMoney(fuelPrice * -1)
                                framework.clear()

                                print(f"\nKoneesi on tankattu. Sinulla on polttoainetta {player.getFuel()}/{player.getMaxFuel()}.")
                                time.sleep(2)
                                framework.clear()
                                print("\nKiitos käynnistä!")
                                time.sleep(1)

                                gas = False

                            else:
                                framework.clear()
                                print(
                                "\nEt voi ostaa näin paljon polttoainetta, koska tankissasi ei ole tilaa tai olet liian köyhä.")
                                time.sleep(3)

                        elif fuelConfirmation == "e":
                            airport = False


                        else:
                            framework.clear()
                            print("\nVäärä komento!")
                            time.sleep(2)

            elif command == 'tehtävät':
                questMenu = True
                while questMenu == True:
                    framework.clear()
                    separator = ", "
                    print(f'Sijaintisi on {separator.join(player.getLocAll())}')
                    print(f'Polttoaineen määrä: {player.getFuel()}')

                    questList = []
                    questTable = []
                    selection = []
                    select = 0
                    questList.append(quest.genQuest(1))
                    questList.append(quest.genQuest(1))
                    questList.append(quest.genQuest(2))
                    questList.append(quest.genQuest(3))
                    questList.append(quest.genQuest(5))
                    
                    for i in questList:
                        select += 1
                        questTable.append((f'[{str(select)}]', f'Otsikko - {i["title"]}', f'Kuvaus - {i["desc"]}', f'Rahti - {i["cargo"]}', f'Yksikkö hinta - {i["unitPrice"]} €', f'Etäisyys {i["dist"]} km'))
                        selection.append(select)
                        separator = '\n '
                    for i in questTable:
                        print(f'\n{separator.join(i)}')

                    command = input(
                    f'\nValitse tehtävät --> {selection[0]}-{selection[-1]}'
                    f'\nPalaa edelliseen valikkoon --> Palaa'
                    f'\n--> ').lower()

                    if command == 'palaa':
                        questMenu = False
                    elif command.isnumeric():
                        framework.clear()
                        if int(command) > selection[-1]: command = selection[-1]
                        selectedQuest = questList[int(command)-1]
                        print(
                        f'Koneen painoraja: {player.getCargoWeight()}/{player.getPlaneMaxWeight()}kg'
                        f'\nRooman tilavuus: {player.getCargoVolume()}/{player.getPlaneMaxVolume()}l\n'
                        )
                        maxQty = sqlQuery(f'SELECT max_qty FROM cargo WHERE id = "{selectedQuest["cid"]}"', 0)[0]
                        command = input(
                        f'\nValitse lastattavan rahdin määrä --> 1-{maxQty}'
                        f'\nPalaa edelliseen valikkoon --> Palaa'
                        f'\n--> ').lower()
                        reward = quest.calcReward(player.pid, selectedQuest, int(command)) if command.isnumeric() else 'pois'
                        if reward == -1:
                            framework.clear()
                            input('Et voi lastata kyseistä tavraa näin montaa yksikköä!\n\nPaina Enter jatkaaksesi...')
                        elif reward == -2:
                            framework.clear()
                            input('Ruuman tilavuus ei riitä!\n\nPaina Enter jatkaaksesi...')                           
                        elif reward == -3:
                            framework.clear()
                            input('Koneen painoraja ylittyy!\n\nPaina Enter jatkaaksesi...')
                        elif reward != 'pois':
                            framework.clear()
                            framework.typewriter(f'Lastataan {command}kpl {selectedQuest["cargo"]}...')
                            quest.setQuest(player.pid, selectedQuest, int(command), reward)                        
                    else:
                        framework.clear()
                        print("\nVäärä komento!")
                        time.sleep(2)

            elif command == 'kauppa':
                shop = True
                while shop:
                    framework.clear()
                    print(f'\nTervetuloa lentokonekauppaamme! Kuinka voimme olla avuksi?')
                    print(f'Valikoimamme kolme parasta konetta ovat:')

                    print(
                        f'\n1. {location.getShopPlane(shopList[0])[1]} hintaan: {location.getShopPlane(shopList[0])[6]:,} €'.replace(","," "))
                    print(
                        f'\n2. {location.getShopPlane(shopList[1])[1]} hintaan: {location.getShopPlane(shopList[1])[6]:,} €'.replace(","," "))
                    print(
                        f'\n3. {location.getShopPlane(shopList[2])[1]} hintaan: {location.getShopPlane(shopList[2])[6]:,} €'.replace(","," "))

                    print('\nKiinnostaako mikään näistä?')
                    command = input('-Valitse kone --> "Koneen numero"\n-Palaa edelliseen valikkoon --> Palaa\n\n---> ').lower()

                    if command == '1' or command == '1.':
                        framework.clear()
                        print(f'\n{location.getShopPlane(shopList[0])[1]}:')
                        print(f'Polttoaineen kulutus: {location.getShopPlane(shopList[0])[2]} l/h')
                        print(f'Polttoainesäiliön tilavuus: {location.getShopPlane(shopList[0])[3]:,} l'.replace(","," "))
                        print(f'Rahdin enimmäispaino: {location.getShopPlane(shopList[0])[4]:,} kg'.replace(","," "))
                        print(f'Rahtitilan koko: {location.getShopPlane(shopList[0])[7]:,} l'.replace(","," "))
                        print(f'Matkanopeus: {location.getShopPlane(shopList[0])[5]} km/h')
                        print(f'Maksimikunto: {location.getShopPlane(shopList[0])[8]}')
                        print(f'Hinta: {location.getShopPlane(shopList[0])[6]:,} €'.replace(","," "))

                        # tähän jatkoa
                        input('\nPaina enter palataksesi takaisin...')

                    elif command == '2' or command == '2.':
                        framework.clear()
                        print(f'\n{location.getShopPlane(shopList[1])[1]}:')
                        print(f'Polttoaineen kulutus: {location.getShopPlane(shopList[1])[2]} l/h')
                        print(f'Polttoainesäiliön tilavuus: {location.getShopPlane(shopList[1])[3]:,} l'.replace(","," "))
                        print(f'Rahdin enimmäispaino: {location.getShopPlane(shopList[1])[4]:,} kg'.replace(","," "))
                        print(f'Rahtitilan koko: {location.getShopPlane(shopList[1])[7]:,} l'.replace(","," "))
                        print(f'Matkanopeus: {location.getShopPlane(shopList[1])[5]} km/h')
                        print(f'Maksimikunto: {location.getShopPlane(shopList[1])[8]}')
                        print(f'Hinta: {location.getShopPlane(shopList[1])[6]:,} €'.replace(","," "))

                        # tähän jatkoa
                        input('\nPaina enter palataksesi takaisin...')

                    elif command == '3' or command == '3.':
                        framework.clear()
                        print(f'\n{location.getShopPlane(shopList[2])[1]}:')
                        print(f'Polttoaineen kulutus: {location.getShopPlane(shopList[2])[2]} l/h')
                        print(f'Polttoainesäiliön tilavuus: {location.getShopPlane(shopList[2])[3]:,} l'.replace(","," "))
                        print(f'Rahdin enimmäispaino: {location.getShopPlane(shopList[2])[4]:,} kg'.replace(","," "))
                        print(f'Rahtitilan koko: {location.getShopPlane(shopList[2])[7]:,} l'.replace(","," "))
                        print(f'Matkanopeus: {location.getShopPlane(shopList[2])[5]} km/h')
                        print(f'Maksimikunto: {location.getShopPlane(shopList[2])[8]}')
                        print(f'Hinta: {location.getShopPlane(shopList[2])[6]:,}€'.replace(","," "))

                        # tähän jatkoa
                        input('\nPaina enter palataksesi takaisin...')

                    elif command == 'palaa':
                        shop = False

                    else:
                        print('Väärä komento')
                        time.sleep(1)

            elif command == 'palaa':
                airport = False

            else:
                print('Väärä komento!')
                time.sleep(1)



    # Pelaaja valitsee "lennä"
    elif command == 'lennä':
        fly = True
        while fly:
            framework.clear()

            # hae pelaajan sijainti
            origin = player.getLocICAO() #(Testaamista varten pois. Korvaava --> origin = 'LFPG')
            # origin = 'LFPG'

            # hae lähimmät lentokentät
            fields = location.findAirports(origin, 15, (3, 3), (3, 3))
            
            #Lisätää hakuun kenttien etäisyys pelaajasta
            for i in fields:
                dist = round(location.icaoDistance(origin, i[0]), 2)
                fields[fields.index(i)] += (f'{dist}km',)

            #Sort funktio

            #Järjestetään kentät etäisyyden mukaan
            fields.sort(key=lambda fields: float(fields[3].replace('km', '')))
            

            # printtaa löydetyt lentokentät omille riveilleen
            separator = ", "
            print (f'\nSijaintisi on {separator.join(player.getLocAll())}')
            print(f'Polttoaineen määrä: {player.getFuel()}')
            print('\nSinua lähinnä olevat lentokentät:\n')
    
            fields.insert(0, ('ICAO', 'LENTOKENTTÄ', 'MAA', 'ETÄISYYS'))
            fields.insert(1, ('----', '-----------', '---', '--------'))
            print(tabulate(fields))

            print(f'\nVoit myös hakea tiettyä kohdetta ICAO:n perusteella. Muutoin käytä komentoa joka on haluamasi kohteen ICAO.')
            print(f'-Valitse kohde --> "ICAO"\n-Hae lentokenttää --> Hae\n-Palaa aloitusvalikkoon --> Palaa')
            action = input('\n--> ').upper()

            # Pelaaja hakee tiettyä kenttää
            if action == 'HAE':
                # Lentokentän haku
                framework.clear()
                separator = ", "
                print(f'\nSijaintisi on {separator.join(player.getLocAll())}')
                print(f'Polttoaineen määrä: {player.getFuel()}')
                search = input('\n-Hae lentokenttää (ICAO) ---> "ICAO"\n-Palaa edelliseen valikkoon --> Palaa\n\n--> ').upper()
                search_airport = location.getAirportName(search)

                # Jos pelaaja valitsee "palaa"
                if search == 'PALAA':
                    pass

                # Jos hakuehdoilla ei osumia
                elif search_airport == False:
                    framework.clear()
                    print(f'\nHaulla "{search}" ei löytynyt kenttää.')
                    time.sleep(2)

                else:
                    # Haku tarkentamaan pelaajan hakua
                    # Tarkasetetaan onko lentäminen mahdollista
                    check = player.checkFly(search)
                    separator = ", "
                    print(f'\nSijaintisi on {separator.join(player.getLocAll())}')
                    print(f'\nHaulla löytyi:\n{search}, {search_airport}\nJonka sijainti on {location.getAirportCountry(search)}.')
                    print(f'Polttoainetta tankissa: {player.getFuel()}')
                    print(f'Polltoainetta kuluu lennolla {check}l')
                    action = input(f'\nHaluatko lentää kyseiseen kohteeseen?\n-Kyllä\n-Ei\n\n--> ').lower()
                    
                    # Jos pelaaja haluaa lentää valittuun kohteeseen
                    if action == 'kyllä':
                        if player.getPlaneHealth() <= 0:
                            framework.clear()
                            input('Koneesei on epäkunnossa. Sinun tulee korjata se ensin!'
                                  '\n'
                                  '\nPaina enter jatkaaksesi...')
                        elif check <= player.getFuel():
                            player.doFly(search, check)
                            shopList = framework.randomizeShop(3)
                            fly = False
                        else:
                            framework.clear()
                            input('Sinulla ei ole riittävästi polttoainetta!\n\nPaina enter jatkaaksesi...')
                    # Jos pelaaja ei halua lentää valittuun kohteeseen
                    else:
                        pass

            # Pelaaja valitsee palaa
            elif action == 'PALAA':
                fly = False

            # Pelaaja valitsee kentän suoraan annetusta listasta
            else:
                # Tarkistetaan pelaajan komento
                search_airport = location.getAirportName(action)

                # Jos komento on väärä
                if search_airport == False:
                    framework.clear()
                    print(f'\n{action} ei löytynyt kenttää.')
                    time.sleep(2)

                # Jos komento on oikein
                else:
                    framework.clear()
                    #Tarkastetaan onko lentäminen mahdollista
                    check = player.checkFly(action)
                    separator = ", "
                    print(f'\nSijaintisi on {separator.join(player.getLocAll())}')
                    print(f'\nValittu:\n{action}, {search_airport}\nJonka sijainti on {location.getAirportCountry(action)}.')
                    print(f'Polttoainetta tankissa: {player.getFuel()}')
                    print(f'Polttoainetta kuluu lennolla {check}l')
                    command = input(f'\nHaluatko lentää kyseiseen kohteeseen?\n-Kyllä\n-Ei\n\n--> ').lower()
                
                    # Jos pelaaja haluaa lentää valittuun kohteeseen
                    if command == 'kyllä':
                        if player.getPlaneHealth() <= 0:
                            framework.clear()
                            input('Koneesei on epäkunnossa. Sinun tulee korjata se ensin!'
                                '\n'
                                '\nPaina enter jatkaaksesi...')
                        elif check <= player.getFuel():
                            player.doFly(action, check)
                            shopList = framework.randomizeShop(3)
                            fly = False
                        else:
                            framework.clear()
                            input('Sinulla ei ole riittävästi polttoainetta!\n\nPaina enter jatkaaksesi...')
                            command = 'ei'
                    # Jos pelaaja ei halua lentää valittuun kohteeseen
                    elif command == 'ei':
                        pass

                    # Jos pelaajan komento on väärä
                    else:
                        framework.clear()
                        print('Väärä komento!')
                        time.sleep(2)
    elif command == 'lopeta':
        exit('Hyvästi')




    # Pelaaja antaa väärän komennon
    # Palataan loopin alkuun
    else:
        framework.clear()
        print('Väärä komento!')
        time.sleep(1)

# End

framework.clear()
GG_1 = 'Onneksi olkoon! Voitit pelin.'
framework.typewriter(GG_1)
time.sleep(10)