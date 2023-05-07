import copy
import sys
sys.path.append('./')
from AI.src.AI import Minimax, State
from Game.src.Board import Checkers, Player
from src import Printer

AI_COLOR = Player.WHITE
DIFFICULTY = 2

def checkForValidInput(to_x, to_y):
    if (len(to_x) == 0 or len(to_x) > 1) or (len(to_y) == 0 or len(to_y) > 1):
        return False

    if (not to_x.isdigit()) or (not to_y.isdigit()):
        return False
    
    return True

checkers = Checkers()

print("Welcome to Checkers!")
print("Instructions: ...")
success = True
while (not checkers.isFinished()):
    if (not success):
        print("Invalid move! Try again:")
    else:
        checkers.printBoard()
        print("{}'s turn!".format(checkers.get_turn()))

    # ====================================================
    # Call AI whenever its turn it is
    if (checkers.get_turn() == AI_COLOR):
        # save state
        start_state = State(copy.deepcopy(checkers), AI_COLOR)
        print("\n")
        print("🤖 is thinking...")
        ai = Minimax(checkers, AI_COLOR, DIFFICULTY)
        nextState = ai.getBestMove(True)
        print("🤖 has made a move")

        # print move
        # Printer().printAI(ai, nextState)

        checkers = nextState.game  # not sure if this works :D
        (from_x, from_y), [(to_x, to_y)] = start_state.format_move_for_human(start_state.difference(nextState))
        print("{} moving from ({}, {}) to ({}, {})".format(AI_COLOR, from_x, from_y, to_x, to_y))
        continue
    # ==========================================================

    # List of possible to moves
    to_moves_list = []

    print("What piece would you like to move? {}".format("\'X\' to submit the move" if len(to_moves_list) > 1 else ""))
    from_x = input("    enter x cord: ")
    from_y = input("    enter y cord: ")

    if (checkForValidInput(from_x, from_y) == False):
        print("Invalid input! Please enter a number between 0 and 7")
        continue
    
    # ask the user multiple times for to moves until they press X
    while True:
        if len(to_moves_list) > 0:
            print("Do you want to go for a double jump? \'x\' to submit the move.")
        else:
            print("What square would you like to move to?")
        
        to_x = input("  enter x cord: ")
        to_x = to_x.lower()
        if len(to_moves_list) > 0 and to_x == "X".lower():
            if len(to_moves_list) == 0:
                print("You must move at least one piece!")
                continue
            else:
                break

        to_y = input("  enter y cord: ")
        to_y = to_y.lower()
        if len(to_moves_list) > 0 and to_y == "X".lower():
            if len(to_moves_list) == 0:
                print("You must move at least one piece!")
                continue
            else:
                break

        if (checkForValidInput(to_x, to_y) == False):
            print("Invalid input! Please enter a number between 0 and 7")
            continue
        to_moves_list.append((int(to_y), int(to_x)))
    
    # print("{} moving from ({}, {}) to ({}, {})".format(checkers.get_turn(), from_x, from_y, to_x, to_y))
    checkers.move((int(from_y), int(from_x)), to_moves_list)

print("Game over! {} won!!".format(checkers.win))
print(checkers.printBoard())

