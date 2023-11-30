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

board = create_board()
print("Is column 0 ok?", is_valid_location(board, 0))
print("Is column 7 ok?", is_valid_location(board, 7))