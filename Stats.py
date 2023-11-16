from dataclasses import dataclass

def score(stats):
    if stats['FGA'] is None:
        return 0
    return stats['FG%'] * 10 + stats['FT%'] * 10 + stats['3PM'] * 3 + stats['PTS'] + stats['REB'] * 1.2 + stats['AST'] * 1.5 + stats['ST'] * 3 + stats['BLK'] * 3 - stats['TO'] * 1.5

@dataclass
class Stats:
    fga: float | None = None
    fgm: float | None = None
    fg_pct: float | None = None
    ftm: float | None = None
    fta: float | None = None
    ft_pct: float | None = None
    threes_made: float | None = None
    points: float | None = None
    rebounds: float | None = None
    assists: float | None = None
    steals: float | None = None
    blocks: float | None = None
    turnovers: float | None = None
    double_doubles: float | None = None

    @staticmethod
    def from_dict(stat_dict: dict):
        return Stats(
            fga=stat_dict.get("FGA", 0),
            fgm=stat_dict.get("FGM", 0),
            fg_pct=stat_dict.get("FG%", 0),
            ftm=stat_dict.get("FTM", 0),
            fta=stat_dict.get("FTA", 0),
            ft_pct=stat_dict.get("FT%", 0),
            threes_made=stat_dict.get("3PM", 0),
            points=stat_dict.get("PTS", 0),
            rebounds=stat_dict.get("REB", 0),
            assists=stat_dict.get("AST", 0),
            steals=stat_dict.get("ST", 0),
            blocks=stat_dict.get("BLK", 0),
            turnovers=stat_dict.get("TO", 0),
            double_doubles=stat_dict.get("DD", 0),
        )