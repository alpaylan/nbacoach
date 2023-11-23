from Player import Player
from pydantic import BaseModel
from functools import reduce

class PlayerPosition(BaseModel):
    name: str # FK (Player)
    position: str # FK (Position)

class YahooTeam(BaseModel):
    id: int # PK
    name: str # PK
    manager: str # PK
    roster: list[PlayerPosition] # FK (Player, Position)
    def score(self, db):
        score = 0
        for player in self.roster:
            player : Player = db.get_player_by_name(player.name)
            if player.current_position == "BN":
                continue
            score += player.score()
        return round(score, 2)
    