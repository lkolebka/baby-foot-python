import psycopg2
from openpyxl import load_workbook
from config import DATABASE_CONFIG
import math

# Connect to the database
conn = psycopg2.connect(
    host=DATABASE_CONFIG['host'],
    database=DATABASE_CONFIG['database'],
    user=DATABASE_CONFIG['user'],
    password=DATABASE_CONFIG['password']
)
print("Connected to the database!")

# Create a cursor
cur = conn.cursor()

# Load the workbook
wb = load_workbook('data.xlsx')

# Select the active sheet
ws = wb.active
print("Connected to the XLS sheet!")

 # Get the player ID of the players playing a match
def get_player_id(player1_name, player2_name, player3_name, player4_name, cur):
        cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player1_name,))
        player1_id = cur.fetchone()[0]
        print(f'Processing player1 {player1_name} with id {player1_id}')

        cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player2_name,))
        player2_id = cur.fetchone()[0]
        print(f'Processing player2 {player2_name} with id {player2_id}')

        cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player3_name,))
        player3_id = cur.fetchone()[0]
        print(f'Processing player3 {player3_name} with id {player3_id}')

        cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player4_name,))
        player4_id = cur.fetchone()[0]
        print(f'Processing player4 {player4_name} with id {player4_id}')


        # Return a tuple containing all the player IDs
        return (player1_id, player2_id, player3_id, player4_id)

# Get the team ID of the teams playing a match
def insert_team_or_get_team_id(player1_id, player2_id, player3_id, player4_id, cur):
     # Check if the first team already exists
        cur.execute("SELECT team_id FROM team WHERE (team_player_1_id=%s AND team_player_2_id=%s) OR (team_player_1_id=%s AND team_player_2_id=%s)", (player1_id, player2_id, player2_id, player1_id))
        team1_id = cur.fetchone()
        if team1_id is None:
            # If the team does not exist, insert them into the teams table with a unique id
            cur.execute("SELECT nextval('team_id_seq')")
            id = cur.fetchone()[0]
            cur.execute("INSERT INTO team (team_id, team_player_1_id, team_player_2_id) VALUES (%s, %s, %s)", (id, player1_id, player2_id))
            team1_id = id
        else:
            # If the team already exists, retrieve their id
            team1_id = team1_id[0]
            print(f"Team with id={team1_id} with players {player1_id} and {player2_id} already exists")


        # Check if the second team already exists
        cur.execute("SELECT team_id FROM team WHERE (team_player_1_id=%s AND team_player_2_id=%s) OR (team_player_1_id=%s AND team_player_2_id=%s)", (player3_id, player4_id, player4_id, player3_id))
        team2_id = cur.fetchone()
        if team2_id is None:
            # If the team does not exist, insert them into the teams table with a unique id
            cur.execute("SELECT nextval('team_id_seq')")
            id = cur.fetchone()[0]
            cur.execute("INSERT INTO team (team_id, team_player_1_id, team_player_2_id) VALUES (%s, %s, %s)", (id, player3_id, player4_id))
            team2_id = id
        else:
            # If the team already exists, retrieve their id
            team2_id = team2_id[0]
            print(f"Team with id={team2_id} with players {player3_id} and {player4_id} already exists")

        # Return the team player IDs as a tuple
        return (team1_id, team2_id)         

def number_of_games_player(player1_id, player2_id, player3_id, player4_id, date, cur):
    cur.execute("SELECT COUNT(*) FROM PlayerMatch pm  INNER JOIN Match m ON pm.match_id = m.match_id  WHERE pm.player_id =%s AND m.match_timestamp <=%s;", (player1_id, date))
    number_of_game_player1 = cur.fetchone()[0] or 0
    print(f'number of game for player {player1_id} on the {date} is {number_of_game_player1}')

    cur.execute("SELECT COUNT(*) FROM PlayerMatch pm  INNER JOIN Match m ON pm.match_id = m.match_id  WHERE pm.player_id =%s AND m.match_timestamp <=%s;", (player2_id, date))
    number_of_game_player2 = cur.fetchone()[0] or 0
    print(f'number of game for player {player2_id} on the {date} is {number_of_game_player2}')

    cur.execute("SELECT COUNT(*) FROM PlayerMatch pm  INNER JOIN Match m ON pm.match_id = m.match_id  WHERE pm.player_id =%s AND m.match_timestamp <=%s;", (player3_id, date))
    number_of_game_player3 = cur.fetchone()[0] or 0
    print(f'number of game for player {player3_id} on the {date} is {number_of_game_player3}')

    cur.execute("SELECT COUNT(*) FROM PlayerMatch pm  INNER JOIN Match m ON pm.match_id = m.match_id  WHERE pm.player_id =%s AND m.match_timestamp <=%s;", (player4_id, date))
    number_of_game_player4 = cur.fetchone()[0] or 0
    print(f'number of game for player {player4_id} on the {date} is {number_of_game_player4}')

    # Return the number of games played by each player as a tuple
    return (number_of_game_player1, number_of_game_player2, number_of_game_player3, number_of_game_player4)


