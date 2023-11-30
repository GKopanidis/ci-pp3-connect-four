def create_board():
    """
    Create a board with 6 rows and 7 columns
    """
    return [[' ' for _ in range(7)] for _ in range(6)]

board = create_board()
print("Board after init:")
for row in board:
    print(row)