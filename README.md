Below is a polished, rewritten version of your README.md that you can use for your GitHub repository or as part of your blog post on Medium:

---

# Battleship Simulator

Battleship Simulator is an AI-powered game simulation built with CrewAI and Cerebras, featuring a sleek, custom Tkinter user interface. In this project, two advanced AI agents—each with distinct strategic philosophies—compete in a game of Battleship. This setup lets you experiment with sophisticated strategies like systematic search, probability analysis, and immediate ship finishing.

## Demo

https://github.com/varun1352/BattleSim/blob/main/Screen%20Recording%202025-02-25%20at%203.40.07%E2%80%AFAM.mov

Watch the AI agents battle it out in real-time as they employ their strategic decision-making processes.


## Features

- **Agentic Simulation:**  
  Two AI agents engage in real-time Battleship using advanced probability modeling and a “hunt and target” approach.

- **Customizable Strategies:**  
  Define and fine-tune complex roles, goals, and tactics via detailed YAML configuration files.

- **High-Speed Inference:**  
  Leverages Cerebras’ high-speed inference (LLM) to make decisions in near real time.

- **Intuitive User Interface:**  
  A custom Tkinter UI displays each player’s personal board (dynamically updated) and the static real board, ensuring clear, real-time status feedback.

- **Rate Limiting:**  
  The simulation respects Cerebras’ rate limit of approximately 2 calls per second.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/<your-username>/battleship-simulator.git
   cd battleship-simulator
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**

   Create a `.env` file in the project root with the following content:

   ```
   CEREBRAS_API_KEY=your_cerebras_api_key_here
   ```

## Usage

### Running the Simulation via the Terminal

To run the simulation in terminal mode, simply execute:

```bash
crewai run
```

### Launching the Graphical UI

To start the Tkinter-based interface:

```bash
python -m battleship.ui
```

*Ensure your PYTHONPATH is set appropriately or run the command from the project root.*

### Customizing AI Strategies

To tailor the AI behaviors, edit the configuration files located in the `src/battleship/config/` directory:

- **agents.yaml:**  
  Customize each agent’s role, goal, and detailed backstory.

- **tasks.yaml:**  
  Refine the move-generation prompt to encourage optimal play—such as prioritizing sinking a ship immediately after a hit.

## Project Structure

```
battleship/
├── README.md
├── knowledge/
│   └── user_preference.txt
├── output/
│   ├── player1_move.md
│   └── player2_move.md
├── pyproject.toml
├── src/
│   └── battleship/
│       ├── __init__.py
│       ├── board.py
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       ├── crew.py
│       ├── main.py
│       └── tools/
│           ├── __init__.py
│           └── custom_tool.py
├── tests/
├── ui.py
└── uv.lock
```

## Contributing

Contributions are welcome! Feel free to fork the repository, make improvements, and open pull requests. For major changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License.
