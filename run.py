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


# Prepare game


def prepare_game(player_name, vs_computer, player2_name=""):
    """
    Prepares the game environment by setting up players and clearing the screen.

    This function first clears the screen and then finds or adds the first player using their name.
    It greets the first player accordingly. If the game is not against the computer, it repeats the
    process for the second player using 'player2_name'. Finally, it prompts the user to press any key
    to start the game and clears the screen again.

    Args:
        player_name (str): The name of the first player.
        vs_computer (bool): True if the game is against the computer, False otherwise.
        player2_name (str, optional): The name of the second player if playing against another player.
                                      Defaults to an empty string.

    Note:
        This function relies on 'find_player' to locate or add player information and 'greet_player'
        to greet the players. It also uses a 'clear_screen' method to clear the console screen.
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
    """
    Prompts the user to input a player name and validates it.

    The function repeatedly prompts the user until a valid name is entered. A valid name must be at least
    three characters long and contain at least one alphabetic character. If the input is invalid,
    an error message is displayed and the user is prompted again.

    Args:
        prompt (str, optional): The prompt message to display. Defaults to "Enter your name".

    Returns:
        str: A validated player name that meets the criteria.
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
            player = {
                "player_name": player_data[0],
                "games_won": int(player_data[1]),
                "games_lost": int(player_data[2]),
            }
            return player, cell.row

        # Handling when the player is not found
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


# Add player if not found in sheet


