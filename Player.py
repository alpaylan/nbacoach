from datetime import datetime
from Stats import Stats
from Positions import Position

class Player:
    name: str # PK
    nba_id: int 
    yahoo_id: int
    nba_team: str # FK (NbaTeam)
    yahoo_team: str | None # FK (YahooTeam)
    status: str | None
    stats: Stats
    current_position: Position | None
    eligible_positions: list[Position]
    active: bool