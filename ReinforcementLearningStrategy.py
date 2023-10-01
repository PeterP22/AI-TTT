import pickle
import random
from Algorithm import Algorithm


class ReinforcementLearningStrategy(Algorithm):
    """
    This class represents a Tic Tac Toe AI that uses a Q-table to decide its moves.
    """

    def __init__(self, board, ai_symbol, human_symbol, learning_rate=0.5, discount_factor=0.9):
        self.board = board
        self.ai_symbol = ai_symbol
        self.human_symbol = human_symbol
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.last_move = None

    def calculate_best_move(self, game_state):
        state = str(game_state.board.board)
        if state not in self.q_table:
            self.q_table[state] = {move: 0 for move in game_state.get_valid_moves()}

        max_q_value = max(self.q_table[state].values())
        best_moves = [move for move, q_value in self.q_table[state].items() if q_value == max_q_value]
        return random.choice(best_moves)

    def update_q_table(self, reward, next_state):
        state = str(self.board.board)  # Adjusted from grid to board
        if next_state not in self.q_table:
            self.q_table[next_state] = {move: 0 for move in self.board.get_empty_positions()}

        max_next_q_value = max(self.q_table[next_state].values())
        self.q_table[state][self.last_move] += self.learning_rate * (
                    reward + self.discount_factor * max_next_q_value - self.q_table[state][self.last_move])

    def save_q_table(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            self.q_table = {}
