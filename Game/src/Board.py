import numpy as np
from enum import Enum
import copy
import math
# import emoji
# import regex

BOARD_DIM = 8

class Player(Enum):
    WHITE = 1
    BLACK = 2
    NONE = 0

class Pieces(Enum):
    BLACK = " B "
    WHITE = " W "
    BLACK_KING = " BK"
    WHITE_KING = " WK"
    EMPTY = "   "

    def __sub__(self, other):
        if (self == other):
            return 0
        elif (self != self.EMPTY and other == self.EMPTY):
            return -1
        elif (self == self.EMPTY and other != self.EMPTY):
            return 1
        else:
            return -2

class Checkers:
    def __init__(self):
        self.board = [[Pieces.EMPTY for _ in range(BOARD_DIM)] for _ in range(BOARD_DIM)]
        self.bs = None
        self.bks = None
        self.ws = None
        self.wks = None
        self._setupBoard("pieces")
        self.turn = Player.BLACK
        self.game_ended = False
        self.win = Player.NONE

    def _create_place_piece(self, piece, cord):
        if piece == "w":
            self.board[cord[0]][cord[1]] = Pieces.WHITE
            self.ws = self.ws + 1
        elif piece == "wk":
            self.board[cord[0]][cord[1]] = Pieces.WHITE_KING
            self.wks = self.wks + 1
        elif piece == "b":
            self.board[cord[0]][cord[1]] = Pieces.BLACK
            self.bs = self.bs + 1
        elif piece == "bk":
            self.board[cord[0]][cord[1]] = Pieces.BLACK_KING
            self.bks = self.bks + 1
        else:
            raise ValueError("Not a damn piece type")


    def _setupBoard(self, init_type):
        if init_type.lower() == "pieces":
            self.bs = 12
            self.bks = 0
            self.ws = 12
            self.wks = 0
            for i in range(BOARD_DIM):
                for j in range(BOARD_DIM):
                    if (i+j) % 2 == 0:
                        if i < 3:
                            self.board[i][j] = Pieces.WHITE
                        elif i > 4:
                            self.board[i][j] = Pieces.BLACK
                        else:
                            self.board[i][j] = Pieces.EMPTY
                    else:
                        self.board[i][j] = Pieces.EMPTY
        elif init_type.lower() == "clear":
            self.bs = 0
            self.bks = 0
            self.ws = 0
            self.wks = 0
            for i in range(BOARD_DIM):
                for j in range(BOARD_DIM):
                    self.board[i][j] = Pieces.EMPTY
        
        else:
            raise ValueError

    def printBoard(self):
        print("\n")
        print(" ---0-----1-----2-----3-----4-----5-----6-----7---")
        for i, row in enumerate(self.board):
            print(" | ", end="")
            for j, col in enumerate(row):
                col_value = col.value
                if col == Pieces.EMPTY:
                    if (i+j) % 2:
                        col_value = "   "
                    else:
                        col_value = " _ "
                if j > 6:
                    print(col_value, end=f" | {i}")
                else:
                    print(col_value, end=f" | ")
            print("\n -------------------------------------------------")

    def saveBoardToFile(self, f):
        f.write(" ---0-----1-----2-----3-----4-----5-----6-----7---\n")
        for i, row in enumerate(self.board):
            f.write(" | ")
            for j, col in enumerate(row):
                col_value = col.value
                if col == Pieces.EMPTY:
                    if (i+j) % 2:
                        col_value = "   "
                    else:
                        col_value = " _ "
                if j > 6:
                    f.write(f"{col_value} | ")
                else:
                    f.write(f"{col_value} | ")
            f.write("\n -------------------------------------------------\n")

    def saveSingleRowToFile(self, row, f):
        boardRow = self.board[row]
        f.write(" | ")
        for j, col in enumerate(boardRow):
            col_value = col.value
            if col == Pieces.EMPTY:
                if (row+j) % 2:
                    col_value = "   "
                else:
                    col_value = " _ "
            if j > 6:
                f.write(f"{col_value} |")
            else:
                f.write(f"{col_value} | ")

    def isFinished(self):
        """
        Checks if the game has ended
        A game ends when one of the players has no pieces left
        OR when one of the players cannot make a move
        Returns if the game is finished or not
        """
        whiteMoves_possible = False
        blackMoves_possible = False

        for i in range(BOARD_DIM):
            for j in range(BOARD_DIM):
                if whiteMoves_possible == False and (self.board[i][j] == Pieces.WHITE or self.board[i][j] == Pieces.WHITE_KING):
                    if len(self.possibleMoves([i, j])) > 0:
                        whiteMoves_possible = True
                elif blackMoves_possible == False and (self.board[i][j] == Pieces.BLACK or self.board[i][j] == Pieces.BLACK_KING):
                    if len(self.possibleMoves([i, j])) > 0:
                        blackMoves_possible = True

                elif blackMoves_possible == True and whiteMoves_possible == True:
                    break

                else:
                    continue

        if whiteMoves_possible == False and blackMoves_possible == True:
            self.game_ended = True
            self.win = Player.BLACK

        elif blackMoves_possible == False and whiteMoves_possible == True:
            self.game_ended = True
            self.win = Player.WHITE

        elif blackMoves_possible == False and whiteMoves_possible == False:
            self.game_ended = True
            self.win = Player.NONE

        else:
            self.game_ended = False
            self.win = Player.NONE

        return self.game_ended

    def onBoard(self, cord):
        valid_range = range(0,BOARD_DIM)
        x, y = cord
        return (x in valid_range and y in valid_range)
    
    def countPossibleMovesForPlayer(self, player):
        numberMoves = 0
        pieces = [Pieces.WHITE, Pieces.WHITE_KING] if player == Player.WHITE else [Pieces.BLACK, Pieces.BLACK_KING]
        for i in range(BOARD_DIM):
            for j in range(BOARD_DIM):
                if pieces.__contains__(self.board[i][j]):
                    numberMoves += len(self.possibleMoves([i,j]))
        return numberMoves

    def countPiecesInOwnHalf(self, player):
        numberOfPlayers = 0
        pieces = [Pieces.WHITE, Pieces.WHITE_KING] if player == Player.WHITE else [Pieces.BLACK, Pieces.BLACK_KING]
        for i in range(BOARD_DIM):
            for j in range(BOARD_DIM):
                if pieces.__contains__(self.board[i][j]):
                    if player == Player.WHITE and i < 4:
                        numberOfPlayers += 1
                    elif player == Player.BLACK and i > 3:
                        numberOfPlayers += 1

        return numberOfPlayers

    def possibleMoves(self, cord, evalBoard=None, moves=None, interimPath=None):
        if evalBoard == None:
            evalBoard = self.board

        if moves == None:
            moves = []

        if (not self.onBoard(cord)):
            raise ValueError("Board index out of range")

        x, y = cord
        piece = evalBoard[x][y]
        opponents = [Pieces.WHITE, Pieces.WHITE_KING] if (piece == Pieces.BLACK or piece == Pieces.BLACK_KING) else [
            Pieces.BLACK, Pieces.BLACK_KING]
        player_multiplier = -1 if (
                    piece == Pieces.BLACK or piece == Pieces.BLACK_KING) else 1  # for the player move direction
        piece = evalBoard[x][y]

        # get diagonals
        if piece == Pieces.BLACK_KING or piece == Pieces.WHITE_KING:
            diagonals = [i for i in [(x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)] if self.onBoard(i)]
        else:
            if (piece == Pieces.BLACK and x == 0) or (piece == Pieces.WHITE and x == 7):
                diagonals = []
            else:
                diagonals = [i for i in [(x + 1 * player_multiplier, y + 1), (x + 1 * player_multiplier, y - 1)] if
                         self.onBoard(i)]
            
        internalInterim = copy.deepcopy(interimPath)
        for dx, dy in diagonals:
            # if the square is empty, we can move there
            if evalBoard[dx][dy] == Pieces.EMPTY and interimPath is None:
                moves.append([(dx, dy)])
            # if there's an opponent at a diagonal, we can jump over it
            if evalBoard[dx][dy] in opponents:
                ddx = dx + dx - x
                ddy = dy + dy - y
                if (self.onBoard((ddx, ddy)) and evalBoard[ddx][ddy] == Pieces.EMPTY):
                    newBoard = copy.deepcopy(evalBoard)
                    newBoard[dx][dy] = Pieces.EMPTY
                    newBoard[ddx][ddy] = piece
                    newBoard[x][y] = Pieces.EMPTY

                    if interimPath is None:
                        moves.append([(ddx, ddy)])
                        internalInterim = moves[-1]
                    else:
                        newInterim = copy.deepcopy(interimPath)
                        newInterim.append((ddx, ddy))
                        moves.append(newInterim)
                        internalInterim = newInterim

                    self.possibleMoves((ddx, ddy), newBoard, moves, internalInterim)
        return moves


    def validMove(self, from_cord, to_cord):
        """
        Checks that move is valid:
            normal pieces can move forward diagonals
            kings can move to any diagonals
            any pieces can capture an opponent's piece that is next to it
        :param from_cord: tuple (x, y) Where your move starts from
        :param to_cord: tuple (x, y) Where you are going. In case of multiple jumps in one turn, provide list of coordinate tuples
        :returns: boolean is valid move
        """
        from_x, from_y = from_cord
        to_x, to_y = to_cord
        # check that from_cord and to_cord are in range (0-7)
        if (not self.onBoard(from_cord) or not self.onBoard(to_cord)):
            raise ValueError("Board index out of range")
        # check that to_cord is unoccupied
        if (self.board[to_x][to_y] != Pieces.EMPTY):
            raise ValueError("Trying to move to occupied field {}".format(to_cord))
        # check that the piece at cord belongs to the current player
        if ((self.board[from_x][from_y] in [Pieces.WHITE, Pieces.WHITE_KING] and self.turn == Player.BLACK) or (self.board[from_x][from_y] in [Pieces.BLACK, Pieces.BLACK_KING] and self.turn == Player.WHITE)):
            raise ValueError("Trying to move an opponent's piece at {}".format(from_cord))
        # check that cord is not empty
        if (self.board[from_x][from_y] == Pieces.EMPTY):
            raise ValueError("Trying to move an empty piece at {}".format(from_cord))

        return to_cord in self.possibleMoves(from_cord)

    def move(self, from_cord, to_cord):
        """
        :param from_cord: tuple (x, y) Where your move starts from
        :param to_cord: list of tuples (x, y) Where you are going. In case of multiple jumps in one turn, provide list of coordinate tuples
        """

        last_cord = from_cord
        board_copy = self.board.copy()
        for current_cord in to_cord:
            try: 
                self.validMove(last_cord, current_cord)
            except ValueError as e:
                print(e)
                self.board = board_copy
                return False
            piece_type = self.board[last_cord[0]][last_cord[1]]
            self.board[last_cord[0]][last_cord[1]] = Pieces.EMPTY
            x_last, y_last = last_cord
            x_to, y_to = current_cord
            if abs(x_last-x_to) > 1 and abs(y_last-y_to) > 1:
                index_x = int(last_cord[0] + abs(current_cord[0]-last_cord[0])/(current_cord[0]-last_cord[0]))
                index_y = int(last_cord[1] + abs(current_cord[1]-last_cord[1])/(current_cord[1]-last_cord[1]))
                if self.board[index_x][index_y] == Pieces.BLACK:
                    self.bs = self.bs - 1
                elif self.board[index_x][index_y] == Pieces.BLACK_KING:
                    self.bks = self.bks - 1
                elif self.board[index_x][index_y] == Pieces.WHITE:
                    self.ws = self.ws - 1
                elif self.board[index_x][index_y] == Pieces.WHITE_KING:
                    self.wks = self.wks - 1
                self.board[index_x][index_y] = Pieces.EMPTY # Removes pieces that has been skipped over

            if self.turn == Player.WHITE and x_to == 7:
                self.board[x_to][y_to] = Pieces.WHITE_KING
            elif self.turn == Player.BLACK and x_to == 0:
                self.board[x_to][y_to] = Pieces.BLACK_KING
            else:
                self.board[x_to][y_to] = piece_type

            last_cord = current_cord

        ## Update game state with function?
        if not self.game_ended:
            self.turn = Player.BLACK if self.turn == Player.WHITE else Player.WHITE
        return True

    def get_turn(self):
        return self.turn


class Tester:
    def __init__(self):
        game = Checkers()
        game._setupBoard("pieces")
        game.isFinished()


Tester()