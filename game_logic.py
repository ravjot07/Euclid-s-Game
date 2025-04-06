import random

def initialize_board():
    """
    Initialize the board with two distinct random integers between 10 and 50.
    The board is returned as a sorted list.
    """
    a = random.randint(10, 50)
    b = random.randint(10, 50)
    while b == a:
        b = random.randint(10, 50)
    board = sorted([a, b])
    return board

def get_valid_moves(board):
    """
    Given the current board (list of numbers), return a list of valid moves.
    A valid move is a tuple (a, b, diff) where:
      - a and b are distinct numbers from the board,
      - diff = |a - b| is > 0 and not already on the board.
    """
    moves = []
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            diff = abs(board[j] - board[i])
            if diff > 0 and diff not in board:
                moves.append((board[i], board[j], diff))
    return moves

def is_game_over(board):
    """
    The game is over if there are no valid moves left.
    """
    return len(get_valid_moves(board)) == 0

def computer_move(board):
    """
    Return a valid move for the computer.
    For a simple strategy, choose the move with the largest difference.
    Returns the new number (the difference) or None if no move is possible.
    """
    moves = get_valid_moves(board)
    if not moves:
        return None
    best_move = max(moves, key=lambda move: move[2])
    return best_move[2]

def add_number(board, number):
    """
    Add a number to the board if not already present and return the new sorted board.
    """
    if number not in board:
        board.append(number)
        board.sort()
    return board
