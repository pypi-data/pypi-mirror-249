from threading import Thread
from cocapiwrapper.player import Player
def loadplayersThreaded(playersTagsList:list[str]) -> list[Player]:
    players = []
    threads = []

    # Create and start a thread for each player tag
    for tag in playersTagsList:
        thread = Thread(target=lambda: players.append(Player(tag,True)))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return players