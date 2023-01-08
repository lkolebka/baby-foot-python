# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="user",
    password="password"
)


# Create a cursor
cur = conn.cursor()

def calculate_elo(old_rating, opponent_rating, outcome):
    K = 32  # The constant that determines the impact of the match on the rating
    expected_outcome = 1 / (1 + 10 ** ((opponent_rating - old_rating) / 400))
    return old_rating + K * (outcome - expected_outcome)


# Retrieve the form data from the HTML form
player1_name = request.form['player1_name']  # Assuming the name of the player is a form field named "Equipe 1 p1"
player2_name = request.form['player2_name']  # Assuming the name of the player is a form field named "Equipe 1 p2"
player3_name = request.form['player3_name']  # Assuming the name of the player is a form field named "Equipe 2 p1"
player4_name = request.form['player4_name']  # Assuming the name of the player is a form field named "Equipe 2 p2"
team1_score = request.form['team1_score']  # Assuming the score of team 1 is a form field named "score equipe 1"
team2_score = request.form['team2_score']  # Assuming the score of team 2 is a form field named "score equipe 2"

# Calculate the Elo ratings for the individual players
player1_outcome = 0
player2_outcome = 0
player3_outcome = 0
player4_outcome = 0
if team1_score > team2_score:
    # Team 1 won, so players 1 and 2 get a win
    player1_outcome = 1
    player2_outcome = 1
else:
    # Team 1 lost, so players 1 and 2 get a loss
    player1_outcome = 0
    player2_outcome = 0

if team2_score > team1_score:
    # Team 2 won, so players 3 and 4 get a win
    player3_outcome = 1
    player4_outcome = 1
else:
    # Team 2 lost, so players 3 and 4 get a loss
    player3_outcome = 0
    player4_outcome = 0

    # Get the current ratings of the players
cur.execute("SELECT Rating FROM Players WHERE Name=%s", (player3_name,))
player3_rating = cur.fetchone()[0]
cur.execute("SELECT Rating FROM Players WHERE Name=%s", (player4_name,))
player4_rating = cur.fetchone()[0]

# Calculate the new ratings for the players
player1_new_rating = calculate_elo(player1_rating, player3_rating, player1_outcome)
player2_new_rating = calculate_elo(player2_rating, player4_rating, player2_outcome)
player3_new_rating = calculate_elo(player3_rating, player1_rating, player3_outcome)
player4_new_rating = calculate_elo(player4_rating, player2_rating, player4_outcome)

# Update the player ratings in the database
cur.execute("UPDATE Players SET Rating=%s WHERE Name=%s", (player1_new_rating, player1_name))
cur.execute("UPDATE Players SET Rating=%s WHERE Name=%s", (player2_new_rating, player2_name))
cur.execute("UPDATE Players SET Rating=%s WHERE Name=%s", (player3_new_rating, player3_name))
cur.execute("UPDATE Players SET Rating=%s WHERE Name=%s", (player4_new_rating, player4_name))

# Calculate the Elo ratings for the teams
team1_rating = (player1_new_rating + player2_new_rating) / 2
team2_rating = (player3_new_rating + player4_new_rating) / 2

# Update the team ratings in the database
# (You will need to modify this query to update the team ratings in the correct table)
cur.execute("UPDATE Teams SET Rating=%s WHERE Player1ID=%s AND Player2ID=%s", (team1_rating, player1_name, player2_name))
cur.execute("UPDATE Teams SET Rating=%s WHERE Player1ID=%s AND Player2ID=%s", (team2_rating, player3_name, player4_name))

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
