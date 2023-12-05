# Library imports

import gspread
from google.oauth2.service_account import Credentials
import random
import pyfiglet
from colorama import just_fix_windows_console

just_fix_windows_console()
from colorama import Fore, Back, Style
import os

# Global variable

is_running = True


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

# Clear screen


def clear_screen():
    """
    Clear Screen
    """
    # For Windows
    if os.name == "nt":
        os.system("cls")
    # For Mac and Linux
    else:
        os.system("clear")


# Prepare game


def prepare_game(player_name, vs_computer, player2_name=""):
    """
    Prepare game and show welcome message
    """
    clear_screen()
    existing_player, player1_index = find_player(player_name)
    greet_player(existing_player, player_name)

    if not vs_computer:
        existing_player2, player2_index = find_player(player2_name)
        greet_player(existing_player2, player2_name)
    input("Press any key to start the game...")
    clear_screen()


# Get valid player


def get_valid_player_name(prompt="Enter your name"):
    while True:
        player_name = input(
            f"{prompt} (min. 3 characters with at least 1 letter): \n"
        ).strip()
        if len(player_name) >= 3 and any(char.isalpha() for char in player_name):
            return player_name
        else:
            print(
                Fore.RED
                + "Invalid name. Please enter at least 3 characters with at least 1 letter.\n"
                + Style.RESET_ALL
            )


# Find player


def find_player(player_name):
    """
    Find a player in the hof sheet by name using a more efficient method.
    """
    try:
        cell = HOF_SHEET.find(player_name)
        if cell:
            player_data = HOF_SHEET.row_values(cell.row)
            player = {
                "player_name": player_data[0],
                "games_won": int(player_data[1]),
                "games_lost": int(player_data[2])
            }
            return player, cell.row
        else:
            raise ValueError("Player not found")

    except (gspread.exceptions.GSpreadException, ValueError):
        # Add a new player if not found
        if any(char.isalpha() for char in player_name) and len(player_name) > 2:
            new_index = add_new_player(player_name)
            return None, new_index
        else:
            print(Fore.RED + "Invalid player name." + Style.RESET_ALL)
            return None, -1


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


# Greet players


def greet_player(existing_player, player_name):
    if existing_player:
        print(Fore.CYAN + f"Welcome back, {existing_player['player_name']}!")
        print(Fore.GREEN + f"Won Games: {existing_player['games_won']}")
        print(Fore.RED + f"Lost Games: {existing_player['games_lost']}\n")
    else:
        print(Fore.CYAN + f"Welcome, {player_name}!\n")
    print(Style.RESET_ALL)


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


# Player move


def get_player_move(player_name):
    while True:
        col_input = input(
            f"{player_name}, choose a column to place your piece (1-7), or press 'Q' to quit: \n"
        )

        if col_input.lower() == "q":
            confirm_quit = input("Are you sure you want to quit? (y/n): \n").lower()
            if confirm_quit == "y":
                print("\nQuitting the game.\n")
                return None
            elif confirm_quit == "n":
                continue
            else:
                print(Fore.RED + "Invalid input. Please enter 'y' or 'n'.\n")
                print(Style.RESET_ALL)
        elif col_input.isdigit():
            col = int(col_input) - 1
            if 0 <= col < 7:
                return col
            else:
                print(
                    Fore.RED
                    + "Column number out of range. Please choose a number between 1 and 7.\n"
                )
                print(Style.RESET_ALL)
        else:
            print(
                Fore.RED
                + "Invalid input. Please enter a valid number between 1 and 7 or 'Q' to quit.\n"
            )
            print(Style.RESET_ALL)


# Check blocking move


def check_for_blocking_move(board, player_piece):
    """
    Checks if a move by the player can be blocked
    """
    opponent_piece = (
        Fore.GREEN + "P" + Style.RESET_ALL
        if player_piece == Fore.RED + "C" + Style.RESET_ALL
        else Fore.RED + "C" + Style.RESET_ALL
    )

    # Horizontal
    for row in range(6):
        for col in range(4):
            if (
                board[row][col] == player_piece
                and board[row][col + 1] == player_piece
                and board[row][col + 2] == player_piece
                and board[row][col + 3] == " "
                and (row == 5 or board[row + 1][col + 3] != " ")
            ):
                return col + 3

    # Vertical
    for col in range(7):
        for row in range(3):
            if (
                board[row][col] == opponent_piece
                and board[row + 1][col] == opponent_piece
                and board[row + 2][col] == opponent_piece
                and board[row + 3][col] == " "
            ):
                print(f"Blocking vertical move at column {col}")
                return col

    # Diagonal (from top left to bottom right)
    for row in range(3):
        for col in range(4):
            if (
                board[row][col] == opponent_piece
                and board[row + 1][col + 1] == opponent_piece
                and board[row + 2][col + 2] == opponent_piece
                and board[row + 3][col + 3] == " "
            ):
                print(f"Blocking diagonal (left to right) move at column {col + 3}")
                return col + 3

    # Diagonal (from top right to bottom left)
    for row in range(3):
        for col in range(3, 7):
            if (
                board[row][col] == opponent_piece
                and board[row + 1][col - 1] == opponent_piece
                and board[row + 2][col - 2] == opponent_piece
                and board[row + 3][col - 3] == " "
            ):
                print(f"Blocking diagonal (right to left) move at column {col - 3}")
                return col - 3

    return None


