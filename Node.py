class Node:
    def __init__(self, game_state, move=None, parent=None):
        self.game_state = game_state
        self.move = move
        self.parent = parent
        self.children = []
        self.value = 0
        self.visits = 0
