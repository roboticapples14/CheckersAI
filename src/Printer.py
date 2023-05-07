from Game.src.Board import Checkers, Player, Pieces, BOARD_DIM

class Printer:
    def saveRowOfStates(self, BigStates, depth, f):
        separater = "  "
        firstPusher = "   "

        f.write("\n\n\n\n")
        f.write(firstPusher + f" Depth: {depth}\n" + firstPusher + " ")

        # divide states into arrays of maximum length 5
        subarrays = []
        i = 0
        while i < len(BigStates):
            subarray = BigStates[i:i+5]
            subarrays.append(subarray)
            i += 5

        for states in subarrays:
            for i in states: 
                name, state = i

                leftValue = (50 - (len(name) + 2)) / 2
                value = (50 - (len(name) + 2)) / 2

                leftValue -= 1

                dashSepsLeft = ""
                dashSepsLeft += '-' * int(leftValue)
                dashSepsRight = ""
                dashSepsRight += '-' * int(value)

                f.write(f"{dashSepsLeft} {name} {dashSepsRight}")
                f.write(separater + " ")

            f.write("\n\n")
            f.write(firstPusher)


            for i in states:
                name, state = i
                f.write(f" ------------------ Utility: {state.utilityValue} {'-' if state.utilityValue < 10 and state.utilityValue > 0 else ''}------------------")
                f.write(separater)

            f.write("\n\n")
            f.write(firstPusher)
            for i in states:
                name, state = i
                f.write(f" ------------- Player: {state.player} --------------")
                f.write(separater)

            f.write("\n\n")
            f.write(firstPusher)
            for i in states:
                f.write(" ---0-----1-----2-----3-----4-----5-----6-----7---")
                f.write(separater)

            f.write("\n")

            for row in range(BOARD_DIM):
                f.write(f" {row} ")
                for tup in states:
                    name, state = tup
                    state.game.saveSingleRowToFile(row, f)
                    f.write(separater)
                f.write("\n")
                f.write(firstPusher)
                for state in states:
                    f.write(" -------------------------------------------------")
                    f.write(separater)
                f.write("\n")

            f.write("\n\n")
            f.write(firstPusher + " ")

    def printBoard(self, board):
        with open("tree.txt", "w") as f:
            f.write(f"Player: {board.turn}")
            board.saveBoardToFile(f)

    def printAllBoard(self, boards):
        with open("gameHistory.txt", "w") as f:
            for board in boards:
                f.write(f"Player: {board.turn}\n")
                board.saveBoardToFile(f)

    def printAI(self, ai, nextState, sorting=False):
        wholeTree = ai.getDecisionTree()

        with open("tree.txt", "w") as f:
            f.write("\n\n   Decision Tree:")
            for i in range(len(wholeTree)):
                array = wholeTree[i]
                if sorting:
                    if i % 2 == 1:
                        array.sort(key=lambda x: x[1].utilityValue, reverse=True)
                    else:
                        array.sort(key=lambda x: x[1].utilityValue)

                self.saveRowOfStates(array, i, f)
                f.write("\n")
            f.write("\n")
            f.write("Chosen state:")
            f.write("\n")
            nextState.game.saveBoardToFile(f)