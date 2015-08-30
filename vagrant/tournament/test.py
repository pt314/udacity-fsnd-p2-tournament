#!/usr/bin/env python
#
# Temporary test file for tournament.py

from tournament import *

registerPlayer("Turtle")

num_players = countPlayers()
print("Number of players: " + str(num_players))

reportMatch(1, 2)
reportMatch(2, 3)
reportMatch(3, 1)
