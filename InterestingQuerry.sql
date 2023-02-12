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

