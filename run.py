import gspread
from google.oauth2.service_account import Credentials
import random

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("connect_four")
HOF_SHEET = SHEET.worksheet("hof")


def main_menu():
    while True:
        print("Main Menu:\n")
        print("1. Start Game")
        print("2. Game Instructions")
        print("3. Hall of Fame")
        print("4. Quit\n")

        choice = input("Please choose an option (1/2/3/4):\n")
        print()

        if choice == "1":
            start_game()
        elif choice == "2":
            show_game_instructions()
        elif choice == "3":
            show_hall_of_fame()
        elif choice == "4":
            print("Good bye. Thank you for playing!")
            break
        else:
            print("Invalid input. Please select one of the available options\n")


def start_game():
    while True:
        player_name = input("Please enter your name (min. 3 characters): ")
        if len(player_name) >= 3:
            break
        elif len(player_name) > 0:
            print("Error: Name must be at least 3 characters long.\n")
        else:
            print("Error: Name cannot be empty.\n")

    print()

    existing_player, player_index = find_player(player_name)

    if existing_player:
        print(f"Welcome back, {existing_player['player_name']}!")
        print(f"Won Games: {existing_player['games_won']}")
        print(f"Lost Games: {existing_player['games_lost']}\n")
    else:
        print(f"Welcome {player_name}!\n")

    while True:
        board = create_board()
        print_board(board)
        game_over = False

        while not game_over:
            col_input = input(
                "Choose a column to place your piece (1-7), or press Enter to quit: "
            )

            if not col_input:
                confirm_quit = input("Are you sure you want to quit? (y/n): ").lower()
                if confirm_quit == "y":
                    print("Quitting the game.")
                    return
                else:
                    continue

            try:
                col = int(col_input) - 1

                if 0 <= col < 7:
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        place_piece(board, row, col, "P")

                        print_board(board)

                        if check_win(board, "P"):
                            print(f"Congratulations, {player_name}! You won!\n")
                            update_player_record(player_index, True)
                            game_over = True

                        if all(row.count("P") + row.count("O") == 7 for row in board):
                            print("It's a tie!")
                            game_over = True

                        if not game_over:
                            computer_col = random.randint(0, 6)

                            if is_valid_location(board, computer_col):
                                computer_row = get_next_open_row(board, computer_col)
                                place_piece(board, computer_row, computer_col, "C")
                                print_board(board)

                                if check_win(board, "C"):
                                    print("Computer wins!\n")
                                    update_player_record(player_index, False)
                                    game_over = True
                            else:
                                print(
                                    "Invalid move by computer. Skipping computer's turn.\n"
                                )
                    else:
                        print("Invalid move. Please choose a valid column.\n")
                else:
                    print(
                        "Column number out of range. Please choose a number between 1 and 7.\n"
                    )
            except ValueError:
                print(
                    "Invalid input. Please enter a valid number between 1 and 7 or press Enter to quit.\n"
                )

            if game_over:
                break

        play_again = input("Do you want to play again? (y/n):\n").lower()
        print()
        if play_again != "y":
            print("Returning to Main Menu.")
            break


def find_player(player_name):
    """
    Find a player in the hof sheet by name
    """
    player_data = HOF_SHEET.get_all_records()
    for index, player in enumerate(player_data):
        if player["player_name"] == player_name:
            return player, index + 2
    new_index = add_new_player(player_name)
    return None, new_index


def add_new_player(player_name):
    """
    Adds a new player to the hof sheet
    """
    new_player_data = [player_name, 0, 0]
    HOF_SHEET.append_row(new_player_data)
    print(f"New Player {player_name} added...\n")

    player_data = HOF_SHEET.get_all_records()
    new_index = len(player_data) + 1
    return new_index


def update_player_record(player_index, won):
    """
    Update the player win and loss in the google sheet
    """
    player_record = HOF_SHEET.row_values(player_index)
    new_wins = int(player_record[1])
    new_losses = int(player_record[2])

    if won:
        new_wins += 1
        HOF_SHEET.update_cell(player_index, 2, new_wins)
    else:
        new_losses += 1
        HOF_SHEET.update_cell(player_index, 3, new_losses)

    return f"Updated record for player at index {player_index}: Wins - {new_wins}, Losses - {new_losses}"


def show_game_instructions():
    print("Game Instructions:\n")
    print("Connect Four is a two-player connection game in which")
    print("the players take turns dropping discs from the top into")
    print("a seven-column, six-row vertically suspended grid.\n")
    print("The goal of the game is to connect four discs vertically,")
    print("horizontally, or diagonally before your opponent.\n")
    input("Press Enter to return to Main Menu!\n")


def show_hall_of_fame():
    print("Hall of Fame:\n")
    print(f"{'Player':<20}{'Wins':<10}{'Losses':<10}")
    print("-" * 40)

    player_data = HOF_SHEET.get_all_records()
    for player in player_data:
        print(
            f"{player['player_name']:<20}{player['games_won']:<10}{player['games_lost']:<10}"
        )

    input("\nPress Enter to return to Main Menu!\n")


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
    print("---------------\n")


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
