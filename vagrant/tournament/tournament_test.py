#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDeletePlayers():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, score1, matches1), (id2, name2, score2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or score1 != 0.0 or score2 != 0.0:
        raise ValueError(
            "Newly registered players should have no matches and should have a zero score.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch((id1, 'win'), (id2, 'lose'))
    reportMatch((id3, 'draw'), (id4, 'draw'))
    result_scores = readScoresConfig()
    standings = playerStandings()
    for (i, n, s, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1,) and s != result_scores['win']:
            raise ValueError("Each match winner should have a score of "
                + str(result_scores['win']) + ".")
        elif i in (id2,) and s != result_scores['lose']:
            raise ValueError("Each match loser should have a score of "
                + str(result_scores['lose']) + ".")
        elif i in (id3, id4) and s != result_scores['draw']:
            raise ValueError("Each player with a draw should have a score of "
                + str(result_scores['draw']) + ".")
    print "7. After a match, players have updated standings."


def testReportBye():
    deleteMatches()
    deletePlayers()
    id1 = registerPlayer("A")
    id2 = registerPlayer("B")
    id3 = registerPlayer("C")
    reportBye(id1)
    result_scores = readScoresConfig()
    standings = playerStandings()
    for (i, n, s, m) in standings:
        if m != 0:
            raise ValueError("Each player should have zero matches recorded.")
        if i in (id1,) and s != result_scores['bye']:
            raise ValueError("Each player with a bye should have a score of "
                + str(result_scores['bye']) + ".")
        elif i in (id2, id3) and s != 0.0:
            raise ValueError("Each player without a bye should have a score of 0.0.")
    print "8. After a bye, players have correct scores."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch((id1, 'win'), (id2, 'lose'))
    reportMatch((id3, 'win'), (id4, 'lose'))
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "9. After one match, players with one win are paired."


def testPairingsWithByes():
    deleteMatches()
    deletePlayers()
    registerPlayer("A")
    registerPlayer("B")
    registerPlayer("C")

    # Initial standings
    standings = playerStandings()
    [id1, id2, id3] = [row[0] for row in standings]

    # First round
    pairings = swissPairings()
    if len(pairings) != 1:
        raise ValueError(
            "For three players, swissPairings should return one pair.")
    byes = playerByes()
    if len(byes) != 1 and byes != [id3]:
        raise ValueError(
            "Only the lowest player without a bye should receive a bye.")
    reportMatch((id1, 'win'), (id2, 'lose'))

    # Second round
    pairings = swissPairings()
    if len(pairings) != 1:
        raise ValueError(
            "For three players, swissPairings should return one pair.")
    byes = playerByes()
    if len(byes) != 2 and set(byes) != set([id3, id2]):
        raise ValueError(
            "Only the lowest player without a bye should receive a bye.")
    reportMatch((id1, 'win'), (id3, 'lose'))

    # Third round
    pairings = swissPairings()
    if len(pairings) != 1:
        raise ValueError(
            "For three players, swissPairings should return one pair.")
    byes = playerByes()
    if len(byes) != 2 and set(byes) != set([id3, id2, id1]):
        raise ValueError(
            "Only the lowest player without a bye should receive a bye.")
    reportMatch((id1, 'win'), (id3, 'lose'))

    print "10. For several matches, byes are assigned correctly."


if __name__ == '__main__':
    testDeleteMatches()
    testDeletePlayers()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testReportBye()
    testPairings()
    testPairingsWithByes()
    print "Success!  All tests pass!"
