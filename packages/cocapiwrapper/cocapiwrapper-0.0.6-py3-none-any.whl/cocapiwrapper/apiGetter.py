import requests
from cocapiwrapper.application import application
from cocapiwrapper.requestsSettings import *


def getPlayerInfo(playerTag:str):
    response = application.session.get(getPlayerApiUrl(playerTag))
    if response.status_code == 200:
        player_info = response.json()
        return player_info
    else:
        print("Error, status code : ", response.status_code)


def getClanInfo(clanTag:str):
    response = application.session.get(getClanApiUrl(clanTag))
    if response.status_code == 200:
        clan_info = response.json()
        return clan_info
    else:
        print("Error, status code : ", response.status_code)

