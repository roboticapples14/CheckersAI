import copy
from AI.src.AI import State, Minimax, UtilityMode
from Game.src.Board import Checkers, Player
from src.Printer import Printer

class MyBenchMark():
    def test_stdAI_vs_stdAI(self):

        number = 4
        benchmarkResults = [[[] for _ in range(number)] for _ in range(number)] # [[(whiteWins, blackWins, ties, timeouts)]]

        for depth1 in range(number):
            for depth2 in range(number):
                # boardStates = []
                rounds = 0
                whiteWins = 0
                blackWins = 0
                ties = 0
                timeouts = 0

                x = 100
                AI1 = depth1 + 1
                AI2 = depth2 + 1

                AI1Mode = UtilityMode.Standard
                AI2Mode = UtilityMode.StandardPro

                print(f"🔔🔔🔔AI1 on {AI1Mode}, {AI1} vs AI2 on {AI2Mode}, {AI2}!🔔🔔🔔")
                # print(f"Black will play on mode {AI1Mode} with difficulty {AI1}")
                # print(f"White will play on mode {AI2Mode} with difficulty {AI2}")
                # print("\n🔔🔔🔔The games starts now!🔔🔔🔔")

                for _ in range(x):
                    game = Checkers()
                    # boardStates.append(game)

                    while game.game_ended == False:
                        # AI BLACK
                        ai_black = Minimax(game, Player.BLACK, AI1, utilityMode=AI1Mode)
                        nextState = ai_black.getBestMove(True, firstMove=(rounds == 0))
                        game = nextState.game
                        # boardStates.append(game)

                        if game.game_ended:
                            # print(f"🏁 Game ended, winner is: {game.win} 🏁 after {rounds} rounds")
                            # game.printBoard()
                            if game.win == Player.WHITE:
                                whiteWins += 1
                            elif game.win == Player.BLACK:
                                blackWins += 1
                            else:
                                ties += 1
                            break

                        # AI WHITE
                        ai_white = Minimax(game, Player.WHITE, AI2, utilityMode=AI2Mode)
                        nextState2 = ai_white.getBestMove(True)
                        game = nextState2.game
                        # boardStates.append(game)

                        if game.game_ended:
                            # print(f"🏁 Game ended, winner is: {game.win} 🏁 after {rounds} rounds")
                            # game.printBoard()
                            if game.win == Player.WHITE:
                                whiteWins += 1
                            elif game.win == Player.BLACK:
                                blackWins += 1
                            else:
                                ties += 1
                            break

                        rounds += 1
                        n = 300
                        if rounds > n:
                            # print(f"Just hit more than {n} rounds")
                            # boardStates[-1].printBoard()
                            timeouts += 1
                            break
                
                benchmarkResults[depth1-1][depth2-1] = (whiteWins, blackWins, ties, timeouts)

        # print(f"Summary after {x} games:")
        # print(f"Black won {blackWins} times on mode {AI1Mode} with difficulty {AI1}")
        # print(f"White won {whiteWins} times on mode {AI2Mode} with difficulty {AI2}")
        # print(f"Timeouts: {timeouts}")

        # print the bemchmark results matrix
        print("Benchmark results:")
        for row in benchmarkResults:
            print(row)


MyBenchMark().test_stdAI_vs_stdAI()