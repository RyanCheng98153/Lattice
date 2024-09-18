class NodeHelper:
    def __init__(self, _L:int, _W:int):
        self.L:int = _L
        self.W:int = _W
    
    def getCood(self, _id):
        return _id // self.W, _id % self.W
    
    def getId(self, _i, _j):
        return _i * self.W + _j
    
    def getRight(self, _id):
        i, j = self.getCood(_id)
        return self.getId( i, (j+1) % self.W ) 
    
    def getBottom(self, _id):
        i, j = self.getCood(_id)
        return self.getId( (i+1) % self.L, j )
    
    def getBottomRight(self, _id):
        i, j = self.getCood(_id)
        return self.getId( (i+1) % self.L, (j+1) % self.W )

    # reversed position
    def getRight(self, _id):
        i, j = self.getCood(_id)
        return self.getId( i, (j+1) % self.W ) 
    
    def getBottom(self, _id):
        i, j = self.getCood(_id)
        return self.getId( (i+1) % self.L, j )
    
    def getBottomRight(self, _id):
        i, j = self.getCood(_id)
        return self.getId( (i+1) % self.L, (j+1) % self.W )


class PrintHelper:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def getPrettyId( _id ):
        if _id == None:
            return "[   ]"
        elif _id < 10:
            return "[ " + str(_id) + " ]"
        elif _id < 100:
            return "[ " + str(_id) + "]"
        elif _id < 1000:
            return "["  + str(_id) + "]"
        else:
            return "[INF]"