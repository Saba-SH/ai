# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from curses import newpad
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

class DoublyNode:
    def __init__(self, state):
        self.state = state
        self.prev = None
        self.next = None

    def __init__(self, state, prev, next):
        self.state = state
        self.prev = prev
        self.next = next

class Path:
    def __init__(self, start : DoublyNode):
        self.start = start

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def defese(problem, start, curr_stack : util.Stack, visited : set):
    if problem.isGoalState(start):
        return curr_stack.list
    
    visited.add(start)

    succ = problem.getSuccessors(start)
    succ.reverse()

    if succ == []:
        return None

    for triple in succ:     # triple : successor, action, stepCost
        if triple[0] not in visited:
            curr_stack.push(triple[1])
            res = defese(problem, triple[0], curr_stack, visited)
            if res is not None:
                return res
            curr_stack.pop()

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    return defese(problem, problem.getStartState(), util.Stack(), set())
    
    
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    ueue = util.Queue()     # queue of paths of triples
    visited = set()
    visited.add(problem.getStartState())
    ueue.push([[problem.getStartState(), 0, 0]])

    while not ueue.isEmpty():
        curr_path = ueue.pop()
        curr_state = curr_path[-1][0]
        if problem.isGoalState(curr_state):
            return [triple[1] for triple in curr_path[1:]]

        succ = problem.getSuccessors(curr_state)
        
        for triple in succ:      # triple : successor, action, stepCost
            if triple[0] not in visited:
                ueue.push(curr_path + [triple])
                visited.add(triple[0])


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    ueue = util.PriorityQueue()         # queue of paths of triples ordered by their costs
    ueue.push([], 0)
    visited = set()

    while not ueue.isEmpty():
        cheap_path = ueue.pop()
        path_last_state = cheap_path[-1][0] if len(cheap_path) > 0 else problem.getStartState()
        
        if problem.isGoalState(path_last_state):
            return [triple[1] for triple in cheap_path]
        
        if path_last_state not in visited:
            visited.add(path_last_state)
            succ = problem.getSuccessors(path_last_state)

            for triple in succ:         # triple : successor, action, stepCost
                new_path = cheap_path + [triple]
                ueue.push(new_path, sum(triple[2] for triple in new_path))

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    ueue = util.PriorityQueue()         # queue of paths of triples ordered by their costs
    ueue.push([], heuristic(problem.getStartState(), problem))
    visited = dict()        # map visited states to lengths of paths to them

    path_cost = lambda path : (sum(triple[2] for triple in path) + (heuristic(path[-1][0], problem)) if len(path) > 0 else heuristic(problem.getStartState(), problem))

    while not ueue.isEmpty():
        cheap_path = ueue.pop()
        path_last_state = cheap_path[-1][0] if len(cheap_path) > 0 else problem.getStartState()

        if problem.isGoalState(path_last_state):
            return [triple[1] for triple in cheap_path]

        if path_last_state not in visited or visited[path_last_state] > path_cost(cheap_path):      # no need for the second check in case of a consistent heuristic, right?
            visited[path_last_state] = path_cost(cheap_path)
            succ = problem.getSuccessors(path_last_state)

            for triple in succ:         # triple : successor, action, stepCost
                new_path = cheap_path + [triple]
                ueue.push(new_path, path_cost(new_path))

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