def add_new_player(player_name):
    """
     Adds a new player to the Hall of Fame (HOF) sheet.

    Args:
        player_name (str): The name of the player to be added.

    Returns:
        int: The index of the newly added player in the HOF sheet.

    Note:
        This function depends on the 'HOF_SHEET' global variable, which should support
        'append_row' and 'get_all_records' methods.
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
    """
    Greets the player by displaying a welcome message and their game statistics.

    If the player exists (i.e., 'existing_player' is not None), the function displays a welcome back message
    along with the player's game statistics (games won and lost). If the player is new (i.e., 'existing_player'
    is None), a welcome message for a new player is displayed. All messages are color-coded for visual distinction.

    Args:
        existing_player (dict or None): A dictionary containing the player's data (name, games won, games lost)
                                        if they exist, otherwise None.
        player_name (str): The name of the player.

    Note:
        This function uses the 'Fore' class from the 'colorama' module to color the text displayed in the console.
    """
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
    Updates the win-loss record of a player in the Hall of Fame (HOF) sheet.

    Retrieves the current record of a player from the HOF sheet using their index,
    then updates the record based on the game outcome. If the player won, their wins count is incremented;
    if they lost, their losses count is incremented. The updated record is then saved back to the HOF sheet.

    Args:
        player_index (int): The index of the player in the HOF sheet.
        won (bool): True if the player won the game, False otherwise.

    Returns:
        str: A message indicating the player's updated record.

    Note:
        This function relies on the 'HOF_SHEET' global variable and assumes that
        the win and loss counts are in the second and third columns, respectively.
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
    """
    Prompts the player to choose a column for their move or to quit the game.

    The function repeatedly prompts the player to select a column by entering a number from 1 to 7,
    or to press 'Q' to quit. If the input is 'Q', the player is asked to confirm their decision to quit.
    If the input is a valid column number, it is returned as an integer. Invalid inputs result in
    an error message and the prompt is repeated.

    Args:
        player_name (str): The name of the player making the move.

    Returns:
        int or None: The chosen column as an integer (0-6), or None if the player chooses to quit.

    Note:
        This function handles input validation and displays messages using the 'Fore' class from the
        'colorama' module for text coloring. The returned column number is zero-indexed.
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
                return col
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
    Identifies a potential blocking move against the opponent.

    This function scans the game board to find a move that would block the opponent from winning.
    It temporarily simulates the opponent's moves on the board. If a simulated move results in a win for the opponent,
    that column is identified as a potential blocking move and its index is returned.

    Args:
        board (list of lists): The current state of the game board, represented as a 2D list.
        player_piece (str): The piece representation of the current player.

    Returns:
        int or None: The index of the column where a blocking move can be made, or None if no blocking move is found.

    Note:
        This function assumes the board is a 6x7 grid and relies on 'is_valid_location' to check if a column can be played,
        and 'check_win' to determine if a move results in a win. The piece representations for players are formatted using
        the 'colorama' module.
    """
    opponent_piece = (
        Fore.GREEN + "P" + Style.RESET_ALL
        if player_piece == Fore.RED + "C" + Style.RESET_ALL
        else Fore.RED + "C" + Style.RESET_ALL
    )

    for c in range(7):
        for r in range(6):
            if board[r][c] == " " and is_valid_location(board, c):
                # Temporarily simulate an opponent's move
                board[r][c] = opponent_piece
                if check_win(board, opponent_piece):
                    board[r][c] = " "  # Undo the move
                    return c  # Return the blocking column
                board[r][c] = " "  # Undo the move if it does not result in a win

    return None


# Computer move


def get_computer_move(board, player_piece):
    """
    Determines the computer's move in the game.

    The function first checks for any potential blocking moves to prevent the player from winning on their next turn.
    If a blocking move is found, it is returned as the computer's move. If no blocking move is necessary,
    the function selects a random valid column from the available locations on the board.

    Args:
        board (list of lists): The current state of the game board, represented as a 2D list.
        player_piece (str): The piece representation of the current player.

    Returns:
        int: The index of the column chosen for the computer's move.

    Note:
        This function relies on 'check_for_blocking_move' to identify possible blocking moves and
        'is_valid_location' to determine valid columns for placing a piece. It uses the 'random'
        module to select a random column from valid locations.
    """
    blocking_move = check_for_blocking_move(board, player_piece)
    if blocking_move is not None:
        return blocking_move

    valid_locations = [col for col in range(7) if is_valid_location(board, col)]
    return random.choice(valid_locations)


# Create board


def create_board():
    """
    Creates a new game board for playing.

    Initializes a 6x7 grid to represent the game board, with each cell initially set to an empty space.
    This grid represents the standard layout for the game with 6 rows and 7 columns.

    Returns:
        list of lists: A 2D list representing the game board, with each element initialized to " ".
    """
    return [[" " for _ in range(7)] for _ in range(6)]


# Print board


def print_board(board):
    """
    Displays the game board in a readable format.

    Clears the console screen and then prints the current state of the game board. Each cell of the board
    is displayed, along with column numbers at the top for reference. The board is represented in a grid format
    with each cell separated by vertical bars.

    Args:
        board (list of lists): The current state of the game board, represented as a 2D list.

    Note:
        This function uses 'clear_screen' to clear the console before displaying the board. The board layout
        includes headers for columns and separators for rows.
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
    Determines if a move can be made in a specified column.

    Checks if the top cell of the given column is empty, indicating that a piece can be dropped in this column.
    Also ensures that the column index is within the valid range of the board (0 to 6).

    Args:
        board (list of lists): The current state of the game board, represented as a 2D list.
        col (int): The index of the column to check for a valid move.

    Returns:
        bool: True if the move is valid (the column is within range and not full), False otherwise.
    """
    if 0 <= col < 7:
        return board[0][col] == " "
    else:
        return False


# Find next open row


def get_next_open_row(board, col):
    """
    Finds the next open row in a specified column.

    Iterates through the rows of the given column, starting from the bottom, to find the first available
    (empty) row. This is where a new piece can be placed. If the column is full, no open row is available.

    Args:
        board (list of lists): The current state of the game board, represented as a 2D list.
        col (int): The index of the column to check for an open row.

    Returns:
        int: The index of the next open row in the specified column, or -1 if the column is full.
    """
    for row in range(5, -1, -1):
        if board[row][col] == " ":
            return row
    return -1


# Place piece


def place_piece(board, row, col, piece):
    """
    Places a piece on the game board at the specified location.

    Updates the board by placing the given piece in the specified row and column. This function is typically
    called after confirming that the location is valid and available for a new piece.

    Args:
        board (list of lists): The current state of the game board, represented as a 2D list.
        row (int): The row index where the piece is to be placed.
        col (int): The column index where the piece is to be placed.
        piece (str): The representation of the piece to place on the board.

    Note:
        This function modifies the board in-place and does not return any value.
    """
    board[row][col] = piece


# Check win conditions


def check_win(board, piece):
    """
    Checks if the current piece placement results in a win.

    The function examines the board to see if there are four consecutive pieces of the same type
    in a row, column, or diagonally. This check is performed across the entire board. A win occurs
    if any such sequence of four is found.

    Args:
        board (list of lists): The current state of the game board, represented as a 2D list.
        piece (str): The piece to check for a winning sequence.

    Returns:
        bool: True if a winning sequence is found, False otherwise.

    Note:
        The function checks all possible winning combinations - horizontal, vertical, and both
        diagonal directions. It is designed to work with a 6x7 board.
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
    Displays the instructions for playing Connect Four.

    Clears the screen and shows a stylized title 'Game Instructions'. The instructions cover the
    basics of how to play Connect Four, including the layout of the game board, the symbols used
    to represent the players and the computer in single-player and two-player modes, and the
    objective of the game. The instructions also explain the turn-taking process and the goal to
    connect four discs in a row. The function prompts the user to press Enter to return to the
    main menu after reading the instructions.

    Note:
        This function uses 'pyfiglet' for stylized text formatting, 'colorama' for text coloring,
        and 'clear_screen' to clear the console before displaying the instructions.
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
    Displays the Hall of Fame, listing players and their win-loss records.

    The function clears the screen and presents a stylized title 'Hall of Fame'. It then retrieves
    and displays the player data from the Hall of Fame sheet, including player names, number of games
    won, and number of games lost. The data is formatted in a tabular form for readability. After displaying
    the list, the function prompts the user to press Enter to return to the main menu.

    Note:
        This function uses 'pyfiglet' for the title formatting, 'colorama' for text coloring, and
        'clear_screen' to clear the console. It relies on the global variable 'HOF_SHEET' to retrieve
        player data.
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
            clear_screen()
            result = pyfiglet.figlet_format(
                "ByeBye, thank you for playing!", font="bulbhead"
            )
            print(Fore.YELLOW + result)
            print(Style.RESET_ALL)
            is_running = False
            return


