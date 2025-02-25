# src/battleship/board.py
import random

class Board:
    EMPTY = 0
    SHIP = 1
    HIT = 2
    MISS = 3

    def __init__(self, size=10):
        self.size = size
        self.grid = [[self.EMPTY for _ in range(size)] for _ in range(size)]
        self.ships = []  # Each ship is a set of coordinates

    def place_ship(self, length):
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            attempts += 1
            orientation = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - length)
                coords = [(row, col + i) for i in range(length)]
            else:
                row = random.randint(0, self.size - length)
                col = random.randint(0, self.size - 1)
                coords = [(row + i, col) for i in range(length)]
            if self._can_place(coords):
                for r, c in coords:
                    self.grid[r][c] = self.SHIP
                self.ships.append(set(coords))
                placed = True
        if not placed:
            raise Exception(f"Failed to place ship of length {length}")

    def _can_place(self, coords):
        return all(self.grid[r][c] == self.EMPTY for r, c in coords)

    def receive_attack(self, coord):
        row, col = coord
        if self.grid[row][col] == self.SHIP:
            self.grid[row][col] = self.HIT
            for ship in self.ships:
                if coord in ship:
                    ship.remove(coord)
                    break
            return True
        elif self.grid[row][col] == self.EMPTY:
            self.grid[row][col] = self.MISS
            return False
        return None

    def all_ships_sunk(self):
        return all(len(ship) == 0 for ship in self.ships)

    def to_string(self):
        symbols = {
            self.EMPTY: '.',
            self.SHIP: 'S',
            self.HIT: 'X',
            self.MISS: 'O'
        }
        lines = []
        for row in self.grid:
            line = " ".join(symbols[cell] for cell in row)
            lines.append(line)
        return "\n".join(lines)
