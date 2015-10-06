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

This project includes a Vagrant environment including everything necessary. To use it, install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/downloads), and follow the project installation steps bellow.

Alternatively, you may install a [Python](http://www.python.org/) environment with psycopg2, and [PostgreSQL](http://www.postgresql.org/). But note that this has not been tested, and you may have to follow additional steps or make changes to some of the files.


Usage
-----



Installation
------------

After installing VirtualBox and Vagrant, do the following on the terminal:

1) Clone the project (if you don't have git, you may download the project from github).

```
$ git clone git@github.com:pt314/udacity-fsnd-p2-tournament.git
```

2) Start the virtual machine (the first time will take a while to download and setup things).

```
$ cd udacity-fsnd-p2-tournament/vagrant
$ vagrant up
```

3) Connect to the virtual machine.

```
$ vagrant ssh
$ cd /vagrant/tournament
```

  (Use ```vagrant halt``` to turn it off.)

4) Install the database.

```
$ psql
vagrant=> \i tournament.sql
```

5) Update scores configuration, by updating the scores in the ```scores_config```.

This is optional. The default configuration, which is used by chess and other games, gives 1 point for a win or bye, 0.5 for a draw, and 0 for a loss. Other games use different values.
