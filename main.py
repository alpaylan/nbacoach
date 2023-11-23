from Database import Database

db = Database(update=False, offline=True)

# for team in db.yahoo_teams.values():
#     print(team.name, team.manager, team.score(db))


jc = db.get_player_by_name("Jordan Clarkson")
kh = db.get_player_by_name("Kevin Huerter")
ct = db.get_player_by_name("Cam Thomas")
jc2 = db.get_player_by_name("John Collins")
bi = db.get_player_by_name("Brandon Ingram")

print(f"Jordan({jc.score()}) and Kevin({kh.score()}) vs Brandon({bi.score()})")
print(f"John({jc2.score()}) and Cam({ct.score()}) vs Brandon({bi.score()})")

print(ct.compare(bi))

db.simulate_trade({
    "t1": {
        "name": "Yozguard 66'ers",
        "players": ["Jordan Clarkson", "Kevin Huerter"]
    }, 
    "t2": {
        "name": "GoebenBreslau",
        "players": ["Brandon Ingram"]
    }
})

# for team in db.yahoo_teams.values():
#     print(team.name, team.manager, team.score(db))