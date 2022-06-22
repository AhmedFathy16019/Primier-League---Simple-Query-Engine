-- Add a new user review on a match
INSERT INTO fan_review
VALUES ("");

-- Show all the players from a certain nationality and their home teams history
SELECT player_name, hist_club_name, pl_nationality
FROM	player_hist
INNER JOIN player
ON player.pl_name = player_hist.player_name AND player.pl_date_birth = player_hist.date_birth
WHERE pl_nationality = 'England';

-- Show the top 10 teams by matches won
SELECT mt_won.clb_name_home, COUNT(*)
FROM 
(SELECT clb_name_home 
FROM match_statistics
WHERE goals_home > goals_away
UNION ALL
SELECT clb_name_away
FROM match_statistics
WHERE goals_home < goals_away) AS mt_won
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;

-- Show the top 10 teams by home matches won
SELECT COUNT(*), clb_name_home
FROM match_statistics
WHERE goals_home > goals_away
GROUP BY clb_name_home
ORDER BY 1 DESC
LIMIT 10;

-- Show the top 10 teams by yellow cards 
SELECT mt_yellow.clb_name_home, SUM(mt_yellow.cards)
FROM 
(SELECT clb_name_home, SUM(yellow_cards_home) AS cards
FROM match_statistics
GROUP BY 1
UNION ALL
SELECT clb_name_away, SUM(yellow_cards_away) AS cards
FROM match_statistics
GROUP BY 1) AS mt_yellow
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;

-- Show the top 10 teams by fouls
SELECT mt_foul.clb_name_home, SUM(mt_foul.fouls)
FROM 
(SELECT clb_name_home, SUM(fouls_home) AS fouls
FROM match_statistics
GROUP BY 1
UNION ALL
SELECT clb_name_away, SUM(fouls_away) AS fouls
FROM match_statistics
GROUP BY 1) AS mt_foul
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;

-- Show the top 10 teams by shots
SELECT mt_shot.clb_name_home, SUM(mt_shot.shots)
FROM 
(SELECT clb_name_home, SUM(shots_home) AS shots
FROM match_statistics
GROUP BY 1
UNION ALL
SELECT clb_name_away, SUM(shots_away) AS shots
FROM match_statistics
GROUP BY 1) AS mt_shot
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;

-- Show all the teams who won the most games by season
SELECT mt_won.clb_name_home, mt_won.mtch_season, mt_won.season_wins
FROM 
(SELECT clb_name_home, mtch_season, COUNT(*) AS season_wins
FROM match_statistics
WHERE goals_home > goals_away
GROUP BY 1, 2
UNION ALL
SELECT clb_name_away, mtch_season, COUNT(*) AS season_wins
FROM match_statistics
WHERE goals_home < goals_away
GROUP BY 1,2
ORDER BY 3 DESC) AS mt_won
GROUP BY 2;

-- Query and view a given team information
SELECT *
FROM club
WHERE club.club_name = 'Arsenal';

-- Query and view a given player information (by their first and last name)
SELECT *
FROM player
WHERE pl_name = '';

-- Identify the home team for a given stadium name
SELECT club.club_name
FROM club
WHERE club.stadium_name = '';

-- Show all the players who played a certain position
SELECT *
FROM player
WHERE player.pl_position = '';

-- Identify all the teams in a given city in the UK
Select club.club_name
FROM club INNER JOIN stadium
ON club.stadium_name = stadium.std_name
WHERE std_address LIKE '%Liverpool%';