/*Show the elo score for Lazare*/
SELECT pr.rating, pm.match_id, m.match_timestamp
FROM PlayerMatch pm
JOIN Player p ON pm.player_id = p.player_id
JOIN PlayerRating pr ON pm.player_match_id = pr.player_match_id
JOIN Match m ON pm.match_id = m.match_id
WHERE p.first_name = 'Lazare'
ORDER BY pr.rating ASC;

/*Show the elo score for Lazare and Matthieu*/

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

/*Show the elo score for two player all time*/
SELECT
    m.match_timestamp,
    MAX(CASE WHEN p.first_name = 'Lazare' THEN pr.rating ELSE NULL END) AS lazare_rating,
    MAX(CASE WHEN p.first_name = 'Matthieu' THEN pr.rating ELSE NULL END) AS matthieu_rating,
	MAX(CASE WHEN p.first_name = 'Elie' THEN pr.rating ELSE NULL END) AS elie_rating
FROM PlayerMatch pm
JOIN Player p ON pm.player_id = p.player_id
JOIN PlayerRating pr ON pm.player_match_id = pr.player_match_id
JOIN Match m ON pm.match_id = m.match_id
WHERE p.first_name IN ('Lazare', 'Matthieu', 'Elie')
GROUP BY m.match_timestamp
ORDER BY m.match_timestamp ASC;

/*Show the elo score for two player by week*/
SELECT
    DATE_TRUNC('week', m.match_timestamp) AS week_start,
    MAX(CASE WHEN p.first_name = 'Lazare' THEN pr.rating ELSE NULL END) AS lazare_rating,
    MAX(CASE WHEN p.first_name = 'Matthieu' THEN pr.rating ELSE NULL END) AS matthieu_rating,
    MAX(CASE WHEN p.first_name = 'Elie' THEN pr.rating ELSE NULL END) AS elie_rating,
	MAX(CASE WHEN p.first_name = 'Wissam' THEN pr.rating ELSE NULL END) AS wissam_rating,
	MAX(CASE WHEN p.first_name = 'NathanD' THEN pr.rating ELSE NULL END) AS NathanD_rating,
	MAX(CASE WHEN p.first_name = 'Lante' THEN pr.rating ELSE NULL END) AS Lante_rating
FROM PlayerMatch pm
JOIN Player p ON pm.player_id = p.player_id
JOIN PlayerRating pr ON pm.player_match_id = pr.player_match_id
JOIN Match m ON pm.match_id = m.match_id
WHERE p.first_name IN ('Lazare', 'Matthieu', 'Elie','Wissam','NathanD','Lante')
GROUP BY DATE_TRUNC('week', m.match_timestamp)
ORDER BY week_start ASC;


/*show the number of game by team*/

SELECT t.team_id, p1.first_name AS player1_name, p2.first_name AS player2_name, COUNT(tm.match_id) AS number_of_games
FROM Team t
INNER JOIN Player p1 ON t.team_player_1_id = p1.player_id
INNER JOIN Player p2 ON t.team_player_2_id = p2.player_id
LEFT JOIN TeamMatch tm ON t.team_id = tm.team_id
GROUP BY t.team_id, p1.first_name, p1.last_name, p2.first_name, p2.last_name
ORDER BY COUNT(tm.match_id) DESC;

/*show the rating from a team given their id*/
SELECT
    DATE_TRUNC('week', m.match_timestamp) AS week_start,
    MAX(CASE WHEN t.team_id = 1 THEN tr.rating ELSE NULL END) AS Lazare_Matthieu,
    MAX(CASE WHEN t.team_id = 7 THEN tr.rating ELSE NULL END) AS Lazare_Wissam,
    MAX(CASE WHEN t.team_id = 8 THEN tr.rating ELSE NULL END) AS Matthieu_wissam
FROM Team t
JOIN TeamMatch tm ON t.team_id = tm.team_id
JOIN TeamRating tr ON tm.team_match_id = tr.team_match_id
JOIN Match m ON tm.match_id = m.match_id
WHERE t.team_id IN (1, 7, 8)
GROUP BY DATE_TRUNC('week', m.match_timestamp)
ORDER BY week_start ASC;



/* show the rating for a team given their name*/
SELECT
    t.team_id,
    CONCAT(p1.first_name, ' ', p1.last_name) AS player_1_name,
    CONCAT(p2.first_name, ' ', p2.last_name) AS player_2_name,
    DATE_TRUNC('week', m.match_timestamp) AS week_start,
    MAX(tr.rating) AS team_rating
