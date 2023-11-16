from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
import os
import json
import requests

from Matchups import NbaMatchup, YahooMatchup
from NbaTeam import NbaTeam
from Player import Player
from YahooTeam import YahooTeam

import nba_api.stats.endpoints as ep
from yfpy.query import YahooFantasySportsQuery

import nba_api.stats.static.teams as nba_api_teams
import nba_api.stats.static.players as nba_api_players

GAME_ID = 428
load_dotenv(dotenv_path=Path(__file__).parent / "auth" / ".env")
auth_dir = Path(__file__).parent / "auth"
data_dir = Path(__file__).parent / "db"


PLAYER_NAME_FIXER = {
    "OG Anunoby": "O.G. Anunoby",
    "P.J. Washington Jr.": "P.J. Washington",
    "Xavier Tillman Sr.": "Xavier Tillman",
    "Patrick Baldwin Jr.": "Patrick Baldwin",
    "A.J. Green": "AJ Green",
    "GG Jackson II": "GG Jackson",
    "Craig Porter Jr.": "Craig Porter",
}

class Database:
    yahoo_query: YahooFantasySportsQuery
    last_updated: datetime
    players: list[Player]
    nba_teams: list[NbaTeam]
    yahoo_teams: list[YahooTeam]
    yahoo_matchups: list[YahooMatchup]
    nba_matchups: list[NbaMatchup]

    """
    DB Schema

    db
    |--> metadata.json
        |--> last_updated
    |
    |--> nba_teams.json
    |--> nba_matchups.json
    |--> yahoo_matchups.json
    |--> yahoo_teams.json
    |--> players.json


    """

    def __init__(self, update: bool = False) -> None:
        self.yahoo_query = YahooFantasySportsQuery(
            auth_dir,
            league_id="53545",
            game_id=GAME_ID,
            game_code="nba",
            offline=False,
            all_output_as_json_str=False,
            consumer_key=os.environ["YFPY_CONSUMER_KEY"],
            consumer_secret=os.environ["YFPY_CONSUMER_SECRET"],
            browser_callback=True,
        )
        self.yahoo_query.league_key = "428.l.53545"

        if update:
            self.update()

    def update(self) -> None:
        # self.update_nba_teams()
        # self.update_nba_matchups()
        # self.update_yahoo_matchups()
        # self.update_yahoo_teams()
        self.update_players()

    def update_nba_teams(self) -> None:
        allteams = nba_api_teams.get_teams()
        for team in allteams:
            team["players"] = []

        allplayers = self.yahoo_query.get_league_players(1000, 0)
        for player in allplayers:
            for team in allteams:
                if team["abbreviation"] == player.editorial_team_abbr:
                    team["players"].append(player.name.full)

        for team in allteams:
            team["name"] = team["full_name"]
            del team["full_name"]
            del team["city"]
            del team["state"]
            del team["year_founded"]
            del team["nickname"]

        teams_dict = {}
        for team in allteams:
            teams_dict[team["abbreviation"]] = team

        json.dump(
            teams_dict,
            open(data_dir / "nba_teams.json", "w"),
            indent=4,
            ensure_ascii=False,
        )

    def update_nba_matchups(self) -> None:
        url = "https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2023/league/00_full_schedule.json"
        r = requests.get(url)
        raw_data = json.loads(r.text)

        all_games = []
        for month_data in raw_data["lscd"]:
            month_data = month_data["mscd"]
            for game_data in month_data["g"]:
                time = game_data["etm"]
                t1 = game_data["v"]["ta"]
                t2 = game_data["h"]["ta"]
                all_games.append(
                    {
                        "date": time,
                        "home_team": t1,
                        "away_team": t2,
                    }
                )
        all_games = sorted(
            all_games, key=lambda game: datetime.fromisoformat(game["date"])
        )

        with open(data_dir / "nba_matchups.json", "w") as f:
            f.write(json.dumps(all_games, ensure_ascii=False, indent=4))

    def update_yahoo_matchups(self) -> None:
        def get_matches_by_week_online(week):
            try:
                matches = self.yahoo_query.get_league_matchups_by_week(week)
                matchups = list(
                    map(
                        lambda match: [
                            match.teams[0].name.decode("utf-8"),
                            match.teams[1].name.decode("utf-8"),
                        ],
                        matches,
                    )
                )
                return matchups
            except:
                return []

        matchups = []
        for week in range(1, 20):
            for matchup in get_matches_by_week_online(week):
                matchups.append(
                    {"week": week, "home_team": matchup[0], "away_team": matchup[1]}
                )

        json.dump(
            matchups,
            open(data_dir / "yahoo_matchups.json", "w"),
            indent=4,
            ensure_ascii=False,
        )

    def update_yahoo_teams(self) -> None:
        def get_week(day: datetime):
            weeks = self.yahoo_query.get_game_weeks_by_game_id(GAME_ID)
            for week in weeks:
                week_start = datetime.fromisoformat(week.start)
                week_end = datetime.fromisoformat(week.end)
                if week_start <= day <= week_end:
                    return week.week
            return 0

        def next_week():
            today = datetime.today()
            next_tuesday = today + timedelta((1 - today.weekday()) % 7)
            return get_week(next_tuesday)

        yahoo_teams = self.yahoo_query.get_league_teams()
        yahoo_teams = {
            team.name.decode("utf-8"): {
                "name": team.name.decode("utf-8"),
                "id": team.team_id,
                "roster": list(
                    map(
                        lambda player: {
                            "name": player.name.full,
                            "position": player.selected_position.position,
                        },
                        self.yahoo_query.get_team_roster_by_week(
                            team.team_id, next_week()
                        ).players,
                    )
                ),
            }
            for team in yahoo_teams
        }

        json.dump(
            yahoo_teams,
            open(data_dir / "yahoo_teams.json", "w"),
            indent=4,
            ensure_ascii=False,
        )

    def update_players(self) -> None:
        # Note: This update requires Yahoo Teams to be updated.
        def yahoo_team_roster_to_player_positions():
            yahoo_teams = json.load(open(data_dir / "yahoo_teams.json"))
            player_positions = {}
            for team in yahoo_teams:
                for player in yahoo_teams[team]["roster"]:
                    player_positions[player["name"]] = {
                        "team": team,
                        "position": player["position"],
                    }
            return player_positions

        def stats_not_found():
            return {
                "FGM": None,
                "FGA": None,
                "FG%": None,
                "FTM": None,
                "FTA": None,
                "FT%": None,
                "3PM": None,
                "PTS": None,
                "REB": None,
                "AST": None,
                "ST": None,
                "BLK": None,
                "TO": None,
                "DD": None,
            }

        def get_player_stats(player_id, mode="PerGame", season="2023-24"):
            pergamestats = ep.PlayerCareerStats(
                player_id=str(player_id), per_mode36=mode
            )

            pergamestats = pergamestats.get_normalized_dict()

            try:
                last_season = pergamestats["SeasonTotalsRegularSeason"][-1]
                if last_season["SEASON_ID"] == season:
                    return {
                        "FGM": last_season["FGM"],
                        "FGA": last_season["FGA"],
                        "FG%": last_season["FG_PCT"],
                        "FTM": last_season["FTM"],
                        "FTA": last_season["FTA"],
                        "FT%": last_season["FT_PCT"],
                        "3PM": last_season["FG3M"],
                        "PTS": last_season["PTS"],
                        "REB": last_season["REB"],
                        "AST": last_season["AST"],
                        "ST": last_season["STL"],
                        "BLK": last_season["BLK"],
                        "TO": last_season["TOV"],
                        "DD": None,
                    }
                else:
                    return stats_not_found()
            except:
                return stats_not_found()

        player_positions = yahoo_team_roster_to_player_positions()
        allplayers = self.yahoo_query.get_league_players(1000, 0)

        if not os.path.exists(data_dir / "players.json"):
            players_dict = {}
        else:    
            players_dict = json.load(open(data_dir / "players.json"))

        for player in allplayers:
            print(player.status_full)
            if player.name.full in players_dict:
                continue
            print(player.name)

            name = PLAYER_NAME_FIXER[player.name.full] if player.name.full in PLAYER_NAME_FIXER else player.name.full

            full_name_search = nba_api_players.find_players_by_full_name(
                name
            )
            if len(full_name_search) == 0:
                nba_player = {
                    "id": -1,
                    "is_active": False,
                }
            else:
                nba_player = full_name_search[0]

            players_dict[player.name.full] = {
                "updated": datetime.now().isoformat(),
                "name": player.name.full,
                "nba_id": nba_player["id"],
                "yahoo_id": player.player_id,
                "nba_team": player.editorial_team_abbr,
                "status": player.status_full if player.status_full else None,
                "yahoo_team": player_positions.get(player.name.full, {}).get("team"),
                "stats": {
                    "season_avg": get_player_stats(nba_player["id"], "PerGame"),
                    "season_total": get_player_stats(nba_player["id"], "Totals"),
                },
                "current_position": player_positions.get(player.name.full, {}).get(
                    "position"
                ),
                "eligible_positions": player.display_position.split(","),
                "active": nba_player["is_active"],
            }
            print(players_dict[player.name.full])

            json.dump(
                players_dict,
                open(data_dir / "players.json", "w"),
                indent=4,
                ensure_ascii=False,
            )
