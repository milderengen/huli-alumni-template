import pandas as pd
import requests

# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def func():
    url = "https://odds.p.rapidapi.com/v4/sports/upcoming/odds"
    querystringUs = {"regions": "us", "oddsFormat": "decimal", "markets": "totals", "dateFormat": "iso"}
    querystringEu = {"regions": "eu", "oddsFormat": "decimal", "markets": "totals", "dateFormat": "iso"}
    querystringAu = {"regions": "au", "oddsFormat": "decimal", "markets": "totals", "dateFormat": "iso"}
    querystringUk = {"regions": "uk", "oddsFormat": "decimal", "markets": "totals", "dateFormat": "iso"}
    headers = {
        "X-RapidAPI-Key": "a5c6ab14f2mshf3bc51a8e156dccp170adfjsn06e7e2074939",
        "X-RapidAPI-Host": "odds.p.rapidapi.com"
    }
    responseUs = requests.request("GET", url, headers=headers, params=querystringUs)
    responseEu = requests.request("GET", url, headers=headers, params=querystringEu)
    responseAu = requests.request("GET", url, headers=headers, params=querystringAu)
    responseUk = requests.request("GET", url, headers=headers, params=querystringUk)
    if responseUs.status_code == 200:
        valuesUs = responseUs.json()
        valuesEu = responseEu.json()
        valuesAu = responseAu.json()
        valuesUk = responseUk.json()
        dfUs = pd.json_normalize(valuesUs)
        dfEu = pd.json_normalize(valuesEu)
        dfAu = pd.json_normalize(valuesAu)
        dfUk = pd.json_normalize(valuesUk)
        dfFinal = pd.concat([dfUs, dfEu, dfAu, dfUk], ignore_index=True)
        return dfFinal
    else:
        print("Error:", responseUs.status_code)

def bruh():
    df = func()
    for col,row in df.iterrows():
        sportsKey = []
        commence_time = []
        home = []
        away = []
        bookie = []
        lastUpdate = []
        over = []
        point = []
        under = []
        if len(row['bookmakers']) == 0:
            continue
        else:
            sportsKey.append(row['sport_key'])
            commence_time.append(row['commence_time'])
            home.append(row['home_team'])
            away.append(row['away_team'])
            for i in row['bookmakers']:
                bookie.append(i['key'])
                lastUpdate.append(i['last_update'])
                for k in i['markets']:
                    for l in range(len(k['outcomes'])):
                        point.append(k['outcomes'][l]['point'])
                        if k['outcomes'][l]['name'] == 'Over':
                            over.append(k['outcomes'][l]['price'])
                        else: under.append(k['outcomes'][l]['price'])
            for i, x in enumerate(over):
                for j, k in enumerate(under):
                    if point[i] == point[j]:
                        a = (1/float(over[i]))*100
                        b = (1/float(under[j]))*100
                        c = a+b
                        if c<99.5:
                            print("Sport: " + sportsKey[0])
                            print("Date: " + commence_time[0])
                            print("Home team: " + home[0])
                            print("Away team: " + away[0])
                            print("Bookie one: " + bookie[i] + " Odds: " + str(over[i]))
                            print("Bookie two: " + bookie[j] + " Odds: " + str(under[j]))
                            print("Last update on odds: " + lastUpdate[0])
                            print("%tage: " + str(c))
                            print("Points to bet on: " + str(point[i]))
                            print()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bruh()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/


