from tinydb import TinyDB, Query

class InterfaceDb():
    def addEntry(self, entry) -> int:
        pass
    
    def save(self) ->None:
        pass

    def removeEntry(self) ->None:
        pass

    def getEntryByName(self):
        pass

    def getEntryById(self):
        pass

    #... all queries?


class BlocDb():
    def save(self):
        pass