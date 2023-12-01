def create_board():
    """
    Create a game board with 6 rows and 7 columns
    """
    return [[" " for _ in range(7)] for _ in range(6)]


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
        return board[0][col] == " "
    else:
        return False


def get_next_open_row(board, col):
    """
    Finds the next available row in a given column
    """
    for row in range(5, -1, -1):
        if board[row][col] == " ":
            return row
    return -1


def place_piece(board, row, col, piece):
    """
    Place a piece on the game board at specified location
    """
    board[row][col] = piece


def check_win(board, piece):
    """
    Checks if a player has won
    """
    for row in range(6):
        for col in range(4):
            if (
                board[row][col] == piece
                and board[row][col + 1] == piece
                and board[row][col + 2] == piece
                and board[row][col + 3] == piece
            ):
                return True

    for row in range(3):
        for col in range(7):
            if (
                board[row][col] == piece
                and board[row + 1][col] == piece
                and board[row + 2][col] == piece
                and board[row + 3][col] == piece
            ):
                return True

    for row in range(3):
        for col in range(4):
            if (
                board[row][col] == piece
                and board[row + 1][col + 1] == piece
                and board[row + 2][col + 2] == piece
                and board[row + 3][col + 3] == piece
            ):
                return True

    for row in range(3):
        for col in range(3, 7):
            if (
                board[row][col] == piece
                and board[row + 1][col - 1] == piece
                and board[row + 2][col - 2] == piece
                and board[row + 3][col - 3] == piece
            ):
                return True

    return False


board = create_board()
place_piece(board, 0, 0, "C")
place_piece(board, 0, 1, "C")
place_piece(board, 0, 2, "C")
place_piece(board, 0, 3, "P")
place_piece(board, 0, 4, "P")
place_piece(board, 0, 5, "P")
place_piece(board, 0, 6, "P")

if check_win(board, "P"):
    print("Player wins!")
elif check_win(board, "C"):
    print("Computer wins!")
else:
    print("Nobody has won yet.")