# Computer move


def get_computer_move(board, player_piece):
    blocking_move = check_for_blocking_move(board, player_piece)
    if blocking_move is not None:
        return blocking_move

    valid_locations = [col for col in range(7) if is_valid_location(board, col)]
    return random.choice(valid_locations)


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
    clear_screen()
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
    """
    Show the game instructions
    """
    clear_screen()
    result = pyfiglet.figlet_format("Game Instructions", font="bulbhead")
    print(Fore.YELLOW + result)
    print(Style.RESET_ALL)
    print("-" * 60)
    print("\nConnect Four is a two-player connection game where players")
    print("take turns dropping discs from the top into a seven-column, ")
    print("six-row vertically suspended grid.\n")
    print("In the two-player mode, one player is represented by the")
    print(
        ("symbol ")
        + Fore.GREEN
        + "P"
        + Style.RESET_ALL
        + (" and the other player by the symbol ")
        + Fore.YELLOW
        + "O"
        + Style.RESET_ALL
        + ".\n"
    )
    print(
        ("In the single-player mode, player is displayed as ")
        + Fore.GREEN
        + "P"
        + Style.RESET_ALL
        + " on the"
    )
    print("game board when they place a piece and the computer is")
    print(("represented by a ") + Fore.RED + "C" + Style.RESET_ALL + ".\n")
    print("Each player alternates turns, dropping one of their discs")
    print("into the grid each turn.\n")
    print("The goal of the game is to connect four discs vertically,")
    print("horizontally, or diagonally before your opponent.\n")
    print("-" * 60)
    print()
    input(Fore.BLUE + "Press Enter to return to Main Menu!\n")
    print(Style.RESET_ALL)


# Hall of Fame


def show_hall_of_fame():
    """
    Show the hall of fame
    """
    clear_screen()
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


# Main function


def main_menu():
    global is_running
    while is_running:
        """
        Show welcome message and menu
        """
        clear_screen()
        result = pyfiglet.figlet_format("Welcome to Connect Four", font="bulbhead")
        print(Fore.YELLOW + result)
        print(Style.RESET_ALL)

        print("1. Start Game against Computer")
        print("2. Start Game against another Player")
        print("3. Game Instructions")
        print("4. Hall of Fame")
        print("5. Quit\n")

        choice = input("Please choose an option (1/2/3/4/5):\n")
        print()

        if choice == "1":
            player_name = get_valid_player_name()
            start_game(player_name, vs_computer=True)
        elif choice == "2":
            player1_name = get_valid_player_name("Player 1")
            player2_name = get_valid_player_name("Player 2")
            start_game(player1_name, vs_computer=False, player2_name=player2_name)
        elif choice == "3":
            show_game_instructions()
        elif choice == "4":
            show_hall_of_fame()
        elif choice == "5":
            print(Fore.YELLOW + "ByeBye, thank you for playing!" + Style.RESET_ALL)
            is_running = False
            return


# Start game


def start_game(player_name, vs_computer=True, player2_name=""):
    """
    Start Game
    """
    prepare_game(player_name, vs_computer, player2_name)
    existing_player, player1_index = find_player(player_name)
    player2_index = None
    if not vs_computer:
        _, player2_index = find_player(player2_name)

    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    while not game_over:
        if turn == 0:
            col = get_player_move(player_name)
            if col is None:
                return
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                place_piece(board, row, col, Fore.GREEN + "P" + Style.RESET_ALL)
                print_board(board)
                if check_win(board, Fore.GREEN + "P" + Style.RESET_ALL):
                    print(f"Congratulations, {player_name}! You won!\n")
                    game_over = True
                else:
                    turn = 1

        else:
            if vs_computer:
                col = get_computer_move(board, Fore.RED + "C" + Style.RESET_ALL)
            else:
                col = get_player_move(player2_name)
                if col is None:
                    return
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                piece = (
                    Fore.RED + "C" + Style.RESET_ALL
                    if vs_computer
                    else Fore.YELLOW + "O" + Style.RESET_ALL
                )
                place_piece(board, row, col, piece)
                print_board(board)
                if check_win(board, piece):
                    winner = (
                        player_name
                        if turn == 0
                        else (player2_name if not vs_computer else "Computer")
                    )
                    print(f"Congratulations, {winner}! You won!\n")
                    game_over = True
                else:
                    turn = 0

        if all(row.count("P") + row.count("O") == 7 for row in board):
            print(Fore.YELLOW + "It's a tie!")
            print(Style.RESET_ALL)
            game_over = True

        if game_over:
            if player1_index is not None:
                update_player_record(player1_index, True if turn == 0 else False)
            if (
                player2_index is not None
                and not vs_computer
                and player2_index != player1_index
            ):
                update_player_record(player2_index, True if turn == 1 else False)

            while True:
                play_again = input("Do you want to play again? (y/n):\n").lower()
                if play_again == "y":
                    prepare_game(player_name, vs_computer, player2_name)
                    board = create_board()
                    print_board(board)
                    game_over = False
                    turn = 0
                    break
                elif play_again == "n":
                    break
                else:
                    print(
                        Fore.RED
                        + "Invalid input. Please enter 'y' or 'n'.\n"
                        + Style.RESET_ALL
                    )


# Run game


def run_game():
    while is_running:
        main_menu()


if __name__ == "__main__":
    run_game()


# Main menu

main_menu()
