# Battleship Simulator

A Battleship simulation project powered by CrewAI and Cerebras, featuring a custom Tkinter UI.  
This project allows you to test advanced AI strategies in a game of Battleship with two agents:
•⁠  ⁠*Aggressive Hunter:* Focuses on systematic search and rapid targeting.
•⁠  ⁠*Defensive Counter:* Balances exploration with careful targeting.

## Features

•⁠  ⁠*Agentic Simulation:* Two AI agents play Battleship using advanced probability analysis and a “hunt and target” strategy.
•⁠  ⁠*Customizable Strategies:* Detailed YAML configurations allow you to define complex roles, goals, and strategies.
•⁠  ⁠*High-Speed Inference:* Integrated with Cerebras' high-speed inference (LLM) for real-time decision making.
•⁠  ⁠*Intuitive UI:* A custom Tkinter interface displays both the personal board (updated dynamically) and the real board (static), with clear status updates.
•⁠  ⁠*Rate Limiting:* The simulation respects Cerebras’ rate limit of approximately 2 calls/second.

## Installation

1.⁠ ⁠*Clone the Repository:*

   ⁠ bash
   git clone https://github.com/<your-username>/battleship-simulator.git
   cd battleship-simulator
    ⁠

2.⁠ ⁠*Create and Activate a Virtual Environment:*

⁠ bash
Copy
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
 ⁠

3.⁠ ⁠*Install Dependencies:*

⁠ bash
pip install -r requirements.txt
 ⁠

4.⁠ ⁠*Set Up Environment Variables:*
Create a .env file in the project root with:

    CEREBRAS_API_KEY=your_cerebras_api_key_here


⁠ ## Usage

1. **Run the Simulation:**

 ⁠bash
python ui.py


⁠ 2. **Configure the Simulation:**

Edit the `config/agents.yaml` file to customize the AI agents' roles, goals, and strategies.

3. **Run the Simulation to test out the new strategies:**

 ⁠bash
python ui.py
```