FROM Team t
JOIN Player p1 ON t.team_player_1_id = p1.player_id
JOIN Player p2 ON t.team_player_2_id = p2.player_id
JOIN TeamMatch tm ON t.team_id = tm.team_id
JOIN TeamRating tr ON tm.team_match_id = tr.team_match_id
JOIN Match m ON tm.match_id = m.match_id
JOIN PlayerMatch pm1 ON m.match_id = pm1.match_id AND pm1.player_id = p1.player_id
JOIN PlayerMatch pm2 ON m.match_id = pm2.match_id AND pm2.player_id = p2.player_id
WHERE (p1.first_name = 'Lazare' AND p2.first_name = 'Matthieu')
   OR (p1.first_name = 'Matthieu' AND p2.first_name = 'Lazare')
GROUP BY (t.team_id, player_1_name, player_2_name, week_start)
ORDER BY week_start ASC;

/*show the team id based on the player names*/
SELECT DISTINCT t.team_id
FROM Team t
JOIN Player p1 ON t.team_player_1_id = p1.player_id
JOIN Player p2 ON t.team_player_2_id = p2.player_id
WHERE p1.first_name = 'Lazare' AND p2.first_name = 'Matthieu'


/* retrieve the last uplaod */
SELECT
    m.match_id as matchid,
	m.match_timestamp as time,
	p1.first_name AS player1_name,
    p2.first_name AS player2_name,
    p3.first_name AS player3_name,
    p4.first_name AS player4_name,
    m.winning_team_score AS team1_score,
    m.losing_team_score AS team2_score
FROM
    Match m
INNER JOIN Team wt ON m.winning_team_id = wt.team_id
INNER JOIN Team lt ON m.losing_team_id = lt.team_id
INNER JOIN Player p1 ON wt.team_player_1_id = p1.player_id
INNER JOIN Player p2 ON wt.team_player_2_id = p2.player_id
INNER JOIN Player p3 ON lt.team_player_1_id = p3.player_id
INNER JOIN Player p4 ON lt.team_player_2_id = p4.player_id
ORDER BY
    m.match_timestamp DESC
LIMIT 1;

/*delete last match*/
WITH latest_match AS (
    SELECT match_id FROM "match" ORDER BY match_timestamp DESC LIMIT 1
),
player_rating_deletion AS (
    DELETE FROM PlayerRating
    WHERE player_match_id IN (
        SELECT player_match_id FROM PlayerMatch WHERE match_id = (SELECT match_id FROM latest_match)
    )
),
team_rating_deletion AS (
    DELETE FROM TeamRating
    WHERE team_match_id IN (
        SELECT team_match_id FROM TeamMatch WHERE match_id = (SELECT match_id FROM latest_match)
    )
),
player_match_deletion AS (
    DELETE FROM PlayerMatch WHERE match_id = (SELECT match_id FROM latest_match)
),
team_match_deletion AS (
    DELETE FROM TeamMatch WHERE match_id = (SELECT match_id FROM latest_match)
)
DELETE FROM "match" WHERE match_id = (SELECT match_id FROM latest_match);

/*ranking*/ 
WITH latest_player_ratings AS (
    SELECT pm.player_id, pr.rating, pr.player_rating_timestamp
    FROM PlayerRating pr
    JOIN PlayerMatch pm ON pr.player_match_id = pm.player_match_id
    WHERE pr.player_rating_timestamp = (
        SELECT MAX(pr2.player_rating_timestamp)
        FROM PlayerRating pr2
        JOIN PlayerMatch pm2 ON pr2.player_match_id = pm2.player_match_id
        WHERE pm2.player_id = pm.player_id
    )
)

SELECT p.player_id, p.first_name, p.last_name, lpr.rating, lpr.player_rating_timestamp
FROM Player p
JOIN latest_player_ratings lpr ON p.player_id = lpr.player_id
WHERE p.active = true
ORDER BY lpr.rating DESC;

/*retrive all the matchs*/
SELECT 
    m.match_id as ID,
	P1.first_name AS player_1,
    P2.first_name AS player_2,
    M.winning_team_score AS score_team_1,
    P3.first_name AS player_3,
    P4.first_name AS player_4,
    M.losing_team_score AS score_team_2,
    M.match_timestamp
FROM Match M
JOIN Team WT ON M.winning_team_id = WT.team_id
JOIN Team LT ON M.losing_team_id = LT.team_id
JOIN Player P1 ON WT.team_player_1_id = P1.player_id
JOIN Player P2 ON WT.team_player_2_id = P2.player_id
JOIN Player P3 ON LT.team_player_1_id = P3.player_id
JOIN Player P4 ON LT.team_player_2_id = P4.player_id
WHERE M.match_timestamp >= '2023-03-01 13:33:15'AND M.match_timestamp <= '2023-04-01 13:33:15';


