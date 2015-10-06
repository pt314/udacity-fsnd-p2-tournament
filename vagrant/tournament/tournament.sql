-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Disconnect from the database
\c vagrant

-- For now, recreate the database every time
DROP DATABASE tournament;
CREATE DATABASE tournament;

-- Connect to the database
\c tournament

-- Stores the number of points a player can get on a match for each
-- type of result (win, lose, or draw), and the number of points a
-- player can get for receiving a bye.
-- The types of results are fixed, but the scores can be customized
-- for games that use different values.
CREATE TABLE scores_config (
	result	varchar(4) PRIMARY KEY,
	score	real,
	CHECK	(result IN ('win', 'lose', 'draw', 'bye'))
);

-- Default scores config (used for many games such as chess).
INSERT INTO scores_config (result, score) VALUES('win', 1);
INSERT INTO scores_config (result, score) VALUES('lose', 0);
INSERT INTO scores_config (result, score) VALUES('draw', 0.5);
INSERT INTO scores_config (result, score) VALUES('bye', 1);



CREATE TABLE players (
	id		serial	PRIMARY KEY,
	name	text
);

CREATE TABLE matches (
	id			serial	PRIMARY KEY
);

-- TODO: Add constraint: A match can only hav two players.
CREATE TABLE match_players (
	match_id	integer	REFERENCES matches(id),
	player_id	integer REFERENCES players(id),
	PRIMARY KEY	(match_id, player_id)
);

-- Includes match results (wins, losses, draws).
CREATE TABLE match_results (
	match_id	integer	REFERENCES matches(id),
	player_id	integer	REFERENCES players(id),
	result		varchar(4)	REFERENCES scores_config(result),
	PRIMARY KEY	(match_id, player_id),
	FOREIGN KEY (match_id, player_id) REFERENCES match_players(match_id, player_id),
	CHECK		(result IN ('win', 'lose', 'draw'))
);

CREATE TABLE byes (
	player_id	integer	PRIMARY KEY	REFERENCES players(id)
);

-- List of player results, including a row for each win, loss, draw, and bye.
CREATE VIEW player_results AS
SELECT p.id, p.name, m.result AS result, s.score, m.match_id AS match_id
	FROM players p
	JOIN match_results m on p.id = m.player_id
	JOIN scores_config s on s.result = m.result
UNION ALL
SELECT p.id, p.name, 'bye' AS result, s.score, NULL AS match_id
	FROM players p
	JOIN byes b on p.id = b.player_id
	JOIN scores_config s on s.result = 'bye'
ORDER BY id ASC, match_id ASC;


-- Player standings, including total score and number of matches.
-- Byes counted in score, but not in matches.
CREATE VIEW standings AS
SELECT p.id, p.name, COALESCE(SUM(r.score), 0) AS score, COUNT(r.match_id) AS matches
FROM players p
LEFT JOIN player_results r ON p.id = r.id
GROUP BY p.id
ORDER BY score DESC, p.name ASC, p.id ASC;


-- Some sample data
INSERT INTO players(name) VALUES('Amy');
INSERT INTO players(name) VALUES('Ender');
INSERT INTO players(name) VALUES('Kent');

SELECT * FROM players;
SELECT * FROM matches;
