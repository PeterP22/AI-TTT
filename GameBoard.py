class GameBoard:
    """
    This class represents a game board for Tic Tac Toe.

    Attributes:
    board (list): A 2D list representing the game board.
    size (int): The size of the game board.
    """

    def __init__(self, size):
        self.width = size
        self.height = size
        # Initialize the board as a 2D list filled with empty spaces (' ')
        self.board = [[' ' for _ in range(self.width)] for _ in range(self.height)]

    def is_winner(self, player):
        return self.check_winner_on_board(self.board, player)

    def check_winner_on_board(self, board, player):
        # Check rows and columns
        for i in range(self.width):
            if all([board[i][j] == player for j in range(self.width)]) or \
               all([board[j][i] == player for j in range(self.width)]):
                return True

        # Check diagonals
        if all([board[i][i] == player for i in range(self.width)]) or \
           all([board[i][self.width - 1 - i] == player for i in range(self.width)]):
            return True

        return False

    def print_board(self):
        """
        Prints the current state of the game board.
        """
        for row in self.board:
            print('|'.join(row))
            print('-' * (2 * self.width - 1))

    def is_game_over(self):
        """
        Checks if the game is over.

        Returns:
        str or bool: Returns the winning symbol if there's a winner, 'Draw' if it's a draw, or False otherwise.
        """
        for row in self.board:
            if len(set(row)) == 1 and row[0] != ' ':
                return row[0]

        for col in range(self.width):
            column = [self.board[row][col] for row in range(self.width)]
            if len(set(column)) == 1 and column[0] != ' ':
                return column[0]

        diagonal1 = [self.board[i][i] for i in range(self.width)]
        if len(set(diagonal1)) == 1 and diagonal1[0] != ' ':
            return diagonal1[0]

        diagonal2 = [self.board[i][self.width - 1 - i] for i in range(self.width)]
        if len(set(diagonal2)) == 1 and diagonal2[0] != ' ':
            return diagonal2[0]

        if all(cell != ' ' for row in self.board for cell in row):
            return 'Draw'

        return False

    def get_empty_positions(self):
        """
        Returns the positions of the empty cells on the game board.

        Returns:
        list of tuple: A list containing tuples representing the positions of the empty cells.
        """
        positions = []
        for i in range(self.width):
            for j in range(self.width):
                if self.board[i][j] == ' ':
                    positions.append((i, j))
        return positions

    def make_move(self, position, symbol):
        """
        Makes a move on the board.

        Parameters:
        position (tuple): The row and column where the move should be made.
        symbol (str): The symbol ('X' or 'O') to place on the board.
        """
        if 0 <= position[0] < self.width and 0 <= position[1] < self.width:
            if self.board[position[0]][position[1]] == ' ':
                self.board[position[0]][position[1]] = symbol

    def undo_move(self, position):
        self.board[position[0]][position[1]] = ' '  # assuming ' ' represents an empty cell

    def copy(self):
        """
        Create a deep copy of the current game board.
        """
        new_board = GameBoard(self.width)
        new_board.board = [row.copy() for row in self.board]

        return new_board
