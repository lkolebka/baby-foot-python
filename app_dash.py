from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from sqlalchemy import create_engine
from config import DATABASE_CONFIG
from app import get_players
import dash_bootstrap_components as dbc
import sys
import os

def get_responsive_margins():
    screen_width = os.get_terminal_size().columns
    
    if screen_width <= 576:  # Small screens (e.g., mobile devices)
        return dict(l=10, r=10, t=20, b=10)
    else:  # Larger screens (e.g., desktop)
        return dict(l=30, r=30, t=50, b=30)

fontFormat = dict(family="Segoe UI, Roboto, Helvetica Neue, Helvetica, Microsoft YaHei, Meiryo, Meiryo UI, Arial Unicode MS, sans-serif",
                  size=18,)


# create database connection
engine = create_engine(
    f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@"
    f"{DATABASE_CONFIG['host']}/{DATABASE_CONFIG['database']}"
)


app.layout = dbc.Container([
    html.H1('Rating Evolution'),
    html.Link(href='/static/style.css', rel='stylesheet'),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='player-dropdown',
                options=[{'label': player, 'value': player} for player in get_players()],
                value=['Matthieu', 'Lazare'],
                multi=True
            ),
            width={"size": 10, "offset": 1},
            lg={"size": 6, "offset": 3},
            md={"size": 8, "offset": 2},
            sm={"size": 12, "offset": 0},
        )
    ], style={"margin-top": "20px"}),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='rating-graph'),
            width=12
        )
    ], style={"margin-top": "20px", "height": "calc(100vh - 200px)"})
])



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
    autosize=True,
    margin=get_responsive_margins(),
    paper_bgcolor="white",
    plot_bgcolor="white",
    dragmode='zoom',
    uirevision='constant',
    xaxis=dict(
        fixedrange=False,
        showgrid=True,  # Show the grid along the X axis
        gridcolor='lightgray',  # Set the grid color along the X axis
        gridwidth=0.5,  # Set the grid width along the X axis
    ),
    yaxis=dict(
        fixedrange=True,
        showgrid=True,  # Show the grid along the Y axis
        gridcolor='lightgray',  # Set the grid color along the Y axis
        gridwidth=0.5,  # Set the grid width along the Y axis
    ),
    legend=dict(
        orientation="h",  # Set the legend orientation to horizontal
        xanchor="center",  # Anchor the legend horizontally at the center
        x=0.5,  # Position the legend at the center along the X axis
        yanchor="bottom",  # Anchor the legend vertically at the bottom
        y=-0.25,  # Position the legend slightly below the bottom along the Y axis
    ),
)

    
    fig.update_layout(
        {
            "title": {
                "font": {"size": 12},
            }
        }
    )
    
    return fig

  