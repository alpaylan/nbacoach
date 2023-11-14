
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import os
import json
import requests

from Matchups import NbaMatchup, YahooMatchup
from NbaTeam import NbaTeam
from Player import Player
from YahooTeam import YahooTeam

from yfpy.query import YahooFantasySportsQuery

import nba_api.stats.static.teams as nba_api_teams
import nba_api.stats.static.players as nba_api_players





load_dotenv(dotenv_path=Path(__file__).parent / "auth" / ".env")
auth_dir = Path(__file__).parent / "auth"
data_dir = Path(__file__).parent / "db"

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
    |--> players.json
    |--> nba_teams.json
    |--> yahoo_teams.json
    |--> yahoo_matchups.json
    |--> nba_matchups.json


    """

    def __init__(self, update: bool = False) -> None:
        self.yahoo_query = YahooFantasySportsQuery(
            auth_dir,
            league_id="53545",
            game_id=428,
            game_code="nba",
            offline=False,
            all_output_as_json_str=False,
            consumer_key=os.environ["YFPY_CONSUMER_KEY"],
            consumer_secret=os.environ["YFPY_CONSUMER_SECRET"],
            browser_callback=True
        )
        self.yahoo_query.league_key = "428.l.53545"

        if update:
            self.update()
        
    def update(self) -> None:
        self.update_nba_teams()
        # self.update_nba_matchups()

    def update_nba_teams(self) -> None:
        allteams = nba_api_teams.get_teams()
        for team in allteams:
            team['players'] = []

        allplayers = self.yahoo_query.get_league_players(1000, 0)
        print(allplayers)
        for player in allplayers:
            for team in allteams:
                if team['abbreviation'] == player.editorial_team_abbr:
                    team['players'].append(player.name.full)

        for team in allteams:
            team['name'] = team['full_name']
            del team['full_name']
            del team['city']
            del team['state']
            del team['year_founded']
            del team['nickname']

        teams_dict = {}
        for team in allteams:
            teams_dict[team['abbreviation']] = team

        json.dump(allteams, open(data_dir / "nba_teams.json", "w"), indent=4, ensure_ascii=False)

    def update_nba_matchups(self) -> None:
        url = "https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2023/league/00_full_schedule.json"
        r = requests.get(url)
        raw_data = json.loads(r.text)

        all_games = []
        for month_data in raw_data['lscd']:
            month_data = month_data['mscd']
            for game_data in month_data['g']:
                time = game_data['etm']
                t1 = game_data['v']['ta']
                t2 = game_data['h']['ta']
                all_games.append({
                    "date": time,
                    "home_team": t1,
                    "away_team": t2,
                })
        all_games = sorted(
            all_games, key=lambda game: datetime.fromisoformat(game['date']))

        with open(data_dir / "nba_matchups.json", "w") as f:
            f.write(json.dumps(all_games, ensure_ascii=False, indent=4))

    def update_yahoo_matchups(self) -> None:
        def get_matches_by_week_online(week):
            try:
                matches = self.yahoo_query.get_league_matchups_by_week(week)
                matchups = list(map(lambda match: [match.teams[0].name.decode(
                    "utf-8"), match.teams[1].name.decode("utf-8")], matches))
                return matchups
            except:
                return []

        matchups = {}
        for week in range(1, 20):
            week_matchups = get_matches_by_week_online(week)
            if week_matchups is []:
                break
            matchups[week] = week_matchups

        json.dump(matchups, open(data_dir / "matchups.json", "w"),
                ensure_ascii=False)


        