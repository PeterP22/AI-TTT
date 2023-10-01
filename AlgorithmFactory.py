from QLearningStrategy import QLearningStrategy
from ReinforcementLearningStrategy import ReinforcementLearningStrategy
from ValueIterationStrategy import ValueIterationStrategy


class AlgorithmFactory:

    @staticmethod
    def create_algorithm(algorithm_type):
        if algorithm_type == "ReinforcementLearning":
            return ReinforcementLearningStrategy
        elif algorithm_type == "ValueIteration":
            return ValueIterationStrategy
        elif algorithm_type == "QLearning":
            return QLearningStrategy
        raise ValueError(f"Algorithm {algorithm_type} not supported.")
