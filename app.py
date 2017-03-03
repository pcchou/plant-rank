from bottle import app as bottleapp
from bottle import route, run, static_file, template
from pymongo import MongoClient
from json import dumps
from datetime import datetime
import sprout

mongo = MongoClient('localhost', 27017)
col = mongo['plant-rank']['users']

@route('/assets/<filename:path>')
def assets(filename):
    return static_file(filename, root='./assets/')

def readable(obj):
    obj['problems'] = ', '.join(map(str, sorted(obj['problems'])))
    obj['updated_at'] = datetime.fromtimestamp(
            obj['updated_at']).strftime('%Y/%m/%d %H:%M:%S')
    return obj

@route('/')
def index():
    board = list(map(readable, col.find({})))
    pointboard = sorted(board, key=lambda x: (x['points'], x['rate']), reverse=True)
    algoboard = sorted(board, key=lambda x: (x['rate'], x['points']), reverse=True)
    return template('index.html', locals())

@route('/users/<uid>')
def user(uid):
    board = map(readable, col.find({'uid': int(uid)}).limit(1))
    return template('user.html', locals())

@route('/users/<uid>', method="POST")
def refresh(uid):
    try:
        sprout.refresh(int(uid))
    except:
        return dumps({'status': False})
    else:
        return dumps({'status': True})

run(app=bottleapp(), port=8787, host="0.0.0.0", debug=False, server='meinheld')
