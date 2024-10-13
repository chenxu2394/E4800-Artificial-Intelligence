#
# Construct PDB heuristics for N-Puzzle

import Npuzzle

import queue


# Breadth-First Search (uninformed)
#
# Modify the breadth-first search algorithm to record the distances of
# all state from the initial state, and to return those distances.
# It is best to use a dictionary, so that distances of state can be
# recorded as distances[s] = ... and accessed as distances[s].

def breadthFirstSearch(initialstate):
    visited = dict()  # dictionary (hash table) for holding visited states
    #### YOUR CODE HERE ####
    distances = {}
    Q = queue.Queue(maxsize=0)  # first-in-first-out queue

    Q.put(initialstate)  # Insert the initial state in the queue
    visited[initialstate] = 1
    distances[initialstate] = 0
    while not Q.empty():
        state = Q.get()  # Next un-expanded state from the queue
        for aname, s, cost in state.successors():  # Go through all successors of state
            if s not in visited:  # Was the state visited already?
                visited[s] = 1
                distances[s] = cost + distances[state]
                #### YOUR CODE HERE ####
                #### YOUR CODE HERE ####
                #### YOUR CODE HERE ####
                Q.put(s)
    #### YOUR CODE HERE ####
    #### YOUR CODE HERE ####
    return distances


# Construct a PDB heuristic based on a subset of tiles
#
# makePDBheuristics takes as input
#
# - the goal state to which distance is estimated
# - the set of tiles that are to be included in the PDB
#
# makePDBheuristics returns a function that
#
# - takes a state as input
# - returns a lower bound estimate for the distance to the goal state

def makePDBheuristic(goalState, tiles):
    g_abstract = goalState.abstract(tiles)
    dis = breadthFirstSearch(g_abstract)

    # def func(s):
    #     s_abstract = s.abstract(tiles)
    #     return dis[s_abstract]

    return lambda s: dis[s.abstract(tiles)]


#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####


# Construct a PDB heuristics based on PDBs for two subsets of tiles
#
# This is like makePDBheuristics, except that two PDBs are constructed
# and used for deriving a lower bound distance estimate.
# Depending on whether the subsets intersect or not, the lower bounds
# from the two PDBs can be combined either by summing or by maximizing.
#
# makePDBheuristic2 return one function just like makePDBheuristic does.

def makePDBheuristic2(goalState, tiles1, tiles2):
    g1_abstract = goalState.abstract(tiles1)
    g2_abstract = goalState.abstract(tiles2)

    dis1 = breadthFirstSearch(g1_abstract)
    dis2 = breadthFirstSearch(g2_abstract)

    if not tiles1 & tiles2:
        def summing(s):
            return dis1[s.abstract(tiles1)] + dis2[s.abstract(tiles2)]
        return summing
    else:
        def maximizing(s):
            return max(dis1[s.abstract(tiles1)], dis2[s.abstract(tiles2)])
        return maximizing
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
