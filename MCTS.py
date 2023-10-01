from Node import Node
import math
import random
from Utils import board_to_state



class MCTS:
    def __init__(self, game, q_table, simulations=1000, C=1.4):
        self.root = Node(game)
        self.game = game
        self.q_table = q_table
        self.simulations = simulations
        self.C = C  # Exploration factor for UCB1

    def search(self):
        for _ in range(self.simulations):
            node = self._select(self.root)
            if not node.children and not node.game_state.is_game_over():
                node = self._expand(node)
            result = self._simulate(node)
            self._backpropagate(node, result)
        return self._best_move(self.root)

    def _ucb1(self, node):
        if node.visits == 0:
            return float('inf')  # Prioritize unexplored nodes
        return node.value / node.visits + self.C * math.sqrt(math.log(node.parent.visits) / node.visits)

    def _select(self, node):
        while node.children:
            node = max(node.children, key=self._ucb1)
        return node

    def _expand(self, node):
        for move in self.game.get_valid_moves():
            if move not in [child.move for child in node.children]:
                child_game_state = node.game_state.copy()
                child_game_state.make_move(move)
                child_node = Node(child_game_state, parent=node)
                node.children.append(child_node)
        return random.choice(node.children)  # Return a random child node

    def _simulate(self, node):
        current_game_state = node.game_state.copy()
        while not current_game_state.is_game_over():
            state = board_to_state(current_game_state.board)
            if state in self.q_table:
                # Use the Q-values to select the best move
                move = max(self.q_table[state], key=self.q_table[state].get)
            else:
                # If the state is not in the Q-table, select a move randomly
                move = random.choice(current_game_state.get_valid_moves())
            current_game_state.make_move(move)

        # Determine the outcome of the game
        winner = current_game_state.get_winner()
        if winner == self.game.AI_symbol:
            return 1
        elif winner == self.game.human_symbol:
            return -1
        else:  # Draw
            return 0

    def _backpropagate(self, node, result):
        while node:  # while node is not None
            node.visits += 1
            node.value += result
            node = node.parent  # move up to the parent

    def _best_move(self, node):
        """
        Determines the best move from the root node.
        Returns the move associated with the child node with the most visits.
        """
        sorted_children = sorted(node.children, key=lambda child: child.visits, reverse=True)
        if not sorted_children:
            return None
        return sorted_children[0].move

