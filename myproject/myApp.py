from flask import Flask, render_template, request
import psycopg2
from config import DATABASE_CONFIG

app = Flask(__name__)

# Function to process the form data and update the database
def process_game_data(player1_name, player2_name, team1_score, player3_name, player4_name, team2_score):
    # Connect to the database
    conn = psycopg2.connect(
        host=DATABASE_CONFIG['host'],
        database=DATABASE_CONFIG['database'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password']
    )

    # Create a cursor
    cur = conn.cursor()

    # Reuse the code from your initial script here
    # Remember to replace any hardcoded data.xlsx reference with the data from the form

    # Start from the code block where you check if the player1_name is not empty
    # ...

    # Continue with the rest of your script
    # ...

    conn.close()

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
        player2_name = request.form['player2_name']
        team1_score = int(request.form['team1_score'])  # Convert to int
        player3_name = request.form['player3_name']
        player4_name = request.form['player4_name']
        team2_score = int(request.form['team2_score'])  # Convert to int
        
        # Process the form data and update the database
        process_game_data(player1_name, player2_name, team1_score, player3_name, player4_name, team2_score)
        
        return "Game created successfully!"
       
    return render_template('create_game.html', players=players)

if __name__ == '__main__':
    app.static_folder = 'static'
    app.run(host='0.0.0.0', port=8080)
