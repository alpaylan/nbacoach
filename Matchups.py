from datetime import datetime
from dataclasses import dataclass

@dataclass
class Matchup:
    date: datetime
    home_team: str
    away_team: str

class NbaMatchup(Matchup):
    pass

class YahooMatchup(Matchup):
    week: int


