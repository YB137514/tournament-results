#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament


import psycopg2
import bleach
import random


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE from Matches")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE from Players")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(*) from Players")
    rows = c.fetchone()[0]
    DB.close()
    return rows


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.
    (This should be handled by your SQL database schema,
    not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    name = bleach.clean(name)
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT into Players(name) values (%s)", (name, ))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    deleteStandings()
    DB = connect()
    c = DB.cursor()
    c.execute(
        "INSERT into Standings( \
         player_ID, \
         name, \
         num_of_wins,\
         num_of_matches_played) \
         select ID, name, num_of_wins, matches_played \
         from StandingsView; \
         SELECT * from Standings")

    rows = c.fetchall()
    DB.commit()
    DB.close()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    winner = bleach.clean(winner)
    loser = bleach.clean(loser)
    DB = connect()
    c = DB.cursor()
    c.execute(
        "INSERT into Matches \
        (player_1_ID, \
         player_2_ID, \
         winner) \
         values (%s, %s, %s)", (winner, loser, winner))

    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    playerStandings()
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT player_id, name from Standings")
    rows = c.fetchall()
    DB.close()
    # See explanation of NearbyPairings in a Helper functions section below.
    zipped = NearbyPairings(rows)
    return zipped


# Below is a list of Helper functions used in Tournament.py and sim.py

def deleteStandings():
    """Helper function to remove current standings"""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE from Standings")
    DB.commit()
    DB.close()


def ChooseTwice(items):
    """This function chooses two distinct players randomly from the list.
    """
    a = random.choice(items)
    b = random.choice(items)
    # Since choosing is done with replacement code below accounts
    # for corner case when the same object is chosen twice
    while a == b:
        b = random.choice(items)
    return a, b


def RandomOrder(standings):
    """Generates a random order of 2-tuples in a list to simulate random drawing
    of players.
    Returns a list of 2-tuples.
    """
    pairings = []
    i = 1
    while i < len(standings):
        (one, two) = ChooseTwice(standings)
        pairings.append(one[0:2])
        pairings.append(two[0:2])
        standings.remove(one)
        standings.remove(two)

    return pairings


def NearbyPairings(rows):
    """NearbyPairings (rows) --Helper function that is used in swiss pairings.
    It takes a list of 2-tuples from the standings table as its argument
    and pairs adjacent players in the standings together.
    A resulting set of pairings is a list of 4-tuples which it returns.
    """
    # Collecting IDs of alternate players starting from first tuple.
    Alt_ID1 = []
    for i in xrange(0, len(rows), 2):
        Alt_ID1.append(rows[i][0])
    # Collecting names of alternate players starting from first tuple
    Alt_Names1 = []
    for i in xrange(0, len(rows), 2):
        Alt_Names1.append(rows[i][1])
    # Collecting IDs of alternate players starting from second tuple
    Alt_ID2 = []
    for i in xrange(1, len(rows), 2):
        Alt_ID2.append(rows[i][0])
    # Collecting names of alternate players starting from second tuple
    Alt_Names2 = []
    for i in xrange(1, len(rows), 2):
        Alt_Names2.append(rows[i][1])

    # Zipping into a list of 4-tuples with paired players
    zipped = zip(Alt_ID1, Alt_Names1, Alt_ID2, Alt_Names2)
    return zipped


def ChooseWinner(items):
    """Function to draw a  winner and a loser in a 4 tubple.
    Random winner and loser are passed to a
    ReportMatch(winner, loser) function and a result
    is recorded into Matches table
    """
    (a, _, b, _) = items
    paired_ids = (a, b)
    winner = random.choice(paired_ids)
    if winner == a:
        loser = b
    else:
        loser = a
    return winner, loser
