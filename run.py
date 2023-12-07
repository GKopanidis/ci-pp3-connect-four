# Library imports

import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import SpreadsheetNotFound, APIError, WorksheetNotFound
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
    Clears the console screen.

    This function detects the operating system and executes the appropriate command to clear the console screen.
    It uses 'cls' for Windows and 'clear' for Unix-based systems (Mac and Linux).

    Note:
        This function relies on the 'os' module for determining the operating system and executing system commands.
    """
    # For Windows
    if os.name == "nt":
        os.system("cls")
    # For Mac and Linux
    else:
        os.system("clear")


# Class board


class Board:
    """
    Represents the game board for Connect Four.

    Attributes:
        rows (int): Number of rows in the game board.
        cols (int): Number of columns in the game board.
        grid (list of lists): A 2D list representing the game board, where each cell can be empty or contain a player's piece.
    """

    def __init__(self, rows=6, cols=7):
        """
        Initializes a new game board with the specified number of rows and columns.

        Args:
            rows (int): Number of rows in the game board, defaults to 6.
            cols (int): Number of columns in the game board, defaults to 7.
        """
        self.rows = rows
        self.cols = cols
        self.grid = [[" " for _ in range(cols)] for _ in range(rows)]

    def add_piece(self, row, col, piece):
        """
        Adds a piece to the specified location on the board.

        Args:
            row (int): The row index to place the piece.
            col (int): The column index to place the piece.
            piece (str): The symbol representing the player's piece.
        """
        self.grid[row][col] = piece

    def is_valid_location(self, col):
        """
        Checks if a column can accept a new piece.

        Args:
            col (int): The column index to check.

        Returns:
            bool: True if the top cell of the column is empty, False otherwise.
        """
        return self.grid[0][col] == " "

    def get_next_open_row(self, col):
        """
        Finds the next open row in the given column.

        Args:
            col (int): The column index to check.

        Returns:
            int: The row index of the next open cell in the specified column, or None if the column is full.
        """
        for r in range(self.rows - 1, -1, -1):
            if self.grid[r][col] == " ":
                return r
        return None

    def print_board(self):
        """
        Displays the game board in a readable format.

        Returns:
            None
        """
        clear_screen()
        print(" 1 2 3 4 5 6 7")
        print("---------------")
        for row in self.grid:
            print("|" + "|".join(row) + "|")
        print("---------------\n")
        pass

    def check_win(self, piece):
        """
        Checks if the current board has a winning condition for the specified piece.

        Args:
            piece (str): The symbol representing the player's piece to check for a win.

        Returns:
            bool: True if there is a sequence of four same pieces in a row, column, or diagonal; False otherwise.
        """
        for row in range(6):
            for col in range(4):
                if (
                    self.grid[row][col] == piece
                    and self.grid[row][col + 1] == piece
                    and self.grid[row][col + 2] == piece
                    and self.grid[row][col + 3] == piece
                ):
                    return True

        for row in range(3):
            for col in range(7):
                if (
                    self.grid[row][col] == piece
                    and self.grid[row + 1][col] == piece
                    and self.grid[row + 2][col] == piece
                    and self.grid[row + 3][col] == piece
                ):
                    return True

        for row in range(3):
            for col in range(4):
                if (
                    self.grid[row][col] == piece
                    and self.grid[row + 1][col + 1] == piece
                    and self.grid[row + 2][col + 2] == piece
                    and self.grid[row + 3][col + 3] == piece
                ):
                    return True

        for row in range(3):
            for col in range(3, 7):
                if (
                    self.grid[row][col] == piece
                    and self.grid[row + 1][col - 1] == piece
                    and self.grid[row + 2][col - 2] == piece
                    and self.grid[row + 3][col - 3] == piece
                ):
                    return True

        return False
        pass


# Class Player


class Player:
    """
    Represents a player in the Connect Four game.

    Attributes:
        name (str): The name of the player.
        games_won (int): The number of games won by the player.
        games_lost (int): The number of games lost by the player.
    """

    def __init__(self, name):
        """
        Initializes a new Player instance.

        Args:
            name (str): The name of the player.
        """
        self.name = name
        self.games_won = 0
        self.games_lost = 0

    def record_win(self):
        """
        Records a win for the player by incrementing their win count.
        """
        self.games_won += 1

    def record_loss(self):
        """
        Records a loss for the player by incrementing their loss count.
        """
        self.games_lost += 1

    def greet(self):
        """
        Greets the player with a welcome message including their current game statistics.

        Displays a customized greeting based on the player's game history, showing the number of games won and lost.
        """
        if self.games_won > 0 or self.games_lost > 0:
            print(Fore.CYAN + f"Welcome back, {self.name}!")
            print(Fore.GREEN + f"Won Games: {self.games_won}")
            print(Fore.RED + f"Lost Games: {self.games_lost}\n")
        else:
            print(Fore.CYAN + f"Welcome, {self.name}! Good luck on your first game!\n")
        print(Style.RESET_ALL)


# Find player in HOF sheet


def find_player(player_name: str):
    """
    Searches for a player in the Hall of Fame spreadsheet.

    Args:
        player_name (str): The name of the player to search for.
    """
    try:
        cell = HOF_SHEET.find(player_name)
        if cell:
            player_data = HOF_SHEET.row_values(cell.row)
            player = Player(player_name)
            player.games_won = int(player_data[1])
            player.games_lost = int(player_data[2])
            player.index = cell.row
            return player

        else:
            if any(char.isalpha() for char in player_name) and len(player_name) > 2:
                new_index = add_new_player(player_name)
                return None, new_index
            else:
                print(Fore.RED + "Invalid player name." + Style.RESET_ALL)
                return None, -1

    except WorksheetNotFound:
        # Specific handling for when a worksheet is not found
        print(
            Fore.RED
            + "Error: The specified worksheet was not found in the spreadsheet."
            + Style.RESET_ALL
        )
        # Log the error and/or take other appropriate actions
        return None, -1

    except SpreadsheetNotFound:
        # Specific handling for when the spreadsheet is not found
        print(
            Fore.RED
            + "Error: The specified spreadsheet was not found."
            + Style.RESET_ALL
        )
        # Log the error and/or take other appropriate actions
        return None, -1

    except APIError as e:
        # Handling other API errors
        print(Fore.RED + f"An API error occurred: {e.message}" + Style.RESET_ALL)
        # Log the error and/or take other appropriate actions
        return None, -1

    except Exception as e:
        # Generic exception handler for any other unforeseen exceptions
        print(Fore.RED + f"An unexpected error occurred: {e}" + Style.RESET_ALL)
        # Log the error and/or take other appropriate actions
        return None, -1


# Update player record in HOF sheet


def update_player_record(player, won):
    """
    Updates the player's win-loss record in the Hall of Fame spreadsheet.

    Increments the win count if the player won, or the loss count if they lost.

    Args:
        player (Player): The player object whose record needs updating.
        won (bool): True if the player won the game, False otherwise.
    """
    if won:
        player.record_win()
    else:
        player.record_loss()

    # Aktualisieren Sie die Daten in der Tabelle unter Verwendung des Spielersindex
    HOF_SHEET.update_cell(player.index, 2, player.games_won)
    HOF_SHEET.update_cell(player.index, 3, player.games_lost)

    return f"Updated record for {player.name}: Wins - {player.games_won}, Losses - {player.games_lost}"


# Prepare game


def prepare_game(player_name, vs_computer, player2_name=""):
    """
    Prepares the game environment by setting up players.

    Finds or adds the first player and optionally a second player if not playing against the computer.
    Clears the screen and prompts the user to start the game.

    Args:
        player_name (str): Name of the first player.
        vs_computer (bool): True if playing against the computer, False otherwise.
        player2_name (str): Name of the second player (if applicable).

    Returns:
        tuple: A tuple containing Player objects for the first and second player.
    """
    clear_screen()
    player1 = find_player(player_name)
    if player1:
        player1.greet()

    player2 = None
    if not vs_computer:
        player2 = find_player(player2_name)
        if player2:
            player2.greet()

    input("Press any key to start the game...")
    clear_screen()

    return player1, player2


# Get valid player


def get_valid_player_name(prompt="Enter your name"):
    """
    Prompts the user for a valid player name and validates it.

    A valid name must be at least three characters long, contain at least one alphabetic character,
    and only consist of letters, numbers, and spaces.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        str: A validated player name.
    """
    while True:
        player_name = input(
            f"{prompt} (3-20 characters, letters, numbers, "
            "and spaces only; at least one letter required): \n"
        ).strip()

        is_length_valid = 3 <= len(player_name) <= 20
        has_at_least_one_letter = any(char.isalpha() for char in player_name)
        has_valid_characters = all(
            char.isalpha() or char.isdigit() or char.isspace() for char in player_name
        )

        if is_length_valid and has_at_least_one_letter and has_valid_characters:
            return player_name
        else:
            print(
                Fore.RED + "Invalid name. Please enter 3-20 characters "
                "(letters, numbers, and spaces only; at least one letter required).\n"
                + Style.RESET_ALL
            )


# Find player


def find_player(player_name):
    """
    Searches for a player by name in the Hall of Fame (HOF) sheet and returns their data.

    If the player is found, their data and row index in the HOF sheet are returned. If not found,
    the function attempts to add them as a new player, given the name is valid (contains alphabetic
    characters and is longer than 2 characters). In case of invalid name or other errors,
    appropriate messages are displayed.

    Args:
        player_name (str): The name of the player to search for.

    Returns:
        tuple: A tuple containing the player's data as a dictionary and their row index in the HOF sheet,
               or None and the new player's index if a new player is added.

    Raises:
        ValueError: If the player is not found in the HOF sheet.
        gspread.exceptions.GSpreadException: For issues related to accessing the HOF sheet.
    """
    try:
        cell = HOF_SHEET.find(player_name)
        if cell:
            player_data = HOF_SHEET.row_values(cell.row)
            player = Player(player_name)
            player.games_won = int(player_data[1])
            player.games_lost = int(player_data[2])
            player.index = cell.row
            return player

        else:
            if any(char.isalpha() for char in player_name) and len(player_name) > 2:
                new_index = add_new_player(player_name)
                player = Player(player_name)
                player.index = new_index
                return player

    except (WorksheetNotFound, SpreadsheetNotFound, APIError, Exception) as e:
        print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)
        return None


# Add player if not found in sheet


def add_new_player(player_name):
    """
    Adds a new player to the Hall of Fame spreadsheet.

    Args:
        player_name (str): The name of the new player to add.

    Returns:
        int: The row index of the newly added player in the HOF sheet.
    """
    new_player_data = [player_name, 0, 0]
    HOF_SHEET.append_row(new_player_data)
    print(Fore.GREEN + f"New Player {player_name} added...\n")
    print(Style.RESET_ALL)

    player_data = HOF_SHEET.get_all_records()
    new_index = len(player_data) + 1
    return new_index


# Player move


def get_player_move(player_name, board):
    """
    Prompts the player to choose a column for their move or to quit the game.

    Args:
        player_name (str): The name of the player making the move.
        board (Board): The current game board.

    Returns:
        int or None: The chosen column number, or None if the player chooses to quit.
    """
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
                print(
                    Fore.RED
                    + "Invalid input. Please enter 'y' or 'n'.\n"
                    + Style.RESET_ALL
                )
        elif col_input.isdigit():
            col = int(col_input) - 1
            if 0 <= col < 7:
                if board.is_valid_location(col):
                    return col
                else:
                    print(
                        Fore.RED
                        + "Column is full. Please choose a different column.\n"
                        + Style.RESET_ALL
                    )
            else:
                print(
                    Fore.RED
                    + "Column number out of range. Please choose a number between 1 and 7.\n"
                    + Style.RESET_ALL
                )
        else:
            print(
                Fore.RED
                + "Invalid input. Please enter a valid number between 1 and 7 or 'Q' to quit.\n"
                + Style.RESET_ALL
            )


# Check blocking move


def check_for_blocking_move(board, player_piece):
    """
    Identifies a column where a blocking move can be made against the opponent.

    Args:
        board (Board): The current game board.
        player_piece (str): The piece representation of the current player.

    Returns:
        int or None: The column index for a blocking move, or None if no such move is found.
    """
    opponent_piece = (
        Fore.GREEN + "P" + Style.RESET_ALL
        if player_piece == Fore.RED + "C" + Style.RESET_ALL
        else Fore.RED + "C" + Style.RESET_ALL
    )

    for c in range(7):
        for r in range(6):
            if board.grid[r][c] == " " and board.is_valid_location(c):
                # Temporarily simulate an opponent's move
                board.grid[r][c] = opponent_piece
                if board.check_win(opponent_piece):
                    board.grid[r][c] = " "  # Undo the move
                    return c  # Return the blocking column
                board.grid[r][c] = " "  # Undo the move if it does not result in a win

    return None


# Computer move


def get_computer_move(board, player_piece):
    """
    Determines the computer's move based on the current state of the board.

    Args:
        board (Board): The current game board.
        player_piece (str): The piece representation of the player.

    Returns:
        int: The chosen column index for the computer's move.
    """
    blocking_move = check_for_blocking_move(board, player_piece)
    if blocking_move is not None:
        return blocking_move

    valid_locations = [col for col in range(7) if is_valid_location(board, col)]
    return random.choice(valid_locations)


# Create board


def create_board():
    """
    Creates a new game board for Connect Four.

    Initializes a 6x7 grid with each cell set to empty space.

    Returns:
        list: A 2D list representing the game board.
    """
    return [[" " for _ in range(7)] for _ in range(6)]


# Validation check


def is_valid_location(board, col):
    """
    Checks if a move can be made in the specified column.

    Args:
        board (Board): The current game board.
        col (int): The column index to check.

    Returns:
        bool: True if the top cell of the column is empty, False otherwise.
    """
    if 0 <= col < 7:
        return board.grid[0][col] == " "
    else:
        return False


# Find next open row


def get_next_open_row(board, col):
    """
    Finds the next open row in a specified column on the board.

    Args:
        board (Board): The current game board.
        col (int): The column index to check.

    Returns:
        int: The row index of the next open cell, or -1 if the column is full.
    """
    for row in range(5, -1, -1):
        if board.grid[row][col] == " ":
            return row
    return -1


# Place piece


def place_piece(board, row, col, piece):
    """
    Places a piece on the board at the specified row and column.

    Args:
        board (Board): The game board.
        row (int): The row index to place the piece.
        col (int): The column index to place the piece.
        piece (str): The piece to place on the board.
    """
    board.grid[row][col] = piece


# Game instructions


def show_game_instructions():
    """
    Displays the instructions for playing Connect Four.

    Clears the screen and shows a detailed explanation of the game rules.
    """
    clear_screen()
    print(
        Fore.YELLOW
        + pyfiglet.figlet_format("Game Instructions", font="bulbhead")
        + Style.RESET_ALL
    )
    print("-" * 67)
    game_description = f"""
    Connect Four is a two-player connection game where players
    take turns dropping discs from the top into a seven-column, 
    six-row vertically suspended grid.

    In the two-player mode, one player is represented by the
    symbol {Fore.GREEN}P{Style.RESET_ALL} and the other player by the symbol {Fore.YELLOW}O{Style.RESET_ALL}.

    In the single-player mode, player is displayed as {Fore.GREEN}P{Style.RESET_ALL} on the
    game board when they place a piece and the computer is
    represented by a {Fore.RED}C{Style.RESET_ALL}.

    Each player alternates turns, dropping one of their discs
    into the grid each turn.

    The goal of the game is to connect four discs vertically,
    horizontally, or diagonally before your opponent.
    """
    print(game_description)
    print("-" * 67)
    print()
    input(Fore.BLUE + "Press Enter to return to Main Menu!\n" + Style.RESET_ALL)


# Hall of Fame


def show_hall_of_fame():
    """
    Displays the Hall of Fame, listing players and their win-loss records.

    Clears the screen and presents player statistics in a tabular format.
    """
    clear_screen()
    print(
        Fore.YELLOW
        + pyfiglet.figlet_format("Game Instructions", font="bulbhead")
        + Style.RESET_ALL
    )
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
    """
    Displays the main menu and handles user interaction for game navigation.

    This function shows a welcome message and a list of options, including starting a game against the computer,
    starting a game against another player, viewing game instructions, viewing the Hall of Fame, and quitting the game.
    It prompts the user to select an option and performs the corresponding action. The menu remains active and
    continues to display after each action until the user chooses to quit.

    Note:
        This function uses global variable 'is_running' to control the game loop. It employs 'pyfiglet' for stylized
        text output and 'colorama' for text coloring. The function 'clear_screen' is used to clear the console
        before displaying the menu.
    """
    global is_running
    while is_running:
        """
        Show welcome message and menu
        """
        clear_screen()
        print(
            Fore.YELLOW
            + pyfiglet.figlet_format("Welcome to Connect Four", font="bulbhead")
            + Style.RESET_ALL
        )

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
            clear_screen()
            print(
                Fore.YELLOW
                + pyfiglet.figlet_format(
                    "ByeBye, thank you for playing!", font="bulbhead"
                )
                + Style.RESET_ALL
            )
            is_running = False
            return


# Start game


def start_game(player_name, vs_computer=True, player2_name=""):
    """
    Initiates and manages a game of Connect Four.

    Sets up players and the game board, alternates turns, and checks for game end conditions.
    Offers the option to play again and updates player records after each game.

    Args:
        player_name (str): Name of the first player.
        vs_computer (bool): True to play against the computer, False for a two-player game.
        player2_name (str): Name of the second player, if applicable.
    """
    player1, player2 = prepare_game(player_name, vs_computer, player2_name)

    board = Board()
    board.print_board()
    game_over = False
    turn = 0

    while not game_over:
        if turn == 0:
            col = get_player_move(player_name, board)
            if col is None:
                return
            if board.is_valid_location(col):
                row = board.get_next_open_row(col)
                board.add_piece(row, col, Fore.GREEN + "P" + Style.RESET_ALL)
                board.print_board()
                if board.check_win(Fore.GREEN + "P" + Style.RESET_ALL):
                    print(f"Congratulations, {player_name}! You won!\n")
                    game_over = True
                else:
                    turn = 1

        else:
            if vs_computer:
                col = get_computer_move(board, Fore.RED + "C" + Style.RESET_ALL)
            else:
                col = get_player_move(player2_name, board)
                if col is None:
                    return
            if board.is_valid_location(col):
                row = board.get_next_open_row(col)
                piece = (
                    Fore.RED + "C" + Style.RESET_ALL
                    if vs_computer
                    else Fore.YELLOW + "O" + Style.RESET_ALL
                )
                board.add_piece(row, col, piece)
                board.print_board()
                if board.check_win(piece):
                    winner = (
                        player_name
                        if turn == 0
                        else (player2_name if not vs_computer else "Computer")
                    )
                    print(f"Congratulations, {winner}! You won!\n")
                    game_over = True
                else:
                    turn = 0

        if all(row.count("P") + row.count("O") == 7 for row in board.grid):
            print(Fore.YELLOW + "It's a tie!")
            print(Style.RESET_ALL)
            game_over = True

        if game_over:
            if player1 is not None:
                update_player_record(player1, True if turn == 0 else False)
            if player2 is not None and not vs_computer:
                update_player_record(player2, True if turn == 1 else False)

            play_again_valid = False
            while not play_again_valid:
                play_again = input("Do you want to play again? (y/n):\n").lower()
                if play_again == "y":
                    player1, player2 = prepare_game(player_name, vs_computer, player2_name)
                    board = Board()
                    board.print_board()
                    game_over = False
                    turn = 0
                    play_again_valid = True
                elif play_again == "n":
                    play_again_valid = True
                    break
                else:
                    print(Fore.RED + "Invalid input. Please enter 'y' or 'n'.\n" + Style.RESET_ALL)


# Run game


def run_game():
    """
    Executes the main loop of the game.

    Continuously displays the main menu and allows user interaction until the game is exited.
    """
    while is_running:
        main_menu()


if __name__ == "__main__":
    run_game()


# Main menu

main_menu()
"""
Displays the main menu of the Connect Four game and handles user input for game options.
"""
