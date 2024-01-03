def usesDistantInfos( func ):
    """
        Decorator to specify that a methode uses distant informations from the api.
        the func will automatically load data if specified by this decorator.
    """
    def wrapper(*args, **kwargs):
        if args[0].global_info is None:
            args[0].loadDistantInfos()
        return func(*args, **kwargs)
    return wrapper

class distantSourceObject:
    def __init__(self,loadInfo:bool) -> None:
        self.global_info:dict = None
        if loadInfo:
            self.loadDistantInfos()

    def loadDistantInfos(self) -> None:
        pass

    @usesDistantInfos
    def getInfos(self) -> dict:
        """
        getInfos is the pure data of the object.
        Returns:
            dict: Json format return of the request to the distant api.
        
        Note: this function will load data if needed.
            
        """
        return self.global_info
    

