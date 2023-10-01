import random
from MCTS import MCTS
from Utils import board_to_state, state_to_board


class QLearningStrategy:

    def __init__(self, board, ai_symbol, human_symbol, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0,
                 exploration_decay=0.995):
        self.board = board
        self.ai_symbol = ai_symbol
        self.human_symbol = human_symbol
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay

        # Q-table, initialized with zeros
        self.Q = {}

    def calculate_best_move(self, game):
        state = board_to_state(game.board)

        # Exploration vs Exploitation
        if random.uniform(0, 1) < self.exploration_rate:
            action = random.choice(self.get_possible_actions(game, state))
        else:
            # Using MCTS to get best action
            mcts = MCTS(game, self.Q)
            action = mcts.search()

            # Adding randomness to exploitation
            best_actions = [act for act in self.get_possible_actions(game, state) if
                            self.Q.get((state, act), 0) == self.Q.get((state, action), 0)]
            action = random.choice(best_actions)

        # Decay exploration rate and ensure it doesn't go below 0.01
        self.exploration_rate = max(self.exploration_rate * self.exploration_decay, 0.01)
        return action

    def update_q_value(self, game, old_state, action, reward, new_state):
        old_value = self.Q.get((old_state, action), 0)

        # If the new state results in the end of the game (win, lose, or draw)
        # then there's no future action from that state, hence the max_future_value is 0
        if game.get_winner() or (' ' not in board_to_state(game.board)):
            max_future_value = 0
        else:
            max_future_value = max(
                [self.Q.get((new_state, new_action), 0) for new_action in
                 self.get_possible_actions_from_state(new_state)]
            )

        new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (
                reward + self.discount_factor * max_future_value)
        self.Q[(old_state, action)] = new_value

    def get_possible_actions(self, game, state):
        board = state_to_board(state)
        return [(i, j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == ' ']

    def get_possible_actions_from_state(self, state):
        board = state_to_board(state)
        return [(i, j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == ' ']

    def get_best_action(self, game, state):
        actions = self.get_possible_actions(game, state)
        best_action = max(actions, key=lambda action: self.Q.get((state, action), 0))
        return best_action


