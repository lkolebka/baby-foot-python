DELETE FROM Player;
DELETE FROM Team;
DELETE FROM Match;
DELETE FROM PlayerMatch;
DELETE FROM PlayerRating;
DELETE FROM TeamMatch;
DELETE FROM TeamRating;



ALTER SEQUENCE player_id_seq RESTART WITH 1;
ALTER SEQUENCE team_id_seq RESTART WITH 1;
ALTER SEQUENCE match_id_seq RESTART WITH 1;
ALTER SEQUENCE player_match_id_seq RESTART WITH 1;
ALTER SEQUENCE team_match_id_seq RESTART WITH 1;
ALTER SEQUENCE player_rating_id_seq RESTART WITH 1;
ALTER SEQUENCE team_rating_id_seq RESTART WITH 1;



ALTER TABLE match ALTER COLUMN match_id DROP DEFAULT;
DROP SEQUENCE match_match_id_seq CASCADE;
CREATE SEQUENCE match_match_id_seq START 1;
ALTER TABLE match ALTER COLUMN match_id SET DEFAULT nextval('match_match_id_seq');

ALTER TABLE playermatch ALTER COLUMN player_match_id DROP DEFAULT;
DROP SEQUENCE player_match_id_seq CASCADE;
CREATE SEQUENCE player_match_id_seq START 1;
ALTER TABLE playermatch ALTER COLUMN player_match_id SET DEFAULT nextval('player_match_id_seq');

ALTER TABLE teammatch ALTER COLUMN team_match_id DROP DEFAULT;
DROP SEQUENCE team_match_id_seq CASCADE;
CREATE SEQUENCE team_match_id_seq START 1;
ALTER TABLE teammatch ALTER COLUMN team_match_id SET DEFAULT nextval('team_match_id_seq');

ALTER TABLE playerrating ALTER COLUMN player_rating_id DROP DEFAULT;
DROP SEQUENCE playerrating_player_rating_id_seq CASCADE;
CREATE SEQUENCE playerrating_player_rating_id_seq START 1;
ALTER TABLE playerrating ALTER COLUMN player_rating_id SET DEFAULT nextval('playerrating_player_rating_id_seq');

ALTER TABLE teamrating ALTER COLUMN team_rating_id DROP DEFAULT;
DROP SEQUENCE teamrating_team_rating_id_seq CASCADE;
CREATE SEQUENCE teamrating_team_rating_id_seq START 1;
ALTER TABLE teamrating ALTER COLUMN team_rating_id SET DEFAULT nextval('teamrating_team_rating_id_seq');




SELECT setval('player_id_seq', 1, false);

SELECT setval('team_id_seq', 1, false);

SELECT setval('match_id_seq', 1, false);

SELECT setval('team_match_id_seq', 1, false);

SELECT setval('player_match_id_seq', 1, false);






