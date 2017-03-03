from pymongo import MongoClient
from json import dumps, loads
from datetime import datetime
from requests import get as GET, post as POST

mongo = MongoClient('localhost', 27017)
col = mongo['plant-rank']['users']
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
          "Referer": "http://neoj.sprout.tw/profile/129?owo",
          "Content-Type": "application/json"}

def refresh(uid):
    profile = loads(POST("http://neoj.sprout.tw/api/user/{}/profile".format(uid), data="{}", headers=headers).text)
    statistic = loads(POST("http://neoj.sprout.tw/api/user/{}/statistic".format(uid), data="{}", headers=headers).text)
    tp = statistic['tried_problems']
    additional = {'problems': [int(x) for x in tp if tp[x]['result'] == 1],
                  'updated_at': int(datetime.today().timestamp())}
    if 'rate' not in profile:
        additional.update({'rate': 0})
    additional.update({'points': len(additional['problems'])})
    col.update({'uid': int(uid)},
               {**profile, **statistic, **additional},
               upsert=True)


def lastuids(count=16):
    cnt = loads(POST("http://neoj.sprout.tw/api/challenge/list", data=dumps({'offset': 0}), headers=headers).text)['count']
    last = loads(POST("http://neoj.sprout.tw/api/challenge/list", data=dumps({'offset': cnt-100}), headers=headers).text)
    return [x['submitter']['uid'] for x in last['data'] if x][::-1][:count]

if __name__ == '__main__':
    for uid in set(lastuids()):
        refresh(uid)
