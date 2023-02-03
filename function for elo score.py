import psycopg2
from openpyxl import load_workbook
from insertTeams import get_team_player1_and_player_2
from insertTeams import get_team_id
from config import DATABASE_CONFIG

import math

# Connect to the database
conn = psycopg2.connect(
    host=DATABASE_CONFIG['host'],
    database=DATABASE_CONFIG['database'],
    user=DATABASE_CONFIG['user'],
    password=DATABASE_CONFIG['password']
)

# Create a cursor
cur = conn.cursor()

import math

def get_number_of_games_by_name(player_name):
    query = """
    SELECT COUNT(*)
    FROM matchplayers
    WHERE playerid IN (
      SELECT id
      FROM players
      WHERE name = %s
    );
    """
    cur.execute(query, (player_name,))
    result = cur.fetchone()
    number_of_games = result[0] if result else 0
    return number_of_games


# calculate the factor of the differnce of the point 
def calculate_point_factor(score_difference):
    return 1 + (math.log(score_difference + 1) / math.log(12))


def calculate_elo(old_rating, opponent_rating, outcome, score_difference, number_of_games):
    K = 50 / (1 + number_of_games / 800)  # The constant that determines the impact of the match on the rating
    expected_outcome = 1 / (1 + 10 ** ((opponent_rating - old_rating) / 400))
    point_factor = calculate_point_factor(score_difference)
    return old_rating + (K) * point_factor * (outcome - expected_outcome)

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

    # Calculate the score difference for the individual players
    score_difference_player1 = 0
    score_difference_player2 = 0
    score_difference_player3 = 0
    score_difference_player4 = 0

    # Calculate the Elo ratings for the individual players
    player1_outcome = 0
    player2_outcome = 0
    player3_outcome = 0
    player4_outcome = 0

    if team1_score > team2_score:
        # Team 1 won, so players 1 and 2 get a win
        player1_outcome = 1
        player2_outcome = 1
        score_difference_player1 = (team1_score - team2_score)
        score_difference_player2 = (team1_score - team2_score)
    else:
        # Team 1 lost, so players 1 and 2 get a loss
        player1_outcome = 0
        player2_outcome = 0

    if team2_score > team1_score:
        # Team 2 won, so players 3 and 4 get a win
        player3_outcome = 1
        player4_outcome = 1
        score_difference_player3 = (team2_score - team1_score)
        score_difference_player4 = (team2_score - team1_score)
    else:
        # Team 2 lost, so players 3 and 4 get a loss
        player3_outcome = 0
        player4_outcome = 0

    # Get the current IDs of the players
    cur.execute("SELECT id FROM players WHERE name=%s", (player1_name,))
    player1_id = cur.fetchone()[0]
    print(f'id of player {player1_name} is {player1_id}')

    cur.execute("SELECT id FROM players WHERE name=%s", (player2_name,))
    player2_id = cur.fetchone()[0]
    print(f'id of player {player2_name} is {player2_id}')

    cur.execute("SELECT id FROM players WHERE name=%s", (player3_name,))
    player3_id = cur.fetchone()[0]
    print(f'id of player {player3_name} is {player3_id}')

    cur.execute("SELECT id FROM players WHERE name=%s", (player4_name,))
    player4_id = cur.fetchone()[0]
    print(f'id of player {player4_name} is {player4_id}')

    # Get the number of games by players 
    cur.execute("SELECT COUNT(*) FROM matchplayers WHERE playerid IN (SELECT id FROM players WHERE id = %s)", (player1_id,))
    number_of_game_player1 = cur.fetchone()[0]
    print(f'number of game for {player1_name} is {number_of_game_player1}')

    cur.execute("SELECT COUNT(*) FROM matchplayers WHERE playerid IN (SELECT id FROM players WHERE id = %s)", (player2_id,))
    number_of_game_player2 = cur.fetchone()[0]
    print(f'number of game for {player2_name} is {number_of_game_player2}')

    cur.execute("SELECT COUNT(*) FROM matchplayers WHERE playerid IN (SELECT id FROM players WHERE id = %s)", (player3_id,))
    number_of_game_player3 = cur.fetchone()[0]
    print(f'number of game for {player3_name} is {number_of_game_player3}')

    cur.execute("SELECT COUNT(*) FROM matchplayers WHERE playerid IN (SELECT id FROM players WHERE id = %s)", (player4_id,))
    number_of_game_player4 = cur.fetchone()[0]
    print(f'number of game for {player4_name} is {number_of_game_player4}')
    
    # Get the current ratings of the players
    cur.execute("SELECT rating FROM eloratings WHERE playerid=%s ORDER BY date DESC LIMIT 1", (player1_id,))
    result = cur.fetchone()
    if result is not None:
        player1_rating = result[0]
    else:
        # handle the case where the query did not return any rows
        player1_rating = 1200
    print(f'current rating of {player1_name} is {player1_rating}')

    cur.execute("SELECT rating FROM eloratings WHERE playerid=%s ORDER BY date DESC LIMIT 1", (player2_id,))
    result = cur.fetchone()
    if result is not None:
        player2_rating = result[0]
    else:
        # handle the case where the query did not return any rows
        player2_rating = 1200
    print(f'current rating of {player2_name} is {player2_rating}')
    
 
    cur.execute("SELECT rating FROM eloratings WHERE playerid=%s ORDER BY date DESC LIMIT 1", (player3_id,))
    result = cur.fetchone()
    if result is not None:
        player3_rating = result[0]
    else:
        # handle the case where the query did not return any rows
        player3_rating = 1200
    print(f'current rating of {player3_name} is {player3_rating}')

    cur.execute("SELECT rating FROM eloratings WHERE playerid=%s ORDER BY date DESC LIMIT 1", (player4_id,))
    result = cur.fetchone()
    if result is not None:
        player4_rating = result[0]
    else:
        # handle the case where the query did not return any rows
        player4_rating = 1200  
    print(f'current rating of {player4_name} is {player4_rating}')                                                                                       

    conn.commit()

    # Calculate the new ratings for the players
    player1_new_rating = (calculate_elo(player1_rating, player3_rating, player1_outcome, score_difference_player1, number_of_game_player1) + calculate_elo(player1_rating, player4_rating, player1_outcome, score_difference_player1, number_of_game_player1))/2
    player2_new_rating = (calculate_elo(player2_rating, player3_rating, player2_outcome, score_difference_player2, number_of_game_player2) + calculate_elo(player2_rating, player4_rating, player2_outcome,score_difference_player2, number_of_game_player2 ))/2
    player3_new_rating = (calculate_elo(player3_rating, player1_rating, player3_outcome, score_difference_player3, number_of_game_player3) + calculate_elo(player3_rating, player2_rating, player3_outcome, score_difference_player3, number_of_game_player3))/2
    player4_new_rating = (calculate_elo(player4_rating, player1_rating, player4_outcome, score_difference_player4, number_of_game_player4) + calculate_elo(player4_rating, player2_rating, player4_outcome, score_difference_player4, number_of_game_player4))/2

    # print the value of the outcome
    if team1_score > team2_score:
        # Team 1 won, so players 1 and 2 get a win
        print(f'{player1_name} and {player2_name} = won')
        print(f'{player3_name} and {player4_name} = lost')
    else:
        # Team 1 lost, so players 1 and 2 get a loss
          print(f'{player3_name} and {player4_name} = won')
          print(f'{player1_name} and {player2_name} = lost')
   
    # print the value for testing
    print(f'new rating for {player1_name} is = {player1_new_rating}')
    print(f'new rating for {player2_name} is = {player2_new_rating}')
    print(f'new rating for {player3_name} is = {player3_new_rating}')
    print(f'new rating for {player4_name} is = {player4_new_rating}')

    # Update the player ratings in the database
    cur.execute("INSERT INTO eloratings (playerid, rating, date) VALUES (%s, %s, %s)", (player1_id, player1_new_rating, date))
    cur.execute("INSERT INTO eloratings (playerid, rating, date) VALUES (%s, %s, %s)", (player2_id, player2_new_rating, date))
    cur.execute("INSERT INTO eloratings (playerid, rating, date) VALUES (%s, %s, %s)", (player3_id, player3_new_rating, date))
    cur.execute("INSERT INTO eloratings (playerid, rating, date) VALUES (%s, %s, %s)", (player4_id, player4_new_rating, date))


    conn.commit()

    # Calculate the Elo ratings for the teams
    team1_rating = (player1_new_rating + player2_new_rating) / 2
    team2_rating = (player3_new_rating + player4_new_rating) / 2

    #Call the function get_team_ids from the players ID
    team1_id = get_team_id(player1_id, player2_id,cur)
    team2_id = get_team_id(player3_id, player4_id,cur)


  

   # Update the team ratings in the elorating_teams table
    cur.execute("INSERT INTO eloratings_teams (teamid, rating, date) VALUES (%s, %s,%s)", (team1_id, team1_rating, date ))
    cur.execute("INSERT INTO eloratings_teams (teamid, rating, date) VALUES (%s, %s,%s)", (team2_id, team2_rating, date))




# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
