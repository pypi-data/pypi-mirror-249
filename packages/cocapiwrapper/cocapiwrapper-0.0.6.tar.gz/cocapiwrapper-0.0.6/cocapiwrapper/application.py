import requests
from cocapiwrapper.requestsSettings import getAPIHeader, verifyTokenValidityApiUrl


def createSession():
    session = requests.Session()
    session.headers.update(getAPIHeader())
    return session

class application :
    session = None
    def createApplication() :
        print("creation of the application...")
        application.session = createSession()
        print("Token validation...")
        if not application.verifyTokenValidity() :
            application.destroyApplication()
            raise Exception("Invalid token :(")
        print("Valid token <3")

    def destroyApplication() :
        application.session.close()
        application.session = None

    def verifyTokenValidity():
        response = application.session.get(verifyTokenValidityApiUrl())
        if response.status_code == 200:
            return True
        else:
            return False
