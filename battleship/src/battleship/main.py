#!/usr/bin/env python
# src/battleship/main.py
import json
import sys
import random
import time
from battleship.board import Board
from battleship.crew import BattleshipCrew
from battleship.tools.custom_tool import board_to_str
from crewai import Crew, Process

SHIP_LENGTHS = [2, 3, 3, 4]

class Player:
    def __init__(self, name):
        self.name = name
        self.real_board = Board()
        self.personal_board = Board()  # Tracks guesses (hits/misses)
        self.place_ships()

    def place_ships(self):
        for length in SHIP_LENGTHS:
            self.real_board.place_ship(length)

def game_over(player1, player2):
    if player1.real_board.all_ships_sunk():
        return True, player2.name
    if player2.real_board.all_ships_sunk():
        return True, player1.name
    return False, None

def get_available_moves(board):
    moves = []
    for r in range(board.size):
        for c in range(board.size):
            if board.grid[r][c] == Board.EMPTY:
                moves.append((r, c))
    return moves

def get_move_from_agent_via_crew(task_obj, board_snapshot, available_moves):
    """
    Build context dynamically and create a temporary crew to execute a single move task.
    The context (board state and available moves) is passed as input,
    and the crew's kickoff method returns the task's output.
    """
    # Convert each tuple in available_moves to a list.
    context = {
        "personal_board": board_snapshot,
        "available_moves": [list(move) for move in available_moves]
    }
    from crewai import Crew, Process
    temp_crew = Crew(
        agents=[task_obj.agent],
        tasks=[task_obj],
        process=Process.sequential,
        verbose=True
    )
    output = temp_crew.kickoff(inputs=context)
    
    import json
    try:
        # Check if output is already a string
        if isinstance(output, str):
            output_json = json.loads(output)
        # Otherwise, check if it has a 'json' attribute.
        elif hasattr(output, "json"):
            # If json is callable, call it; otherwise, assume it's a property containing a string.
            if callable(output.json):
                output_json = output.json()
            else:
                output_json = json.loads(output.json)
        elif hasattr(output, "to_dict"):
            output_json = output.to_dict()
        else:
            raise Exception("Unrecognized output type")
        move = output_json.get("move")
        return move
    except Exception as e:
        print("Error parsing task output:", e)
        import random
        return random.choice(context["available_moves"])

def simulate_turn(player, opponent, move_task):
    available_moves = get_available_moves(player.personal_board)
    if not available_moves:
        raise Exception(f"No available moves for {player.name}")
    board_snapshot = board_to_str(player.personal_board)
    print(f"\n{player.name}'s turn:")
    print("Personal Board:")
    print(board_snapshot)
    print("Available moves:", available_moves)
    move = get_move_from_agent_via_crew(move_task, board_snapshot, available_moves)
    if not move or tuple(move) not in available_moves:
        print(f"{player.name} produced an invalid move: {move}. Selecting a random valid move.")
        move = random.choice(available_moves)
    else:
        move = tuple(move)
    result = opponent.real_board.receive_attack(move)
    if result is True:
        print(f"{player.name} HIT at {move}!")
        player.personal_board.grid[move[0]][move[1]] = Board.HIT
    elif result is False:
        print(f"{player.name} MISS at {move}.")
        player.personal_board.grid[move[0]][move[1]] = Board.MISS
    else:
        print(f"{player.name} attempted an already attacked cell at {move}. Turn skipped.")

def run_simulation(ui_update_callback=None):
    player1 = Player("Player1")
    player2 = Player("Player2")
    crew_instance = BattleshipCrew()
    player1_task = crew_instance.player1_move_task()
    player2_task = crew_instance.player2_move_task()
    current_player, opponent = player1, player2
    turn_count = 0
    while True:
        over, winner = game_over(player1, player2)
        if over:
            print(f"\nGame Over! Winner: {winner}")
            if ui_update_callback:
                ui_update_callback(game_over=True, winner=winner)
            break
        turn_count += 1
        print(f"\n--- Turn {turn_count} ---")
        if current_player.name == "Player1":
            simulate_turn(current_player, opponent, player1_task)
        else:
            simulate_turn(current_player, opponent, player2_task)
        if ui_update_callback:
            ui_update_callback(player1=player1, player2=player2)
        current_player, opponent = opponent, current_player
        time.sleep(2)  # Rate limiting: 0.5 seconds between turns

def run():
    run_simulation()

if __name__ == '__main__':
    run()
