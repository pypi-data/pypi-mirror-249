import cocapiwrapper.apiGetter as apiGetter
from cocapiwrapper.distantSourceObject import distantSourceObject,usesDistantInfos

class Clan(distantSourceObject) : 
    def __init__(self, clan_tag:str,loadInfo=True):
        self.clan_tag = clan_tag
        super().__init__(loadInfo)

    def loadDistantInfos(self) -> dict:
        self.global_info = apiGetter.getClanInfo(self.clan_tag)

    @usesDistantInfos
    def getMembersTags(self) -> list[str]:
        playerTaglist: str = []
        for member in self.clan_info.get("memberList", []) :
            playerTaglist.append(member.get("tag"))
        return playerTaglist
