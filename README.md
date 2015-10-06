Project 2: Tournament Results
=============================

This project uses a simple database to keep track of players and matches in a game tournament. The tournament uses the
[Swiss system](https://en.wikipedia.org/wiki/Swiss-system_tournament) for pairing the players in each round.

There are many variations of the system, but basically: players are matched with other players with similar scores, no players are eliminated, and the number of rounds required to decide the winner is small (usually log base 2 of n or less).

The pairing algorithm used in this project is simple: after giving a skipping a player if the number of players is odd, adjacent players are matched in the list of players sorted by score.


Extra features
--------------

- Support for draws (tied games). For each player, the result of a match is either win, lose, or draw.
- Support for an odd number of players. A player with lowest score gets a bye (skipped round) on each round, and each player can receive at most one bye.
- The scores players get for wins, losses, draws, and byes can be configured.


Things that would be nice
-------------------------

- Prevent rematches between players.
- When two players have the same number of wins, use OMW (Opponent Match Wins) to break ties.
- Add randomnes to pairing algorithm. For example, if several players have the same score, choose a random pair to match.
- Support multiple tournaments. Currently, the database is for one tournament, and tables must be cleared before a new tournament.


Requirements
------------


Usage
-----


Installation
------------

- Go to the vagrant/tournament directory
- Start vagrant VM: `vagrant up`
- Connect to the VM: `vagrant ssh`
- Start psql CLI: `psql`
- Build the database: `\i tournament.sql`
