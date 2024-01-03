from cocapiwrapper.player import Player
from cocapiwrapper.clan import Clan
class playerService:
    def getClanOfPlayer(self, player:Player, loadPlayersData=False) -> Clan:
        return Clan(player.getClanTag())
    
