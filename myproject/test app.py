from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def create_game():
    if request.method == 'POST':
        player1_name = request.form['player1_name']
        player2_name = request.form['player2_name']
        team1_score = request.form['team1_score']
        player3_name = request.form['player3_name']
        player4_name = request.form['player4_name']
        team2_score = request.form['team2_score']
        # Do something with the data (e.g. save it to a database)
        return "Game created successfully!"
    return render_template('create_game.html')

if __name__ == '__main__':
    app.static_folder = 'static'
    app.run()
