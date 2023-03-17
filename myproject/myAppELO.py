from flask import Flask, render_template, request
import psycopg2
from config import DATABASE_CONFIG
from datetime import datetime
import math
import logging



app = Flask(__name__)

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

    # Convert date string to datetime object
    



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
        query = "SELECT first_name FROM player"  # Change the column name to match your database
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

        # Convert date to string in the desired format
        date_str = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')

        # Process the form data and update the database
        process_game_data(player1_name, player2_name, team1_score, player3_name, player4_name, team2_score, date_str)
        
        return "Game created successfully!"
       
    return render_template('create_game.html', players=players)

if __name__ == '__main__':
    app.static_folder = 'static'
    app.run(host='0.0.0.0', port=8081)
