# main.py

#Hash salt
PYTHONHASHSEED = 0.69

from datetime import datetime
import hashlib
import inspect
from db import sqlSafeQuery, sqlQuery, sqlExists
from classes import Player, Airport
from flask import json, Flask, request, session, redirect, url_for
from flask_cors import CORS

debug = True

def Response(status:int, content=None):
    if content==None:
        if status==400: content='Bad request'
    return json.dumps({
        'status': status,
        'content': content
    }, default=lambda a: a.__dict__, sort_keys=True, indent=4, ensure_ascii=False).encode('utf-8')

reh = Flask(__name__)
cors = CORS(reh, supports_credentials=True)
reh.config['CORS_HEADERS'] = 'Content-Type'
#Secret shh...
reh.secret_key = b'590172990fb90cfc74f7c0298e436f1934d06b67443005c631d06613abc6f0f2'

#devi funktio
if debug:
    @reh.route('/debug')
    def debug():
        return Response(200, Airport('EFHK').findAirports()[0].genQuests())

#Sessions
@reh.route('/login', methods=['POST'])
def login():
    if not 'uid' in session:
        login = sqlSafeQuery("""
            SELECT
                id
            FROM
                game
            WHERE
                screen_name = %(usr)s
            AND
                pass = %(pwd)s
        """, {
            'usr': request.form['name'],
            'pwd': hashlib.sha224(request.form['pwd'].encode('utf-8')).hexdigest()
        }, 1)
        if login:
            session['uid'] = login
            return redirect(url_for('user'))          
        else: return Response(400, 'User not found')
    else: return Response(400, 'Already logged in')

        
@reh.route('/logout')
def logout():
    if 'uid' in session:
        session.pop('uid', None)
        return redirect(url_for('/user'))
    else:
        return Response(400, 'Not logged in')

#User and methods
@reh.route('/user')
def user():
    if not 'uid' in session:
        return Response(400, 'Not logged in')
    print(session['uid'][0][0])
    pl = Player(session['uid'][0][0])
    action = request.args.get('a')
    val = request.args.get('val')
    print(action, val)
    
    #Check methods that cant be called with just values
    if(action=='setLocation'and sqlExists('airport', 'ident', val) and not val==None):
        pl.setLocation(Airport(val))
        return Response(200, pl) 
    elif action=='setLocation':
     return Response(400)
    
    #Call specified method if it exists
    if not action== None and hasattr(pl, action) and not val==None:
        val = float(val) if val.lstrip('-+.').isdigit() else 0
        getattr(pl, action)(val)
    #If value is not none print error
    elif not val==None:
        return Response(400)

    #By default user returns player object
    return Response(200, pl)
    
@reh.route('/load')
def load():
    data = sqlQuery('SELECT ident FROM airport WHERE type = "large_airport"')
    return Response(200, [Airport(i[0]) for i in data])
    
@reh.route('/airport/<icao>')
def airport(icao:str=None):
    action = request.args.get('a')
    val = request.args.get('val')
    print(action, val)
    if not sqlExists('airport', 'ident', icao): return Response(400)
    if action == None:
        return Response(200, Airport(icao)) 
    elif action == 'genQuest':
        return Response(200, Airport(icao).genQuest())
    elif action == 'genShop':
        return Response(200, Airport(icao).genShop())
    elif action == 'dist' and sqlExists('airport', 'ident', val):
        return Response(200, Airport(icao).dist(Airport(val).pos))
    return Response(400)

@reh.route('/quest', methods=["POST", "GET"])
def quests():
    if request.method == 'POST':
        req = json.load(request.get_json())
        return Response(200, req)
    else:
        pass

if __name__ == '__main__':
    reh.run(use_reloader=True, host='127.0.0.1', port=3000)
    
    