from abc import abstractmethod, ABC


class Algorithm(ABC):

    @abstractmethod
    def calculate_best_move(self, game_state):
        pass
