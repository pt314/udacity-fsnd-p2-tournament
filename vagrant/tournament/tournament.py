#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM match_results")
    c.execute("DELETE FROM match_players")
    c.execute("DELETE FROM matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM players")
    results = c.fetchall()
    conn.close()
    return results[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players(name) VALUES(%s)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM standings")
    results = c.fetchall()
    conn.close()
    return results

def reportMatch(player1_result, player2_result):
    """Records the outcome of a single match between two players.

    There are two valid cases:
      1) One player wins and the other loses.
      2) Both player draw.

    Args:
      player1_result:  (player id, ['win', 'lose', 'draw'])
      player2_result:  (player id, ['win', 'lose', 'draw'])
    """
    # Check for right combination of results
    results = (player1_result[1], player2_result[1])
    if results not in [('win', 'lose'), ('lose', 'win'), ('draw', 'draw')]:
        raise ValueError("Invalid results")

    conn = connect()
    c = conn.cursor()

    # Create match
    c.execute("INSERT INTO matches DEFAULT VALUES RETURNING id")
    match_id = c.fetchone()[0]

    # Add players to match
    c.execute("INSERT INTO match_players (match_id, player_id) VALUES (%s, %s)",
        (match_id, player1_result[0]))
    c.execute("INSERT INTO match_players (match_id, player_id) VALUES (%s, %s)",
        (match_id, player2_result[0]))

    # Record match results
    c.execute("INSERT INTO match_results (match_id, player_id, result) VALUES (%s, %s, %s)",
        (match_id, player1_result[0], player1_result[1]))
    c.execute("INSERT INTO match_results (match_id, player_id, result) VALUES (%s, %s, %s)",
        (match_id, player2_result[0], player2_result[1]))

    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []

    standings = playerStandings()

    for i in range(0, len(standings), 2):
        player1_id = standings[i][0]
        player1_name = standings[i][1]
        player2_id = standings[i + 1][0]
        player2_name = standings[i + 1][1]
        pair = (player1_id, player1_name, player2_id, player2_name)
        pairings.append(pair)
    
    return pairings


def playerMatches():
    """Returns a map with all the players that have been matched with each player.

    Returns:
      A map, with one entry for each player
        key: player's unique id
        value: a list ids of all the players that have played with the player
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM matches")
    results = c.fetchall()
    conn.close()

    matches = {}
    for match in results:
        id1 = match[1]
        id2 = match[2]

        # init lists if necessary
        if not id1 in matches:
            matches[id1] = []
        if not id2 in matches:
            matches[id2] = []

        # add players to each other's lists
        matches[id1].append(id2)
        matches[id2].append(id1)

    return matches
