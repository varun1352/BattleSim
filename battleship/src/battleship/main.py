#!/usr/bin/env python
from battleship.crew import BattleshipCrew

from battleship.tools.custom_tool import initialize_game, update_boards, check_win

def run():
    # Initialize game state
    game_state = initialize_game()
    print("Game Initialized.")
    print("Player One Real Board:", game_state["player_one"]["real_board"])
    print("Player Two Real Board:", game_state["player_two"]["real_board"])
    
    current_player = "player_one"
    move_count = 0

    # Main game loop: run until one player's ships are all sunk.
    while True:
        if current_player == "player_one":
            personal_board = game_state["player_one"]["personal_board"]
            # Use the agent's tool to decide a move based on current personal board state.
            move = BattleshipCrew().player_one().tools[0]["function"](personal_board)
            print(f"Player One chooses move: {move}")
            result, sunk_info = update_boards(game_state, "player_one", move)
            print(f"Result: {result}")
            if sunk_info:
                print(sunk_info)
            if check_win(game_state["player_two"]["real_board"]):
                print("Player One wins!")
                break
            current_player = "player_two"
        else:
            personal_board = game_state["player_two"]["personal_board"]
            move = BattleshipCrew().player_two().tools[0]["function"](personal_board)
            print(f"Player Two chooses move: {move}")
            result, sunk_info = update_boards(game_state, "player_two", move)
            print(f"Result: {result}")
            if sunk_info:
                print(sunk_info)
            if check_win(game_state["player_one"]["real_board"]):
                print("Player Two wins!")
                break
            current_player = "player_one"
        move_count += 1
        if move_count > 100:  # Prevent infinite loop during testing.
            print("Game simulation stopped after 100 moves.")
            break

if __name__ == "__main__":
    run()