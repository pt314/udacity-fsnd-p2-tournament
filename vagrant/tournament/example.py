from tournament import *

# Clear data before a new tournament
deleteMatches()
deletePlayers()

# Register players
registerPlayer("Peter Pan")
registerPlayer("James Bond")
registerPlayer("Snow White")
registerPlayer("Chess Master")
registerPlayer("Cookie Monster")

# Generate pairings for first round (a bye is given automatically)
pairings = swissPairings()
print("Pairings:")
for pair in pairings:
    print(pair)

# Report results for first round
reportMatch((pairings[0][0], 'win'), (pairings[0][2], 'lose'))
reportMatch((pairings[1][0], 'draw'), (pairings[1][2], 'draw'))

# See current standings
standings = playerStandings()
print("Standings:")
for player in standings:
    print(player)

# Generate pairings for second round...
# (Repeat for the desired number of rounds, usually log base 2 of n times)
pairings = swissPairings()
