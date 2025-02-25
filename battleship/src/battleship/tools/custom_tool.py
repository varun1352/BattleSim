from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."


# src/battleship/tools/custom_tool.py
# src/battleship/tools/custom_tool.py
def board_to_str(board):
    """
    Converts a board (or a 2D list) into a human-readable string representation.
    If a Board instance is passed, its grid attribute is used.
    Symbols: '.' for empty, 'S' for ship, 'X' for hit, 'O' for miss.
    """
    if hasattr(board, 'grid'):
        board = board.grid
    symbols = {
        0: '.',
        1: 'S',
        2: 'X',
        3: 'O'
    }
    lines = []
    for row in board:
        line = " ".join(symbols[cell] for cell in row)
        lines.append(line)
    return "\n".join(lines)


