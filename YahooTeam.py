from datetime import datetime

class YahooTeam:
    last_updated: datetime
    id: int # PK
    name: str # PK
    players: list[str] # FK (Player)