def number_of_games_team(team1_id, team2_id,date, cur):
    cur.execute("SELECT COUNT(*) FROM Match  WHERE winning_team_id =%s OR losing_team_id = %s AND match_timestamp <=%s", (team1_id,team1_id,date))
    number_of_game_team_1 = cur.fetchone()[0] or 0 
    print(f'number of game for team {team1_id} on the {date} is {number_of_game_team_1}')

    cur.execute("SELECT COUNT(*) FROM Match  WHERE winning_team_id =%s OR losing_team_id = %s AND match_timestamp <=%s", (team2_id,team2_id,date))
    number_of_game_team_2 = cur.fetchone()[0] or 0
    print(f'number of game for team {team2_id} on the {date} is {number_of_game_team_2}')  
    
     # Return the number of games played by each team as a tuple
    return (number_of_game_team_1, number_of_game_team_2)
             
def get_player_ratings(player1_id, player2_id, player3_id, player4_id, cur):
    cur.execute("SELECT rating FROM PlayerRating WHERE player_rating_id=%s ORDER BY player_rating_timestamp DESC LIMIT 1", (player1_id,))
    result = cur.fetchone()
    player1_rating = result[0] if result else 1200
    print(f'current rating of player {player1_id} is {player1_rating}')

    cur.execute("SELECT rating FROM PlayerRating WHERE player_rating_id=%s ORDER BY player_rating_timestamp DESC LIMIT 1", (player2_id,))
    result = cur.fetchone()
    player2_rating = result[0] if result else 1200
    print(f'current rating of player {player2_id} is {player2_rating}')

    cur.execute("SELECT rating FROM PlayerRating WHERE player_rating_id=%s ORDER BY player_rating_timestamp DESC LIMIT 1", (player3_id,))
    result = cur.fetchone()
    player3_rating = result[0] if result else 1200
    print(f'current rating of player {player3_id} is {player3_rating}')

    cur.execute("SELECT rating FROM PlayerRating WHERE player_rating_id=%s ORDER BY player_rating_timestamp DESC LIMIT 1", (player4_id,))
    result = cur.fetchone()
    player4_rating = result[0] if result else 1200
    print(f'current rating of player {player4_id} is {player4_rating}')

    return player1_rating, player2_rating, player3_rating, player4_rating


def get_team_ratings(team1_id, team2_id, cur):
    cur.execute("SELECT rating FROM TeamRating WHERE team_match_id =%s ORDER BY team_rating_timestamp DESC LIMIT 1", (team1_id,))
    result = cur.fetchone()
    team1_rating = result[0] if result else 1200
    print(f'current rating of team {team1_id} is {team1_rating}')

    cur.execute("SELECT rating FROM TeamRating WHERE team_match_id =%s ORDER BY team_rating_timestamp DESC LIMIT 1", (team2_id,))
    result = cur.fetchone()
    team2_rating = result[0] if result else 1200
    print(f'current rating of team {team2_id} is {team2_rating}')

    return team1_rating, team2_rating





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

    # Call the get_player_id function inside the loop
    player1_id, player2_id, player3_id, player4_id = get_player_id(player1_name, player2_name, player3_name, player4_name, cur)

    # Call the insert_team_or_get_team_id function inside the loop
    team1_id, team2_id = insert_team_or_get_team_id(player1_id, player2_id, player3_id, player4_id, cur)

    # Call the number_of_games_player function inside the loop
    number_of_game_player1, number_of_game_player2, number_of_game_player3, number_of_game_player4 = number_of_games_player(player1_id, player2_id, player3_id, player4_id, date, cur)

    # Call the number_of_games_team function inside the loop
    number_of_games_team1, number_of_games_team2 = number_of_games_team(team1_id, team2_id, date, cur)

    # Call the get_player_ratings function inside the loop
    player1_rating, player2_rating, player3_rating, player4_rating = get_player_ratings(player1_id, player2_id, player3_id, player4_id, cur)

    # Call the get_teams_ratings function inside the loop
    team1_rating, team2_rating = get_team_ratings(team1_id, team2_id, cur)



