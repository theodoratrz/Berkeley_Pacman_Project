
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
        curr_food = currentGameState.getFood()              #find food for current state
        ghost_pos = successorGameState.getGhostPositions()
        "*** YOUR CODE HERE ***"
 
        food = curr_food.asList()
        fdist = []                  # store food's distance from new position
        for i in food:
            fdist.append(manhattanDistance(newPos, i))

        min_food_dist = min(fdist)  # find(and choose) the closest food

        gdist = []                  # store ghosts' distance from new position
        for i in ghost_pos:
            gdist.append(manhattanDistance(newPos,i))
    
        min_ghost_dist = min(gdist) # find the closest ghost
        
        if min_ghost_dist <= 1:     # if ghost is too close , pacman must avoid it
            return -10000           # so return something very bad/small
        elif min_food_dist == 0:    #if there is food in the new position, pacman must eat it
            return 10000            #return something very good/big
        else:
            return (-min_food_dist) #choose the closest food 
                                    #return biggest value for the min distance(3 < 4 but -3>-4, so pacman chooses 3)

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
        max_result = float('-inf')                                                      # max_result starts from -infinity
        temp = 0                                                                        
        max_action = " "                                                                # initialize max_action with ana empty string
        legalMoves = gameState.getLegalActions(0)                                       # legal moves for pacman(index 0)
        for action in legalMoves:
            temp = self.min_value(gameState.generateSuccessor(0,action), 1, 0)          # call min with depth=0 and agent=1(first ghost)
            if max_result < temp:                                                       # if the new return value is greater than the current value
                max_result = temp                                                       # keep the greatest value
                max_action = action                                                     # return the action that caused the greatest value
        return max_action

    def max_value(self, gameState, depth):                                              # function for max 
        if gameState.isWin() or gameState.isLose() or depth == self.depth:              # terminal states
            return self.evaluationFunction(gameState)                                   # when reach a terminal state return the Utility
        v =  float('-inf')                                                              # v starts from -infinity
        legalMoves = gameState.getLegalActions(0)                                       # legal moves for pacman(index 0)
        for action in legalMoves:   
            v = max(v, self.min_value(gameState.generateSuccessor(0,action), 1, depth)) # call min's function with agent=1(first ghost) and depth
        return v                                                                        # return the max between min's return value and v current value

    def min_value(self, gameState, agent, depth):                                       # function for min
        nof_agents = gameState.getNumAgents()                                           # number of agents(pacman and ghosts)
        if gameState.isWin() or gameState.isLose() or depth == self.depth:              # terminal states
            return self.evaluationFunction(gameState)                                   # when reach a terminal state return the Utility
        v =  float('inf')                                                               # v starts from +infinity
        legalMoves = gameState.getLegalActions(agent)                                   # legal moves for ghosts(call for every ghost)
        for action in legalMoves:
            if nof_agents == agent + 1:                                                 # if current agent is the last agent
                v = min(v, self.max_value(gameState.generateSuccessor(agent,action), depth+1))  #  increase depth and call max function
            else:
                v = min(v, self.min_value(gameState.generateSuccessor(agent,action), agent+1,depth)) # else, go to the next agent(agent+1) and call min's function
        return v                                                                        # return the minimum between max or min return values and v current value

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        max_result = float('-inf')                                                      # max_result starts from -infinity
        a = float('-inf')                                                               # a starts from -infinity
        b = float('inf')                                                                # b starts from +infinity
        temp = 0
        max_action = " "                                                                # initialize max_action with ana empty string
        legalMoves = gameState.getLegalActions(0)                                       # legal moves for pacman(index 0)
        for action in legalMoves:
            temp = self.min_value(gameState.generateSuccessor(0,action), 1,a,b, 0)      # call min with depth=0 and agent=1(first ghost)
            if max_result < temp:                                                       # if the new return value is greater than the current value
                max_result = temp                                                       # keep the greatest value
                max_action = action                                                     # return the action that caused the greatest value
                a = max(a,temp)                                                         # a is equal with the max between temp and a previous value
        return max_action

    def max_value(self, gameState, a ,b, depth):                                            # function for max 
        if gameState.isWin() or gameState.isLose() or depth == self.depth:                  # terminal states
            return self.evaluationFunction(gameState)                                       # when reach a terminal state return the Utility
        v =  float('-inf')                                                                  # v starts from -infinity
        legalMoves = gameState.getLegalActions(0)                                           # legal moves for pacman(index 0)
        for action in legalMoves:
            v = max(v, self.min_value(gameState.generateSuccessor(0,action), 1,a,b, depth)) # call min's function with agent=1(first ghost) and depth
            if v > b:                                                                       # if v is greater than b
                return v                                                                    # return v
            a = max(a,v)                                                                    # else, a is equal with the max between v and a previous value
        return v                                                                            # return the maximum between min return value and v current value

    def min_value(self, gameState, agent, a ,b, depth):                                     # function for min
        nof_agents = gameState.getNumAgents()                                               # number of agents(pacman and ghosts)
        if gameState.isWin() or gameState.isLose() or depth == self.depth:                  # terminal states
            return self.evaluationFunction(gameState)                                       # when reach a terminal state return the Utility
        v =  float('inf')                                                                   # v starts from +infinity
        legalMoves = gameState.getLegalActions(agent)                                       # legal moves for ghosts(call for every ghost)
        for action in legalMoves:
            if nof_agents == agent + 1:                                                     # if current agent is the last agent
                v = min(v, self.max_value(gameState.generateSuccessor(agent,action), a,b,depth+1))  #  increase depth and call max function
            else:
                v = min(v, self.min_value(gameState.generateSuccessor(agent,action), agent+1,a,b,depth)) # else, go to the next agent(agent+1) and call min's function
            if v < a:                                                                       # if a is greater than v
                return v                                                                    # return v
            b = min(b,v)                                                                    # else, b is equal with the min between v and b previous value
        return v                                                                            # return the minimum between max or min return values and v current value
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
        max_result = float('-inf')                                                          # max_result starts from -infinity
        temp = 0
        max_action = " "                                                                    # initialize max_action with ana empty string
        legalMoves = gameState.getLegalActions(0)                                           # legal moves for pacman(index 0)
        for action in legalMoves:
            temp = self.chance_value(gameState.generateSuccessor(0,action), 1, 0)           # call min with depth=0 and agent=1(first ghost)
            if max_result < temp:                                                           # if the new return value is greater than the current value
                max_result = temp                                                           # keep the greatest value
                max_action = action                                                         # return the action that caused the greatest value
        return max_action

        
    def max_value(self, gameState, depth):                                                  # function for max 
        if gameState.isWin() or gameState.isLose() or depth == self.depth:                  # terminal states
            return self.evaluationFunction(gameState)                                       # when reach a terminal state return the Utility
        legalMoves = gameState.getLegalActions(0)                                           # legal moves for pacman(index 0)
        v = float('-inf')                                                                   # v starts from -infinity
        for action in legalMoves:
            v = max(v, self.chance_value(gameState.generateSuccessor(0,action), 1, depth))  # call min's function with agent=1(first ghost) and depth
        return v

    def chance_value(self, gameState, agent, depth):                                        # function for chance value
        nof_agents = gameState.getNumAgents()                                               # number of agents(pacman and ghosts)
        if gameState.isWin() or gameState.isLose() or depth == self.depth:                  # terminal states
            return self.evaluationFunction(gameState)                                       # when reach a terminal state return the Utility
        legalMoves = gameState.getLegalActions(agent)                                       # legal moves for ghosts(call for every ghost)
        v = 0                                                                               # v starts from 0
        for action in legalMoves:
            if nof_agents == agent + 1:                                                     # if current agent is the last agent
                v += self.max_value(gameState.generateSuccessor(agent,action), depth+1)     #  increase depth and call max function
            else:
                v += self.chance_value(gameState.generateSuccessor(agent,action), agent+1,depth) # else, go to the next agent(agent+1) and call chance function
        return v/len(legalMoves)                                               # return an average propabitity(we assume that each value has the same propability)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    ghosts_state = currentGameState.getGhostStates()
    score = scoreEvaluationFunction(currentGameState)   # initialize score from score evaluation function

    if currentGameState.isWin():                        # evaluate if is a win or lose state
        return float('inf')                             # if win return +infinity, else return -infinity
    elif currentGameState.isLose():
        return float('-inf')


    food = currentGameState.getFood().asList()          # get food list
    fdist = []                                          # store food's distance from new position
    for i in food:
        fdist.append(manhattanDistance(pos, i))         # compute all food distances from pacman's current position
    min_food = min(fdist)                               # find the closest food to pacman
    score += -2*min_food                              # the larger the distance to closest food the more negative the score

    nof_food = len(food)                                # remaining food in the board
    score += (-5*nof_food)                              # pacman must eat the all the food in the board

    nof_capsules = len(currentGameState.getCapsules())  # remaining capsules in the board
    score += (-25*nof_capsules)                         # we want pacman to eat capsules when they are close

    scared_ghosts = []                                  # store the scared ghosts
    notscared_ghosts = []                               # store the active ghosts

    for ghost in ghosts_state:                          # find which ghosts are scared and which are active
        if ghost.scaredTimer:                           # if the scaredTimer is not equal to 0 the the shost is scared 
            scared_ghosts.append(ghost)
        else:                                           # else the ghost is active
            notscared_ghosts.append(ghost)
    
    scared_ghost_dist = []                              # store scared ghosts' distance from new position
    for i in scared_ghosts:
        scared_ghost_dist.append(manhattanDistance(pos,i.getPosition()))

    notscared_ghost_dist = []                           # store active ghosts' distance from new position
    for i in notscared_ghosts:
        notscared_ghost_dist.append(manhattanDistance(pos,i.getPosition()))

    min_not_scared = 1                                  # initialize minimum distance to active ghosts to 1 (to avoid division by zero)
    if notscared_ghosts:
        min_not_scared = min(notscared_ghost_dist)      # if there are active ghosts then compute the minimum distance to it
    
    min_scared = 0                                      # initialize minimum distance to scared ghosts to 0
    if scared_ghosts:
        min_scared = min(scared_ghost_dist)             # if there are scared ghosts then compute the minimum distance to it

    score += -3*min_scared                              # it's beneficial for pacman to eat a scared ghost(earns a lot of points)
    score += -3*(1/min_not_scared)                      # the larger the distance to active ghost the better the score
                                                        # that's why first we inverse the distance and then multiply it with a negative number
    return score
# Abbreviation
better = betterEvaluationFunction
