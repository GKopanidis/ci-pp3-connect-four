def create_board():
    """
    Create a game board with 6 rows and 7 columns
    """
    return [[' ' for _ in range(7)] for _ in range(6)]

def print_board(board):
    """
    Prints the game board in a readable format
    """
    print(" 1 2 3 4 5 6 7")
    print("---------------")
    for row in board:
        print("|" + "|".join(row) + "|")
    print("---------------")

def is_valid_location(board, col):
    """
    Checks if a move is valid in a given column
    """
    if 0 <= col < 7:
        return board[0][col] == ' '
    else: 
        return False

def get_next_open_row(board, col):
    """
    Finds the next available row in a given column
    """
    for row in range(5, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

board = create_board()
col = 4

next_open_row = get_next_open_row(board, col)
print("next free row in column 2:", next_open_row)