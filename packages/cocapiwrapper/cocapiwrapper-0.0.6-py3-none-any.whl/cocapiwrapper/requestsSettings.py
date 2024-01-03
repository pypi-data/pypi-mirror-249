# Create a new file named TOKEN and add your token into it.
# To get yourself a token, go at : https://developer.clashofclans.com/, register and create a token.
import os

# function that is a wrapper to ensure token is loaded before use of the wrapped function
def usesToken( func ):
    def wrapper(*args, **kwargs):
        ensureToken()
        return func(*args, **kwargs)
    return wrapper


API_TOKEN = None

class tokenLoader:
    def fromFile(tokenfilepath:str) -> bool:
        return loadToken(tokenfilepath)
    
    def fromString(token:str) -> bool:
        global API_TOKEN
        API_TOKEN = token
        return True
    
    def fromEnv():
        global API_TOKEN
        API_TOKEN = os.environ.get("COC_API_TOKEN")
        return True
    

def loadToken(tokenfilepath:str) -> bool:
    global API_TOKEN
    if os.path.exists(tokenfilepath):
        with open(tokenfilepath, "r") as f:
            API_TOKEN = f.read().strip()
            print("Token loaded")
            f.close()
            return True
    else:
        return False

@usesToken
def getAPIHeader() :
    return {
    'Authorization': f'Bearer {API_TOKEN}',
    'Accept': 'application/json'
    }


def ensureToken() :
    if API_TOKEN is None:
        print("Error, no token found.")
        print("Please create a file named TOKEN and add your token into it.")
        print("To get yourself a token, go at : https://developer.clashofclans.com/, register and create a token.")
        print("setup your token using the 'loadToken(tokenfilepath:str)' function of this library")
        exit()


def getPlayerVerifyBody(playerToken:str) -> dict:
    return  {"token": str(playerToken)}
    

def getPlayerApiUrl(PLAYER_TAG) -> str:
    return f"https://api.clashofclans.com/v1/players/%23{PLAYER_TAG.replace('#', '')}"

def getClanApiUrl(CLANTAG) -> str:
    return f"https://api.clashofclans.com/v1/clans/%23{CLANTAG.replace('#', '')}"

def getVerifyPlayerTokenApiUrl(PLAYER_TAG) -> str:
    return f"https://api.clashofclans.com/v1/players/%23{PLAYER_TAG.replace('#', '')}/verifytoken"

def verifyTokenValidityApiUrl() -> str :
    return "https://api.clashofclans.com/v1/clans?name=bruh"
