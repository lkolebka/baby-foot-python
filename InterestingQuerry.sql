#Show the elo score for Lazare
SELECT pr.rating, pm.match_id, m.match_timestamp
FROM PlayerMatch pm
JOIN Player p ON pm.player_id = p.player_id
JOIN PlayerRating pr ON pm.player_match_id = pr.player_match_id
JOIN Match m ON pm.match_id = m.match_id
WHERE p.first_name = 'Lazare'
ORDER BY pr.rating ASC;

#Show the elo score for Lazare and Matthieu 

SELECT
    'Lazare' AS player_name,
    pr.rating AS lazare_rating,
    m.match_timestamp AS lazare_timestamp,
    'Matthieu' AS player_name,
    pr2.rating AS matthieu_rating,
    m2.match_timestamp AS matthieu_timestamp
FROM PlayerMatch pm
JOIN Player p ON pm.player_id = p.player_id
JOIN PlayerRating pr ON pm.player_match_id = pr.player_match_id
JOIN Match m ON pm.match_id = m.match_id
JOIN PlayerMatch pm2 ON pm2.match_id = pm.match_id
JOIN Player p2 ON pm2.player_id = p2.player_id
JOIN PlayerRating pr2 ON pm2.player_match_id = pr2.player_match_id
JOIN Match m2 ON pm2.match_id = m2.match_id
WHERE p.first_name = 'Lazare' AND p2.first_name = 'Matthieu'
ORDER BY lazare_rating ASC, matthieu_rating ASC;

work better 
SELECT
    m.match_timestamp,
    MAX(CASE WHEN p.first_name = 'Lazare' THEN pr.rating ELSE NULL END) AS lazare_rating,
    MAX(CASE WHEN p.first_name = 'Matthieu' THEN pr.rating ELSE NULL END) AS matthieu_rating
FROM PlayerMatch pm
JOIN Player p ON pm.player_id = p.player_id
JOIN PlayerRating pr ON pm.player_match_id = pr.player_match_id
JOIN Match m ON pm.match_id = m.match_id
WHERE p.first_name IN ('Lazare', 'Matthieu')
GROUP BY m.match_timestamp
ORDER BY m.match_timestamp ASC;


#show the number of game by team 

SELECT t.team_id, p1.first_name AS player1_name, p2.first_name AS player2_name, COUNT(tm.match_id) AS number_of_games
FROM Team t
INNER JOIN Player p1 ON t.team_player_1_id = p1.player_id
INNER JOIN Player p2 ON t.team_player_2_id = p2.player_id
LEFT JOIN TeamMatch tm ON t.team_id = tm.team_id
GROUP BY t.team_id, p1.first_name, p1.last_name, p2.first_name, p2.last_name
ORDER BY COUNT(tm.match_id) DESC;