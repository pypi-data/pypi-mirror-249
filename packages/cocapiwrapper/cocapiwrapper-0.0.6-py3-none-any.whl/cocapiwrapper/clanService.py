from cocapiwrapper.player import Player
from cocapiwrapper.clan import Clan
from cocapiwrapper.utils import loadplayersThreaded
class clanService:
    """
    This service class provides functionalities related to Clan operations in the Clash of Clans game.
    It uses the Clash of Clans API to fetch and process data related to clan members.
    """

    def getMembersOfClan(self, clan:Clan, loadPlayersData=False) -> list[Player]:
        """
        Retrieves a list of Player objects who are members of a specified clan.

        This method fetches clan member data using the clan tag. Optionally, it can also load detailed 
        player data using multithreading to speed up the process if `loadPlayersData` is set to True.

        Args:
            clan (str): the clan for which member information is requested.
            loadPlayersData (bool, optional): If True, player data for each clan member is loaded 
                                              using threads. Defaults to False.

        Returns:
            list[Player]: A list of Player objects representing the members of the clan.
                          The Player objects contain detailed information if `loadPlayersData` is True, 
                          otherwise, they contain basic information.
        """
        player_tags = [member.get("tag") for member in clan.getInfos().get("memberList", [])]
        if loadPlayersData :
            ## run thread 
            return loadplayersThreaded(player_tags)
        else :
            return [Player(tag, loadPlayersData) for tag in player_tags]