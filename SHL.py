from SHLConnect import SHLConnect
import pandas as pd
import json
import sqlite3

SHL = SHLConnect()

seasons = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']
loads = {
    1: 'season',
    2: 'stats',
    3: 'team'
}

def do_loadseason():
    method = 'season'
    for season in seasons:
        request = SHL.do_get(f'/seasons/{season}/games')
        if request.status_code == 200:
            d = json.dumps(request.json())
            data = json.loads(d)
            for element in data:
                element.pop('tv_channels', None)
            df = pd.DataFrame(data)
            add_to_database(df, method)
            print(f"{method} for: {season} completed loading")
        elif request.status_code == 403:
            print(f"{method} for: {season} access denied")
        elif request.status_code == 404:
            print(f"{method} for: {season} not found")
        else:
            print(f"{method} for: {season} failed loading")


def do_loadstatsplayer(method, type):
    for season in seasons:
        request = SHL.do_get(f'/seasons/{season}/statistics/{type}')
        if request.status_code == 200:
            d = json.dumps(request.json())
            data = json.loads(d)
            for element in data:
                temp = element.pop('info', None)
                element.update(temp)
                element.pop('team', None)
                temp = element.pop('teams', None)
                i = 0
                for t in temp:
                    element[f"teams{i}"] = t
                    i += 1
                element["season"] = season
            df = pd.DataFrame(data)
            add_to_database(df, method)
            print(f"{method} for: {season} completed loading")
        elif request.status_code == 403:
            print(f"{method} for: {season} access denied")
        elif request.status_code == 404:
            print(f"{method} for: {season} not found")
        else:
            print(f"{method} for: {season} failed loading")

def do_loadstatsteam():
    method = 'teamstats'
    for season in seasons:
        request = SHL.do_get(f'/seasons/{season}/statistics/teams/standings')
        if request.status_code == 200:
            d = json.dumps(request.json())
            data = json.loads(d)
            for element in data:
                element.pop('team', None)
            df = pd.DataFrame(data)
            add_to_database(df, method)
            print(f"{method} for: {season} completed loading")
        elif request.status_code == 403:
            print(f"{method} for: {season} access denied")
        elif request.status_code == 404:
            print(f"{method} for: {season} not found")
        else:
            print(f"{method} for: {season} failed loading")


def add_to_database(df, method):
    conn = sqlite3.connect("hockey.db")
    try:
        df.to_sql(f"{method}", con=conn, if_exists='append', index=False)
    except:
        temp = pd.read_sql(f"select * from {method}", conn)
        df2 = pd.concat([temp, df])
        df2.to_sql(f"{method}", con=conn, if_exists='replace', index=False)


def do_load():
    for i in loads:
        if loads.get(i) == 'season':
            do_loadseason()
        elif loads.get(i) == 'stats':
            do_loadstatsplayer('playerstats', 'players')
            do_loadstatsplayer('goalkeeperstats', 'goalkeepers')
            do_loadstatsteam()
        elif loads.get(i) == 'team':
            print("team")
    print("Load is completed")


do_load()
