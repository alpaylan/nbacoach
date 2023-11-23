from Stats import PlayerStats
from Positions import Position
from pydantic import BaseModel

class Player(BaseModel):
    name: str # PK
    nba_id: int 
    yahoo_id: int
    nba_team: str # FK (NbaTeam)
    yahoo_team: str | None # FK (YahooTeam)
    status: str | None
    stats: PlayerStats
    current_position: Position | None
    eligible_positions: list[Position]
    active: bool

    def score(self):
        return self.stats.score()
    
    def compare(self, other):
        return self.stats.compare(other.stats)