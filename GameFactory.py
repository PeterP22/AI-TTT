from TicTacToeGame import TicTacToeGame
from AlgorithmFactory import AlgorithmFactory


class GameFactory:

    @staticmethod
    def create_game(game_type, algorithm_type, board_size):
        ai_strategy = AlgorithmFactory.create_algorithm(algorithm_type)
        if game_type == "TicTacToe":
            return TicTacToeGame(ai_strategy, board_size)
        raise ValueError(f"Game {game_type} not supported.")

