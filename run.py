# Library imports

import gspread
from google.oauth2.service_account import Credentials
import random
import pyfiglet
from colorama import just_fix_windows_console

just_fix_windows_console()
from colorama import Fore, Back, Style

# API setup

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

# Main function


def main_menu():
    while True:
        """
        Show welcome message and menu
        """
        result = pyfiglet.figlet_format("Welcome to Connect Four", font="bulbhead")
        print(Fore.YELLOW + result)
        print(Style.RESET_ALL)

        print("1. Start Game")
        print("2. Game Instructions")
        print("3. Hall of Fame")
        print("4. Quit\n")

        choice = input("Please choose an option (1/2/3/4):\n")
        print()

        if choice == "1":
            while True:
                player_name = input(
                    "Please enter your name (min. 3 characters with at least 1 letter): \n"
                )
                if len(player_name) >= 3 and any(char.isalpha() for char in player_name):
                    start_game(player_name)
                    break
                else:
                    print(
                        Fore.RED
                        + "Invalid name. Please enter at least 3 characters with at least 1 letter.\n"
                    )
                    print(Style.RESET_ALL)
        elif choice == "2":
            show_game_instructions()
        elif choice == "3":
            show_hall_of_fame()
        elif choice == "4":
            print(Fore.YELLOW + "ByeBye, thank you for playing!" + Style.RESET_ALL)
            break


# Start game


def start_game(player_name):
    print()

    existing_player, player_index = find_player(player_name)

    if existing_player:
        print(Fore.CYAN + f"Welcome back, {existing_player['player_name']}!")
        print(Fore.GREEN + f"Won Games: {existing_player['games_won']}")
        print(Fore.RED + f"Lost Games: {existing_player['games_lost']}\n")
        print(Style.RESET_ALL)
    else:
        print(Fore.CYAN + f"Welcome, {player_name}!\n")
        print(Style.RESET_ALL)

    while True:
        board = create_board()
        print_board(board)
        game_over = False
        quit_game = False

        while not game_over:
            col_input = input(
                "Choose a column to place your piece (1-7), or press 'Q' to quit: \n"
            )

            if col_input.lower() == "q":
                while True:
                    confirm_quit = input(
                        "Are you sure you want to quit? (y/n): \n"
                    ).lower()
                    if confirm_quit == "y":
                        print("\nQuitting the game.\n")
                        main_menu()
                        return
                    elif confirm_quit == "n":
                        break
                    else:
                        print(Fore.RED + "Invalid input. Please enter 'y' or 'n'.\n")
                        print(Style.RESET_ALL)
                if quit_game:
                    main_menu()
                    return
            elif col_input.isdigit():
                col = int(col_input) - 1
                if 0 <= col < 7:
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        place_piece(board, row, col, Fore.GREEN + "P" + Style.RESET_ALL)

                        print_board(board)

                        if check_win(board, Fore.GREEN + "P" + Style.RESET_ALL):
                            print(
                                Fore.GREEN
                                + f"Congratulations, {player_name}! You won!\n"
                            )
                            print(Style.RESET_ALL)
                            update_player_record(player_index, True)
                            game_over = True

                        if all(row.count("P") + row.count("O") == 7 for row in board):
                            print(Fore.YELLOW + "It's a tie!")
                            print(Style.RESET_ALL)
                            game_over = True

                        if not game_over:
                            computer_col = random.randint(0, 6)

                            if is_valid_location(board, computer_col):
                                computer_row = get_next_open_row(board, computer_col)
                                place_piece(
                                    board,
                                    computer_row,
                                    computer_col,
                                    Fore.RED + "C" + Style.RESET_ALL,
                                )
                                print_board(board)
                                print(Style.RESET_ALL)

                                if check_win(board, Fore.RED + "C" + Style.RESET_ALL):
                                    print(Fore.RED + "Computer wins!\n")
                                    print(Style.RESET_ALL)
                                    update_player_record(player_index, False)
                                    game_over = True
                            else:
                                print()
                                print(
                                    Fore.RED
                                    + "Invalid move by computer. Skipping computer's turn.\n"
                                )
                                print(Style.RESET_ALL)
                    else:
                        print()
                        print(
                            Fore.RED + "Invalid move. Please choose a valid column.\n"
                        )
                        print(Style.RESET_ALL)
                else:
                    print()
                    print(
                        Fore.RED
                        + "Column number out of range. Please choose a number between 1 and 7.\n"
                    )
                    print(Style.RESET_ALL)
            else:
                print()
                print(
                    Fore.RED
                    + "Invalid input. Please enter a valid number between 1 and 7 or 'Q' to quit.\n"
                )
                print(Style.RESET_ALL)

            if game_over or quit_game:
                while True:
                    play_again = input("Do you want to play again? (y/n):\n").lower()
                    print()
                    if play_again == "y":
                        print(Fore.BLUE + "Starting a new game.")
                        print(Style.RESET_ALL)
                        return start_game(player_name)
                    elif play_again == "n":
                        print(Fore.BLUE + "Returning to Main Menu.")
                        print(Style.RESET_ALL)
                        return
                    else:
                        print(Fore.RED + "Invalid input. Please enter 'y' or 'n'.\n")
                        print(Style.RESET_ALL)

    return

    play_again = input("Do you want to play again? (y/n):\n").lower()
    print()
    if play_again != "y":
        print(Fore.BLUE + "Returning to Main Menu.")
        print(Style.RESET_ALL)
        return main_menu()


