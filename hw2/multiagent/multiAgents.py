# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        if successorGameState.isWin(): return 1000
        score = successorGameState.getScore()
        
        # Food part
        newFoodNum = successorGameState.getNumFood()
        score -= newFoodNum * 10

        nearestFoodDistance = 1000
        for x in range(newFood.width):
            for y in range(newFood.height):
                if (newFood[x][y] ==  True):
                    newDistance = util.manhattanDistance(newPos, (x, y))
                    nearestFoodDistance = min(nearestFoodDistance, newDistance)
        score -= nearestFoodDistance
        
        # Ghost part
        newGhostPos = [ghostState.configuration.getPosition() for ghostState in newGhostStates]
        for id, ghostPos in enumerate(newGhostPos):
            distance = util.manhattanDistance(newPos, ghostPos)
            if distance < 5:
                if newScaredTimes[id] > 0: score -= distance*5
                else: score += distance*5
        
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        agentNum = gameState.getNumAgents()
        agentId_next = 1 # self.index = 0

        actions = gameState.getLegalActions(self.index)
        gameStateSuccessors = [ gameState.generateSuccessor(self.index, action) for action in actions]
        scores = [self.miniMaxSearch(agentId_next, agentNum, successor, self.depth) for successor in gameStateSuccessors]
        
        score_wanted = max(scores)
        action_wanted = actions[scores.index(score_wanted)]
        return action_wanted
      
    def miniMaxSearch(self, agentId, agentNum, gameState, depth):
        agentId_next = (agentId + 1) % agentNum
        depth = (depth - 1) if (agentId_next == 0) else depth
        if depth == 0:
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(agentId)
        if len(actions) == 0: return self.evaluationFunction(gameState)
        gameStateSuccessors = [ gameState.generateSuccessor(agentId, action) for action in actions]
        scores = [self.miniMaxSearch(agentId_next, agentNum, successor, depth) for successor in gameStateSuccessors]

        maxMode = (agentId == 0)
        score_wanted = max(scores) if maxMode else min(scores)
        return score_wanted


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        agentNum = gameState.getNumAgents()
        agentId_next = 1 # self.index = 0

        actions = gameState.getLegalActions(self.index)
        gameStateSuccessors = [ gameState.generateSuccessor(self.index, action) for action in actions]
        
        alpha, beta = -9999999, 9999999
        v = -9999999
        action_wanted = Directions.STOP
        for i, successor in enumerate(gameStateSuccessors):
            successor_value = self.alphaBetaSearch(alpha, beta, agentId_next, agentNum, successor, self.depth)
            v = max(v, successor_value)
            if alpha < v:
                alpha = v
                action_wanted = actions[i]
    
        return action_wanted

    def alphaBetaSearch(self, alpha, beta, agentId, agentNum, gameState, depth):
        agentId_next = (agentId + 1) % agentNum
        depth = (depth - 1) if (agentId_next == 0) else depth
        if depth == 0:
            return self.evaluationFunction(gameState)

        maxMode = (agentId == 0)
        actions = gameState.getLegalActions(agentId)
        if len(actions) == 0: return self.evaluationFunction(gameState)
        gameStateSuccessors = [ gameState.generateSuccessor(agentId, action) for action in actions]

        if maxMode:
            v = -9999999
            for successor in gameStateSuccessors:
                successor_value = self.alphaBetaSearch(alpha, beta, agentId_next, agentNum, successor, depth)
                v = max(v, successor_value)
                if v >= beta: return v
                alpha = max(alpha, v) 
            return v

        else:
            v = 9999999
            for successor in gameStateSuccessors:
                successor_value = self.alphaBetaSearch(alpha, beta, agentId_next, agentNum, successor, depth)
                v = min(v, successor_value)
                if v <= alpha: return v
                beta = min(beta, v)
            return v
        
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        agentNum = gameState.getNumAgents()
        agentId_next = 1 # self.index = 0

        actions = gameState.getLegalActions(self.index)
        gameStateSuccessors = [ gameState.generateSuccessor(self.index, action) for action in actions]
        scores = [self.expectimaxSearch(agentId_next, agentNum, successor, self.depth) for successor in gameStateSuccessors]
        score_wanted = max(scores)
        action_wanted = actions[scores.index(score_wanted)]
        return action_wanted

    def expectimaxSearch(self, agentId, agentNum, gameState, depth):
        agentId_next = (agentId + 1) % agentNum
        depth = (depth - 1) if (agentId_next == 0) else depth
        if depth == 0:
            return self.evaluationFunction(gameState)
        
        actions = gameState.getLegalActions(agentId)
        if len(actions) == 0: return self.evaluationFunction(gameState)
        gameStateSuccessors = [ gameState.generateSuccessor(agentId, action) for action in actions]
        scores = [self.expectimaxSearch(agentId_next, agentNum, successor, depth) for successor in gameStateSuccessors]
        score_ave = sum(scores)/float(len(scores))
        return score_ave


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      
      I first get the original score of the current state,
      and add or minus some score according to different situation
      
      (1) Food-related algorithm
        I make the pacman chose the direction to the nearest food,
        and encourage it to consume the food by reducting scores 
        according to the total number of foods, otherwise, the 
        pacman would just stay right next to a food and stop.
        
      (2) Capsule-related algorithm
        I encourage the pacman to look for the capsule and consume it.
        Quite similar to the food-related algorithm, but the weights
        are different, the pacman temds to consume capsule than foods.

      (3) Ghost-related algorithm
        I let the pacman consider the ghosts only if they are close,
        and the close they are, the more scores are reducted. But if 
        after consuming capsule and the ghost is "scared", then the 
        pacman would hunt them to get more scores. If the ghost are 
        far from current position, pacman would just go to the nearest
        food and consume it as if there aren't any ghost.

      The weights of each term is selected after several experiments.

    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin(): return 99999
    elif currentGameState.isLose(): return -99999
    
    pacmanPos = currentGameState.getPacmanPosition()
    score = currentGameState.getScore()

    # Food-related algorithm
    foodNum = currentGameState.getNumFood()
    score -= foodNum * 1000
    food = currentGameState.getFood()
    nearestFoodDistance = 99999
    for x in range(food.width):
        for y in range(food.height):
            if (food[x][y] ==  True):
                newDistance = util.manhattanDistance(pacmanPos, (x, y))
                nearestFoodDistance = min(nearestFoodDistance, newDistance)
    score -= nearestFoodDistance
    
    # Capsule-related algorithm
    capsulePosList = currentGameState.getCapsules()
    capsuleNum = len(capsulePosList)
    if capsuleNum > 0:
        distance2capsule = [util.manhattanDistance(pacmanPos, capsulePos) for capsulePos in capsulePosList]
        score -= min(distance2capsule)
        score -= capsuleNum * 5000

    # Ghost-related algorithm
    ghostStates = currentGameState.getGhostStates()
    ghostPosList = currentGameState.getGhostPositions()
    scareTimes  = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostNum2eat = 0
    for i, ghostPos in enumerate(ghostPosList):
        dist2ghost = util.manhattanDistance(pacmanPos, ghostPos)
        if scareTimes[i] >0: ghostNum2eat += 1
        if dist2ghost < 3:
            if scareTimes[i] > 0:
                score += 10/(dist2ghost+1)
            else:
                score -= 10/(dist2ghost+1)
    
    score -= ghostNum2eat * 100    

    return score

# Abbreviation
better = betterEvaluationFunction

