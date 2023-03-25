from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from config import DATABASE_CONFIG
import datetime
import math
import calendar


app = Flask(__name__, template_folder='Templates')


def get_player_match_id_by_timestamp_and_by_player_id(player1_id, player2_id, player3_id, player4_id, date, cur):
        cur.execute("SELECT PlayerMatch.player_match_id FROM Match JOIN PlayerMatch ON Match.match_id = PlayerMatch.match_id WHERE PlayerMatch.player_id = %s AND Match.match_timestamp =%s;", (player1_id, date))
        player1_match_id = cur.fetchone()[0]

        cur.execute("SELECT PlayerMatch.player_match_id FROM Match JOIN PlayerMatch ON Match.match_id = PlayerMatch.match_id WHERE PlayerMatch.player_id = %s AND Match.match_timestamp =%s;", (player2_id, date))
        player2_match_id = cur.fetchone()[0]

        cur.execute("SELECT PlayerMatch.player_match_id FROM Match JOIN PlayerMatch ON Match.match_id = PlayerMatch.match_id WHERE PlayerMatch.player_id = %s AND Match.match_timestamp =%s;", (player3_id, date))
        player3_match_id = cur.fetchone()[0]

        cur.execute("SELECT PlayerMatch.player_match_id FROM Match JOIN PlayerMatch ON Match.match_id = PlayerMatch.match_id WHERE PlayerMatch.player_id = %s AND Match.match_timestamp =%s;", (player4_id, date))
        player4_match_id = cur.fetchone()[0]

        return (player1_match_id, player2_match_id, player3_match_id, player4_match_id)

def get_team_match_id_by_timestamp_and_by_team_id(team1_id,team2_id, date, cur):
        cur.execute("SELECT TeamMatch.team_match_id FROM Match JOIN TeamMatch ON Match.match_id = TeamMatch.match_id WHERE TeamMatch.team_id =%s AND Match.match_timestamp =%s;", (team1_id, date))
        team_match1_id = cur.fetchone()[0]

        cur.execute("SELECT TeamMatch.team_match_id FROM Match JOIN TeamMatch ON Match.match_id = TeamMatch.match_id WHERE TeamMatch.team_id =%s AND Match.match_timestamp =%s;", (team2_id, date))
        team_match2_id = cur.fetchone()[0]
        return (team_match1_id,team_match2_id)




# Get the player ID of the players playing a match
def get_player_id(player1_name, player2_name, player3_name, player4_name, cur):
        cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player1_name,))
        player1_id = cur.fetchone()[0]

        cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player2_name,))
        player2_id = cur.fetchone()[0]


        cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player3_name,))
        player3_id = cur.fetchone()[0]

        cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player4_name,))
        player4_id = cur.fetchone()[0]


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

        # Return the team player IDs as a tuple
        return (team1_id, team2_id)         

def number_of_games_player(player1_id, player2_id, player3_id, player4_id, date, cur):
    cur.execute("SELECT COUNT(*) FROM PlayerMatch pm  INNER JOIN Match m ON pm.match_id = m.match_id  WHERE pm.player_id =%s AND m.match_timestamp <=%s;", (player1_id, date))
    number_of_game_player1 = cur.fetchone()[0] or 0

    cur.execute("SELECT COUNT(*) FROM PlayerMatch pm  INNER JOIN Match m ON pm.match_id = m.match_id  WHERE pm.player_id =%s AND m.match_timestamp <=%s;", (player2_id, date))
    number_of_game_player2 = cur.fetchone()[0] or 0

    cur.execute("SELECT COUNT(*) FROM PlayerMatch pm  INNER JOIN Match m ON pm.match_id = m.match_id  WHERE pm.player_id =%s AND m.match_timestamp <=%s;", (player3_id, date))
    number_of_game_player3 = cur.fetchone()[0] or 0

    cur.execute("SELECT COUNT(*) FROM PlayerMatch pm  INNER JOIN Match m ON pm.match_id = m.match_id  WHERE pm.player_id =%s AND m.match_timestamp <=%s;", (player4_id, date))
    number_of_game_player4 = cur.fetchone()[0] or 0

    # Return the number of games played by each player as a tuple
    return (number_of_game_player1, number_of_game_player2, number_of_game_player3, number_of_game_player4)


