from datetime import datetime
from pydantic import BaseModel

class Matchup(BaseModel):
    date: datetime
    home_team: str
    away_team: str

class NbaMatchup(Matchup):
    pass

class YahooMatchup(Matchup):
    week: int


