[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Flkolebka%2Fbaby-foot-python&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
# Creating Connection Throuh Competition: The Development of an Elo-Based, Data-Driven Ranking System for Baby-Foot

This project is a sophisticated baby-foot (table soccer) Elo rating system, built as part of a thesis research. Designed specifically for four-player (2vs2) games, it refines the Elo rating system with new parameters and a modified K-value to provide accurate player ratings. The system is implemented in Python and comprises two major components:




- A data processing module that handles initial data from Excel files.
- A web application that continuously updates player ratings based on the game outcomes, offering multiple interactive features for users.

## Installation

1. Clone this repository.
2. Install dependencies via 

```bash
  pip install -r requirements.txt
```
3. Set up a local PostgreSQL database and create an config.py file at the root of the repository
```bash
  from urllib.parse import urlparse

ENV = "dev"

if ENV == 'dev':
    DATABASE_CONFIG = {
        'host': "localhost",
        'database': "babyfoot",
        'user': "*****",
        'password': "*****"
    }
else: 

    uri = "*****"
    parsed_uri = urlparse(uri)

    DATABASE_CONFIG = {
        'host': "*****",
        'database': "****",
        'user': "****",
        'password': "****",
        'port': "5432"
    } 
```
## Database Schema
Before diving into the features, it is important to understand the underlying database schema. The code for the database creation can be found  [here](https://github.com/lkolebka/baby-foot-python/blob/main/create_uppload%20_match/createDB.sql). This schema illustrates how different data points are linked to each other within the database. The schema consists of the following tables: 

![Database Diagram](https://github.com/lkolebka/baby-foot-python/blob/main/database%20diagram.png?raw=true)

## Features and Workflow
#### Data Processing


This initial step prepares player data for the Elo rating calculations. It handles the processing of Excel files, extracting raw match data and transforming it into a suitable format for accurate Elo calculations and appropriate database insertion. This step is optional and depends on whether there's an Excel file containing previous match data.

To use this module, an Excel file with previous match data is required. An example Excel file is provided in the repository for reference.

After obtaining the Excel file, run the script `V3_Working_without_logg.py`. This script reads the data from the Excel file, transforms it, and effectively manages the data insertion into the database, ensuring the correct links between tables. It also initiates and compute the Elo rating for every player involved in a match.

#### Web Application
The web application is the primary interface for users to interact with the Elo rating system. It provides several main features:
- Record Matches: Users can record match results including players, scores, and the winning team.

- Calculate Odds: The application can calculate the odds of winning a match between two players based on their past performance.
- Match History: Provides a list of past matches including players, scores, and outcomes.

#### Data Visualization 
- Player Rating Evolution: A line graph showing the evolution of a player's rating over time.
- Player Metrics: Detailed metrics of each player are available, including total games, wins, losses, average score, most played with and against, and win rates.

To use the application, run the `app.py` script. This starts the web server and makes the application accessible via a web browser.

## Using the System
To use the system, follow these steps:

1. Create and configure your database settings in the `config.py` file
2. Run the `create_database.py`
3. If you have an Excel file with previous match data, use the data processing module `V3_Working_without_logg.py` to transform this data into a suitable format for the rating system.
4. Run the application by using the module `app.py` to calculate and update player ratings based on match outcomes.
5. Continuously feed match data into the system to keep player ratings up-to-date.
6. Take a look at the data vizualiation and the different players metrics in the app.

The baby-foot Elo rating system allows for fair player performance evaluation and fosters a competitive environment for players of all skill levels.

## Authors

- [@lkolebka] https://www.github.com/lkolebka


## License

This application is available under the MIT License. See the [LICENSE](LICENSE) file for more information.
