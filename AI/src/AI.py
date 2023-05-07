import os
import random
import sys
import math
import copy
path = os.getcwd()
sys.path.append(path)
import numpy as np
from Game.src.Board import Checkers, Player, Pieces

BOARD_DIM = 8

class UtilityMode:
    Simple = "Simple"
    Standard = "Standard"
    Sophisticated = "Sophisticated"
    StandardPro = "StandardPro"

class State:
    '''
    Represents game states, or configurations of the board
    '''
    def __init__(self, game: Checkers, player: Player, forwardedUtility=None, utilityMode=None):
        '''
        game is of the type Checkers
        sets the initial attributes
        '''
        self.player = player
        self.game = game
        self.next_states = []
        if utilityMode == None:
            self.utilityMode = UtilityMode.Standard
        else:
            self.utilityMode = utilityMode
        if forwardedUtility is not None:
            self.utilityValue = forwardedUtility
        else:
            self.utility()

    def turn(self):
        return self.game.turn
    
    def actions_result(self):
        '''
        we look at all pieces of current player, and for every possible move
        add the state to self.next_state
        We limit the depth of the tree to avoid ridiculously long computation time
        '''
        for i in range(BOARD_DIM):
            for j in range(BOARD_DIM):
                corresponding_piece = [Pieces.BLACK, Pieces.BLACK_KING] if self.game.turn == Player.BLACK else [Pieces.WHITE, Pieces.WHITE_KING]

                if corresponding_piece.__contains__(self.game.board[i][j]):
                    moves = self.game.possibleMoves((i, j))
                    for move in moves:
                        tmpGame = copy.deepcopy(self.game)
                        tmpGame.move((i, j), move)
                        childState = State(
                            game=tmpGame,
                            player=tmpGame.turn,
                            utilityMode=self.utilityMode
                        )
                        self.next_states.append(childState)

    def terminal_test(self):
        return self.game.isFinished()
    
    def utility(self):
        if self.utilityMode == UtilityMode.Simple:
            self.simpleUtility()
        elif self.utilityMode == UtilityMode.StandardPro:
            self.standardProUtility()
        elif self.utilityMode == UtilityMode.Sophisticated:
            self.sophisticatedUtility()
        else:
            self.standardUtility()

    def simpleUtility(self):
        if self.player == Player.WHITE:
            self.utilityValue = - self.game.bs - self.game.bks
        else:
            self.utilityValue = - self.game.ws - self.game.wks
    
    def standardUtility(self):
        if self.player == Player.WHITE:
            self.utilityValue = self.game.ws + self.game.wks*2  - self.game.bs - self.game.bks*2
        else:
            self.utilityValue = self.game.bs + self.game.bks*2  - self.game.ws - self.game.wks*2

    def standardProUtility(self):
        if self.player == Player.WHITE:
            self.utilityValue = self.game.ws + self.game.wks*2 + self.game.countPossibleMovesForPlayer(Player.WHITE)  - self.game.bs - self.game.bks*2 - self.game.countPossibleMovesForPlayer(Player.BLACK)
        else:
            self.utilityValue = self.game.bs + self.game.bks*2 + self.game.countPossibleMovesForPlayer(Player.BLACK)  - self.game.ws - self.game.wks*2 - self.game.countPossibleMovesForPlayer(Player.WHITE)

    # This was just a small test to see if we could improve the AI
    def sophisticatedUtility(self):
        if self.player == Player.WHITE:
            self.utilityValue = self.game.ws + self.game.wks*2 + self.game.countPiecesInOwnHalf(Player.WHITE)  - self.game.bs - self.game.bks*2 - self.game.countPiecesInOwnHalf(Player.BLACK)
        else:
            self.utilityValue = self.game.bs + self.game.bks*2 + self.game.countPiecesInOwnHalf(Player.BLACK)  - self.game.ws - self.game.wks*2 - self.game.countPiecesInOwnHalf(Player.WHITE)

    def difference(self, nextState):
        '''
        Calculates the move taken between self and nextState (only valid for single jumps)
        '''
        oldBoard = np.array(self.game.board)
        newBoard = np.array(nextState.game.board)
        # subtraction of old board and newboard returns a 8x8 np array with 1 at the new square, and -1 at old square
        moveBoard = oldBoard - newBoard
        from_x, from_y = (cord[0] for cord in np.where(moveBoard==-1))
        to_x, to_y = (cord[0] for cord in np.where(moveBoard==1))
        return ((from_x, from_y), [(to_x, to_y)])

    def format_move_for_human(self, move):
        '''
        Calculates the move taken between self and nextState (only valid for single jumps)
        '''
        (from_x, from_y), [(to_x, to_y)] = move
        return ((from_y, from_x), [(to_y, to_x)])


