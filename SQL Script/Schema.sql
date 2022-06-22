CREATE DATABASE MSIII_2;
USE MSIII_2;

CREATE TABLE club(
club_name	VARCHAR(100)	NOT NULL	PRIMARY KEY, 
stadium_name	VARCHAR(100),
club_website	VARCHAR(150),  
FOREIGN KEY (stadium_name) REFERENCES stadium(std_name)
);

CREATE TABLE stadium(
std_name	VARCHAR(100)	NOT NULL	PRIMARY KEY,
std_address	VARCHAR(150),
std_building_date	VARCHAR(20),
std_record_attendance	VARCHAR(700),
std_capacity	VARCHAR(50),
std_pitch_height	VARCHAR(25),
std_pitch_width	VARCHAR(25));

CREATE TABLE player(
pl_name	VARCHAR(50)	NOT NULL,
pl_nationality	VARCHAR(100),
pl_date_birth	VARCHAR(50),
pl_position	VARCHAR(100),
pl_height	VARCHAR(50),
PRIMARY KEY (pl_name, pl_date_birth));

CREATE TABLE player_hist(
player_name	VARCHAR(50)	NOT NULL,
hist_club_name	VARCHAR(100)	NOT NULL,
season VARCHAR(50),
date_birth	VARCHAR(50),
PRIMARY	KEY	(player_name, date_birth, hist_club_name, season),
FOREIGN KEY (player_name, date_birth) REFERENCES player(pl_name, pl_date_birth),
FOREIGN	KEY	(hist_club_name) REFERENCES	club(club_name));

CREATE TABLE league_match (
match_date	VARCHAR(50)	NOT NULL,
match_season	VARCHAR(50),
match_team_home_name	VARCHAR(100)	NOT NULL,
match_team_away_name	VARCHAR(100)	NOT NULL,
match_result	VARCHAR(20),
PRIMARY KEY (match_date, match_team_home_name, match_team_away_name),
FOREIGN KEY	(match_team_home_name) REFERENCES club(club_name),
FOREIGN KEY	(match_team_away_name) REFERENCES club(club_name));

CREATE TABLE match_statistics (
mtch_date	VARCHAR(50)	NOT NULL,
mtch_season VARCHAR(50) NOT NULL,
clb_name_home	VARCHAR(100)	NOT	NULL,
clb_name_away	VARCHAR(100)	NOT	NULL,
possession_home	VARCHAR(10),
possession_away	VARCHAR(10),
goals_home	VARCHAR(10),
goals_away	VARCHAR(10),
shots_home	VARCHAR(10),
shots_away	VARCHAR(10),
fouls_home	VARCHAR(10),
fouls_away	VARCHAR(10),
yellow_cards_home	VARCHAR(10),
yellow_cards_away	VARCHAR(10),
red_cards_home	VARCHAR(10),
red_cards_away	VARCHAR(10),
PRIMARY KEY (mtch_date, clb_name_home, clb_name_away),
FOREIGN KEY	(mtch_date, clb_name_home, clb_name_away)	REFERENCES league_match(match_date, match_team_home_name, match_team_away_name),
FOREIGN KEY	(clb_name_home) REFERENCES	club(club_name),
FOREIGN KEY (clb_name_away) REFERENCES club(club_name));

CREATE	TABLE fan (
fan_email	VARCHAR(25)	NOT	NULL	PRIMARY KEY,
fan_username	VARCHAR(25) NOT NULL UNIQUE,
fan_password	VARCHAR(50) NOT NULL,
fan_gender	CHAR,
fan_birthdate	VARCHAR(50),
fan_fav_club_name	VARCHAR(100),
FOREIGN KEY (fan_fav_club_name) REFERENCES club(club_name));

CREATE TABLE	fan_review (
fn_email	VARCHAR(25)	NOT NULL,
mt_date	VARCHAR(50)	NOT	NULL,
mt_home	VARCHAR(100) NOT NULL,
mt_away	VARCHAR(100) NOT NULL,
rating	INT,
text_rev	VARCHAR(150),
CHECK (rating >= 0 AND rating <= 10),
PRIMARY KEY	(fn_email, mt_date, mt_home, mt_away),
FOREIGN KEY (fn_email) REFERENCES fan(fan_email),
FOREIGN KEY (mt_date, mt_home, mt_away) REFERENCES	league_match(match_date, match_team_home_name, match_team_away_name));

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\stadium.csv'
IGNORE INTO TABLE msiii_2.stadium
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\club.csv'
IGNORE INTO TABLE msiii_2.club
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\player.csv'
IGNORE INTO TABLE msiii_2.player
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\player_hist.csv'
IGNORE INTO TABLE msiii_2.player_hist
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\league_match.csv'
IGNORE INTO TABLE msiii_2.league_match
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\match_stats.csv'
IGNORE INTO TABLE msiii_2.match_statistics
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';