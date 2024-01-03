import requests
from cocapiwrapper.requestsSettings import *

def verifyPlayerToken(playerTag:str, playerToken:str):
    """
    verify from the distant api if the given token is valid for the given player.
    """
    response = requests.post(getVerifyPlayerTokenApiUrl(playerTag), headers=getAPIHeader(), json=getPlayerVerifyBody(playerToken))

    if response.json()["status"] == "ok":
        return True
    else:
        return False
