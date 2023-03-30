from flask import Flask
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from sqlalchemy import create_engine
from config import DATABASE_CONFIG
from app import get_players

# create database connection
engine = create_engine(
    f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@"
    f"{DATABASE_CONFIG['host']}/{DATABASE_CONFIG['database']}"
)



app = dash.Dash(__name__, external_stylesheets=['/static/style.css'])
server = app.server

app.layout = html.Div([
    html.H1('Player Rating Evolution Dashboard'),
    html.Link(href='/static/style.css', rel='stylesheet'),
    html.Div(className='dropdown-container', children=[

       dcc.Dropdown(
            id='player-dropdown',
            options=[{'label': player, 'value': player} for player in get_players()],
            value=['Matthieu', 'Lazare'],
            multi=True
        )
    ], style={'width': '50%', 'margin': 'auto'}), # set the width and center the container horizontally
    html.Div(className='chart-container', children=[
        dcc.Graph(id='rating-graph')
    ], style={'width': '80%', 'margin': 'auto'}), # set the width and center the container horizontally
], style={'max-width': '1200px', 'margin': 'auto'}) # set the maximum width of the layout and center it horizontally


@app.callback(
    Output('rating-graph', 'figure'),
    Input('player-dropdown', 'value')
)
def update_rating_graph(players):
    fig = go.Figure()
    for player in players:
        query = f"""SELECT
                        DATE_TRUNC('week', m.match_timestamp) AS week_start,
                        MAX(CASE WHEN p.first_name = '{player}' THEN pr.rating ELSE NULL END) AS rating
                    FROM PlayerMatch pm
                    JOIN Player p ON pm.player_id = p.player_id
                    JOIN PlayerRating pr ON pm.player_match_id = pr.player_match_id
                    JOIN Match m ON pm.match_id = m.match_id
                    WHERE p.first_name = '{player}'
                    GROUP BY DATE_TRUNC('week', m.match_timestamp)
                    ORDER BY week_start ASC"""
        data = pd.read_sql(query, engine)
        fig.add_trace(go.Scatter(x=data['week_start'], y=data['rating'], name=player))
    fig.update_layout(title='Player Rating Evolution',
                      xaxis_title='Week',
                      yaxis_title='Rating')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)