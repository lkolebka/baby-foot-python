#Show the elo score 

WITH ratings AS (
SELECT
players.name AS player_name,
date_trunc ('week', eloratings.date) AS week,
eloratings.rating
FROM eloratings
JOIN players ON eloratings.playerid
= players.id
WHERE players.name IN ('Matthieu', 'Lazare','Nathan','Wissam', 'Elie', 'Ilan', 'Nathanael', 'Edouard')
	)
SELECT
week, 
AVG (CASE WHEN player_name ='Matthieu'THEN rating END) AS Matthieu_rating,
AVG (CASE WHEN player_name ='Lazare'THEN rating END) AS Lazare_rating,
AVG (CASE WHEN player_name ='Nathan'THEN rating END) AS Nathan_rating,
AVG (CASE WHEN player_name ='Wissam'THEN rating END) AS Wissam_rating,
AVG (CASE WHEN player_name ='Elie'THEN rating END) AS Elie_rating,
AVG (CASE WHEN player_name ='Ilan'THEN rating END) AS Ilan_rating,
AVG (CASE WHEN player_name ='Edouard'THEN rating END) AS Edoauard_rating

FROM ratings
GROUP BY week
ORDER BY week;

#show the number of game by team 

SELECT t.team_id, p1.first_name AS player1_name, p2.first_name AS player2_name, COUNT(tm.match_id) AS number_of_games
FROM Team t
INNER JOIN Player p1 ON t.team_player_1_id = p1.player_id
INNER JOIN Player p2 ON t.team_player_2_id = p2.player_id
LEFT JOIN TeamMatch tm ON t.team_id = tm.team_id
GROUP BY t.team_id, p1.first_name, p1.last_name, p2.first_name, p2.last_name
ORDER BY COUNT(tm.match_id) DESC;