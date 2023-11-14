from nba_api.stats.endpoints import playercareerstats, commonplayerinfo


# Nikola Jokić
career = playercareerstats.PlayerCareerStats(player_id='203999') 

# pandas data frames (optional: pip install pandas)
career.get_data_frames()[0]

# json
career.get_json()

# dictionary
print(career.get_dict())