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


    def get_team_id(team_player1_id, team_player2_id, cur):
        """
        Given the ids of two players and a cursor, return the team_id of the team they are in,
        or insert the team into the teams table if it does not exist and return its new id.
        """
        cur.execute("SELECT team_id FROM team WHERE (team_player_1_id=%s AND team_player_2_id=%s) OR (team_player_1_id=%s AND team_player_2_id=%s)", (team_player1_id, player2_id, team_player1_id, player1_id))
        team_id = cur.fetchone()
        return team_id


    def calculate_point_factor(score_difference):
        return 1 + (math.log(score_difference + 1) / math.log(25))

    def calculate_elo(player1_name, player2_name, team1_score, player3_name, player4_name, team2_score, date, player1_rating, player2_rating, player3_rating, player4_rating):
        # Calculate the expected scores and actual scores for the two teams
        player1_expected_score = 1 / (1 + 10**((player2_rating - player1_rating) / 400))
        player2_expected_score = 1 / (1 + 10**((player1_rating - player2_rating) / 400))
        player3_expected_score = 1 / (1 + 10**((player4_rating - player3_rating) / 400))
        player4_expected_score = 1 / (1 + 10**((player3_rating - player4_rating) / 400))

        team1_expected_score = player1_expected_score + player2_expected_score
        team2_expected_score = player3_expected_score + player4_expected_score

        team1_actual_score = team1_score / (team1_score + team2_score)
        team2_actual_score = team2_score / (team1_score + team2_score)

        # Calculate the point factor using the function you provided
        score_difference = abs(team1_score - team2_score)
        point_factor = calculate_point_factor(score_difference)

        # Get the current IDs of the players
        cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player1_name,))
        player1_id = cur.fetchone()[0]

        cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player2_name,))
        player2_id = cur.fetchone()[0]

        cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player3_name,))
        player3_id = cur.fetchone()[0]

        cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player4_name,))
        player4_id = cur.fetchone()[0]

        # Get the number of games played by each player
        cur.execute("SELECT COUNT(*) FROM PlayerMatch mp INNER JOIN match m ON mp.player_match_id = m.player_id WHERE player_id IN (%s, %s, %s, %s) AND m.match_timestamp <= %s;", (player1_id, player2_id, player3_id, player4_id, date))
        number_of_games = cur.fetchall()

        # Calculate the K value for each player based on the number of games played
        k1 = 50 / (1 + number_of_games[0][0] / 800)
        k2 = 50 / (1 + number_of_games[1][0] / 800)
        k3 = 50 / (1 + number_of_games[2][0] / 800)
        k4 = 50 / (1 + number_of_games[3][0] / 800)

        # Calculate the new Elo ratings for each player
        player1_new_rating = player1_rating + k1 * point_factor * (team1_actual_score - player1_expected_score)
        player2_new_rating = player2_rating + k2 * point_factor * (team1_actual_score - player2_expected_score)
        player3_new_rating = player3_rating + k3 * point_factor * (team2_actual_score - player3_expected_score)
        player4_new_rating = player4_rating + k4 * point_factor * (team2_actual_score - player4_expected_score)

        # Update the database with the new ratings
        cur.execute("INSERT INTO PlayerRating (player_rating_id, rating, player_rating_timestamp) VALUES (%s, %s, %s)", (player1_id, player1_new_rating, date))
        cur.execute("INSERT INTO PlayerRating (player_rating_id, rating, player_rating_timestamp) VALUES (%s, %s, %s)", (player2_id, player2_new_rating, date))
        cur.execute("INSERT INTO PlayerRating (player_rating_id, rating, player_rating_timestamp) VALUES (%s, %s, %s)", (player3_id, player3_new_rating, date))
        cur.execute("INSERT INTO PlayerRating (player_rating_id, rating, player_rating_timestamp) VALUES (%s, %s, %s)", (player4_id, player4_new_rating, date))
        conn.commit()

        # Get the team IDs
        team1_id = get_team_id(player1_id, player2_id, cur)
        team2_id = get_team_id(player3_id, player4_id, cur)

        # Calculate the new team ratings
        team1_new_rating = (player1_new_rating + player2_new_rating) / 2
        team2_new_rating = (player3_new_rating + player4_new_rating) / 2

        # Update the TeamRating table
        cur.execute("INSERT INTO TeamRating (team_rating_id, rating, team_rating_timestamp) VALUES (%s, %s, %s)", (team1_id, team1_new_rating, date))
        cur.execute("INSERT INTO TeamRating (team_rating_id, rating, team_rating_timestamp) VALUES (%s, %s, %s)", (team2_id, team2_new_rating, date))

        # Commit the changes to the database
        conn.commit()

    def calculate_team_elo(team1_player1_name, team1_player2_name, team2_player1_name, team2_player2_name, team1_score, team2_score, date, team1_rating, team2_rating, cur):
        # Calculate the expected scores and actual scores for the two teams
        team1_player1_rating, team1_player2_rating = team1_rating
        team2_player1_rating, team2_player2_rating = team2_rating

        team1_expected_score = 1 / (1 + 10**((team2_player1_rating + team2_player2_rating - team1_player1_rating - team1_player2_rating) / 400))
        team2_expected_score = 1 / (1 + 10**((team1_player1_rating + team1_player2_rating - team2_player1_rating - team2_player2_rating) / 400))

        team1_actual_score = team1_score / (team1_score + team2_score)
        team2_actual_score = team2_score / (team1_score + team2_score)

        # Calculate the point factor using the function you provided
        score_difference = abs(team1_score - team2_score)
        point_factor = calculate_point_factor(score_difference)

        # Get the current IDs of the players
        cur.execute("SELECT player_id FROM player WHERE first_name=%s OR first_name=%s", (team1_player1_name, team1_player2_name))
        team1_player1_id, team1_player2_id = cur.fetchall()

        cur.execute("SELECT player_id FROM player WHERE first_name=%s OR first_name=%s", (team2_player1_name, team2_player2_name))
        team2_player1_id, team2_player2_id = cur.fetchall()

        # Get the number of games played by each team
        cur.execute("SELECT COUNT(*) FROM PlayerMatch mp INNER JOIN match m ON mp.player_match_id = m.player_id WHERE player_id IN (%s, %s) AND m.match_timestamp <= %s;", (team1_player1_id, team1_player2_id, date))
        team1_number_of_games = cur.fetchall()[0][0]

        cur.execute("SELECT COUNT(*) FROM PlayerMatch mp INNER JOIN match m ON mp.player_match_id = m.player_id WHERE player_id IN (%s, %s) AND m.match_timestamp <= %s;", (team2_player1_id, team2_player2_id, date))
        team2_number_of_games = cur.fetchall()[0][0]

        # Calculate the K value for each team based on the number of games played
        team1_k = 50 / (1 + team1_number_of_games / 800)
        team2_k = 50 / (1 + team2_number_of_games / 800)

        # Calculate the new Elo ratings for each team
        team1_new_rating = team1_rating + team1_k * point_factor * (team1_actual_score - team1_expected_score)
        team2_new_rating = team2_rating + team2_k * point_factor * (team2_actual_score - team2_expected_score)

        # Update the database with the new ratings
        cur.execute("INSERT INTO TeamRating (team_rating_id, rating, team_rating_timestamp) VALUES (%s, %s, %s)", (get_team_id(team1_player1_id, team1_player2_id, cur), team1_new_rating, date))
        cur.execute("INSERT INTO TeamRating (team_rating_id, rating, team_rating_timestamp) VALUES (%s, %s, %s)", (get_team_id(team2_player1_id, team2_player2_id, cur), team2_new_rating, date))


    # Close the database connection
        cur.close()
        conn.close() 



