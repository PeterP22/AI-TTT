from AlgorithmFactory import AlgorithmFactory
from GameFactory import GameFactory


class GameFramework:

    def __init__(self, game_type, algorithm_type):
        self.game = GameFactory.create_game(game_type)
        self.algorithm = AlgorithmFactory.create_algorithm(algorithm_type)

    def play_game(self):
        self.game.display_game()  # Show initial game state
        while not self.game.is_game_over():
            if self.game.current_player == 'O':  # Assuming 'O' is the human player's symbol
                move = tuple(map(int, input("Enter your move (format: row,col): ").split(',')))
            else:
                move = self.algorithm.calculate_best_move()
            self.game.make_move(move)
            self.game.display_game()
