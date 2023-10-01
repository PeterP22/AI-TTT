from Utils import state_to_board, board_to_state
import random


class ValueIterationStrategy:
    def __init__(self, board=None, AI_symbol=None, human_symbol=None, discount_factor=0.9):
        self.discount_factor = discount_factor
        self.V = {}  # Value function

    def value_iteration(self, game, num_iterations=10000, tolerance=1e-6):
        """
        Perform the value iteration algorithm.
        """
        for _ in range(num_iterations):
            delta = 0  # Track max change in value function
            for state in self.get_all_possible_states(game):
                if state not in self.V:
                    self.V[state] = 0

                old_value = self.V[state]
                possible_actions = self.get_possible_actions(game, state)
                if possible_actions:  # Only compute Q-values if there are valid actions
                    q_values = {action: self.compute_q_value(game, state, action) for action in possible_actions}
                    self.V[state] = max(q_values.values())

                delta = max(delta, abs(old_value - self.V[state]))

            # Check for convergence
            if delta < tolerance:
                break

    def compute_q_value(self, game, state, action):
        """
        Compute the Q-value for a given state and action.
        """
        next_state, reward = self.get_next_state_and_reward(game, state, action)
        return reward + self.discount_factor * self.V.get(next_state, 0)

    def get_all_possible_states(self, game):
        current_state = board_to_state(game.board)
        if current_state not in self.V:
            self.V[current_state] = 0

        return self.V.keys()

    def get_possible_actions(self, game, state):
        board = state_to_board(state)
        return [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == ' ']

    def get_next_state_and_reward(self, game, state, action):
        board = state_to_board(state)
        x, y = action
        board[x][y] = game.current_player

        winner = game.check_winner(board)
        if winner == game.current_player:
            return board_to_state(board), 1
        elif winner == game.human_symbol:
            return board_to_state(board), -1
        elif not game.get_valid_moves():
            return board_to_state(board), 0
        else:
            return board_to_state(board), -0.1

    def get_best_action(self, game, state):
        actions = self.get_possible_actions(game, state)
        q_values = {action: self.compute_q_value(game, state, action) for action in actions}
        return max(q_values, key=q_values.get)

    def calculate_best_move(self, game):
        state = board_to_state(game.board)
        # Add a 40% chance to make a random move
        if random.random() < 0.4:
            return random.choice(self.get_possible_actions(game, state))
        return self.get_best_action(game, state)