def number_of_games_team(team1_id, team2_id,date, cur):
    cur.execute("SELECT COUNT(*) FROM Match WHERE (winning_team_id =%s OR losing_team_id = %s ) AND match_timestamp <=%s", (team1_id,team1_id,date))
    number_of_game_team_1 = cur.fetchone()[0] or 0 

    cur.execute("SELECT COUNT(*) FROM Match WHERE (winning_team_id =%s OR losing_team_id = %s ) AND match_timestamp <=%s", (team2_id,team2_id,date))
    number_of_game_team_2 = cur.fetchone()[0] or 0
    
     # Return the number of games played by each team as a tuple
    return (number_of_game_team_1, number_of_game_team_2)
             
def get_player_ratings(player1_id, player2_id, player3_id, player4_id, cur):
    cur.execute("SELECT rating, player_rating_timestamp FROM playerrating WHERE player_match_id IN (SELECT player_match_id FROM playermatch WHERE player_id = %s) ORDER BY player_rating_timestamp DESC LIMIT 1;", (player1_id,))

    result = cur.fetchone()
    if result is not None:
        player1_rating = result[0]
    else:
     player1_rating = 1500


    cur.execute("SELECT rating, player_rating_timestamp FROM playerrating WHERE player_match_id IN (SELECT player_match_id FROM playermatch WHERE player_id = %s) ORDER BY player_rating_timestamp DESC LIMIT 1;", (player2_id,))
    result = cur.fetchone()
    if result is not None:
        player2_rating = result[0]
    else:
     player2_rating = 1500

    cur.execute("SELECT rating, player_rating_timestamp FROM playerrating WHERE player_match_id IN (SELECT player_match_id FROM playermatch WHERE player_id = %s) ORDER BY player_rating_timestamp DESC LIMIT 1;", (player3_id,))
    result = cur.fetchone()
   
    if result is not None:
        player3_rating = result[0]
    else:
     player3_rating = 1500
    

    cur.execute("SELECT rating, player_rating_timestamp FROM playerrating WHERE player_match_id IN (SELECT player_match_id FROM playermatch WHERE player_id = %s) ORDER BY player_rating_timestamp DESC LIMIT 1;", (player4_id,))
    result = cur.fetchone()
    if result is not None:
        player4_rating = result[0]
    else:
        player4_rating = 1500   

    return player1_rating, player2_rating, player3_rating, player4_rating


def get_team_ratings(team1_id, team2_id, cur):
    cur.execute("SELECT rating, team_rating_timestamp FROM teamrating WHERE team_match_id IN (SELECT team_match_id FROM teammatch WHERE team_id = %s) ORDER BY team_rating_timestamp DESC LIMIT 1;", (team1_id,))
    result = cur.fetchone()
    
    if result is not None:
        team1_rating = result[0]
    else:
     team1_rating = 1500

    cur.execute("SELECT rating, team_rating_timestamp FROM teamrating WHERE team_match_id IN (SELECT team_match_id FROM teammatch WHERE team_id = %s) ORDER BY team_rating_timestamp DESC LIMIT 1;", (team2_id,))
    result = cur.fetchone()
    if result is not None:
        team2_rating = result[0]
    else:
     team2_rating = 1500

    return team1_rating, team2_rating

# Get the point factor 
def calculate_point_factor(score_difference):
    return 2 + (math.log(score_difference + 1) / math.log(10)) ** 3

# Function to process the form data and update the database

