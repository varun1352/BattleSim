from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from battleship.tools.custom_tool import initialize_game, decide_move, update_boards, check_win

@CrewBase
class BattleshipCrew():
    """Battleship Crew for the Battleship Simulator"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def player_one(self) -> Agent:
        # Aggressive strategist: analyzes the opponent's personal board to decide an aggressive move.
        return Agent(
            config=self.agents_config['player_one'],
            verbose=True,
            tools=[{"name": "DecideMoveAggressive", "function": lambda board: decide_move(board, "aggressive")}]
        )

    @agent
    def player_two(self) -> Agent:
        # Defensive strategist: analyzes the opponent's personal board to decide a defensive move.
        return Agent(
            config=self.agents_config['player_two'],
            verbose=True,
            tools=[{"name": "DecideMoveDefensive", "function": lambda board: decide_move(board, "defensive")}]
        )

    @agent
    def commander(self) -> Agent:
        # Command center: aggregates game state and decides on recommendations or game results.
        return Agent(
            config=self.agents_config['commander'],
            verbose=True
        )

    @task
    def task_initialize(self) -> Task:
        return Task(config=self.tasks_config['initialize_game'])

    @task
    def task_move_player_one(self) -> Task:
        return Task(config=self.tasks_config['simulate_move_player_one'])

    @task
    def task_move_player_two(self) -> Task:
        return Task(config=self.tasks_config['simulate_move_player_two'])

    @task
    def task_predict(self) -> Task:
        return Task(config=self.tasks_config['predict_move'])

    @crew
    def crew(self) -> Crew:
        # The crew executes tasks sequentially: initialize the game, then alternate moves, then predict.
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
