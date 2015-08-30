-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- For now, recreate the database every time
DROP DATABASE tournament;
CREATE DATABASE tournament;
-- Connect to the database
\c tournament

-- Just a test for now
CREATE TABLE players (
	id		serial	PRIMARY KEY,
	name	text
);

-- Some sample data
INSERT INTO players(name) VALUES('Amy');
INSERT INTO players(name) VALUES('Ender');

SELECT * FROM players;

-- Disconnect from the database
\c vagrant