def process_game_data(player1_name, player2_name, team1_score, player3_name, player4_name, team2_score,date):
    # Connect to the database
    conn = psycopg2.connect(
        host=DATABASE_CONFIG['host'],
        database=DATABASE_CONFIG['database'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password']
    )

    print("date is",date)
    
    # Create a cursor
    cur = conn.cursor()

    # Check if the player name is not empty
    if player1_name:
      # Check if the player already exists in the Player table
      cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player1_name,))
      player1_id = cur.fetchone()
      if player1_id is None:
        # If the player does not exist, insert them into the players table with a unique id
        cur.execute("SELECT nextval('player_id_seq')")
        id = cur.fetchone()[0]
        cur.execute("INSERT INTO player (player_id, first_name) VALUES (%s, %s)", (id, player1_name))
        player1_id = id
      else:
        # If the player already exists, retrieve their player_id
        player1_id = player1_id[0]
      


  # Check if the player2 first_name is not empty
    if player2_name:
      # Check if the player already exists in the Players table
      cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player2_name,))
      player2_id = cur.fetchone()
      if player2_id is None:
        # If the player does not exist, insert them into the players table with a unique id
        cur.execute("SELECT nextval('player_id_seq')")
        id = cur.fetchone()[0]
        cur.execute("INSERT INTO player (player_id, first_name) VALUES (%s, %s)", (id, player2_name))
        player2_id = id
      else:
        # If the player already exists, retrieve their player_id
        player2_id = player2_id[0]
  

  # Check if the player3 first_name is not empty
    if player3_name:
      # Check if the player already exists in the Players table
      cur.execute("SELECT player_id FROM player WHERE first_name=%s", (str(player3_name),))
      player3_id = cur.fetchone()
      if player3_id is None:
        # If the player does not exist, insert them into the players table with a unique id
        cur.execute("SELECT nextval('player_id_seq')")
        id = cur.fetchone()[0]
        cur.execute("INSERT INTO player (player_id, first_name) VALUES (%s, %s)", (id, player3_name))
        player3_id = id
      else:
        # If the player already exists, retrieve their player_id
        player3_id = player3_id[0]  


  # Check if the player4 first_name is not empty
    if player4_name:
      # Check if the player already exists in the Players table
      cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player4_name,))
      player4_id = cur.fetchone()
      if player4_id is None:
        # If the player does not exist, insert them into the players table with a unique id
        cur.execute("SELECT nextval('player_id_seq')")
        id = cur.fetchone()[0]
        cur.execute("INSERT INTO player (player_id, first_name) VALUES (%s, %s)", (id, player4_name))
        player4_id = id
      else:
        # If the player already exists, retrieve their id
        player4_id = player4_id[0]  


  # Check if the team already exists in the Teams table
      cur.execute("SELECT team_id FROM team WHERE (team_player_1_id=%s AND team_player_2_id=%s) OR (team_player_1_id=%s AND team_player_2_id=%s)", (player1_id, player2_id, player2_id, player1_id))
      team_player_1_id = cur.fetchone()
      if team_player_1_id is None:
        # If the team does not exist, insert them into the teams table with a unique id
        cur.execute("SELECT nextval('team_id_seq')")
        id = cur.fetchone()[0]
        cur.execute("INSERT INTO team (team_id, team_player_1_id, team_player_2_id) VALUES (%s, %s, %s)", (id, player1_id, player2_id))
        team_player_1_id = id
      else:
        # If the team already exists, retrieve their id
        team_player_1_id = team_player_1_id[0]  
      
  # Repeat the process for the other team
      cur.execute("SELECT team_id FROM team WHERE (team_player_1_id=%s AND team_player_2_id=%s) OR (team_player_1_id=%s AND team_player_2_id=%s)", (player3_id, player4_id, player4_id, player3_id))
      team_player_2_id = cur.fetchone()
      if team_player_2_id is None:
        cur.execute("SELECT nextval('team_id_seq')")
        id = cur.fetchone()[0]
        cur.execute("INSERT INTO team (team_id, team_player_1_id, team_player_2_id) VALUES (%s, %s, %s)", (id, player3_id, player4_id))
        team_player_2_id = id
      else:
        team_player_2_id = team_player_2_id[0]    


  # Commit the changes to the database
    conn.commit()

    # Function to check winning team
    def get_winning_team(team1_score, team2_score):
      if team1_score > team2_score:
          return 1
      elif team2_score > team1_score:
          return 2
      else:
          return 0  


  # Insert the game into the matches table
    winning_team = get_winning_team(team1_score, team2_score)

    if winning_team == 1:
        winning_team_id = team_player_1_id
        losing_team_id = team_player_2_id
        winning_team_score = team1_score
        losing_team_score = team2_score
    elif winning_team == 2:
        winning_team_id = team_player_2_id
        losing_team_id = team_player_1_id
        winning_team_score = team2_score
        losing_team_score = team1_score
    else:
        winning_team_id = None
        losing_team_id = None
        winning_team_score = None
        losing_team_score = None  

    cur.execute("SELECT * FROM match WHERE match_timestamp=%s AND winning_team_id=%s AND losing_team_id=%s AND winning_team_score=%s AND losing_team_score=%s", (date, winning_team_id, losing_team_id, winning_team_score, losing_team_score))
    match = cur.fetchone()
    if match is None:
            cur.execute("INSERT INTO match (match_timestamp, winning_team_id, losing_team_id, winning_team_score, losing_team_score) VALUES (%s, %s, %s, %s, %s)", (date, winning_team_id, losing_team_id, winning_team_score, losing_team_score))
            print(f'processing match: {date} with {player1_name} and {player2_name} vs {player3_name} and {player4_name}: {team1_score} - {team2_score}  ')
            conn.commit()

            # get the last of the matches
            cur.execute("SELECT match_id FROM match ORDER BY match_id DESC LIMIT 1")
            match_id = cur.fetchone()[0]
          
            # Insert the players into the PlayerMatch table
            cur.execute("INSERT INTO PlayerMatch (player_id,match_id) VALUES (%s, %s)", (player1_id,match_id))
            cur.execute("INSERT INTO PlayerMatch (player_id,match_id) VALUES (%s, %s)", (player2_id,match_id))
            cur.execute("INSERT INTO PlayerMatch (player_id,match_id) VALUES (%s, %s)", (player3_id,match_id))
            cur.execute("INSERT INTO PlayerMatch (player_id,match_id) VALUES (%s, %s)", (player4_id,match_id))

            # Insert the team into the TeamMatch table
            cur.execute("INSERT INTO TeamMatch (team_id,match_id) VALUES (%s, %s)", (winning_team_id,match_id))
            cur.execute("INSERT INTO TeamMatch (team_id,match_id) VALUES (%s, %s)", (losing_team_id,match_id))
  
    else:
        print(f'Skipping match      : {date} with {player1_name} and {player2_name} vs {player3_name} and {player4_name}: {team1_score} - {team2_score}  , the match already exist')


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

    # Call the get_player_match_id_by_timestamp_and_by_player_id function inside the loop
    player_match1_id, player_match2_id, player_match3_id, player_match4_id  = get_player_match_id_by_timestamp_and_by_player_id(player1_id, player2_id, player3_id, player4_id, date, cur)

    # Call the get_team_match_id_by_timestamp_and_by_team_id function inside the loop
    team_match1_id, team_match2_id  = get_team_match_id_by_timestamp_and_by_team_id(team1_id, team2_id, date, cur)

 # Calculate the expected scores for the players
    player1_expected_score_against_player3 = 1 / (1 + 10**((player3_rating - player1_rating) / 500))
    player1_expected_score_against_player4 = 1 / (1 + 10**((player4_rating - player1_rating) / 500))
    player1_expected_score = (player1_expected_score_against_player3 + player1_expected_score_against_player4) / 2
   
    player2_expected_score_against_player3 = 1 / (1 + 10**((player3_rating - player2_rating) / 500))
    player2_expected_score_against_player4 = 1 / (1 + 10**((player4_rating - player2_rating) / 500))
    player2_expected_score = (player2_expected_score_against_player3 + player2_expected_score_against_player4) / 2
   

    player3_expected_score_against_player1 = 1 / (1 + 10**((player1_rating - player3_rating) / 500))
    player3_expected_score_against_player2 = 1 / (1 + 10**((player2_rating - player3_rating) / 500))
    player3_expected_score = (player3_expected_score_against_player1 + player3_expected_score_against_player2) / 2
   

    player4_expected_score_against_player1 = 1 / (1 + 10**((player1_rating - player4_rating) / 500))
    player4_expected_score_against_player2 = 1 / (1 + 10**((player2_rating - player4_rating) / 500))
    player4_expected_score = (player4_expected_score_against_player1 + player4_expected_score_against_player2) / 2
   
    #input("Press enter to continue...")

    # Calculate the expected scores for the teams
    team1_expected_score = (player1_expected_score + player2_expected_score) / 2
    team2_expected_score = (player3_expected_score + player4_expected_score) / 2

   
    #input("Press enter to continue...")



    # Calculate the point factor to be used as a variable
    score_difference = abs(team1_score - team2_score)
    point_factor = calculate_point_factor(score_difference)
   
    # Calculate the K value for each player based on the number of games played and their rating

    k1 = 50 / (1 + number_of_game_player1 / 300)
    k2 = 50 / (1 + number_of_game_player2 / 300) 
    k3 = 50 / (1 + number_of_game_player3 / 300) 
    k4 = 50 / (1 + number_of_game_player4 / 300) 

    #delta = 32 * (1 - winnerChanceToWin)

    # Calculate the K value for each team based on the number of games played
    k5 = 50 / (1 + number_of_games_team1/ 100)
    k6 = 50 / (1 + number_of_games_team2/ 100)

 #logg the wining team
    if team1_score > team2_score:
        team1_actual_score = 1
        team2_actual_score = 0

    else:
        team1_actual_score = 0
        team2_actual_score = 1
       
    # Calculate the new Elo ratings for each player
    player1_new_rating = player1_rating + k1 * point_factor  * (team1_actual_score - player1_expected_score)
    player2_new_rating = player2_rating + k2 * point_factor  * (team1_actual_score - player2_expected_score)
    player3_new_rating = player3_rating + k3 * point_factor  * (team2_actual_score - player3_expected_score)
    player4_new_rating = player4_rating + k4 * point_factor  * (team2_actual_score - player4_expected_score)

    # Calculate the new Elo ratings for each team
    team1_new_rating = team1_rating + k5 * point_factor * (team1_actual_score - team1_expected_score)
    team2_new_rating = team2_rating + k6 * point_factor * (team2_actual_score - team2_expected_score)
    # Log the new ratings for teams

    # Update the database with the player ratings
    print("Inserting player rating for player 1 with match ID", player_match1_id, "and new rating", player1_new_rating)
    cur.execute("INSERT INTO playerrating (player_match_id, rating, player_rating_timestamp) VALUES (%s, %s, %s)", (player_match1_id, player1_new_rating, date))

    print("Inserting player rating for player 2 with match ID", player_match2_id, "and new rating", player2_new_rating)
    cur.execute("INSERT INTO playerrating (player_match_id, rating, player_rating_timestamp) VALUES ( %s, %s, %s)", (player_match2_id, player2_new_rating, date))

    print("Inserting player rating for player 3 with match ID", player_match3_id, "and new rating", player3_new_rating)
    cur.execute("INSERT INTO playerrating (player_match_id,rating, player_rating_timestamp) VALUES (%s, %s, %s)", (player_match3_id,player3_new_rating, date))

    print("Inserting player rating for player 4 with match ID", player_match4_id, "and new rating", player4_new_rating)
    cur.execute("INSERT INTO playerrating (player_match_id, rating, player_rating_timestamp) VALUES (%s, %s, %s)", (player_match4_id, player4_new_rating, date))

    conn.commit()

    # Update the database with the team ratings
    cur.execute("INSERT INTO teamrating (team_match_id, rating, team_rating_timestamp) VALUES (%s, %s, %s)", (team_match1_id, team1_new_rating, date))
    cur.execute("INSERT INTO teamrating (team_match_id, rating, team_rating_timestamp) VALUES (%s, %s, %s)", (team_match2_id, team2_new_rating, date))
  
    conn.commit() 