/*retrieve the rating from a specific date*/
SELECT 
    CONCAT(p.first_name, '.', SUBSTRING(p.last_name FROM 1 FOR 1)) as player_name, 
    pr.rating, 
    COUNT(DISTINCT pm.match_id) as num_matches,
    pr.player_rating_timestamp
FROM Player p
JOIN (
    SELECT 
        pm.player_id, 
        pr.rating, 
        pr.player_rating_timestamp,
        pm.match_id
    FROM PlayerMatch pm
    JOIN PlayerRating pr ON pm.player_match_id = pr.player_match_id
    WHERE pr.player_rating_timestamp = (
        SELECT MAX(pr2.player_rating_timestamp)
        FROM PlayerMatch pm2
        JOIN PlayerRating pr2 ON pm2.player_match_id = pr2.player_match_id
        WHERE pm2.player_id = pm.player_id
          AND pr2.player_rating_timestamp >= '2023-01-23' AND pr2.player_rating_timestamp <= '2023-02-22'
    ) AND pm.player_id IN (
        SELECT DISTINCT pm3.player_id
        FROM PlayerMatch pm3
        JOIN PlayerRating pr3 ON pm3.player_match_id = pr3.player_match_id
        WHERE pr3.player_rating_timestamp >= '2023-01-23' AND pr3.player_rating_timestamp <= '2023-02-22'
    )
) pr ON p.player_id = pr.player_id
JOIN PlayerMatch pm ON p.player_id = pm.player_id
WHERE p.active = true AND pm.match_id IN (
    SELECT match_id FROM Match
    WHERE match_timestamp >= '2023-01-23' AND match_timestamp <= '2023-02-22'
)
GROUP BY p.player_id, pr.rating, pr.player_rating_timestamp
ORDER BY pr.rating DESC;

/*retreive ranking with % of winning*/
SELECT 
    wp.player_name,
    wp.rating,
    wp.num_matches,
    wp.winning_percentage,
    wp.player_rating_timestamp
FROM (
    SELECT 
        CONCAT(p.first_name, '.', SUBSTRING(p.last_name FROM 1 FOR 1)) AS player_name,
        pr.rating,
        COUNT(DISTINCT pm.match_id) AS num_matches,
        pr.player_rating_timestamp,
        ROUND(100 * COUNT(CASE 
                            WHEN tm.team_id = m.winning_team_id THEN 1
                            ELSE NULL 
                        END) / COUNT(pm.match_id), 2) AS winning_percentage
    FROM Player p
    JOIN (
        SELECT 
            pm.player_id, 
            pr.rating, 
            pr.player_rating_timestamp,
            pm.match_id
        FROM PlayerMatch pm
        JOIN PlayerRating pr ON pm.player_match_id = pr.player_match_id
        WHERE pr.player_rating_timestamp = (
            SELECT MAX(pr2.player_rating_timestamp)
            FROM PlayerMatch pm2
            JOIN PlayerRating pr2 ON pm2.player_match_id = pr2.player_match_id
            WHERE pm2.player_id = pm.player_id
              AND pr2.player_rating_timestamp >= '2023-03-01' AND pr2.player_rating_timestamp <= '2023-03-31'
        ) AND pm.player_id IN (
            SELECT DISTINCT pm3.player_id
            FROM PlayerMatch pm3
            JOIN PlayerRating pr3 ON pm3.player_match_id = pr3.player_match_id
            WHERE pr3.player_rating_timestamp >= '2023-03-01' AND pr3.player_rating_timestamp <= '2023-03-31'
        )
    ) pr ON p.player_id = pr.player_id
    JOIN PlayerMatch pm ON p.player_id = pm.player_id
    JOIN Team t ON p.player_id = ANY(ARRAY[t.team_player_1_id, t.team_player_2_id])
    JOIN TeamMatch tm ON tm.team_id = t.team_id AND tm.match_id = pm.match_id
    JOIN Match m ON tm.match_id = m.match_id
    WHERE p.active = true AND pm.match_id IN (
        SELECT match_id FROM Match
        WHERE match_timestamp >= '2023-03-01' AND match_timestamp <= '2023-03-31'
    )
    GROUP BY p.player_id, pr.rating, pr.player_rating_timestamp
) wp
JOIN Player p ON wp.player_name = CONCAT(p.first_name, '.', SUBSTRING(p.last_name FROM 1 FOR 1))
ORDER BY wp.rating DESC;


/*delete a specific match*/
DELETE FROM playerrating WHERE player_match_id IN (SELECT player_match_id FROM playermatch WHERE match_id = 1157);
DELETE FROM teamrating WHERE team_match_id IN (SELECT team_match_id FROM teammatch WHERE match_id = 1157);
DELETE FROM playermatch WHERE match_id = 1157;
DELETE FROM teammatch WHERE match_id = 1557;
DELETE FROM match WHERE match_id = 1557

