import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("connect_four")


def main_menu():
    while True:
        print("Main Menu:\n")
        print("1. Start Game")
        print("2. Game Instructions")
        print("3. Hall of Fame")
        print("4. Quit\n")

        choice = input("Please choose an option (1/2/3/4):\n")

        if choice == "1":
            start_game()
        elif choice == "2":
            show_game_instructions()
        elif choice == "3":
            show_hall_of_fame
        elif choice == "4":
            print("Good bye. Thank you for playing!")
            break
        else:
            print("Invalid input. Please select one of the available options\n")


def start_game():
    player_name = input("Please enter your name:")
    print(f"Welcome, {player_name}!")

    while True:
        board = create_board()
        print_board(board)

        while True:
            col_input = input(
                "Choose a column to place your piece (1-7), or press Enter to quit: "
            )

            if not col_input:
                print("Quitting the game.")
                return

            try:
                col = int(col_input) - 1

                if 0 <= col < 7:
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        place_piece(board, row, col, "P")

                        print_board(board)

                        if check_win(board, "P"):
                            print(f"Congratulations, {player_name}! You won!\n")
                            break

                        if all(row.count("P") + row.count("O") == 7 for row in board):
                            print("It's a tie!")
                            break
                    else:
                        print("Invalid move. Please choose a valid column.")
                else:
                    print(
                        "Column number out of range. Please choose a number between 1 and 7."
                    )
            except ValueError:
                print(
                    "Invalid input. Please enter a valid number between 1 and 7 or press Enter to quit."
                )

        play_again = input("Do you want to play again? (y/n):\n").lower()
        if play_again != "y":
            print("Back to Main Menu!\n")
            break


def show_game_instructions():
    print("Game Instructions:\n")
    print("Connect Four is a two-player connection game in which")
    print("the players take turns dropping discs from the top into")
    print("a seven-column, six-row vertically suspended grid.\n")
    print("The goal of the game is to connect four discs vertically,")
    print("horizontally, or diagonally before your opponent.\n")
    input("Press Enter to return to Main Menu!\n")


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


main_menu()
