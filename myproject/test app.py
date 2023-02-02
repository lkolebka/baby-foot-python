from flask import Flask, render_template, request
import psycopg2
from config import DATABASE_CONFIG


app = Flask(__name__)

#get the players from the database 
def get_players():
    try:
        conn = psycopg2.connect(
            host=DATABASE_CONFIG['host'],
            database=DATABASE_CONFIG['database'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password']
        )
        cursor = conn.cursor()
        query = "SELECT name FROM players"
        cursor.execute(query)
        players = cursor.fetchall()
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
        team1_score = request.form['team1_score']
        player3_name = request.form['player3_name']
        player4_name = request.form['player4_name']
        team2_score = request.form['team2_score']
        # Do something with the data (e.g. save it to a database)
        return "Game created successfully!"
    return render_template('create_game.html', players=players)

if __name__ == '__main__':
    app.static_folder = 'static'
    app.run(host='0.0.0.0', port=8080)

    