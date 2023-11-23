from pydantic import BaseModel, Field

class Stats(BaseModel):
    fga: float | None = Field(alias="FGA")
    fgm: float | None = Field(alias="FGM")
    fg_pct: float | None = Field(alias="FG%")
    ftm: float | None = Field(alias="FTM")
    fta: float | None = Field(alias="FTA")
    ft_pct: float | None = Field(alias="FT%")
    threes_made: float | None = Field(alias="3PM")
    points: float | None = Field(alias="PTS")
    rebounds: float | None = Field(alias="REB")
    assists: float | None = Field(alias="AST")
    steals: float | None = Field(alias="ST")
    blocks: float | None = Field(alias="BLK")
    turnovers: float | None = Field(alias="TO")
    double_doubles: float | None = Field(alias="DD")

    def score(self):
        if (
            self.fga is None
            or self.fgm is None
            or self.fg_pct is None
            or self.fta is None
            or self.ftm is None
            or self.ft_pct is None
            or self.threes_made is None
            or self.points is None
            or self.rebounds is None
            or self.assists is None
            or self.steals is None
            or self.blocks is None
            or self.turnovers is None
        ):
            return 0
        return (
            self.fg_pct * (2 * self.fgm - self.fga)
            + self.ft_pct * (2 * self.ftm - self.fta)
            + self.threes_made * 3
            + self.points * 0.8
            + self.rebounds * 1.2
            + self.assists * 1.5
            + self.steals * 3
            + self.blocks * 3
            - self.turnovers * 1.5
        )



        
class PlayerStats(BaseModel):
    season_avg: Stats
    season_total: Stats

    def score(self):
        return self.season_avg.score()

    def compare(self, other):
        results = { "wins": [], "losses": []}
        for stat in ["fg_pct", "ft_pct", "threes_made", "points", "rebounds", "assists", "steals", "blocks", "turnovers"]:
            if self.season_avg.__getattribute__(stat) > other.season_avg.__getattribute__(stat):
                results["wins"].append((stat, round(self.season_avg.__getattribute__(stat) - other.season_avg.__getattribute__(stat), 2)))
            elif self.season_avg.__getattribute__(stat) < other.season_avg.__getattribute__(stat):
                results["losses"].append((stat, round(other.season_avg.__getattribute__(stat) - self.season_avg.__getattribute__(stat), 2)))
        return results