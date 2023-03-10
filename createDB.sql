CREATE TABLE Player (
    player_id serial PRIMARY KEY,
    first_name varchar(50) NOT NULL,
    last_name varchar(50),
    active boolean NOT NULL DEFAULT TRUE
);

CREATE TABLE Team (
    team_id serial PRIMARY KEY,
    team_player_1_id int REFERENCES Player(player_id),
    team_player_2_id int REFERENCES Player(player_id)
);

CREATE TABLE Match (
    match_id serial PRIMARY KEY,
    match_timestamp timestamp NOT NULL,
    winning_team_id int REFERENCES Team(team_id),
    losing_team_id int REFERENCES Team(team_id),
    winning_team_score int,
    losing_team_score int NOT NULL
);

CREATE TABLE PlayerMatch (
    player_match_id serial PRIMARY KEY,
    player_id int REFERENCES Player(player_id),
    match_id int REFERENCES Match(match_id)
);

CREATE TABLE PlayerRating (
    player_rating_id serial PRIMARY KEY,
    player_match_id int REFERENCES PlayerMatch(player_match_id),
    rating int NOT NULL,
    player_rating_timestamp timestamp  NOT NULL

);

CREATE TABLE TeamMatch (
    team_match_id serial PRIMARY KEY,
    team_id int REFERENCES Team(team_id),
    match_id int REFERENCES Match(match_id)
);

CREATE TABLE TeamRating (
    team_rating_id serial PRIMARY KEY,
    team_match_id int REFERENCES TeamMatch(team_match_id),
    rating int NOT NULL,
    team_rating_timestamp timestamp  NOT NULL

);
