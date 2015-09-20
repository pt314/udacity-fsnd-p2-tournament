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
	id			serial	PRIMARY KEY,
	winner_id	integer REFERENCES players(id),
	loser_id	integer REFERENCES players(id),
	CHECK		(winner_id != loser_id)
);

CREATE VIEW standings AS
SELECT p.id, p.name,
	(
		SELECT COUNT(*) FROM matches
		WHERE winner_id = p.id
	) wins,
	count(m.*) matches
FROM players p
LEFT JOIN matches m ON p.id IN (m.winner_id, m.loser_id)
GROUP BY p.id
ORDER BY wins DESC, p.name ASC;


-- Some sample data
INSERT INTO players(name) VALUES('Amy');
INSERT INTO players(name) VALUES('Ender');
--INSERT INTO players(name) VALUES('Kent');

-- Test with invalid players
-- TODO: create tests in python code
INSERT INTO matches(winner_id, loser_id) VALUES(1, 1);
INSERT INTO matches(winner_id, loser_id) VALUES(3, 1);
INSERT INTO matches(winner_id, loser_id) VALUES(1, 3);

SELECT * FROM players;
SELECT * FROM matches;
