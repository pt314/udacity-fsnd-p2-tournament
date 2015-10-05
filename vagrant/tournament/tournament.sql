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
	result		varchar(4),
	FOREIGN KEY	(match_id, player_id) REFERENCES match_players(match_id, player_id),
	CHECK		(result IN ('win', 'lose'))
);

CREATE VIEW standings AS
SELECT p.id, p.name,
	(
		SELECT COUNT(*) FROM match_results
		WHERE player_id = p.id
		AND result = 'win'
	) wins,
	count(r.*) matches
FROM players p
LEFT JOIN match_results r ON p.id = r.player_id
GROUP BY p.id
ORDER BY wins DESC, p.name ASC, p.id ASC;


-- Some sample data
INSERT INTO players(name) VALUES('Amy');
INSERT INTO players(name) VALUES('Ender');
INSERT INTO players(name) VALUES('Kent');

SELECT * FROM players;
SELECT * FROM matches;
