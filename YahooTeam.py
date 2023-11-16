from datetime import datetime
from collections import namedtuple

PlayerPosition = namedtuple("PlayerPosition", ["player", "position"])

class YahooTeam:
    last_updated: datetime
    id: int # PK
    name: str # PK
    players: list[PlayerPosition] # FK (Player, Position)
