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
        results = self.stats.compare(other.stats)
        return PlayerComparison(self, other, results["wins"], results["losses"])
    
class PlayerComparison:
    p1 : Player
    p2 : Player
    wins : list[tuple[str, float]]
    losses: list[tuple[str, float]]

    def __init__(self, p1, p2, wins, losses):
        self.p1 = p1
        self.p2 = p2
        self.wins = wins
        self.losses = losses

    def __str__(self):
        result = f"{self.p1.name} vs {self.p2.name}\n"
        result += f"Wins/Losses: {len(self.wins)}/{len(self.losses)}"
        result += "\nWins:"
        for stat, diff in self.wins:
            result += f"\n\t{stat}: {diff}"
        result += "\nLosses:"
        for stat, diff in self.losses:
            result += f"\n\t{stat}: {diff}"
        return result