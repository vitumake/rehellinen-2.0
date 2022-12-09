# main.py

#Hash salt
PYTHONHASHSEED = 0.69

from datetime import datetime
import hashlib

from db import sqlSafeQuery
from classes import Player, Cargo, Plane, Airport, Quest
from flask import json, Flask, request, session, redirect, url_for

def Response(status:int, content:object=None):
    return json.dumps({
        'status': status,
        'content': content
    }, default=lambda a: a.__dict__, sort_keys=True, indent=4)

reh = Flask(__name__)

#Secret shh...
reh.secret_key = b'590172990fb90cfc74f7c0298e436f1934d06b67443005c631d06613abc6f0f2'

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
            redirect(url_for('user'))          
        else: return Response(400, 'User not found')
    else: return Response(400, 'Already logged in')

@reh.route('/logout')
def logout():
    if 'uid' in session:
        session.pop('uid', None)
        redirect(url_for('/user'))
    else:
        return Response(404, 'Not logged in')

#User and 
@reh.route('/user')
def user():   
    if 'uid' in session:
        return Response(200, Player(session['uid'][0][0]))
    else:
        return Response(404, 'Not logged in')
if __name__ == '__main__':
    reh.run(use_reloader=True, host='127.0.0.1', port=3000)