# Start game


def start_game(player_name, vs_computer=True, player2_name=""):
    """
    Initiates and manages a game of Connect Four.

    The function prepares the game by setting up players and the game board. It alternates turns between
    the player and the opponent (either another player or the computer). On each turn, it prompts for a move,
    validates it, updates the board, and checks for a win or a tie. If a player wins or the game ends in a tie,
    it offers the option to play again. Player win/loss records are updated after each game.

    Args:
        player_name (str): The name of the first player.
        vs_computer (bool, optional): True to play against the computer, False to play against another player.
                                      Defaults to True.
        player2_name (str, optional): The name of the second player, if playing against another player.
                                      Defaults to an empty string.

    Note:
        This function uses 'prepare_game' to set up the game, 'create_board' to create the game board,
        and 'print_board' to display the board. It relies on several other functions to handle game logic,
        including 'get_player_move', 'is_valid_location', 'get_next_open_row', 'place_piece', 'check_win',
        and 'update_player_record'. It also uses the 'colorama' module for text coloring.
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
    """
    Executes the main loop of the game.

    This function continuously displays the main menu and allows the user to navigate through different
    game options (such as starting a new game, viewing instructions, or checking the Hall of Fame) as long
    as the global variable 'is_running' is True. The loop breaks and the game ends when 'is_running' is set to False.

    Note:
        The function relies on the global variable 'is_running' to maintain the game loop and calls
        'main_menu' to display the menu and handle user interaction. Changes to 'is_running' are expected
        to be made within 'main_menu' or other functions called from it.
    """
    while is_running:
        main_menu()


if __name__ == "__main__":
    run_game()


# Main menu
"""
    Displays the main menu and handles user selections for different game options.

    This function presents the main menu of the game, providing options to start a new game against the 
    computer or another player, view game instructions, see the Hall of Fame, or quit the game. 
    It processes the user's choice and directs to the appropriate action or game mode. The menu remains 
    active until the user chooses to exit the game.

    Note:
        This function is part of the main game loop controlled by the global variable 'is_running'. It uses 
        'pyfiglet' for stylized text display and 'colorama' for text coloring. The menu options are handled 
        by calling respective functions such as 'start_game', 'show_game_instructions', and 'show_hall_of_fame'.
    """
main_menu()
