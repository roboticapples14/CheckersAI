import copy
from AI.src.AI import State, Minimax
from Game.src.Board import Checkers, Player
from Printer import Printer


class MyTestCase(unittest.TestCase):
    def test_double_jump(self):
        print("Running test_diff")
        game = Checkers()
        game._setupBoard('clear')
        game._create_place_piece("w", (3, 5))
        game._create_place_piece("b", (4, 4))
        game._create_place_piece("b", (6, 4))
        game.turn = Player.WHITE

        ai = Minimax(game, Player.WHITE, 2)
        nextState = ai.getBestMove()

        # print move
        Printer().printAI(ai, nextState)

MyTestCase().test_double_jump()