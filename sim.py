
from tournament import *
import math

# Swiss style tournament simulation.

deleteMatches()
deletePlayers()

# Example of a list of players to be entered into the tournament.
# Any even number of players can be entered into a tournament by
# substituting list below with user list.

names = ["A", "B", "C", "D", "E",
         "A", "G", "H", "I", "J",
         "K", "L", "C", "N", "O",
         "P"]


# Register all players in the database
for name in names:
    registerPlayer(name)

# Calculate mathematical facts needed to play the tournament:
# Total number of players
player_count = countPlayers()
# Calculate total number of rounds in Swiss style tournament
rounds_num = math.log(player_count, 2)
# Calculate total number of matches played in a Swiss style tournament
total_matches = (rounds_num * player_count) / 2
# Player standings before first match
standings = playerStandings()


# Main simulation code.
# Random drawing and pairings of players before first round
Random_pairings = RandomOrder(standings)
# Organizing pairings of players in a 4 tuple
Random_pairings = NearbyPairings(Random_pairings)

# Main Loop to simulate rounds of a tournament
for i in xrange(0, int(rounds_num), 1):
    # Playing one round of games
    for pair in Random_pairings:
        (winner, loser) = ChooseWinner(pair)
        reportMatch(winner, loser)
    # After each round create new pairing based on standings
    Random_pairings = swissPairings()

# Final standings after the last round
standings = playerStandings()

print "Winning player is:", standings[0][1], ", \
having ID_number:", standings[0][0]
print "Final standings are:"
for standing in standings:
    print standing
