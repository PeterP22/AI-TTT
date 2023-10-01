from abc import ABC, abstractmethod


class Game(ABC):

    @abstractmethod
    def make_move(self, move):
        pass

    @abstractmethod
    def is_game_over(self):
        pass

    @abstractmethod
    def get_winner(self):
        pass

    @abstractmethod
    def get_valid_moves(self):
        pass
