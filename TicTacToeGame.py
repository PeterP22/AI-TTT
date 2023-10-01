from Game import Game
from QLearningStrategy import board_to_state
from GameBoard import GameBoard
from Utils import state_to_board


class TicTacToeGame(Game):
    """
    This class represents a game of Tic Tac Toe.
    """

    def __init__(self, ai_strategy_type, board_size=3):
        """
        The constructor for TicTacToeGame class.
        """
        self.board = GameBoard(board_size)
        self.AI = ai_strategy_type(self.board, 'X', 'O')
        self.AI_symbol = 'X'
        self.human_symbol = 'O'
        self.current_player = 'O'  # Human starts first
        self.ai_strategy_type = ai_strategy_type

    def get_valid_moves(self):
        """
        Gets the valid moves on the game board for the current player.
        """
        return self.board.get_empty_positions()

    def make_move(self, move):
        self.board.make_move(move, self.current_player)

        # Switch current player
        self.current_player = 'X' if self.current_player == 'O' else 'O'

    def is_game_over(self):
        """
        Checks if the game is over.
        """
        result = self.board.is_game_over()
        return result != False

    def get_winner(self):
        if self.board.is_winner(self.human_symbol):
            return self.human_symbol
        if self.board.is_winner(self.AI_symbol):
            return self.AI_symbol
        return None  # No winner yet

    def display_game(self):
        """
        Displays the current state of the game board and the game's result.
        """
        self.board.print_board()
        result = self.board.is_game_over()
        if result == 'Draw':
            print('Game Over. Draw!')
        elif result == self.AI_symbol:
            print('Game Over. AI wins!')
        elif result:
            print('Game Over. You win!')

    def calculate_reward(self):
        """
        Calculate and return the reward based on the current state of the game.
        """
        winner = self.get_winner()
        if winner == self.AI_symbol:
            return 1  # AI wins
        elif winner == self.human_symbol:
            return -1  # Human wins
        elif winner is None and ' ' not in board_to_state(self.board):
            return 0  # Draw
        else:
            return 0  # Default reward for non-terminal states

    def reset_game(self):
        self.board.board = [[' ' for _ in range(self.board.width)] for _ in range(self.board.height)]
        self.current_player = self.human_symbol  # or whichever player starts first
        # Reset any other necessary game state attributes here

    def copy(self):
        """
        Create a deep copy of the current game instance.
        """
        # Create a new instance of the game
        new_game = TicTacToeGame(self.ai_strategy_type, self.board.width)  # Using board.width to get the board size

        # Copy the board state
        new_game.board = self.board.copy()

        # Copy other necessary attributes
        new_game.AI_symbol = self.AI_symbol
        new_game.human_symbol = self.human_symbol
        new_game.current_player = self.current_player

        return new_game

    def check_winner(self, board):
        """
        Check for a winner on the provided board.
        """
        if isinstance(board, list):  # If the board is a list, convert it to a GameBoard object
            temp_board = GameBoard(len(board))
            temp_board.board = board
            board = temp_board

        if board.is_winner(self.human_symbol):
            return self.human_symbol
        elif board.is_winner(self.AI_symbol):
            return self.AI_symbol
        return None  # No winner

    def is_game_over_state(self, state):
        board = state_to_board(state)
        return self.check_winner(board) is not None or not self.get_valid_moves()

    def is_win_state(self, state, player_symbol):
        board = state_to_board(state)
        return self.check_winner(board) == player_symbol



