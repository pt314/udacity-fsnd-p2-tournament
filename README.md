rdb-fullstack
=============

Common code for the Relational Databases and Full Stack Fundamentals courses


Project 2: Tournament Results
-----------------------------

Swiss system tournament.

There are many Swiss system variations. For more information, refer to:
https://en.wikipedia.org/wiki/Swiss-system_tournament

Tournament rules to be used in this project:

- Given n players, the number of rounds of a tournament is log base 2 of n.
- A win is worth 1 point, a loss is worth 0 points, and a draw is worth 0.5 points.
- On the first round, players are paired randomly.
- On subsequent rounds, players are paired with other players with similar scores, avoiding rematches.
  - At each step, the pairing algorithm picks an unmatched player with highest score,
    and pairs it with the next player with highest score that has never been an opponent.
    (Usually there should be such a player, since the number of rounds is small.)

Features
--------

- Draws are possible.

TODO
----

- Prevent rematches between players.
- Allow an odd number of players, giving a bye to a player on each round, and avoiding multiple byes.
- When two players have the same number of wins, they are according to the total number of wins by players they have played against.
- Support multiple tournaments.


Technical details
-----------------

Usage:

- Go to the vagrant/tournament directory
- Start vagrant VM: `vagrant up`
- Connect to the VM: `vagrant ssh`
- Start psql CLI: `psql`
- Build the database: `\i tournament.sql`

Tables:

- players
- matches

Views:

- standings
