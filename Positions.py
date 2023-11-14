from enum import Enum

class Position(Enum):
    PG = "PG"
    SG = "SG"
    SF = "SF"
    PF = "PF"
    C = "C"
    G = "G"
    F = "F"
    UTIL = "UTIL"
    BN = "BN"

    def __str__(self):
        return self.value
    
    def playable(self):
        match = {
            Position.PG: [Position.PG, Position.G, Position.UTIL, Position.BN],
            Position.SG: [Position.SG, Position.G, Position.UTIL, Position.BN],
            Position.SF: [Position.SF, Position.F, Position.UTIL, Position.BN],
            Position.PF: [Position.PF, Position.F, Position.UTIL, Position.BN],
            Position.C: [Position.C, Position.UTIL, Position.BN],
        }
        return match[self]
    

    def gs():
        return [Position.PG, Position.SG, Position.G]
    
    def fs():
        return [Position.SF, Position.PF, Position.F]
    
    def os():
        return [Position.UTIL, Position.BN]
