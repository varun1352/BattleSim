# src/battleship/crew.py
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
import yaml
import logging
from pydantic import BaseModel

# Define a simple Pydantic model for the move.
class Move(BaseModel):
    move: list[int]

# Initialize the LLM with Cerebras configuration.
llm = LLM(
    model="cerebras/llama3.1-8b",
    base_url="https://api.cerebras.ai/v1",
    api_key=os.getenv("CEREBRAS_API_KEY")
)

@CrewBase
class BattleshipCrew:
    """
    BattleshipCrew sets up two agents (Player 1 and Player 2) who generate their next move
    based on their personal board state and available moves.
    """
    def __init__(self, inputs={}):
        super().__init__()
        self.inputs = inputs
        with open(os.path.join(os.path.dirname(__file__), 'config', 'tasks.yaml'), 'r') as task_file:
            self.tasks_config = yaml.safe_load(task_file)
        with open(os.path.join(os.path.dirname(__file__), 'config', 'agents.yaml'), 'r') as agent_file:
            self.agents_config = yaml.safe_load(agent_file)

    @agent
    def player1_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['player1'],
            verbose=True,
            llm=llm
        )

    @agent
    def player2_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['player2'],
            verbose=True,
            llm=llm
        )

    @task
    def player1_move_task(self) -> Task:
        return Task(
            config=self.tasks_config['move_task'],
            agent=self.player1_agent(),
            output_json=Move
        )

    @task
    def player2_move_task(self) -> Task:
        return Task(
            config=self.tasks_config['move_task'],
            agent=self.player2_agent(),
            output_json=Move
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.player1_agent(), self.player2_agent()],
            tasks=[self.player1_move_task(), self.player2_move_task()],
            process=Process.sequential,
            verbose=True
        )

def get_agent_move(context):
    """
    Uses dynamic context to generate a strategic move via the LLM.
    The prompt is built from the tasks.yaml template.
    """
    import os
    from os import path
    import json
    import yaml
    # Import the global LLM instance from the crew module.
    from battleship.crew import llm

    # Load the tasks configuration to get the prompt template.
    tasks_config_path = path.join(path.dirname(__file__), 'config', 'tasks.yaml')
    with open(tasks_config_path, 'r') as f:
        tasks_config = yaml.safe_load(f)
    prompt_template = tasks_config['move_task']['description']
    
    # Format the prompt using the current context.
    prompt = prompt_template.format(
        personal_board=context["personal_board"],
        available_moves=context["available_moves"]
    )
    print("Generated prompt for LLM:")
    print(prompt)
    
    try:
        # Call the LLM using the correct method (here we assume 'complete' is the right method).
        response = llm.complete(prompt)
        print("LLM response:", response)
        
        # If the response is a string, assume it is the JSON output.
        if isinstance(response, str):
            # Optionally, verify that it can be parsed as JSON.
            json.loads(response)  # Will raise an error if not valid.
            return response
        # Otherwise, if response.json is callable, use that.
        elif callable(getattr(response, "json", None)):
            return json.dumps(response.json())
        else:
            # Fallback: try converting response to dict if possible.
            return json.dumps(response.to_dict())
    except Exception as e:
        print("LLM generation failed, fallback to random move.", e)
        import random
        move = random.choice(context["available_moves"])
        return json.dumps({"move": move})
