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

fontFormat = dict(family="sans-serif",
                      size=22,)

# create database connection
engine = create_engine(
    f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@"
    f"{DATABASE_CONFIG['host']}/{DATABASE_CONFIG['database']}"
)



app = dash.Dash(__name__, external_stylesheets=['/static/style.css'])
server = app.server

app.layout = html.Div([
    html.H1('Rating Evolution'),
    html.Link(href='/static/style.css', rel='stylesheet'),
    html.Div(className='dropdown-container', children=[
       dcc.Dropdown(
            id='player-dropdown',
            options=[{'label': player, 'value': player} for player in get_players()],
            value=['Matthieu', 'Lazare'],
            multi=True
        )
    ], style={'width': '50%', 'margin': 'auto'}),
    html.Div(className='chart-container', children=[
        dcc.Graph(id='rating-graph', style={'width': '100%', 'height': '100%'})
    ], style={'width': '100%', 'height': 'calc(100vh - 200px)'})
], style={'max-width': '1200px', 'margin': 'auto'})


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
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    fig.update_layout(font=fontFormat)
    fig.update_yaxes(ticksuffix = "  ")
    fig.update_layout(legend_orientation="h")
    
    # Set different width and height values based on screen size
    fig.update_layout(
        width=350,
        height=500,
        margin=dict(l=30, r=30, t=50, b=30),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    fig.update_layout(
        {
            "title": {
                "font": {"size": 12},
            }
        }
    )
    
    return fig



if __name__ == '__main__':
    app.static_folder = 'static'
    app.run(host='0.0.0.0', port=8082) 