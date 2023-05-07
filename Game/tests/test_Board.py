import unittest
import os
import sys
path = os.getcwd()
sys.path.append(path)

from Game.src.Board import Checkers, Pieces, Player

class TestBoard(unittest.TestCase):

    def test_move(self):
        print("Running test_move...")
        game = Checkers()
        game._setupBoard("clear")
        game._create_place_piece("b", (2, 1))
        game._create_place_piece("w", (3, 2))
        game.printBoard()
        game.move((2, 1), [(4, 3)])
        game.printBoard()
        test1 = game.board[3][2]
        test2 = game.board[4][3]
        self.assertEqual(test1, Pieces.EMPTY)
        self.assertEqual(test2, Pieces.BLACK)
        print("Success")

    def test_move_not_backwards(self):
        print("Running test_move...")
        game = Checkers()
        game._setupBoard("clear")
        game._create_place_piece("w", (3, 2))
        game.printBoard()
        game.move((3, 2), [(2, 1)])
        game.printBoard()
        test1 = game.board[3][2]
        test2 = game.board[2][1]
        self.assertEqual(test1, Pieces.WHITE)
        self.assertEqual(test2, Pieces.EMPTY)
        print("Success")

    def test_move_advanced(self):
        print("Running test_move_advanced...")
        game = Checkers()
        game._setupBoard("clear")
        game._create_place_piece("b", (2, 1))
        game._create_place_piece("w", (3, 2))
        game._create_place_piece("w", (5, 4))
        game.printBoard()
        game.move((2, 1), [(4, 3), (6, 5)])
        game.printBoard()
        test1 = game.board[3][2]
        test2 = game.board[5][4]
        test3 = game.board[6][5]
        self.assertEqual(test1, Pieces.EMPTY)
        self.assertEqual(test2, Pieces.EMPTY)
        self.assertEqual(test3, Pieces.BLACK)
        print("Success")

    def test_move_opposite_direction(self):
        print("Running test_move_opposite_direction...")
        game = Checkers()
        game._setupBoard("clear")
        game._create_place_piece("w", (2, 1))
        game._create_place_piece("w", (4, 3))
        game._create_place_piece("b", (5, 4))
        game.printBoard()
        game.move((5, 4), [(3, 2), (1, 0)])
        game.printBoard()
        test1 = game.board[3][2]
        test2 = game.board[5][4]
        test3 = game.board[1][0]
        self.assertEqual(test1, Pieces.EMPTY)
        self.assertEqual(test2, Pieces.EMPTY)
        self.assertEqual(test3, Pieces.BLACK)
        print("Success")

    def test_move_3rd_direction(self):
        print("Running test_move_3rd_direction...")
        game = Checkers()
        game._setupBoard("clear")
        game._create_place_piece("w", (1, 2))
        game._create_place_piece("w", (3, 4))
        game._create_place_piece("b", (4, 5))
        game.printBoard()
        game.move((4, 5), [(2, 3), (0, 1)])
        game.printBoard()
        test1 = game.board[3][2]
        test2 = game.board[5][4]
        test3 = game.board[0][1]
        self.assertEqual(test1, Pieces.EMPTY)
        self.assertEqual(test2, Pieces.EMPTY)
        self.assertEqual(test3, Pieces.BLACK_KING)
        print("Success")

    def test_move_create_king_piece(self):
        print("Running test_move_king_piece...")
        game = Checkers()
        game._setupBoard("clear")
        game._create_place_piece("w", (6, 6))
        game.turn = Player.WHITE
        game.printBoard()
        game.move((6, 6), [(7, 7)])
        game.printBoard()
        test1 = game.board[7][7]
        self.assertEqual(test1, Pieces.WHITE_KING)
        print("Success")

    def test_move_existing_king_piece(self):
        print("Running test_move_king_piece...")
        game = Checkers()
        game._setupBoard("clear")
        game._create_place_piece("wk", (7, 7))
        game.turn = Player.WHITE
        game.printBoard()
        game.move((7, 7), [(6, 6)])
        game.printBoard()
        test1 = game.board[6][6]
        self.assertEqual(test1, Pieces.WHITE_KING)
        print("Success")

    def test_valid_move(self):
        print("Running test_valid_move...")
        game = Checkers()
        game._create_place_piece("w", (2, 1))
        game._create_place_piece("b", (3, 2))
        valid = game.validMove((3, 2), (1, 0))
        self.assertTrue(valid)
        print("Success")

    # tries to move other player's piece
    def test_invalid_move(self):
        print("Running test_invalid_move...")
        game = Checkers()
        game._setupBoard("pieces")
        with self.assertRaises(ValueError):
            game.validMove((0, 0), (4, 3))
        print("Success")

    # tries to move other player's piece
    def test_valid_jump(self):
        print("Running test_valid_jump...")
        game = Checkers()
        game._setupBoard("pieces")
        game._create_place_piece("w", (4, 2))
        valid = game.validMove((5, 1), (3, 3))
        self.assertTrue(valid)
        print("Success")

    # moves Black from (1,5) to 

    def test_isFinished(self):
        print("Running test_isFinished...")
        game = Checkers()
        game._setupBoard("pieces")
        game.isFinished()
        self.assertFalse(game.game_ended)
        self.assertEqual(game.win, Player.NONE)
        print("Success")

    def test_countPieces(self):
        print("Running test_countPieces...")
        game = Checkers()
        game._setupBoard("clear")
        game._create_place_piece("w", (2, 2))
        self.assertEqual(game.countPossibleMovesForPlayer(Player.WHITE), 2)
        game._create_place_piece("b", (3, 3))
        self.assertEqual(game.countPossibleMovesForPlayer(Player.BLACK), 2)
        game._setupBoard("clear")
        game._create_place_piece("wk", (2, 2))
        self.assertEqual(game.countPossibleMovesForPlayer(Player.WHITE), 4)
        game._create_place_piece("bk", (3, 3))
        self.assertEqual(game.countPossibleMovesForPlayer(Player.BLACK), 4)

# test = TestBoard()
# test.test_move()
# test.test_move_advanced()
# test.test_move_opposite_direction()
# test.test_move_3rd_direction()
# test.test_move_king_piece()
# test.test_valid_move()
# test.test_invalid_move()
# test.test_valid_jump()
# test.test_isFinished()

TestBoard().test_countPieces()
