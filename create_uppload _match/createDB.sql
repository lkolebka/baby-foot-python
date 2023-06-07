CREATE TABLE Player (
    player_id serial PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE
);
 
CREATE TABLE Team (
    team_id serial PRIMARY KEY,
    team_player_1_id INT NOT NULL REFERENCES Player(player_id),
    team_player_2_id INT NOT NULL REFERENCES Player(player_id)
);
 
CREATE TABLE MATCH (
    match_id serial PRIMARY KEY,
    match_timestamp TIMESTAMP NOT NULL,
    winning_team_id INT NOT NULL REFERENCES Team(team_id),
    losing_team_id INT NOT NULL REFERENCES Team(team_id),
    winning_team_score INT NOT NULL CHECK (winning_team_score = 11),
    losing_team_score INT NOT NULL CHECK (losing_team_score >= 0 AND losing_team_score != 11)
);
 
CREATE TABLE PlayerMatch (
    player_match_id serial PRIMARY KEY,
    player_id INT NOT NULL REFERENCES Player(player_id),
    match_id INT NOT NULL REFERENCES MATCH(match_id)
);
 
CREATE TABLE PlayerRating (
    player_rating_id serial PRIMARY KEY,
    player_match_id INT NOT NULL REFERENCES PlayerMatch(player_match_id),
    rating INT NOT NULL,
    player_rating_timestamp TIMESTAMP  NOT NULL
);
 
CREATE TABLE TeamMatch (
    team_match_id serial PRIMARY KEY,
    team_id INT NOT NULL REFERENCES Team(team_id),
    match_id INT NOT NULL REFERENCES MATCH(match_id)
);
 
CREATE TABLE TeamRating (
    team_rating_id serial PRIMARY KEY,
    team_match_id INT NOT NULL REFERENCES TeamMatch(team_match_id),
    rating INT NOT NULL,
    team_rating_timestamp TIMESTAMP  NOT NULL
 
);
 
CREATE SEQUENCE player_id_seq START 1;
CREATE SEQUENCE team_id_seq START 1;
CREATE SEQUENCE match_id_seq START 1;
CREATE SEQUENCE player_match_id_seq START 1;
CREATE SEQUENCE player_rating_id_seq START 1;
CREATE SEQUENCE team_match_id_seq START 1;
CREATE SEQUENCE team_rating_id_seq START 1;