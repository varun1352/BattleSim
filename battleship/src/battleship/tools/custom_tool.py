import random
import string

# --- Board Initialization and Ship Placement ---

def create_empty_board():
    """Creates a 10x10 board represented as a dictionary of coordinates to statuses."""
    board = {}
    for letter in string.ascii_uppercase[:10]:
        for number in range(1, 11):
            board[f"{letter}{number}"] = "empty"
    return board

def place_ships(board, ship_lengths=[2, 3, 3, 4]):
    """
    Places ships on the board.
    Each ship is represented as a list of coordinates.
    Ships can be placed horizontally or vertically without overlapping.
    Returns:
        A list of ships.
    """
    ships = []
    for length in ship_lengths:
        placed = False
        while not placed:
            orientation = random.choice(["horizontal", "vertical"])
            if orientation == "horizontal":
                row = random.choice(string.ascii_uppercase[:10])
                start = random.randint(1, 11 - length)
                coords = [f"{row}{num}" for num in range(start, start + length)]
            else:
                col = random.randint(1, 10)
                start_row_index = random.randint(0, 10 - length)
                coords = [f"{string.ascii_uppercase[i]}{col}" for i in range(start_row_index, start_row_index + length)]
            
            # Check if any coordinate is already occupied
            if all(board.get(coord) == "empty" for coord in coords):
                for coord in coords:
                    board[coord] = "ship"  # mark as ship (for the real board)
                ships.append(coords)
                placed = True
    return ships

def initialize_game():
    """
    Initializes the game by creating real and personal boards for both players,
    placing ships on each player's real board.
    Returns:
        A dictionary with keys:
          'player_one': {'real_board', 'personal_board', 'ships'},
          'player_two': {'real_board', 'personal_board', 'ships'}.
    """
    # For each player, create two boards: the real board and the personal board.
    player_one_real = create_empty_board()
    player_one_personal = create_empty_board()
    player_two_real = create_empty_board()
    player_two_personal = create_empty_board()
    
    # Place ships on the real boards and store the ship coordinates.
    ships_player_one = place_ships(player_one_real.copy())  # copy to preserve original board state if needed
    ships_player_two = place_ships(player_two_real.copy())
    
    return {
        "player_one": {
            "real_board": player_one_real,
            "personal_board": player_one_personal,
            "ships": ships_player_one
        },
        "player_two": {
            "real_board": player_two_real,
            "personal_board": player_two_personal,
            "ships": ships_player_two
        }
    }

# --- Move Decision and Board Analysis ---

def get_available_moves(personal_board):
    """Returns a list of coordinates from the personal board that have not been targeted (i.e., still 'empty')."""
    return [coord for coord, status in personal_board.items() if status == "empty"]

def analyze_board_state(personal_board, strategy):
    """
    Analyzes the player's personal board (opponent view) to choose an optimal move.
    If a previous move was a hit, try probing adjacent cells; otherwise, choose randomly.
    Args:
        personal_board (dict): The player's view of the opponent's board.
        strategy (str): "aggressive" or "defensive" strategy.
    Returns:
        A coordinate string (e.g., "B5").
    """
    available = get_available_moves(personal_board)
    if not available:
        return None

    # Look for cells adjacent to a hit:
    hit_cells = [coord for coord, status in personal_board.items() if status == "hit"]
    adjacent_candidates = []
    for cell in hit_cells:
        row, col = cell[0], int(cell[1:])
        # Potential adjacent coordinates: up, down, left, right
        potential = [
            f"{chr(ord(row)-1)}{col}" if row > 'A' else None,
            f"{chr(ord(row)+1)}{col}" if row < 'J' else None,
            f"{row}{col-1}" if col > 1 else None,
            f"{row}{col+1}" if col < 10 else None
        ]
        for candidate in potential:
            if candidate and candidate in available:
                adjacent_candidates.append(candidate)
    if adjacent_candidates:
        # If there are candidates adjacent to hits, pick one (can add weighting later).
        return random.choice(adjacent_candidates)
    
    # Otherwise, choose a random available cell.
    return random.choice(available)

def decide_move(personal_board, strategy):
    """
    Determines the next move based on the player's personal board view.
    Args:
        personal_board (dict): The current view of the opponent's board.
        strategy (str): "aggressive" or "defensive" (can be used for future weighting).
    Returns:
        A coordinate string.
    """
    return analyze_board_state(personal_board, strategy)

# --- Updating Boards and Checking Game Status ---

def update_boards(game_state, player, move):
    """
    Updates both the opponent's real board and the player's personal board based on a move.
    Args:
        game_state (dict): The overall game state.
        player (str): "player_one" or "player_two" making the move.
        move (str): The targeted coordinate.
    Returns:
        A tuple (result, sunk_ship_info) where result is "hit" or "miss",
        and sunk_ship_info is a message if a ship is sunk, else None.
    """
    opponent = "player_two" if player == "player_one" else "player_one"
    opponent_board = game_state[opponent]["real_board"]
    personal_board = game_state[player]["personal_board"]
    
    if opponent_board.get(move) == "ship":
        result = "hit"
        opponent_board[move] = "hit"
        personal_board[move] = "hit"
        sunk_ship_info = check_ship_sunk(game_state[opponent]["ships"], opponent_board, move)
    else:
        result = "miss"
        opponent_board[move] = "miss"
        personal_board[move] = "miss"
        sunk_ship_info = None
    return result, sunk_ship_info

def check_ship_sunk(ships, real_board, move):
    """
    Checks if the move has resulted in a sunk ship.
    Args:
        ships (list): List of ships (each ship is a list of coordinates).
        real_board (dict): The opponent's real board.
        move (str): The move that resulted in a hit.
    Returns:
        A message string if a ship is sunk, else None.
    """
    for ship in ships:
        if move in ship:
            # If all coordinates of the ship are hit, then the ship is sunk.
            if all(real_board[coord] == "hit" for coord in ship):
                return f"Ship sunk! (Ship of length {len(ship)})"
    return None

def check_win(real_board):
    """Returns True if no ships remain on the board, else False."""
    for status in real_board.values():
        if status == "ship":
            return False
    return True
