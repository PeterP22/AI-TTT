def state_to_board(state):
    board_size = int(len(state) ** 0.5)
    board = []

    for i in range(board_size):
        row = list(state[i * board_size:(i + 1) * board_size])
        board.append(row)

    return board


def board_to_state(game_board):
    # If the game_board is a list, use it directly; otherwise, use game_board.board
    board = game_board if isinstance(game_board, list) else game_board.board
    return ''.join([''.join(row) for row in board])




