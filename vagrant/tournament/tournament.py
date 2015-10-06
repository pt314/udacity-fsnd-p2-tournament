#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def readScoresConfig():
    """Returns the scores that a player gets for each possible result.

    Returns:
      A map, with one entry for each possible result, where:
        key: a possible match result 
        value: the score given to a player for obtaining that result
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM scores_config")
    results = c.fetchall()
    conn.close()

    result_scores = {}
    for row in results:
        result_scores[row[0]] = row[1]
    return result_scores


def deleteMatches():
    """Remove all the match and bye records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM match_results")
    c.execute("DELETE FROM match_players")
    c.execute("DELETE FROM matches")
    c.execute("DELETE FROM byes")
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

    Returns:
      The new player's id.
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players(name) VALUES(%s) RETURNING id", (name,))
    player_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    return player_id


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


def reportBye(player_id):
    """Records a bye for a player.
  
    Args:
      player_id: the player's id.
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO byes(player_id) VALUES(%s)", (player_id,))
    conn.commit()
    conn.close()


def playerByes():
    """Returns the list of ids for players with byes."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM byes")
    results = c.fetchall()
    bye_player_ids = set([x[0] for x in results])
    conn.close()
    return bye_player_ids


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


def swissPairingsBye(standings):
    """Repots a bye if the number of players is odd, before pairing the other players.
  
    A bye is given to a player with lowest score and no bye so far.
  
    Args:
      standings: standings in the format returned by playerStandings()

    Returns:
      Updated standings with the bye player removed.
    """
    # If number of payers is even, no bye is given
    if len(standings) % 2 == 0:
        return standings

    # Get previous byes
    bye_player_ids = playerByes()

    # For the next bye, select a player with lowest score and no bye
    for player in reversed(standings):
        if player[0] not in bye_player_ids:
            standings.remove(player)
            reportBye(player[0])
            break

    # Return the standings for the remaining players to be matched
    return standings


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    If the are a odd number of players registered, a bye is given to one of the
    players, and the remaining players are paired as if the number was even.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []

    standings = playerStandings()

    # Report bye if necessary
    standings = swissPairingsBye(standings)
    
    # Match remaining players
    for i in range(0, len(standings), 2):
        player1_id = standings[i][0]
        player1_name = standings[i][1]
        player2_id = standings[i + 1][0]
        player2_name = standings[i + 1][1]
        pair = (player1_id, player1_name, player2_id, player2_name)
        pairings.append(pair)
    
    return pairings
