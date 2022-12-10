# main.py

#Hash salt
PYTHONHASHSEED = 0.69

from datetime import datetime
import hashlib
import inspect
from db import sqlSafeQuery
from classes import Player, Cargo, Plane, Airport, Quest, Country
from flask import json, Flask, request, session, redirect, url_for

debug = True

def Response(status:int, content=None):
    if content==None:
        if status==400: content='Bad request'
    return json.dumps({
        'status': status,
        'content': content
    }, default=lambda a: a.__dict__, sort_keys=True, indent=4)

reh = Flask(__name__)

#Secret shh...
reh.secret_key = b'590172990fb90cfc74f7c0298e436f1934d06b67443005c631d06613abc6f0f2'

#devi funktio
if debug:
    @reh.route('/debug')
    def debug():
        return Response(200, Country('Fi'))

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
    
    pl = Player(session['uid'][0][0])
    action = request.args.get('a')
    val = request.args.get('val')
    
    #Call specified method if it exists
    if not action== None and hasattr(pl, action) and not val==None:
        val = float(val) if val.lstrip('-+.').isdigit() else 0
        getattr(pl, action)(val)
    #If value is not none print error
    elif not val==None:
        return Response(400)

    #By default user returns player object
    return Response(200, pl)
    
if __name__ == '__main__':
    reh.run(use_reloader=True, host='127.0.0.1', port=3000)