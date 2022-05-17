# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import json
import time
import math
import calendar
import requests

request_url = "https://americas.api.riotgames.com/"
apikey = "RGAPI-d4154d38-8558-4243-bfe3-88d1c673f559" #Generate the latest APIKey at https://developer.riotgames.com/


class Summoner:
    def __init__(self, name, apikey = apikey):
        self.name = name
        self.requestNo = 10
        self.puuid = self.find_puuid()
        self.last10Matches = self.find_last_10_matches()
        self.matchesData = self.findMatchesData()
        self.KDA = self.find_average_KDA()
        self.position = self.find_position();
        self.winRate = self.find_win_rate();
        self.champ = self.most_played_champ();



    def find_puuid(self):
        response = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + self.name + "?api_key=" + apikey).json()
        puuid = response["puuid"]
        return puuid

    def find_last_10_matches(self):
        matches_url = request_url + "lol/match/v5/matches/by-puuid/" + self.puuid + "/ids?start=0&count=10&api_key=" + apikey
        matchList = requests.get(matches_url).json()
        return matchList

    def findMatchesData(self):
        summonerInfo = []
        for matchNum in range(10):
            KDA_URL = request_url + "lol/match/v5/matches/" + self.last10Matches[matchNum] + "?api_key=" + apikey
            response = requests.get(KDA_URL).json()
            matchInfo = response["info"]
            playerInfos = matchInfo["participants"]
            participantNum = 0


            # get the order of the summoner in the match
            for i in range(10):
                if (playerInfos[i]["summonerName"] == self.name):
                    participantNum = i
                    break

            summonerInfo.append(playerInfos[participantNum])

        return summonerInfo

    def find_average_KDA(self):
        totalKills = 0
        totalDeaths = 0
        totalAssists = 0

        for matchNum in range (10):
            summonerInfo = self.matchesData[matchNum]
            totalKills += summonerInfo["kills"]
            totalDeaths += summonerInfo["deaths"]
            totalAssists += summonerInfo["assists"]

        KDA = "KDA in recent 10 games: " + str(totalKills/10) + "/" + str(totalDeaths/10) + "/" + str(totalAssists/10)
        return KDA

    def find_position(self):
        positionList = []
        for matchNum in range (10):
            summonerInfo = self.matchesData[matchNum]
            if (summonerInfo["individualPosition"] != "Invalid"):
                positionList.append(summonerInfo["individualPosition"])

        position = max(positionList,key=positionList.count)
        return position;

    def find_win_rate(self):
        winNum = 0;
        for matchNum in range (10):
            summonerInfo = self.matchesData[matchNum]
            if (summonerInfo["win"]):
                winNum = winNum+1

        return str(winNum*10) + "%";

    def most_played_champ(self):
        chgampList = []
        for matchNum in range (10):
            summonerInfo = self.matchesData[matchNum]
            chgampList.append(summonerInfo["championName"])

        champ = max(chgampList,key=chgampList.count)
        return champ;

if __name__ == "__main__":
    #asenFever = LeagueApi (name='RROOBBIEWUUHQ')
    #print(asenFever.puuid)


    #Get the Summoner's Names from user input
    print("Enter the Teammates Information: ")
    name1 = input().split(' ')[0]
    name2 = input().split(' ')[0]
    name3 = input().split(' ')[0]
    name4 = input().split(' ')[0]
    name5 = input().split(' ')[0]
    #Get name Done!

    #Obtain data from Riot API by using the summoner's name
    # summoner0 = Summoner(name='Asenfever')
    summoner1 = Summoner(name = name2)
    # summoner2 = Summoner(name = name2)
    # summoner3 = Summoner(name = name3)
    # summoner4 = Summoner(name = name4)
    # summoner5 = Summoner(name = name5)



    #print(summoner1.last10Matches)
    print(summoner1.name + ":\n" +summoner1.KDA)
    print("Most played position:" + summoner1.position)
    print("Most played champ:" + summoner1.champ)
    print("Win rate:" + summoner1.winRate)
    # print(summoner2.name + ":\n" +summoner2.KDA)
    # print(summoner3.name + ":\n" +summoner3.KDA)
    # print(summoner4.name + ":\n" +summoner4.KDA)
    # print(summoner5.name + ":\n" +summoner5.KDA)
