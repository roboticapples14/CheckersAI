import copy
import unittest
import os
import sys
path = os.getcwd()
sys.path.append(path)

from AI.src.AI import State, Minimax
from Game.src.Board import Checkers, Player
from src.Printer import Printer

class TestAI(unittest.TestCase):

    def test_double_jump(self):
        print("Running test_diff")
        game = Checkers()
        game._setupBoard('clear')
        game._create_place_piece("w", (1, 1))
        game._create_place_piece("w", (3, 3))
        game._create_place_piece("b", (4, 4))
        game.turn = Player.BLACK

        game.move((4, 4), [(2,2), (0,0)])
        game.printBoard()

    def test_double_decision_jump(self):
        print("Running double decision jump test")
        game = Checkers()
        game._setupBoard('clear')
        game._create_place_piece("w", (3, 5))
        game._create_place_piece("b", (4, 4))
        game._create_place_piece("b", (6, 2))
        game._create_place_piece("b", (6, 4))
        game.turn = Player.WHITE

        ai = Minimax(game, Player.WHITE, 2)
        nextState = ai.getBestMove()

        # print move
        Printer().printAI(ai, nextState, sorting=True)

    def test_double_double_decision_jump(self):
        print("Running double decision jump test")
        game = Checkers()
        game._setupBoard('clear')
        game._create_place_piece("w", (1, 3))
        game._create_place_piece("b", (2, 2))
        game._create_place_piece("b", (2, 4))
        game._create_place_piece("b", (4, 2))
        game._create_place_piece("b", (4, 4))
        game._create_place_piece("b", (4, 6))
        game._create_place_piece("b", (6, 2))
        game._create_place_piece("b", (6, 4))
        game._create_place_piece("b", (6, 6))
        game.turn = Player.WHITE
        game.printBoard()
        ai = Minimax(game, Player.WHITE, 2)
        nextState = ai.getBestMove()

        # print move
        Printer().printAI(ai, nextState)

    def test_actions(self):
        print("Running test_actions")
        game = Checkers()
        game._setupBoard("clear")
        game._create_place_piece("b", (1, 1))
        game._create_place_piece("w", (2, 2))
        game.printBoard()
        state = State(game, Player.BLACK)
        print(state.game)
        state.actions_result()
        print(state.game)
        for s in state.next_states:
            s.game.printBoard()
        print("success")

    def test_weird_behavior(self):
        print("Running test_weird_behavior")
        game = Checkers()
        game._setupBoard("clear")
        game._create_place_piece("bk", (4, 4))
        game._create_place_piece("b", (5, 7))
        game._create_place_piece("w", (1, 7))
        game._create_place_piece("w", (3, 7))
        game._create_place_piece("w", (6, 4))
        game._create_place_piece("w", (6, 6))
        game._create_place_piece("wk", (7, 7))
        game._create_place_piece("wk", (7, 5))
        game._create_place_piece("wk", (7, 3))
        game._create_place_piece("wk", (7, 1))
        game.turn = Player.WHITE

        ai = Minimax(game, Player.WHITE, 2)
        nextState = ai.getBestMove()

        # print move
        Printer().printAI(ai, nextState, sorting=True)

    def test_diff(self):
        print("Running test_diff")
        game = Checkers()
        game._setupBoard("clear")
        game._create_place_piece("b", (3, 2))
        state1 = State(copy.deepcopy(game), Player.BLACK)
        game.move((3, 2), [(2, 1)])
        state2 = State(game, Player.BLACK)
        move = state1.difference(state2)
        self.assertEqual(move, ((3, 2), [(2, 1)]))
        print("Success")

test = TestAI()
test.test_double_jump()