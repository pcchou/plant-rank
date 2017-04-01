#!/usr/bin/python3
from pymongo import MongoClient
from json import dumps, loads
from datetime import datetime
from requests import get as GET, post as POST

mongo = MongoClient('localhost', 27017)
col = mongo['plant-rank']['users']
pcol = mongo['plant-rank']['problems']
scol = mongo['plant-rank']['submissions']
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
          "Referer": "http://neoj.sprout.tw/profile/129?owo",
          "Content-Type": "application/json"}

def prob_cat(pid, s=False):
    a = pcol.find({'uid': pid})
    if a.count():
        return a[0]['category'] == 1

    if s:
        return 0
    else:
        for c in (1, 2, 3):
            for p in loads(POST("http://neoj.sprout.tw/api/proset/{}/list".format(c),
                                data="{}", headers=HEADERS).text):
                pcol.update({'uid': int(p['problem']['uid'])},
                            {**p['problem'], 'category': c},
                            upsert=True)
        return prob_cat(pid, True)

def refresh(uid):
    profile = loads(POST("http://neoj.sprout.tw/api/user/{}/profile".format(uid),
                    data="{}", headers=HEADERS).text)
    statistic = loads(POST("http://neoj.sprout.tw/api/user/{}/statistic".format(uid),
                      data="{}", headers=HEADERS).text)

    tp = statistic['tried_problems']
    additional = {'problems': [int(x) for x in tp if tp[x]['result'] == 1],
                  'algoprobs': [x for x in tp
                                if tp[x]['result'] == 1 and prob_cat(int(x))],
                  'updated_at': int(datetime.today().timestamp())}
    if 'rate' not in profile:
        additional.update({'rate': 0})

    col.update({'uid': int(uid)},
               {**profile, **statistic, **additional},
               upsert=True)

def migrate_algoprobs(uid):
    q = col.find({'uid': int(uid)})[0]
    col.update({'uid': int(uid)},
               {**q, **{'algoprobs': [int(x) for x in q['tried_problems']
                                      if q['tried_problems'][x]['result'] == 1 and prob_cat(int(x)) == 1]}},
               upsert=True)

def last_submitters(count=87):
    cnt = loads(POST("http://neoj.sprout.tw/api/challenge/list",
                data=dumps({'offset': 0}), headers=HEADERS).text)['count']
    latest = loads(POST("http://neoj.sprout.tw/api/challenge/list",
                   data=dumps({'offset': cnt-100}), headers=HEADERS).text)

    for subm in latest['data'][-count:]:
        if subm and scol.find({'uid': subm['uid']}).count() == 0:
            scol.insert(subm)
            yield subm['submitter']['uid']

if __name__ == '__main__':
    for uid in set(last_submitters()):
        refresh(uid)
