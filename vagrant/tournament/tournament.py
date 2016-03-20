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
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(*) FROM players;")
    num = c.fetchall()[0][0]
    db.close()

    return num


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s);", (name,))
    db.commit()
    db.close()


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
    db = connect()
    c = db.cursor()
    c.execute("SELECT * FROM standings;")
    standings = [(row[0], row[1], row[2], row[3]) for row in c.fetchall()]
    db.close()

    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s,%s);",
        (winner, loser))
    db.commit()
    db.close()

def isRematch(player1, player2):
    """Returns true if players have already competed against each other

    Args:
      player 1: the id number of one player
      player 2: the id number of the other player
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT * FROM matches WHERE winner = %s AND loser = %s \
        OR winner = %s AND loser = %s;", (player1, player2, player2, player1))
    rows = len(c.fetchall())
    db.close()

    if rows == 0:
        return False
    return True

def appendToPairings(pairings, standings, remaining, j):
    """Appends a tuple of pairs of players to the pairings list

    Args:
      pairings: the current list of pairings
      standings: the current list of standings
      remaining: the current list of players unassigned
      j: the index of the opponent in remaining
    """
    pairings.append((standings[remaining[0]][0],
                     standings[remaining[0]][1],
                     standings[remaining[j]][0],
                     standings[remaining[j]][1]))

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player whom they have not yet faced and who has an equal or nearly-equal
    win record, that is, a player adjacent to him or her in the standings. If
    the player has faced all opponents already, only then can they engage in
    a rematch.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    # Track the players not yet assigned with the 'remaining' list
    remaining = range(len(standings))
    pairings = []

    for i in range(len(standings)/2):
        # Keep track of the initial length of our list for remaining players
        initial = len(remaining)
        # Try pairing the first player in our list with the opponent who:
        # 1) Has not yet faced the player, and then
        # 2) Is closest in score
        for j in range(initial):
            # Don't bother competing against oneself
            # Check to see if this matchup would be a rematch
            if j != 0 and not isRematch(standings[remaining[0]][0],
                                        standings[remaining[j]][0]):
                # If not a rematch, construct the tuple!
                appendToPairings(pairings, standings, remaining, j)
                # and remove the players from the list of those remaining
                remaining.remove(remaining[j])
                remaining = remaining[1:]
                break
        # If the above loop hasn't decreased the length of our list of
        # remaining players, it means that all the opponents have faced the
        # first player in our list. So just play against the one who is closest
        # in score.
        if len(remaining) == initial:
            appendToPairings(pairings, standings, remaining, 1)
            # Remove the first two in the list, as they would be the ones
            # with highest score and thus playing against each other
            remaining = remaining[2:]

    return pairings
