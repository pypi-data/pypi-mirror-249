import cocapiwrapper.apiGetter as apiGetter
import cocapiwrapper.apiPost as apiPost
from cocapiwrapper.distantSourceObject import distantSourceObject,usesDistantInfos


class Player(distantSourceObject):
    def __init__(self, playerTag:str,loadInfo=True):
        """
           loadInfo: if true, the player infos will be loaded from the distant api.
           Note: datas will be loaded later if needed
        """
        self.playerTag = playerTag
        super().__init__(loadInfo)

    def loadDistantInfos(self) -> dict:
        self.global_info = apiGetter.getPlayerInfo(self.playerTag)

    @usesDistantInfos
    def getClanTag(self) -> str:
        clan_info = self.global_info.get("clan", {})
        clan_tag = clan_info.get("tag", "No Clan")
        return clan_tag

    def getTag(self) -> str:
        return self.playerTag
    
    def verify(self, playerToken):
        return apiPost.verifyPlayerToken(self.playerTag, playerToken)
    