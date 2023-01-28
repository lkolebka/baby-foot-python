import psycopg2
from openpyxl import load_workbook

# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="babyfoot3",
    user="postgres",
    password="519173"
)

# Create a cursor
cur = conn.cursor()

# Load the workbook
wb = load_workbook('data.xlsx')

# Select the active sheet
ws = wb.active

# Iterate through the rows of the sheet

for row in ws.rows:

    # checking if the rows are not null
    if all(cell.value == None for cell in row):
        break
    date = row[0].value
    player1_name = row[1].value
    player2_name = row[2].value
    team1_score = row[3].value
    player3_name = row[4].value
    player4_name = row[5].value
    team2_score = row[6].value


    # Check if the player name is not empty
    if player1_name:
      # Check if the player already exists in the Players table
      cur.execute("SELECT id FROM players WHERE name=%s", (player1_name,))
      player1_id = cur.fetchone()
      if player1_id is None:
        # If the player does not exist, insert them into the players table with a unique id
        cur.execute("SELECT nextval('players_id_seq')")
        id = cur.fetchone()[0]
        cur.execute("INSERT INTO players (id, name) VALUES (%s, %s)", (id, player1_name))
        player1_id = id
      else:
        # If the player already exists, retrieve their id
        player1_id = player1_id[0]
        


    
    # Check if the player2 name is not empty
      if player2_name:
        # Check if the player already exists in the Players table
        cur.execute("SELECT id FROM players WHERE name=%s", (player2_name,))
        player2_id = cur.fetchone()
        if player2_id is None:
          # If the player does not exist, insert them into the players table with a unique id
          cur.execute("SELECT nextval('players_id_seq')")
          id = cur.fetchone()[0]
          cur.execute("INSERT INTO players (id, name) VALUES (%s, %s)", (id, player2_name))
          player2_id = id
        else:
          # If the player already exists, retrieve their id
          player2_id = player2_id[0]




    # Check if the player3 name is not empty
    if player3_name:
      # Check if the player already exists in the Players table
      cur.execute("SELECT id FROM players WHERE name=%s", (player3_name,))
      player3_id = cur.fetchone()
      if player3_id is None:
        # If the player does not exist, insert them into the players table with a unique id
        cur.execute("SELECT nextval('players_id_seq')")
        id = cur.fetchone()[0]
        cur.execute("INSERT INTO players (id, name) VALUES (%s, %s)", (id, player3_name))
        player3_id = id
      else:
        # If the player already exists, retrieve their id
        player3_id = player3_id[0]



    # Check if the player4 name is not empty
    if player4_name:
      # Check if the player already exists in the Players table
      cur.execute("SELECT id FROM players WHERE name=%s", (player4_name,))
      player4_id = cur.fetchone()
      if player4_id is None:
        # If the player does not exist, insert them into the players table with a unique id
        cur.execute("SELECT nextval('players_id_seq')")
        id = cur.fetchone()[0]
        cur.execute("INSERT INTO players (id, name) VALUES (%s, %s)", (id, player4_name))
        player4_id = id
      else:
        # If the player already exists, retrieve their id
        player4_id = player4_id[0]

    
    


    # Check if the team already exists in the Teams table
    cur.execute("SELECT id FROM teams WHERE (team_player_1_id=%s AND team_player_2_id=%s) OR (team_player_1_id=%s AND team_player_2_id=%s)", (player1_id, player2_id, player2_id, player1_id))
    team_player_1_id = cur.fetchone()
    if team_player_1_id is None:
      # If the team does not exist, insert them into the teams table with a unique id
      cur.execute("SELECT nextval('teams_id_seq')")
      id = cur.fetchone()[0]
      cur.execute("INSERT INTO teams (id, team_player_1_id, team_player_2_id) VALUES (%s, %s, %s)", (id, player1_id, player2_id))
      team_player_1_id = id
    else:
      # If the team already exists, retrieve their id
      team_player_1_id = team_player_1_id[0]
    
    # Repeat the process for the other team
    cur.execute("SELECT id FROM teams WHERE (team_player_1_id=%s AND team_player_2_id=%s) OR (team_player_1_id=%s AND team_player_2_id=%s)", (player3_id, player4_id, player4_id, player3_id))
    team_player_2_id = cur.fetchone()
    if team_player_2_id is None:
      cur.execute("SELECT nextval('teams_id_seq')")
      id = cur.fetchone()[0]
      cur.execute("INSERT INTO teams (id, team_player_1_id, team_player_2_id) VALUES (%s, %s, %s)", (id, player3_id, player4_id))
      team_player_2_id = id
    else:
      team_player_2_id = team_player_2_id[0]

    conn.commit() 



    



    # Insert the game into the matches table
    cur.execute("SELECT * FROM matches WHERE date=%s AND team1id=%s AND team2id=%s AND team1score=%s AND team2score=%s", (date, team_player_1_id, team_player_2_id, team1_score, team2_score))
    match = cur.fetchone()
    if match is None:
        cur.execute("INSERT INTO matches (date, team1id, team2id, team1score, team2score) VALUES (%s, %s, %s, %s, %s)", (date, team_player_1_id, team_player_2_id, team1_score, team2_score))
        print(f'processing match: {date} with {player1_name} and {player2_name} vs {player3_name} and {player4_name}: {team1_score} - {team2_score}  ')
        conn.commit() 

        # get the last of the matches
        cur.execute("SELECT id FROM matches ORDER BY id DESC LIMIT 1")
        match_id = cur.fetchone()[0]

        # Insert the players into the MatchPlayers table
        cur.execute("INSERT INTO MatchPlayers (MatchID, PlayerID) VALUES (%s, %s)", (match_id, player1_id))
        cur.execute("INSERT INTO MatchPlayers (MatchID, PlayerID) VALUES (%s, %s)", (match_id, player2_id))
        cur.execute("INSERT INTO MatchPlayers (MatchID, PlayerID) VALUES (%s, %s)", (match_id, player3_id))
        cur.execute("INSERT INTO MatchPlayers (MatchID, PlayerID) VALUES (%s, %s)", (match_id, player4_id))
    else:
        print(f'Skipping match: {date} with {player1_name} and {player2_name} vs {player3_name} and {player4_name}: {team1_score} - {team2_score}  , the match already exist')

    conn.commit()


conn.close()