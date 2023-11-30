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

board = create_board()
print_board(board)