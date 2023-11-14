from datetime import datetime

class NbaTeam:
    id: int # PK
    name: str # PK
    abbreviation: str # PK
    players: list[str] # FK (Player)