class Minimax():
    def __init__(self, current_board, color: Player, max_depth, utilityMode=UtilityMode.StandardPro):
        '''
        color: The color that the AI is playing as
        initial_state: The initial state of the game 
        '''
        self.color = color
        self.max_depth = max_depth
        self.utilityMode = utilityMode
        self.state = State(current_board, color, utilityMode=utilityMode)

    # evals the state according to the minmax value
    # returns the next state
    def eval(self, state, depth=None):
        if depth is None:
            depth = self.max_depth

        if depth == 0 or state.game.isFinished():
            return state.utilityValue

        state.actions_result()

        if len(state.next_states) == 0:
            return state.utilityValue
        
        if state.player == self.color:
            value = -math.inf
            for child in state.next_states:
                value = max(value, self.eval(child, depth - 1))
            return value
        else:
            value = math.inf
            for child in state.next_states:
                value = min(value, self.eval(child, depth - 1))
            return value
        
    def alphaBetaPruning_eval(self, state, depth=None, alpha=None, beta=None):
        if depth is None:
            depth = self.max_depth

        if alpha is None:
            alpha = -math.inf

        if beta is None:
            beta = math.inf

        if depth == 0 or state.game.isFinished():
            return state.utilityValue
        
        state.actions_result()

        if len(state.next_states) == 0:
            return state.utilityValue
        
        if state.player == self.color:
            value = -math.inf
            for child in state.next_states:
                value = max(value, self.alphaBetaPruning_eval(child, depth - 1, alpha, beta))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        else:
            value = math.inf
            for child in state.next_states:
                value = min(value, self.alphaBetaPruning_eval(child, depth - 1, alpha, beta))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

        
    def getBestMove(self, performanceBoost=False, firstMove=False):
        bestScore = -math.inf
        bestMove = None
        self.state.actions_result()
        if firstMove:
            return random.choice(self.state.next_states)
            
        for child in self.state.next_states:
            if not performanceBoost:
                value = self.eval(child, self.max_depth - 1)
            else:
                value = self.alphaBetaPruning_eval(child, self.max_depth - 1)
            if bestScore < value:
                bestMove = child
                bestScore = value

        if bestMove is None:
            print(f"{self.color} surrenders")
            # self.state.game.printBoard()
            self.state.game.game_ended = True
            self.state.game.win = Player.BLACK if  self.color == Player.WHITE else Player.WHITE 
            return self.state
            # raiseValueError("Something went wrong! No best move found")
        return bestMove

    def getDecisionTree(self, stateTuple=None, treeMatrix=None, depth=None):
        if stateTuple is None:
            stateTuple = ("root", self.state)

        if (treeMatrix is None):
            treeMatrix =  [[] for _ in range(self.max_depth + 1)]

        if depth is None:
            depth = 0
        
        treeMatrix[depth].append(stateTuple)

        if len(stateTuple[1].next_states) == 0:
            return treeMatrix

        for i, child in enumerate(stateTuple[1].next_states):
            self.getDecisionTree((stateTuple[0] + "+" + str(i), child), treeMatrix, depth + 1)

        return treeMatrix

        
