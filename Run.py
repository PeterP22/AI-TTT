import os
import pickle
import random

from AlgorithmFactory import AlgorithmFactory
from GameFactory import GameFactory
from Utils import board_to_state


def display_values_from_file(filename):
    """
    Display the values saved inside the .pkl file.
    """
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            values = pickle.load(f)
            for state, value in values.items():
                print(f"State: {state}, Value: {value}")
    else:
        print(f"{filename} does not exist!")


def print_progress_bar(iteration, total, bar_length=50):
    progress = (iteration / total)
    arrow = '-' * int(round(progress * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    print('\r[{}] {}/{}'.format(arrow + spaces, iteration, total), end='')


def get_board_size():
    print("\nPlease select a board size:")
    print("1 - 3x3 / 2 - 5x5 / 3 - 7x7")
    size_mapping = {1: 3, 2: 5, 3: 7}
    return size_mapping[int(input())]


def get_algorithm_type():
    print("\nPlease select an algorithm to play against:")
    print("Select Algorithm: 1 - ReinforcementLearning / 2 - ValueIteration / 3 - QLearning")
    algorithm_mapping = {1: 'ReinforcementLearning', 2: 'ValueIteration', 3: 'QLearning'}
    algorithm_type = int(input())
    print(f"You have chosen to play against the {algorithm_mapping[algorithm_type]} algorithm")
    return algorithm_mapping[algorithm_type]


def load_strategy(ai_strategy, filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            if 'vi_values' in filename:
                ai_strategy.V = pickle.load(f)
            elif 'q_table' in filename:
                ai_strategy.Q = pickle.load(f)


def train_strategy(game, ai_strategy, num_games, exploration_prob, algorithm_type):
    if algorithm_type == 'ValueIteration':
        for i in range(1, num_games + 1):
            print_progress_bar(i, num_games)
            while not game.is_game_over():
                if game.current_player == game.AI_symbol:
                    move = ai_strategy.calculate_best_move(game)
                    game.make_move(move)
                else:
                    ai_strategy2 = AlgorithmFactory.create_algorithm('ValueIteration')(game.board, game.human_symbol, game.AI_symbol)
                    move = random.choice(game.get_valid_moves()) if random.random() < exploration_prob else ai_strategy2.calculate_best_move(game)
                    game.make_move(move)

            # After each game, perform value iteration for a few iterations to update the value function
            ai_strategy.value_iteration(game, num_iterations=10)
            game.reset_game()

    elif algorithm_type == 'QLearning':
        for i in range(1, num_games + 1):
            print_progress_bar(i, num_games)
            previous_state = None
            previous_action = None
            while not game.is_game_over():
                current_state = board_to_state(game.board)
                if game.current_player == game.AI_symbol:
                    action = ai_strategy.calculate_best_move(game)
                    game.make_move(action)
                    if previous_state is not None:
                        reward = game.calculate_reward()
                        ai_strategy.update_q_value(game, previous_state, previous_action, reward, current_state)
                    previous_state = current_state
                    previous_action = action
                else:
                    move = random.choice(game.get_valid_moves())
                    game.make_move(move)
            game.reset_game()



def save_strategy(ai_strategy, filename):
    with open(filename, "wb") as f:
        if 'vi_values' in filename:
            pickle.dump(ai_strategy.V, f)
        elif 'q_table' in filename:
            pickle.dump(ai_strategy.Q, f)


def play_game(game, ai_strategy):
    while not game.is_game_over():
        game.display_game()
        if game.current_player == game.human_symbol:
            move = tuple(map(int, input("Enter your move (row, col): ").split(",")))
            while move not in game.get_valid_moves():
                print("Invalid move! Try again.")
                move = tuple(map(int, input("Enter your move (row, col): ").split(",")))
            game.make_move(move)
        else:
            print("Current board state before AI move:")
            game.display_game()
            move = ai_strategy.calculate_best_move(game)
            print(f"AI is making move: {move}")
            game.make_move(move)
    game.display_game()


if __name__ == "__main__":
    print("Welcome to Tic Tac Toe!")
    print("You are playing as X, and the AI is playing as O.")
    print("To make a move, enter the row and column of the cell you want to play in, separated by a comma.")
    print("Good luck!")

    # check the values saved in the .pkl file to ensure that the training is updating the values accordingly
    # display_values_from_file("vi_values_3x3.pkl")

    board_size = get_board_size()  # 3x3, 5x5, 7x7
    algorithm_type = get_algorithm_type()  # ReinforcementLearning, ValueIteration, QLearning

    filename_mapping = {
        'ValueIteration': f"vi_values_{board_size}x{board_size}.pkl",
        'QLearning': f"q_table_{board_size}x{board_size}.pkl"
    }

    game = GameFactory.create_game('TicTacToe', algorithm_type, board_size)
    ai_strategy = AlgorithmFactory.create_algorithm(algorithm_type)(game.board, game.AI_symbol, game.human_symbol)

    load_strategy(ai_strategy, filename_mapping[algorithm_type])

    if algorithm_type == 'ValueIteration':
        num_games = int(input("Enter number of training games for ValueIteration (or enter 0 to skip training): "))
    elif algorithm_type == 'QLearning':
        num_games = int(input("Enter number of training episodes for QLearning (or enter 0 to skip training): "))

    exploration_prob = 0.3
    train_strategy(game, ai_strategy, num_games, exploration_prob, algorithm_type)



    save_strategy(ai_strategy, filename_mapping[algorithm_type])

    # Print a new line
    print()

    print("\nPlaying a game against the AI...")

    play_game(game, ai_strategy)

    winner = game.get_winner()
    if winner == "Draw":
        print("It's a draw!")
    elif winner == game.AI_symbol:
        print("AI wins!")
    else:
        print("You win!")