# Get the exptected score for odds   
def calculate_expected_score(player1_name, player2_name, player3_name, player4_name,):
   # Connect to the database
    conn = psycopg2.connect(
        host=DATABASE_CONFIG['host'],
        database=DATABASE_CONFIG['database'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password']
    )

    
    # Create a cursor
    cur = conn.cursor()

    
  # Call the get_player_id function inside the loop
    player1_id, player2_id, player3_id, player4_id = get_player_id(player1_name, player2_name, player3_name, player4_name, cur)

  # Call the get_player_ratings function inside the loop
    player1_rating, player2_rating, player3_rating, player4_rating = get_player_ratings(player1_id, player2_id, player3_id, player4_id, cur)

 # Calculate the expected scores for the players
    player1_expected_score_against_player3 = 1 / (1 + 10**((player3_rating - player1_rating) / 500))
    player1_expected_score_against_player4 = 1 / (1 + 10**((player4_rating - player1_rating) / 500))
    player1_expected_score = (player1_expected_score_against_player3 + player1_expected_score_against_player4) / 2
   
    player2_expected_score_against_player3 = 1 / (1 + 10**((player3_rating - player2_rating) / 500))
    player2_expected_score_against_player4 = 1 / (1 + 10**((player4_rating - player2_rating) / 500))
    player2_expected_score = (player2_expected_score_against_player3 + player2_expected_score_against_player4) / 2
   

    player3_expected_score_against_player1 = 1 / (1 + 10**((player1_rating - player3_rating) / 500))
    player3_expected_score_against_player2 = 1 / (1 + 10**((player2_rating - player3_rating) / 500))
    player3_expected_score = (player3_expected_score_against_player1 + player3_expected_score_against_player2) / 2
   

    player4_expected_score_against_player1 = 1 / (1 + 10**((player1_rating - player4_rating) / 500))
    player4_expected_score_against_player2 = 1 / (1 + 10**((player2_rating - player4_rating) / 500))
    player4_expected_score = (player4_expected_score_against_player1 + player4_expected_score_against_player2) / 2
   

    # Calculate the expected scores for the teams
    team1_expected_score = (player1_expected_score + player2_expected_score) / 2
    team2_expected_score = (player3_expected_score + player4_expected_score) / 2
    team1_expected_scoreQuotation = 1/ team1_expected_score 
    team2_expected_scoreQuotation = 1/ team2_expected_score

    print(f"Player 1 ({player1_name}) expected score: {player1_expected_score}")
    print(f"Player 2 ({player2_name}) expected score: {player2_expected_score}")
    print(f"Player 3 ({player3_name}) expected score: {player3_expected_score}")
    print(f"Player 4 ({player4_name}) expected score: {player4_expected_score}")
    print(f"Team 1 expected score: {team1_expected_score}")
    print(f"Team 2 expected score: {team2_expected_score}")

    return team1_expected_score, team2_expected_score, team1_expected_scoreQuotation, team2_expected_scoreQuotation


# Get the players from the database
def get_players():
    try:
        conn = psycopg2.connect(
            host=DATABASE_CONFIG['host'],
            database=DATABASE_CONFIG['database'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password']
        )
        cursor = conn.cursor()
        query = "SELECT first_name FROM player ORDER BY first_name ASC;"  # 
        cursor.execute(query)
        players = cursor.fetchall()
        print("Players fetched:", players)  # Add this line to print the fetched players
        return [player[0] for player in players]
       
    except Exception as e:
        print("Error connecting to the database:", e)
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_latest_player_ratings(month=None):
    now = datetime.datetime.now()
    default_month = now.month
    default_year = now.year
    selected_month = int(month) if month else default_month
    start_date = f'{default_year}-{selected_month:02d}-01 00:00:00'
    end_date = f'{default_year}-{selected_month:02d}-{get_last_day_of_month(selected_month, default_year):02d} 23:59:59'

    query = '''
                SELECT 
            CONCAT(p.first_name, '.', SUBSTRING(p.last_name FROM 1 FOR 1)) as player_name, 
            pr.rating, 
            COUNT(DISTINCT pm.match_id) as num_matches,
            pr.player_rating_timestamp
        FROM Player p
        JOIN (
            SELECT 
                pm.player_id, 
                pr.rating, 
                pr.player_rating_timestamp,
                pm.match_id
            FROM PlayerMatch pm
            JOIN PlayerRating pr ON pm.player_match_id = pr.player_match_id
            WHERE pr.player_rating_timestamp = (
                SELECT MAX(pr2.player_rating_timestamp)
                FROM PlayerMatch pm2
                JOIN PlayerRating pr2 ON pm2.player_match_id = pr2.player_match_id
                WHERE pm2.player_id = pm.player_id
                AND pr2.player_rating_timestamp >= %s AND pr2.player_rating_timestamp <= %s
            ) AND pm.player_id IN (
                SELECT DISTINCT pm3.player_id
                FROM PlayerMatch pm3
                JOIN PlayerRating pr3 ON pm3.player_match_id = pr3.player_match_id
                WHERE pr3.player_rating_timestamp >= %s AND pr3.player_rating_timestamp <= %s
            )
        ) pr ON p.player_id = pr.player_id
        JOIN PlayerMatch pm ON p.player_id = pm.player_id
        WHERE p.active = true AND pm.match_id IN (
            SELECT match_id FROM Match
            WHERE match_timestamp >= %s AND match_timestamp <= %s
        )
        GROUP BY p.player_id, pr.rating, pr.player_rating_timestamp
        ORDER BY pr.rating DESC;
    '''
    with psycopg2.connect(**DATABASE_CONFIG) as conn:
        cur = conn.cursor()
        cur.execute(query, (start_date, end_date, start_date, end_date,start_date, end_date))
        player_ratings = cur.fetchall()

    return player_ratings

def get_match_list(month=None):
    now = datetime.datetime.now()
    default_month = now.month
    default_year = now.year
    selected_month = int(month) if month else default_month
    start_date = f'{default_year}-{selected_month:02d}-01 00:00:00'
    end_date = f'{default_year}-{selected_month:02d}-{get_last_day_of_month(selected_month, default_year):02d} 23:59:59'
    query = f'''
        SELECT 
            m.match_id as ID,
            P1.first_name AS player_1,
            P2.first_name AS player_2,
            M.winning_team_score AS score_team_1,
            P3.first_name AS player_3,
            P4.first_name AS player_4,
            M.losing_team_score AS score_team_2,
            M.match_timestamp
        FROM Match M
        JOIN Team WT ON M.winning_team_id = WT.team_id
        JOIN Team LT ON M.losing_team_id = LT.team_id
        JOIN Player P1 ON WT.team_player_1_id = P1.player_id
        JOIN Player P2 ON WT.team_player_2_id = P2.player_id
        JOIN Player P3 ON LT.team_player_1_id = P3.player_id
        JOIN Player P4 ON LT.team_player_2_id = P4.player_id
        WHERE M.match_timestamp >= %s AND M.match_timestamp <= %s
        ORDER BY M.match_timestamp DESC;
    '''
    with psycopg2.connect(**DATABASE_CONFIG) as conn:
        cur = conn.cursor()
        cur.execute(query, (start_date, end_date))
        print(start_date,end_date)
        matches = cur.fetchall()

    return matches

def get_last_day_of_month(month, year):
    if month == 12:
        return 31
    else:
        return (datetime.date(year, month+1, 1) - datetime.timedelta(days=1)).day


@app.route('/', methods=['GET', 'POST'])
def create_game():
    players = get_players()
    if request.method == 'POST':
        player1_name = request.form['player1_name']
        print(f"player1_name: {player1_name}")
        player2_name = request.form['player2_name']
        print(f"player2_name: {player2_name}")
        team1_score = int(request.form['team1_score'])
        print(f"team1_score: {team1_score}")
        player3_name = request.form['player3_name']
        print(f"player3_name: {player3_name}")
        player4_name = request.form['player4_name']
        print(f"player4_name: {player4_name}")
        team2_score = int(request.form['team2_score'])
        print(f"team2_score: {team2_score}")
        date = request.form['game_date']

    
        print(f"date: {date}")

         # Get the current time
        now = datetime.now().strftime('%H:%M:%S')
        
        # Convert date to string in the desired format with current time
        date_str = datetime.strptime(date, '%Y-%m-%d').strftime(f'%Y-%m-%d {now}')


        # Process the form data and update the database
        process_game_data(player1_name, player2_name, team1_score, player3_name, player4_name, team2_score, date_str)
        
        return redirect('/thank_you')
       
    return render_template('create_game.html', players=players)

def get_last_match():
    with psycopg2.connect(**DATABASE_CONFIG) as conn:
        cur = conn.cursor()
        cur.execute("SELECT m.match_id as matchid,m.match_timestamp as time, p1.first_name AS player1_name, p2.first_name AS player2_name, p3.first_name AS player3_name, p4.first_name AS player4_name, m.winning_team_score AS team1_score, m.losing_team_score AS team2_score FROM Match m INNER JOIN Team wt ON m.winning_team_id = wt.team_id INNER JOIN Team lt ON m.losing_team_id = lt.team_id INNER JOIN Player p1 ON wt.team_player_1_id = p1.player_id INNER JOIN Player p2 ON wt.team_player_2_id = p2.player_id INNER JOIN Player p3 ON lt.team_player_1_id = p3.player_id INNER JOIN Player p4 ON lt.team_player_2_id = p4.player_id ORDER BY m.match_id DESC LIMIT 1;")
        last_match = cur.fetchone()
        
    return last_match

import psycopg2

def delete_last_match():
    with psycopg2.connect(**DATABASE_CONFIG) as conn:
        cur = conn.cursor()

        # Begin transaction
        cur.execute("BEGIN;")

        # Find the latest match_id
        cur.execute("SELECT match_id FROM \"match\" ORDER BY match_timestamp DESC LIMIT 1;")
        latest_match_id = cur.fetchone()[0]

        # Delete related player ratings
        cur.execute(f"DELETE FROM playerrating WHERE player_match_id IN (SELECT player_match_id FROM playermatch WHERE match_id = {latest_match_id});")

        # Delete related team ratings
        cur.execute(f"DELETE FROM teamrating WHERE team_match_id IN (SELECT team_match_id FROM teammatch WHERE match_id = {latest_match_id});")

        # Delete related player matches
        cur.execute(f"DELETE FROM playermatch WHERE match_id = {latest_match_id};")

        # Delete related team matches
        cur.execute(f"DELETE FROM teammatch WHERE match_id = {latest_match_id};")

        # Delete the match itself
        cur.execute(f"DELETE FROM \"match\" WHERE match_id = {latest_match_id};")

        # Commit transaction
        cur.execute("COMMIT;")


@app.route('/thank_you')
def thank_you():
    last_match = get_last_match()
    message = request.args.get('message', None)
    return render_template('thank_you.html', last_match=last_match, message=message)



@app.route('/delete_last_match', methods=['POST'])
def delete_last_match_route():
    delete_last_match()
    return redirect(url_for('create_game'), code=302)

@app.route('/calculate_odds', methods=['GET', 'POST'])
def calculate_expected_score_route():
    print("calculate_expected_score_route called")
    if request.method == 'POST':
        # Get the form data and process it
        player1_name = request.form['player1_name']
        player2_name = request.form['player2_name']
        player3_name = request.form['player3_name']
        player4_name = request.form['player4_name']
    
        print(f"Form data: player1_name={player1_name}, player2_name={player2_name}, player3_name={player3_name}, player4_name={player4_name}")

        team1_expected_score, team2_expected_score, team1_expected_scoreQuotation, team2_expected_scoreQuotation = calculate_expected_score(player1_name, player2_name, player3_name, player4_name)
        
        # Pass the expected scores and form data to the template
        return render_template('calculate_odds.html', players=get_players(), 
                               team1_expected_score= "{:.2f}".format(team1_expected_score * 100), 
                               team2_expected_score= "{:.2f}".format(team2_expected_score * 100), 
                               team1_expected_scoreQuotation= round(team1_expected_scoreQuotation,2), 
                               team2_expected_scoreQuotation= round(team2_expected_scoreQuotation,2),
                               player1_name=player1_name, player2_name=player2_name,
                               player3_name=player3_name, player4_name=player4_name)
    else:
        # Render the form for entering the game details
        players = get_players()
        print(f"Available players: {players}")
        return render_template('calculate_odds.html', players=players)

@app.route('/rating')
def rating():
    month = request.args.get('month')
    if not month:
       month = request.args.get('month', datetime.datetime.now().strftime('%m'))
    player_ratings = get_latest_player_ratings(month=month)
    return render_template('rating.html', player_ratings=player_ratings, month=month)


@app.route('/match_list')
def match_list():
    month = request.args.get('month')
    if not month:
       month = request.args.get('month', datetime.datetime.now().strftime('%m'))
    matches = get_match_list(month=month)
    return render_template('match_list.html', matches=matches, month=month)



if __name__ == '__main__':
    app.static_folder = 'static'
    app.run(host='0.0.0.0', port=8081) 
