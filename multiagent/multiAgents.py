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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        newCapsules = successorGameState.getCapsules()

        basenum_ = 50
        res = basenum_ / 8 * (successorGameState.getScore() - currentGameState.getScore())
        for index_, timer_ in enumerate(newScaredTimes):
            manhattan_to_ghost = manhattanDistance(newGhostStates[index_].getPosition(), newPos)
            if timer_ == 0:
                try:
                    res -= basenum_*8/manhattan_to_ghost
                except:
                    res = -0xFFFFFFFFFFFFFFFF
            elif manhattan_to_ghost * 2 <= timer_:
                res += basenum_*3/manhattan_to_ghost

        if len(newCapsules) < len(currentGameState.getCapsules()):
            res += basenum_ * 2

        for capsule in newCapsules:
            res += basenum_/manhattanDistance(newPos, capsule)
        
        if successorGameState.getNumFood() < currentGameState.getNumFood():
            res += basenum_ * 2

        for food_ in newFood.asList():
            res += basenum_/manhattanDistance(newPos, food_)

        return res

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimax(gameState, depth_, agent_index):
            num_agents = gameState.getNumAgents()

            if depth_ == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState), None

            legal_actions = gameState.getLegalActions(agent_index)

            if agent_index == 0:
                max_eva = float('-inf')
                max_action = None

                for legal_action in legal_actions:
                    succ = gameState.generateSuccessor(agent_index, legal_action)
                    eva = minimax(succ, depth_, agent_index + 1)[0]
                    
                    if eva > max_eva:
                        max_eva = eva
                        max_action = legal_action
                
                return max_eva, max_action
            else:
                min_eva = float('inf')
                
                for legal_action in legal_actions:
                    succ = gameState.generateSuccessor(agent_index, legal_action)
                    
                    if agent_index == num_agents - 1:
                        eva = minimax(succ, depth_ - 1, 0)[0]
                    else:
                        eva = minimax(succ, depth_, agent_index + 1)[0]
                    
                    if eva < min_eva:
                        min_eva = eva

                return min_eva, None

        return minimax(gameState, self.depth, 0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alpha_beta_minimax(gameState, depth_, agent_index, alpha_, beta_):
            num_agents = gameState.getNumAgents()

            if depth_ == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState), None

            legal_actions = gameState.getLegalActions(agent_index)

            if agent_index == 0:
                max_eva = float('-inf')
                max_action = None

                for legal_action in legal_actions:
                    succ = gameState.generateSuccessor(agent_index, legal_action)
                    eva = alpha_beta_minimax(succ, depth_, agent_index + 1, alpha_, beta_)[0]

                    if eva > max_eva:
                        max_eva = eva
                        max_action = legal_action
                    
                    alpha_ = max([alpha_, max_eva])
                    if beta_ < alpha_:
                        break

                return max_eva, max_action
            else:
                min_eva = float('inf')

                for legal_action in legal_actions:
                    succ = gameState.generateSuccessor(agent_index, legal_action)
                    
                    if agent_index == num_agents - 1:
                        eva = alpha_beta_minimax(succ, depth_ - 1, 0, alpha_, beta_)[0]
                    else:
                        eva = alpha_beta_minimax(succ, depth_, agent_index + 1, alpha_, beta_)[0]

                    min_eva = min([min_eva, eva])
                    
                    beta_ = min([beta_, eva])       # min_eva <= eva, beta_-ს განახლება ნებისმიერით შეგვიძლია
                    """ beta_ <= min_eva <= eva, 
                    alpha_-სთან ნაკლებობის შემოწმება ნებისმიერით შეგვიძლია.
                    თუ ეს პირობა სრულდება, მაშინ beta_ == min_eva == eva,
                    ამიტომ მნიშვნელობა არ აქვს, რომელთან შევამოწმებთ.
                    იგივე ლოგიკა მაქსიმაიზერშიც."""
                    if eva < alpha_:
                        break

                return min_eva, None

        return alpha_beta_minimax(gameState, self.depth, 0, float('-inf'), float('inf'))[1]

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
        def expectimax(gameState, depth_, agent_index):
            num_agents = gameState.getNumAgents()

            if depth_ == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState), None

            legal_actions = gameState.getLegalActions(agent_index)

            if agent_index == 0:
                max_eva = float('-inf')
                max_action = None

                for legal_action in legal_actions:
                    succ = gameState.generateSuccessor(agent_index, legal_action)
                    eva = expectimax(succ, depth_, agent_index + 1)[0]
                    
                    if eva > max_eva:
                        max_eva = eva
                        max_action = legal_action
                
                return max_eva, max_action
            else:
                total_eva = 0
                
                for legal_action in legal_actions:
                    succ = gameState.generateSuccessor(agent_index, legal_action)
                    
                    if agent_index == num_agents - 1:
                        total_eva += expectimax(succ, depth_ - 1, 0)[0]
                    else:
                        total_eva += expectimax(succ, depth_, agent_index + 1)[0]

                return total_eva/len(legal_actions), None

        return expectimax(gameState, self.depth, 0)[1]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    pos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    "*** YOUR CODE HERE ***"
    res = currentGameState.getScore()

    if currentGameState.isWin() or currentGameState.isLose():
        return res

    capsules = currentGameState.getCapsules()

    basenum_ = 50

    for index_, timer_ in enumerate(scaredTimes):
        manhattan_to_ghost = manhattanDistance(ghostStates[index_].getPosition(), pos)
        if timer_ == 0:
            res -= basenum_*20/(manhattan_to_ghost**(3/2))
        elif manhattan_to_ghost <= timer_:
            res += basenum_*4/(manhattan_to_ghost**(5/4))

    for capsule in capsules:
        res += basenum_/(manhattanDistance(pos, capsule)**(5/4))

    # res -= min(manhattanDistance(pos, food_) for food_ in foods.asList()) * 2
    # res -= len(foods.asList()) * 2.5

    for food_ in foods.asList():
        res -= (manhattanDistance(pos, food_)**(5/4))*2/basenum_

    return res

    # basenum_ = 20

    # for index_, timer_ in enumerate(scaredTimes):
    #     manhattan_to_ghost = manhattanDistance(ghostStates[index_].getPosition(), pos)
    #     if timer_ == 0:
    #         res += basenum_*3.5 * (manhattan_to_ghost**(1/6))
    #     elif manhattan_to_ghost * 2 <= timer_:
    #         res -= basenum_/6 * manhattan_to_ghost

    # for capsule in capsules:
    #     res -= basenum_/12 * (manhattanDistance(pos, capsule)**(2/3))

    # for food_ in foods.asList():
    #     res -= basenum_/8 * (manhattanDistance(pos, food_)**(2/3))
    
    # return res

# Abbreviation
better = betterEvaluationFunction
