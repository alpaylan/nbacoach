from datetime import datetime
from Stats import Stats
from Positions import Position

class Player:
    player_id: int # PK
    name: str # PK
    nba_team: str # FK (NbaTeam)
    yahoo_team: str | None # FK (YahooTeam)
    stats: Stats
    current_position: Position
    eligible_positions: list[Position] # FK (Position)
    active: bool