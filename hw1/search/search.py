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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    def dfs(problem, explored_state, stack_state, stack_action):
        if stack_state.isEmpty() == True: return False
        else:
            state = stack_state.list[-1]
            if problem.isGoalState(state): return True
            else:
                for successor in problem.getSuccessors(state):
                    s_state, s_action = successor[0], successor[1]
                    if (s_state not in explored_state) and (s_state not in stack_state.list):   
                        stack_state.push(s_state)
                        stack_action.push(s_action)
                        found = dfs(problem, explored_state, stack_state, stack_action)
                        if found: return True
            
            stack_state.pop()
            stack_action.pop()
            explored_state.append(state)
            return False

    explored_state  = []
    stack_state  = util.Stack()
    stack_action = util.Stack()
    stack_state.push(problem.getStartState())
    dfs(problem, explored_state, stack_state, stack_action)
    return stack_action.list
    
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    states  = []
    paths = []

    frontier = util.Queue()
    startState = problem.getStartState()
    frontier.push(startState)

    while frontier.isEmpty() == False:
        state = frontier.pop()

        if problem.isGoalState(state):
            index = states.index(state)
            return paths[index]

        for successor in problem.getSuccessors(state):
            s_state, s_action = successor[0], successor[1]
            path = [] if state == startState else paths[states.index(state)][:]
            if (s_state not in states) and (s_state == startState) == False:
                frontier.push(s_state)
                states.append(s_state)
                path.append(s_action)
                paths.append(path)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    costFn = problem.costFn if 'costFn' in dir(problem) else lambda x:1
    states  = []
    paths = []
    costs = []

    frontier = util.PriorityQueue()
    startState = problem.getStartState()
    frontier.push(startState, 0)

    while frontier.isEmpty() == False:
        state = frontier.pop()

        if problem.isGoalState(state):
            index = states.index(state)
            return paths[index]

        costNow = 0 if state == startState else costs[states.index(state)]
        for successor in problem.getSuccessors(state):
            s_state, s_action = successor[0], successor[1]
            path = [] if state == startState else paths[states.index(state)][:]
            cost = costFn(s_state) + costNow
            if (s_state not in states) and (s_state == startState) == False:
                frontier.push(s_state, cost)
                states.append(s_state)
                path.append(s_action)
                paths.append(path)
                costs.append(cost)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    costFn = problem.costFn if 'costFn' in dir(problem) else lambda x:1
    states  = []
    paths = []
    costs = []

    frontier = util.PriorityQueue()
    startState = problem.getStartState()
    frontier.push(startState, 0)

    while frontier.isEmpty() == False:
        state = frontier.pop()

        if problem.isGoalState(state):
            index = states.index(state)
            return paths[index]

        costNow = 0 if state == startState else costs[states.index(state)]
        for successor in problem.getSuccessors(state):
            s_state, s_action = successor[0], successor[1]
            path = [] if state == startState else paths[states.index(state)][:]
            cost = costFn(s_state) + costNow
            if (s_state not in states) and (s_state == startState) == False:
                frontier.push(s_state, cost + heuristic(s_state, problem))
                states.append(s_state)
                path.append(s_action)
                paths.append(path)
                costs.append(cost)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