# Find player


def find_player(player_name):
    """
    Find a player in the hof sheet by name
    """
    #  Check if the player name contains at least one letter and has more than 2 characters
    if any(char.isalpha() for char in player_name) and len(player_name) > 2:
        player_data = HOF_SHEET.get_all_records()
        for index, player in enumerate(player_data):
            if player["player_name"] == player_name:
                return player, index + 2
    else:
        print(
            Fore.RED
            + "Error: Name must contain at least one letter and be at least 3 characters long.\n"
        )
        print(Style.RESET_ALL)
        return None, -1

    # Add a new player only if the name contains at least one letter and has more than 2 characters
    if any(char.isalpha() for char in player_name) and len(player_name) > 2:
        new_index = add_new_player(player_name)
        return None, new_index


# Add player if not found in sheet


def add_new_player(player_name):
    """
    Adds a new player to the hof sheet
    """
    new_player_data = [player_name, 0, 0]
    HOF_SHEET.append_row(new_player_data)
    print(Fore.GREEN + f"New Player {player_name} added...\n")
    print(Style.RESET_ALL)

    player_data = HOF_SHEET.get_all_records()
    new_index = len(player_data) + 1
    return new_index


# Update records


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


# Create board


def create_board():
    """
    Create a game board with 6 rows and 7 columns
    """
    return [[" " for _ in range(7)] for _ in range(6)]


# Print board


def print_board(board):
    """
    Prints the game board in a readable format
    """
    print(" 1 2 3 4 5 6 7")
    print("---------------")
    for row in board:
        print("|" + "|".join(row) + "|")
    print("---------------\n")


# Validation check


def is_valid_location(board, col):
    """
    Checks if a move is valid in a given column
    """
    if 0 <= col < 7:
        return board[0][col] == " "
    else:
        return False


# Find next open row


def get_next_open_row(board, col):
    """
    Finds the next available row in a given column
    """
    for row in range(5, -1, -1):
        if board[row][col] == " ":
            return row
    return -1


# Place piece


def place_piece(board, row, col, piece):
    """
    Place a piece on the game board at specified location
    """
    board[row][col] = piece


# Check win conditions


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


# Game instructions


def show_game_instructions():
    result = pyfiglet.figlet_format("Game Instructions", font="bulbhead")
    print(Fore.YELLOW + result)
    print(Style.RESET_ALL)
    print("-" * 60)
    print("\nConnect Four is a two-player connection game in which")
    print("the players take turns dropping discs from the top into")
    print("a seven-column, six-row vertically suspended grid.\n")
    print("The goal of the game is to connect four discs vertically,")
    print("horizontally, or diagonally before your opponent.\n")
    print(
        ("The player is displayed as ")
        + Fore.GREEN
        + "P"
        + Style.RESET_ALL
        + " on the game board when they"
    )
    print(
        ("place a piece, and the computer is represented by a ")
        + Fore.RED
        + "C"
        + Style.RESET_ALL
        + ".\n"
    )
    print("-" * 60)
    print()
    input(Fore.BLUE + "Press Enter to return to Main Menu!\n")
    print(Style.RESET_ALL)


# Hall of Fame


def show_hall_of_fame():
    result = pyfiglet.figlet_format("Hall of Fame", font="bulbhead")
    print(Fore.YELLOW + result)
    print(Style.RESET_ALL)
    print(f"{'Player':<20}{'Wins':<10}{'Losses':<10}")
    print("-" * 40)

    player_data = HOF_SHEET.get_all_records()
    for player in player_data:
        print(
            f"{player['player_name']:<20}{player['games_won']:<10}{player['games_lost']:<10}"
        )
    print("-" * 40)

    input(Fore.BLUE + "\nPress Enter to return to Main Menu!\n")
    print(Style.RESET_ALL)


# Main menu

main_menu()
